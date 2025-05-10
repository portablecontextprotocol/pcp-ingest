import os
import json
import hashlib
import logging
from typing import Dict, Any, Tuple, Optional, List

# Configure logging
logger = logging.getLogger(__name__)

#########################
# File Processing Utils #
#########################


async def process_markdown_file(file_path: str) -> str:
    """Read and process a markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


async def get_markdown_files(base_dir: str) -> list[tuple[str, dict]]:
    """
    Recursively get all markdown files from the base directory and their metadata.
    Returns a list of tuples containing (file_path, metadata).
    """
    markdown_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                # Get the relative path components to determine section
                rel_path = os.path.relpath(file_path, base_dir)
                path_parts = rel_path.split(os.sep)

                # Determine section from the first directory level
                section = path_parts[0].replace("docs_", "")

                metadata = {
                    "file_path": file_path,
                    "file_type": "markdown",
                    "section": section,
                    "document_type": path_parts[-1].replace(".md", ""),
                }
                markdown_files.append((file_path, metadata))
    return markdown_files


#############################
# Database Operations Utils #
#############################


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
