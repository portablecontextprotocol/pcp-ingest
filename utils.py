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


async def count_duplicate_episodes_by_content(driver, group_id: str) -> list[dict]:
    """
    Count how many Episodic nodes have the same content property within a group_id.
    Returns a list of dicts: {"content": ..., "count": ..., "uuids": [...]}, for all contents that appear more than once.

    Args:
        driver: Neo4j AsyncDriver
        group_id: The group ID to filter episodes

    Returns:
        List of dicts with duplicate content info
    """
    query = """
    MATCH (e:Episodic {group_id: $group_id})
    WITH e.content AS content, collect(e.uuid) AS uuids, count(*) AS count
    WHERE count > 1
    RETURN content, count, uuids
    ORDER BY count DESC
    """
    params = {"group_id": group_id}
    sanitized_params = sanitize_neo4j_params(params)
    try:
        records, _, _ = await driver.execute_query(
            query,
            **sanitized_params,
            database_="neo4j",
            routing_="r",
        )
        duplicates = [
            {"content": r["content"], "count": r["count"], "uuids": r["uuids"]}
            for r in records
        ]
        logger.info(
            f"Found {len(duplicates)} duplicate content groups in Episodic nodes for group_id={group_id}"
        )
        return duplicates
    except Exception as e:
        logger.warning(f"Error counting duplicate episodes by content: {str(e)}")
        return []


async def count_duplicate_content_all_nodes(driver, group_id: str) -> list[dict]:
    """
    Count how many nodes (of any type) have the same content property within a group_id.
    Returns a list of dicts: {"content": ..., "count": ..., "uuids": [...], "labels": [...]} for all contents that appear more than once.

    Args:
        driver: Neo4j AsyncDriver
        group_id: The group ID to filter nodes

    Returns:
        List of dicts with duplicate content info
    """
    query = """
    MATCH (n)
    WHERE n.group_id = $group_id AND n.content IS NOT NULL
    WITH n.content AS content, collect(n.uuid) AS uuids, collect(labels(n)) AS labels, count(*) AS count
    WHERE count > 1
    RETURN content, count, uuids, labels
    ORDER BY count DESC
    """
    params = {"group_id": group_id}
    sanitized_params = sanitize_neo4j_params(params)
    try:
        records, _, _ = await driver.execute_query(
            query,
            **sanitized_params,
            database_="neo4j",
            routing_="r",
        )
        duplicates = [
            {
                "content": r["content"],
                "count": r["count"],
                "uuids": r["uuids"],
                "labels": r["labels"],
            }
            for r in records
        ]
        logger.info(
            f"Found {len(duplicates)} duplicate content groups across all node types for group_id={group_id}"
        )
        return duplicates
    except Exception as e:
        logger.warning(f"Error counting duplicate content across all nodes: {str(e)}")
        return []


async def find_similar_facts(
    driver, group_id: str, threshold: float = 0.95, limit: int = 1000
) -> list[dict]:
    """
    Find near-duplicate facts in EntityEdge relationships by comparing their fact_embedding vectors
    using cosine similarity.

    Args:
        driver: Neo4j AsyncDriver
        group_id: The group ID to filter entity edges
        threshold: Similarity threshold (0.0 to 1.0) - higher means more similar
        limit: Maximum number of edges to retrieve for comparison

    Returns:
        List of dicts with similar fact pairs: [{"fact1": str, "fact2": str, "similarity": float, "uuid1": str, "uuid2": str}, ...]
    """
    try:
        # Import numpy only when needed to avoid dependency issues
        import numpy as np

        # Query to get entity edges with fact embeddings
        query = """
        MATCH ()-[e:RELATES_TO]->()
        WHERE e.group_id = $group_id AND e.fact_embedding IS NOT NULL
        RETURN e.uuid as uuid, e.fact as fact, e.fact_embedding as embedding
        LIMIT $limit
        """

        params = {"group_id": group_id, "limit": limit}
        sanitized_params = sanitize_neo4j_params(params)

        # Fetch entity edges with embeddings
        records, _, _ = await driver.execute_query(
            query,
            **sanitized_params,
            database_="neo4j",
            routing_="r",
        )

        if not records:
            logger.info(
                f"No entity edges with embeddings found for group_id={group_id}"
            )
            return []

        # Extract embeddings and metadata
        edges = []
        for r in records:
            if r["embedding"] is not None:
                edges.append(
                    {"uuid": r["uuid"], "fact": r["fact"], "embedding": r["embedding"]}
                )

        logger.info(
            f"Found {len(edges)} entity edges with embeddings for group_id={group_id}"
        )

        if len(edges) < 2:
            return []

        # Compute cosine similarity between all pairs
        similar_pairs = []

        # Convert embeddings to numpy arrays for efficient computation
        uuids = [edge["uuid"] for edge in edges]
        facts = [edge["fact"] for edge in edges]
        embeddings = np.array([edge["embedding"] for edge in edges])

        # Normalize embeddings for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / norms

        # Compute similarity matrix
        similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)

        # Find pairs above threshold
        for i in range(len(edges)):
            for j in range(
                i + 1, len(edges)
            ):  # Only check upper triangle to avoid duplicates
                similarity = similarity_matrix[i, j]
                if similarity >= threshold:
                    similar_pairs.append(
                        {
                            "uuid1": uuids[i],
                            "uuid2": uuids[j],
                            "fact1": facts[i],
                            "fact2": facts[j],
                            "similarity": float(similarity),
                        }
                    )

        logger.info(
            f"Found {len(similar_pairs)} near-duplicate fact pairs with similarity >= {threshold}"
        )
        return similar_pairs

    except ImportError:
        logger.error(
            "NumPy is required for similarity calculations. Install with 'pip install numpy'"
        )
        return []
    except Exception as e:
        logger.warning(f"Error finding similar facts: {str(e)}")
        return []


async def remove_duplicate_facts(
    driver, group_id: str, threshold: float = 0.95, limit: int = 1000
) -> dict:
    """
    Remove duplicate facts from the database, keeping only one from each duplicate group.
    Works with both exact duplicates and near-duplicates (similarity-based).

    Args:
        driver: Neo4j AsyncDriver
        group_id: The group ID to filter entity edges
        threshold: Similarity threshold for near-duplicates
        limit: Maximum number of edges to process

    Returns:
        Dict with statistics about the removal operation
    """
    # Import EntityEdge class
    from graphiti_core.edges import EntityEdge

    # Step 1: Find exact duplicates first (facts with identical content)
    query = """
    MATCH ()-[e:RELATES_TO]->()
    WHERE e.group_id = $group_id
    WITH e.fact AS fact, collect(e.uuid) AS edge_uuids
    WHERE size(edge_uuids) > 1
    RETURN fact, edge_uuids
    """

    params = {"group_id": group_id}
    sanitized_params = sanitize_neo4j_params(params)

    exact_duplicate_groups = []
    try:
        records, _, _ = await driver.execute_query(
            query,
            **sanitized_params,
            database_="neo4j",
            routing_="r",
        )

        for record in records:
            exact_duplicate_groups.append(
                {"fact": record["fact"], "uuids": record["edge_uuids"]}
            )

        logger.info(f"Found {len(exact_duplicate_groups)} groups of exact duplicates")
    except Exception as e:
        logger.error(f"Error finding exact duplicates: {str(e)}")

    # Step 2: Find near-duplicates if requested
    near_duplicate_groups = []
    if threshold < 1.0:
        similar_pairs = await find_similar_facts(driver, group_id, threshold, limit)

        # Convert pairs to groups
        if similar_pairs:
            # Use a simple grouping algorithm (union-find)
            uuid_to_group = {}  # Maps UUID to its group
            groups = []  # List of groups (sets of UUIDs)

            for pair in similar_pairs:
                uuid1, uuid2 = pair["uuid1"], pair["uuid2"]

                group1 = uuid_to_group.get(uuid1)
                group2 = uuid_to_group.get(uuid2)

                if group1 is not None and group2 is not None:
                    if group1 != group2:
                        # Merge groups
                        group1.update(group2)
                        groups.remove(group2)
                        for uuid in group2:
                            uuid_to_group[uuid] = group1
                elif group1 is not None:
                    group1.add(uuid2)
                    uuid_to_group[uuid2] = group1
                elif group2 is not None:
                    group2.add(uuid1)
                    uuid_to_group[uuid1] = group2
                else:
                    # Create new group
                    new_group = {uuid1, uuid2}
                    groups.append(new_group)
                    uuid_to_group[uuid1] = new_group
                    uuid_to_group[uuid2] = new_group

            # Fetch facts for all UUIDs in groups
            all_uuids = list(uuid_to_group.keys())
            facts_map = {}

            if all_uuids:
                facts_query = """
                MATCH ()-[e:RELATES_TO]->()
                WHERE e.uuid IN $uuids
                RETURN e.uuid as uuid, e.fact as fact
                """
                try:
                    facts_records, _, _ = await driver.execute_query(
                        facts_query,
                        uuids=all_uuids,
                        database_="neo4j",
                        routing_="r",
                    )

                    for r in facts_records:
                        facts_map[r["uuid"]] = r["fact"]
                except Exception as e:
                    logger.error(f"Error fetching facts for near-duplicates: {str(e)}")

            # Build near-duplicate groups with facts
            for group in groups:
                group_dict = {
                    "uuids": list(group),
                    "facts": {
                        uuid: facts_map.get(uuid, "Unknown fact") for uuid in group
                    },
                }
                near_duplicate_groups.append(group_dict)

            logger.info(f"Found {len(near_duplicate_groups)} groups of near-duplicates")

    # Step 3: Delete duplicates, keeping one from each group
    deleted_count = 0
    kept_count = 0

    # Process exact duplicates
    for group in exact_duplicate_groups:
        uuids = group["uuids"]
        # Keep the first one, delete the rest
        kept_uuid = uuids[0]
        to_delete = uuids[1:]

        kept_count += 1
        deleted_count += len(to_delete)

        # Use EntityEdge.get_by_uuids and delete methods from Graphiti
        try:
            # Get EntityEdge objects for the UUIDs to delete
            edges_to_delete = await EntityEdge.get_by_uuids(driver, to_delete)

            # Delete each edge using the proper EntityEdge.delete method
            for edge in edges_to_delete:
                await edge.delete(driver)

            logger.info(
                f"Deleted {len(edges_to_delete)} exact duplicates of fact: {group['fact'][:50]}..."
            )
        except Exception as e:
            logger.error(f"Error deleting exact duplicates: {str(e)}")

    # Process near-duplicates
    for group in near_duplicate_groups:
        uuids = group["uuids"]
        # Keep the first one, delete the rest
        kept_uuid = uuids[0]
        to_delete = uuids[1:]

        kept_count += 1
        deleted_count += len(to_delete)

        # Use EntityEdge.get_by_uuids and delete methods from Graphiti
        try:
            # Get EntityEdge objects for the UUIDs to delete
            edges_to_delete = await EntityEdge.get_by_uuids(driver, to_delete)

            # Delete each edge using the proper EntityEdge.delete method
            for edge in edges_to_delete:
                await edge.delete(driver)

            logger.info(
                f"Deleted {len(edges_to_delete)} near-duplicates of fact: {group['facts'][kept_uuid][:50]}..."
            )
        except Exception as e:
            logger.error(f"Error deleting near-duplicates: {str(e)}")

    result = {
        "exact_duplicate_groups": len(exact_duplicate_groups),
        "near_duplicate_groups": len(near_duplicate_groups),
        "kept_edges": kept_count,
        "deleted_edges": deleted_count,
    }

    logger.info(f"Duplicate removal complete: {result}")
    return result


async def remove_duplicate_nodes(
    driver,
    group_id: str,
    node_labels: list[str] = ["Entity"],
    threshold: float = 0.95,
    limit: int = 1000,
) -> dict:
    """
    Remove duplicate nodes from the database, keeping only one from each duplicate group.
    Works with both exact duplicates and near-duplicates (similarity-based).

    Args:
        driver: Neo4j AsyncDriver
        group_id: The group ID to filter nodes
        node_labels: List of node labels to check (e.g., ["Entity", "Episodic"])
        threshold: Similarity threshold for near-duplicates
        limit: Maximum number of nodes to process

    Returns:
        Dict with statistics about the removal operation
    """
    # Import required classes from graphiti_core
    from graphiti_core.nodes import EntityNode, EpisodicNode

    # Node class map for getting the appropriate class by label
    NODE_CLASS_MAP = {
        "Entity": EntityNode,
        "Episodic": EpisodicNode,
    }

    # Build label filter for query
    label_filter = " OR ".join([f"'{label}' IN labels(n)" for label in node_labels])

    # Step 1: Find exact duplicates first (nodes with identical content)
    query = f"""
    MATCH (n)
    WHERE n.group_id = $group_id AND ({label_filter}) AND n.content IS NOT NULL
    WITH n.content AS content, collect(n) AS nodes
    WHERE size(nodes) > 1
    RETURN content, [node.uuid IN nodes | node.uuid] AS node_uuids, labels(nodes[0]) AS node_labels
    LIMIT $limit
    """

    params = {"group_id": group_id, "limit": limit}
    sanitized_params = sanitize_neo4j_params(params)

    exact_duplicate_groups = []
    try:
        records, _, _ = await driver.execute_query(
            query,
            **sanitized_params,
            database_="neo4j",
            routing_="r",
        )

        for record in records:
            exact_duplicate_groups.append(
                {
                    "content": record["content"],
                    "uuids": record["node_uuids"],
                    "labels": record["node_labels"],
                }
            )

        logger.info(
            f"Found {len(exact_duplicate_groups)} groups of exact duplicate nodes"
        )
    except Exception as e:
        logger.error(f"Error finding exact duplicate nodes: {str(e)}")

    # Step 2: Find near-duplicates if requested (using available embeddings)
    # For nodes, we can check name_embedding, content_embedding, or summary_embedding
    near_duplicate_groups = []
    if threshold < 1.0:
        try:
            # Import numpy for similarity calculations
            import numpy as np

            # Query nodes with embeddings
            embedding_query = f"""
            MATCH (n)
            WHERE n.group_id = $group_id AND ({label_filter})
            AND (n.name_embedding IS NOT NULL OR n.content_embedding IS NOT NULL OR n.summary_embedding IS NOT NULL)
            RETURN n.uuid as uuid, n.name as name, n.content as content, 
                   n.name_embedding as name_embedding, 
                   n.content_embedding as content_embedding, 
                   n.summary_embedding as summary_embedding,
                   labels(n) as labels
            LIMIT $limit
            """

            records, _, _ = await driver.execute_query(
                embedding_query,
                **sanitized_params,
                database_="neo4j",
                routing_="r",
            )

            # Extract nodes with embeddings
            nodes_with_embeddings = []
            for r in records:
                # Choose the first available embedding
                embedding = (
                    r["content_embedding"]
                    or r["name_embedding"]
                    or r["summary_embedding"]
                )
                if embedding:
                    nodes_with_embeddings.append(
                        {
                            "uuid": r["uuid"],
                            "name": r["name"],
                            "content": r["content"],
                            "embedding": embedding,
                            "labels": r["labels"],
                        }
                    )

            if len(nodes_with_embeddings) >= 2:
                logger.info(
                    f"Found {len(nodes_with_embeddings)} nodes with embeddings for similarity comparison"
                )

                # Compute similarity matrix
                uuids = [node["uuid"] for node in nodes_with_embeddings]
                labels = [node["labels"] for node in nodes_with_embeddings]
                contents = [node["content"] for node in nodes_with_embeddings]
                embeddings = np.array(
                    [node["embedding"] for node in nodes_with_embeddings]
                )

                # Normalize for cosine similarity
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                normalized_embeddings = embeddings / norms

                # Compute similarity matrix
                similarity_matrix = np.dot(
                    normalized_embeddings, normalized_embeddings.T
                )

                # Find similar pairs
                similar_pairs = []
                for i in range(len(nodes_with_embeddings)):
                    for j in range(i + 1, len(nodes_with_embeddings)):
                        similarity = similarity_matrix[i, j]
                        if similarity >= threshold:
                            similar_pairs.append(
                                {
                                    "uuid1": uuids[i],
                                    "uuid2": uuids[j],
                                    "content1": contents[i],
                                    "content2": contents[j],
                                    "labels1": labels[i],
                                    "labels2": labels[j],
                                    "similarity": float(similarity),
                                }
                            )

                logger.info(
                    f"Found {len(similar_pairs)} similar node pairs with similarity >= {threshold}"
                )

                # Group similar nodes
                uuid_to_group = {}
                groups = []

                for pair in similar_pairs:
                    uuid1, uuid2 = pair["uuid1"], pair["uuid2"]

                    group1 = uuid_to_group.get(uuid1)
                    group2 = uuid_to_group.get(uuid2)

                    if group1 is not None and group2 is not None:
                        if group1 != group2:
                            # Merge groups
                            group1.update(group2)
                            groups.remove(group2)
                            for uuid in group2:
                                uuid_to_group[uuid] = group1
                    elif group1 is not None:
                        group1.add(uuid2)
                        uuid_to_group[uuid2] = group1
                    elif group2 is not None:
                        group2.add(uuid1)
                        uuid_to_group[uuid1] = group2
                    else:
                        # Create new group
                        new_group = {uuid1, uuid2}
                        groups.append(new_group)
                        uuid_to_group[uuid1] = new_group
                        uuid_to_group[uuid2] = new_group

                # Convert groups to our format with node info
                for group in groups:
                    # Get the first node's label to determine class
                    group_uuids = list(group)
                    node_info = {}

                    # Get node info for each UUID
                    for uuid in group_uuids:
                        for node in nodes_with_embeddings:
                            if node["uuid"] == uuid:
                                node_info[uuid] = {
                                    "content": node["content"],
                                    "labels": node["labels"],
                                }
                                break

                    near_duplicate_groups.append(
                        {
                            "uuids": group_uuids,
                            "node_info": node_info,
                            "labels": (
                                next(iter(node_info.values()))["labels"]
                                if node_info
                                else ["Unknown"]
                            ),
                        }
                    )
        except ImportError:
            logger.error(
                "NumPy is required for similarity calculations. Install with 'pip install numpy'"
            )
        except Exception as e:
            logger.error(f"Error finding similar nodes: {str(e)}")

    # Step 3: Delete duplicates, keeping one from each group
    deleted_count = 0
    kept_count = 0
    deletion_errors = 0

    # Process exact duplicates
    for group in exact_duplicate_groups:
        uuids = group["uuids"]
        node_label = (
            group["labels"][0] if group["labels"] else "Entity"
        )  # Default to Entity

        # Keep the first one, delete the rest
        kept_uuid = uuids[0]
        to_delete = uuids[1:]

        kept_count += 1

        # Use appropriate node class based on label
        NodeClass = NODE_CLASS_MAP.get(node_label, EntityNode)

        # Delete each duplicate node using Graphiti native methods
        for uuid in to_delete:
            try:
                # Get node by UUID
                node = await NodeClass.get_by_uuid(driver, uuid)

                # Delete the node
                await node.delete(driver)
                deleted_count += 1

            except Exception as e:
                logger.error(f"Error deleting duplicate node {uuid}: {str(e)}")
                deletion_errors += 1

        logger.info(
            f"Processed exact duplicate group: kept 1, deleted {len(to_delete)} nodes"
        )

    # Process near-duplicates
    for group in near_duplicate_groups:
        uuids = group["uuids"]
        node_info = group["node_info"]
        node_label = (
            group["labels"][0] if group["labels"] else "Entity"
        )  # Default to Entity

        # Keep the first one, delete the rest
        kept_uuid = uuids[0]
        to_delete = uuids[1:]

        kept_count += 1

        # Use appropriate node class based on label
        NodeClass = NODE_CLASS_MAP.get(node_label, EntityNode)

        # Delete each duplicate node using Graphiti native methods
        for uuid in to_delete:
            try:
                # Get node by UUID
                node = await NodeClass.get_by_uuid(driver, uuid)

                # Delete the node
                await node.delete(driver)
                deleted_count += 1

            except Exception as e:
                logger.error(f"Error deleting similar node {uuid}: {str(e)}")
                deletion_errors += 1

        logger.info(
            f"Processed near-duplicate group: kept 1, deleted {len(to_delete)} nodes"
        )

    result = {
        "exact_duplicate_groups": len(exact_duplicate_groups),
        "near_duplicate_groups": len(near_duplicate_groups),
        "kept_nodes": kept_count,
        "deleted_nodes": deleted_count,
        "deletion_errors": deletion_errors,
    }

    logger.info(f"Node duplicate removal complete: {result}")
    return result
