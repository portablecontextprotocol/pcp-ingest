import os
import logging
import json
from datetime import datetime, timezone
from logging import INFO, DEBUG

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from graphiti_core.utils.bulk_utils import RawEpisode
from graphiti_core.llm_client import LLMConfig
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig

from dotenv import load_dotenv

# from entities import ENTITY_TYPES
from clients.openai_compatible_client import OpenAIGenericClientJSONResponse
from models.snippet_extraction_model import SnippetList, Snippet

from utils import get_markdown_files, process_markdown_file


# Configure detailed logging
logging.basicConfig(
    level=INFO,  # Set root logger to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Set up specific loggers
logger = logging.getLogger(__name__)
logger.setLevel(INFO)

# Add console handler for detailed output
console_handler = logging.StreamHandler()
console_handler.setLevel(DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Load environment variables
load_dotenv()

# OpenAI compatible provider configuration
api_key = os.environ.get("OPENAI_API_KEY")
api_base = "http://127.0.0.1:1234/v1"
model = os.environ.get(
    "OPENAI_MODEL", "qwen3-30b-a3b"
)  # Default to gpt-4.1-mini if not specified

if not api_key or not api_base:
    raise ValueError(
        "OPENAI_API_KEY and OPENAI_API_BASE environment variables must be set"
    )

# Neo4j connection parameters
neo4j_uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
neo4j_password = os.environ.get("NEO4J_PASSWORD", "pass123abcd")

if not neo4j_uri or not neo4j_user or not neo4j_password:
    raise ValueError("NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set")


def sanitize_for_neo4j(obj):
    """
    Recursively sanitize an object to ensure it's compatible with Neo4j.
    Neo4j only accepts primitive types (str, int, float, bool, None) and arrays of primitive types.

    Args:
        obj: Object to sanitize

    Returns:
        Sanitized object that can be stored in Neo4j
    """
    if obj is None:
        return None
    elif isinstance(obj, (str, int, float, bool)):
        return obj
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_neo4j(item) for item in obj]
    elif isinstance(obj, dict):
        # Convert dict to JSON string to prevent Neo4j complex object errors
        return json.dumps(obj)
    else:
        # Convert any other types to string
        return str(obj)


def generate_episodes_from_snippets(snippets):
    """
    Convert a list of Snippet objects to RawEpisode objects.
    Uses the full set of fields as seen in the example.
    Ensures all metadata and properties are compatible with Neo4j.
    """
    episodes = []
    for snippet in snippets:
        try:
            # Compose content: description + (optional) code, language, mentions
            content_parts = [snippet.description]

            # Clean the code - handle complex nested objects
            clean_code = None
            if snippet.code:
                try:
                    # Try to detect and clean JSON schema objects that might cause Neo4j errors
                    if any(
                        marker in snippet.code
                        for marker in [
                            '"type": "object"',
                            "description:",
                            "properties:",
                        ]
                    ):
                        # This looks like a JSON schema - convert to string representation
                        clean_code = (
                            f"```{snippet.language or 'json'}\n{snippet.code}\n```"
                        )
                    else:
                        clean_code = snippet.code

                    content_parts.append(
                        f"\n\nCode Example ({snippet.language or 'code'}):\n{clean_code}"
                    )
                except Exception as e:
                    # If there's any issue with the code, log it and continue without the code
                    logger.warning(
                        f"Error processing code in snippet {snippet.title}: {str(e)}"
                    )
                    content_parts.append(f"\n\n[Code content could not be processed]")

            # Clean mentions - ensure they're primitive types only
            clean_mentions = []
            if snippet.mentions:
                for mention in snippet.mentions:
                    if isinstance(mention, (str, int, float, bool)) or mention is None:
                        clean_mentions.append(str(mention))
                    else:
                        # Convert complex objects to strings
                        clean_mentions.append(f"{mention}")

                content_parts.append(f"\nMentions: {', '.join(clean_mentions)}")

            content = "\n".join(content_parts)

            # Extract section from the source path if possible
            source_path = snippet.source
            section = "documentation"
            if "/" in source_path:
                try:
                    section = source_path.split("/")[2].replace("docs_", "")
                except (IndexError, AttributeError):
                    pass

            # Convert mentions to a simple string to avoid nested objects
            mentions_str = ", ".join(clean_mentions) if clean_mentions else ""

            # Create metadata for the episode as a serialized JSON string
            # Neo4j only accepts primitive types
            metadata_dict = {
                "title": snippet.title,
                "source_path": source_path,
                "has_code": bool(snippet.code),
                "language": snippet.language if snippet.code else "",
                "mentions": mentions_str,
                "section": section,
            }

            # Make sure to sanitize ALL properties for Neo4j compatibility
            episode = RawEpisode(
                name=sanitize_for_neo4j(snippet.title),
                content=sanitize_for_neo4j(content),
                source=sanitize_for_neo4j(EpisodeType.json.value),
                source_description=sanitize_for_neo4j(
                    f"Technical documentation snippet from {section}"
                ),
                source_url=sanitize_for_neo4j(snippet.source_path),
                reference_time=datetime.now(
                    timezone.utc
                ),  # Datetime objects are handled by Neo4j driver
                metadata=sanitize_for_neo4j(
                    metadata_dict
                ),  # This ensures metadata is a JSON string
                group_id=sanitize_for_neo4j("sui-docs"),
                valid_at=datetime.now(timezone.utc),
                processed=False,
                summary=sanitize_for_neo4j(
                    snippet.description[:100]
                    + ("..." if len(snippet.description) > 100 else "")
                ),
            )
            logger.debug(f"DEBUG episode_generation.py: episode prepared: {episode}")
            episodes.append(episode)
        except Exception as e:
            logger.warning(
                f"Error generating episode for snippet {getattr(snippet, 'title', 'unknown')}: {str(e)}"
            )
            # Continue to next snippet

    logger.debug(
        f"DEBUG episode_generation.py: 'generate_episodes_from_snippets' is returning: {episodes}"
    )
    if episodes:  # Check if episodes is not empty
        logger.debug(
            f"DEBUG episode_generation.py: Types in list being returned: {[type(ep) for ep in episodes]}"
        )
    return episodes


# if __name__ == "__main__":
#     asyncio.run(generate_episodes())
