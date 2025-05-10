import os
import asyncio
import logging
import json
from datetime import datetime
import time

from graphiti_core.nodes import EpisodeType

from entities.sui_entities import SUI_ENTITY_TYPES
from utils import get_markdown_files, process_markdown_file, sanitize_neo4j_params
from clients.graphiti_client import (
    get_graphiti_client,
    close_graphiti_client,
    clear_graph,
)
from snippet_extractor import format_document, ConnectionError
from snippet_processor import (
    process_snippets_with_deduplication,
    load_snippets_from_cache,
    save_snippets_to_cache,
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main(force: bool = False):
    try:
        logger.info("Starting Graphiti LLM Formatter...")

        # Initialize the Graphiti client (singleton pattern)
        graphiti = get_graphiti_client()

        # await clear_graph()

        # Loop through all markdown files in assets/sui-docs
        markdown_files = await get_markdown_files("./assets/sui-docs")

        # Process all markdown files
        processed_count = 0
        total_snippets = 0
        new_snippets = 0
        skipped_snippets = 0
        failed_files = []  # Track files that fail due to connection errors

        # Ensure the cache directory exists
        os.makedirs("assets/formatted", exist_ok=True)
        os.makedirs("assets/formatted/cache", exist_ok=True)

        for file_path, metadata in markdown_files:
            try:
                logger.info(f"Processing file: {file_path}")

                # Use a cache file per markdown file
                cache_file = (
                    f"assets/formatted/formatted_{os.path.basename(file_path)}.json"
                )

                # Check if we have cached snippets
                if os.path.exists(cache_file):
                    logger.info(f"Loading snippets from {cache_file}")
                    snippets = await load_snippets_from_cache(cache_file)
                else:
                    try:
                        # Extract snippets from the file
                        content = await process_markdown_file(file_path)
                        snippets = await format_document(
                            content=content,
                            config=graphiti.llm_client.config,
                            source_path=file_path,
                        )

                        # Save snippets to cache
                        await save_snippets_to_cache(snippets, cache_file)
                    except ConnectionError as e:
                        logger.warning(
                            f"Connection error processing {file_path}: {str(e)}"
                        )
                        failed_files.append((file_path, metadata))
                        continue  # Skip to next file

                processed_count += 1
                total_snippets += len(snippets)

                logger.info(
                    f"Processed {processed_count} files, found {len(snippets)} snippets in current file"
                )

                # Check for duplicates before generating episodes
                episodes, skipped = await process_snippets_with_deduplication(
                    graphiti.driver, snippets, group_id="sui-docs", force=force
                )

                logger.debug(
                    f"DEBUG app.py: 'process_snippets_with_deduplication' returned 'episodes': {episodes}"
                )
                if (
                    episodes
                ):  # Check if episodes is not empty before trying to get types
                    logger.debug(
                        f"DEBUG app.py: Types in 'episodes': {[type(ep) for ep in episodes]}"
                    )
                logger.debug(
                    f"DEBUG app.py: 'process_snippets_with_deduplication' returned 'skipped': {skipped}"
                )

                new_snippets += len(episodes)
                skipped_snippets += skipped

                if episodes:
                    logger.info(
                        f"Adding {len(episodes)} episodes to the graph for {file_path}..."
                    )
                    # Add logging for entity_types
                    # logger.info(
                    #     f"entity_types being passed to add_episode: {SUI_ENTITY_TYPES}"
                    # )
                    # Add episode with error handling
                    success_count = 0
                    error_count = 0
                    for episode in episodes:
                        # --- Start of loop iteration ---
                        logger.debug(
                            f"DEBUG app.py: Top of loop. Current episode: {episode}, Type: {type(episode)}"
                        )

                        try:
                            if not hasattr(episode, "name") or not hasattr(
                                episode, "content"
                            ):
                                logger.warning(
                                    f"DEBUG app.py: Skipping episode due to missing 'name' or 'content'. Episode: {episode}, Type: {type(episode)}"
                                )
                                continue

                            # Store original reference_time
                            original_reference_time = episode.reference_time
                            logger.debug(
                                f"DEBUG app.py: After hasattr check, before accessing attributes. Episode: {episode}, Type: {type(episode)}"
                            )

                            # Prepare params and sanitize them (without reference_time and source)
                            episode_params = {
                                "name": episode.name,  # Potential error source
                                "episode_body": episode.content,
                                "source_description": episode.source_description,
                                "group_id": "sui-docs",
                                "uuid": None,
                                "update_communities": True,
                            }
                            logger.debug(
                                f"DEBUG app.py: episode_params prepared: {episode_params}"
                            )

                            # Convert any non-primitive types to JSON strings
                            sanitized_params = sanitize_neo4j_params(episode_params)
                            # logger.debug(f"DEBUG app.py: sanitized_params: {sanitized_params}") # Can be verbose

                            # Add episode with error handling
                            await graphiti.add_episode(
                                **sanitized_params,
                                reference_time=original_reference_time,
                                source=EpisodeType.json,
                                entity_types=SUI_ENTITY_TYPES,
                            )
                            success_count += 1
                        except Exception as e:
                            error_count += 1
                            episode_name_for_log = "UNKNOWN (episode object might be a string or lack .name attribute)"
                            if hasattr(episode, "name"):  # Try to get name safely
                                try:
                                    episode_name_for_log = episode.name
                                except (
                                    Exception
                                ):  # If accessing episode.name itself errors
                                    pass
                            elif isinstance(episode, str):
                                episode_name_for_log = (
                                    f"'{episode}' (identified as string)"
                                )

                            logger.error(
                                f"DEBUG app.py: Error adding episode. Attempted Name: {episode_name_for_log}. "
                                f"Original Episode Object during exception: {episode}, Type: {type(episode)}. "
                                f"Exception Type: {type(e).__name__}, Exception: {str(e)}. Full repr(e): {repr(e)}"
                            )
                            # Continue with the next episode

                    logger.info(
                        f"Episodes from {file_path} added: {success_count} successful, {error_count} errors"
                    )
                else:
                    logger.info(
                        f"No new episodes to add from {file_path}, all content already exists in database"
                    )

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
                # Continue with the next file
                continue

        # Close graphiti connection using the dedicated function
        await close_graphiti_client()

        logger.info(
            f"Processing complete: {processed_count} files, {total_snippets} total snippets, {new_snippets} new, {skipped_snippets} skipped as duplicates"
        )

    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        # Make sure we close the connection even if there's an error
        await close_graphiti_client()
        raise


if __name__ == "__main__":
    asyncio.run(main())
