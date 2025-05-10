import logging
import json
from typing import List, Tuple, Optional

from models.snippet_extraction_model import Snippet
from utils import check_episode_exists
from episode_generation import generate_episodes_from_snippets

# Configure logging
logger = logging.getLogger(__name__)


async def process_snippets_with_deduplication(
    driver, snippets: List[Snippet], group_id="sui-docs"
):
    """
    Process snippets with deduplication check before generating episodes.

    Args:
        driver: Neo4j AsyncDriver
        snippets: List of snippet objects to process
        group_id: Group ID for episodes (default: "sui-docs")

    Returns:
        Tuple containing list of generated episodes and count of skipped duplicates
    """
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


async def save_snippets_to_cache(snippets: List[Snippet], cache_file: str) -> None:
    """
    Save extracted snippets to a cache file.

    Args:
        snippets: List of snippets to save
        cache_file: Path to cache file
    """
    try:
        dict_snippets = [s.model_dump() for s in snippets]
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(dict_snippets, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(snippets)} snippets to {cache_file}")
    except Exception as e:
        logger.error(f"Error saving snippets to cache {cache_file}: {str(e)}")


async def load_snippets_from_cache(cache_file: str) -> List[Snippet]:
    """
    Load snippets from a cache file.

    Args:
        cache_file: Path to cache file

    Returns:
        List of snippets loaded from cache
    """
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict) and "snippets" in data:
            data = data["snippets"]

        snippets = [Snippet(**d) for d in data]
        logger.info(f"Loaded {len(snippets)} snippets from {cache_file}")
        return snippets
    except Exception as e:
        logger.error(f"Error loading snippets from cache {cache_file}: {str(e)}")
        return []
