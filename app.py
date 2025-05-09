import os
import asyncio
import hashlib
from urllib.parse import urlparse
import logging
from datetime import datetime, timezone
import json
from typing import Optional, List, Dict, Tuple, Any

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.llm_client import LLMConfig
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig

from llm_clients.openai_compatible_client import OpenAIGenericClientJSONResponse
from llm_clients.openai_client import OpenAIConfig
from snippet_extractor import format_document
from episode_generation import generate_episodes_from_snippets

from models.snippet_extraction_model import Snippet
from entities.sui_entities import SUI_ENTITY_TYPES
from utils import get_markdown_files, process_markdown_file

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def sanitize_neo4j_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes parameters to ensure they're compatible with Neo4j.
    Neo4j only accepts primitive types (str, int, float, bool) and arrays of primitive types.

    Args:
        params: Dictionary of parameters to sanitize

    Returns:
        Dictionary with sanitized parameters
    """
    sanitized = {}

    for key, value in params.items():
        if value is None:
            sanitized[key] = None
        elif isinstance(value, (str, int, float, bool)):
            sanitized[key] = value
        elif isinstance(value, (list, tuple)):
            # Handle lists - ensure all elements are primitive
            sanitized_list = []
            for item in value:
                if isinstance(item, (str, int, float, bool)) or item is None:
                    sanitized_list.append(item)
                else:
                    # Convert complex objects to JSON strings
                    sanitized_list.append(json.dumps(item))
            sanitized[key] = sanitized_list
        elif isinstance(value, dict):
            # Convert dictionaries to JSON strings
            sanitized[key] = json.dumps(value)
        else:
            # Convert any other types to strings
            sanitized[key] = str(value)

    return sanitized


async def check_episode_exists(
    driver, content: str, group_id: str, source_path: str = None
) -> Tuple[bool, Optional[str]]:
    """
    Check if an episode with the same content already exists in the graph database.

    Args:
        driver: Neo4j AsyncDriver
        content: The content to check
        group_id: The group ID the episodes would belong to
        source_path: Optional source path for logging (not used in query)

    Returns:
        Tuple[bool, Optional[str]]: (exists, uuid if exists else None)
    """
    # Create a content hash for fast lookup
    content_hash = hashlib.md5(content.encode()).hexdigest()

    # Try with exact content match
    query = """
    MATCH (e:Episodic {group_id: $group_id})
    WHERE e.content = $content
    RETURN e.uuid as uuid, e.name as name LIMIT 1
    """

    params = {
        "group_id": group_id,
        "content": content,
    }

    # Sanitize parameters for Neo4j
    sanitized_params = sanitize_neo4j_params(params)

    try:
        records, _, _ = await driver.execute_query(
            query,
            **sanitized_params,
            database_="neo4j",  # DEFAULT_DATABASE
            routing_="r",
        )

        if records and len(records) > 0:
            if source_path:
                logger.info(
                    f"Found existing episode for source {source_path}: {records[0]['name']} ({records[0]['uuid']})"
                )
            return True, records[0]["uuid"]

        return False, None
    except Exception as e:
        logger.warning(f"Error checking for existing episode: {str(e)}")
        return False, None


async def process_snippets_with_deduplication(driver, snippets, group_id="sui-docs"):
    """Process snippets with deduplication check before generating episodes"""

    new_snippets = []
    skipped_count = 0

    # Process each snippet
    for snippet in snippets:
        try:
            # Create content as it would appear in the episode
            content_parts = [snippet.description]
            if snippet.code:
                # Detect and sanitize complex JSON schema objects
                if any(
                    marker in snippet.code
                    for marker in ['"type": "object"', "properties:", "required:"]
                ):
                    # This looks like a JSON schema that might cause problems
                    code_repr = f"```{snippet.language or 'json'}\n{snippet.code}\n```"
                    content_parts.append(
                        f"\n\nCode Example ({snippet.language or 'code'}):\n{code_repr}"
                    )
                else:
                    content_parts.append(
                        f"\n\nCode Example ({snippet.language or 'code'}):\n{snippet.code}"
                    )

            # Ensure mentions are properly sanitized
            if snippet.mentions:
                clean_mentions = []
                for mention in snippet.mentions:
                    if isinstance(mention, (str, int, float, bool)) or mention is None:
                        clean_mentions.append(str(mention))
                    else:
                        # Convert complex objects to strings
                        clean_mentions.append(f"{mention}")
                content_parts.append(f"\nMentions: {', '.join(clean_mentions)}")
            content = "\n".join(content_parts)

            # Check if this content already exists in the database
            exists, uuid = await check_episode_exists(
                driver=driver,
                content=content,
                group_id=group_id,
                source_path=snippet.source,
            )

            if exists:
                skipped_count += 1
            else:
                new_snippets.append(snippet)
        except Exception as e:
            logger.warning(f"Error processing snippet {snippet.title}: {str(e)}")
            # Continue to the next snippet

    # Generate episodes only for new snippets
    episodes = generate_episodes_from_snippets(new_snippets) if new_snippets else []

    return episodes, skipped_count


async def main():
    try:
        logger.info("Starting Graphiti LLM Formatter...")

        api_key = os.environ.get("OPENAI_API_KEY")
        api_base = "http://127.0.0.1:1234/v1"
        model = os.environ.get("OPENAI_MODEL", "qwen3-30b-a3b")

        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        # Ensure api_base has a protocol
        parsed_url = urlparse(api_base)
        if not parsed_url.scheme:
            api_base = f"https://{api_base}"
        elif parsed_url.scheme not in ["http", "https"]:
            raise ValueError(
                "OPENAI_API_BASE must use either http:// or https:// protocol"
            )

        # Initialize OpenAI configuration
        config = OpenAIConfig(
            api_key=api_key,
            base_url=api_base,
            model=model,
            temperature=0,  # Set to 0 for deterministic responses
            max_tokens=32768,
        )

        # Initialize Neo4j and Graphiti
        neo4j_uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
        neo4j_password = os.environ.get("NEO4J_PASSWORD", "pass123abcd")
        if not neo4j_uri or not neo4j_user or not neo4j_password:
            raise ValueError("NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set")

        # Loop through all markdown files in assets/sui-docs
        markdown_files = await get_markdown_files("./assets/sui-docs")
        # Process all markdown files
        processed_count = 0
        total_snippets = 0
        new_snippets = 0
        skipped_snippets = 0

        for file_path, metadata in markdown_files:
            try:
                logger.info(f"Processing file: {file_path}")
                # Use a cache file per markdown file
                cache_file = (
                    f"assets/formatted/formatted_{os.path.basename(file_path)}.json"
                )
                if os.path.exists(cache_file):
                    logger.info(f"Loading snippets from {cache_file}")
                    with open(cache_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if isinstance(data, dict) and "snippets" in data:
                        data = data["snippets"]
                    snippets = [Snippet(**d) for d in data]
                else:
                    content = await process_markdown_file(file_path)
                    snippets = await format_document(
                        content=content, config=config, source_path=file_path
                    )
                    dict_snippets = [s.model_dump() for s in snippets]
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(dict_snippets, f, indent=2, ensure_ascii=False)
                processed_count += 1
                total_snippets += len(snippets)

                logger.info(
                    f"Processed {processed_count} files, found {len(snippets)} snippets in current file"
                )

                # Configure Graphiti client
                graphiti = Graphiti(
                    neo4j_uri,
                    neo4j_user,
                    neo4j_password,
                    llm_client=OpenAIGenericClientJSONResponse(
                        config=config,
                        cache=False,
                    ),
                    embedder=OpenAIEmbedder(
                        config=OpenAIEmbedderConfig(
                            embedding_model="text-embedding-nomic-embed-text-v1.5",
                            api_key=api_key,
                            base_url=api_base,
                        ),
                    ),
                )

                # Check for duplicates before generating episodes
                episodes, skipped = await process_snippets_with_deduplication(
                    graphiti.driver, snippets, group_id="sui-docs"
                )

                new_snippets += len(episodes)
                skipped_snippets += skipped

                if episodes:
                    logger.info(
                        f"Adding {len(episodes)} episodes to the graph for {file_path}..."
                    )
                    # Add episodes with error handling
                    success_count = 0
                    error_count = 0
                    for episode in episodes:
                        try:
                            # Prepare params and sanitize them
                            episode_params = {
                                "name": episode.name,
                                "episode_body": episode.content,
                                "source_description": episode.source_description,
                                "reference_time": episode.reference_time,
                                "source": episode.source,
                                "group_id": "sui-docs",
                                "entity_types": SUI_ENTITY_TYPES,
                                "uuid": None,
                                "update_communities": True,
                            }

                            # Convert any non-primitive types to JSON strings
                            sanitized_params = sanitize_neo4j_params(episode_params)

                            # Add episode with sanitized parameters
                            await graphiti.add_episode(**sanitized_params)
                            success_count += 1
                        except Exception as e:
                            error_count += 1
                            logger.error(
                                f"Error adding episode {episode.name}: {str(e)}"
                            )
                            # Continue with the next episode

                    logger.info(
                        f"Episodes from {file_path} added: {success_count} successful, {error_count} errors"
                    )
                else:
                    logger.info(
                        f"No new episodes to add from {file_path}, all content already exists in database"
                    )

                # Close graphiti connection after each file to prevent resource issues
                await graphiti.close()
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
                # Continue with the next file
                continue

        logger.info(
            f"Processing complete: {processed_count} files, {total_snippets} total snippets, {new_snippets} new, {skipped_snippets} skipped as duplicates"
        )

    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
