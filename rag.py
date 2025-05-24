import os
import asyncio
import logging
import argparse
from logging import INFO, DEBUG
from dotenv import load_dotenv

import openai

from graphiti_core.edges import EntityEdge
from graphiti_core.search.search_config_recipes import (
    NODE_HYBRID_SEARCH_EPISODE_MENTIONS,
)

from clients.graphiti_client import (
    get_graphiti_client,
    create_openai_config,
    create_openai_embedder_config,
    close_graphiti_client,
)

from utils import (
    count_duplicate_content_all_nodes,
    find_similar_facts,
    remove_duplicate_facts,
    remove_duplicate_nodes,
)

# Load environment variables
load_dotenv()

# Configure detailed logging
logging.basicConfig(
    level=INFO,  # Set root logger to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Set up specific loggers
logger = logging.getLogger(__name__)
logger.setLevel(INFO)

# OpenAI compatible provider configuration
api_key = os.environ.get("OPENAI_API_KEY")
api_base = "https://api.groq.com/openai/v1"
model = "llama-3.1-8b-instant"

if not api_key or not api_base:
    raise ValueError(
        "OPENAI_API_KEY and OPENAI_API_BASE environment variables must be set"
    )


def print_facts(edges):
    print("\n".join([edge.fact for edge in edges]))


def edges_to_facts_string(entities: list[EntityEdge]):
    return "-" + "\n- ".join([edge.fact for edge in entities])


async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="PCP Ingest Knowledge Graph utilities")
    parser.add_argument(
        "--check-duplicates",
        action="store_true",
        help="Check for duplicate content and facts",
    )
    parser.add_argument(
        "--remove-duplicate-edges",
        action="store_true",
        help="Remove duplicate facts (edges) from the KG",
    )
    parser.add_argument(
        "--remove-duplicate-nodes",
        action="store_true",
        help="Remove duplicate nodes from the KG",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.95,
        help="Similarity threshold for near-duplicates (0.0-1.0)",
    )
    parser.add_argument(
        "--group-id", type=str, default="sui-docs", help="Group ID to check/clean"
    )
    parser.add_argument(
        "--node-labels",
        type=str,
        nargs="+",
        default=["Entity", "Episodic"],
        help="Node labels to check/clean (e.g., Entity Episodic)",
    )
    parser.add_argument(
        "--search-query",
        type=str,
        help="Perform a search with the given query string.",
    )
    parser.add_argument(
        "--focal-node-uuid",
        type=str,
        default=None,
        help="Focal node UUID for node distance reranking in search.",
    )
    parser.add_argument(
        "--num-results",
        type=int,
        default=10,
        help="Number of results to return for the search query (default: 10).",
    )

    args = parser.parse_args()

    # Initialize Graphiti client
    groq_config = create_openai_config(
        api_key=api_key,
        api_base=api_base,
        model=model,
    )

    groq_embedder_config = create_openai_embedder_config(
        api_key=os.environ.get("OPENAI_API_KEY"),
        api_base=os.environ.get("OPENAI_API_BASE"),
        embedding_model="text-embedding-nomic-embed-text-v1.5:2",
    )

    graphiti = get_graphiti_client(
        openai_config=groq_config,
        embedder_config=groq_embedder_config,
    )

    # Check for duplicates
    if args.check_duplicates or (
        not args.remove_duplicate_edges and not args.remove_duplicate_nodes
    ):
        # Find exact duplicate content across all node types
        duplicates = await count_duplicate_content_all_nodes(
            graphiti.driver, args.group_id
        )
        logger.info(f"Exact duplicates: {len(duplicates)}")

        # Find near-duplicate facts using embedding similarity
        similar_facts = await find_similar_facts(
            graphiti.driver,
            group_id=args.group_id,
            threshold=args.similarity_threshold,
            limit=1000,
        )

        logger.info(f"Found {len(similar_facts)} near-duplicate fact pairs")

        # Print a few examples of similar facts if any were found
        if similar_facts:
            logger.info("Example similar facts:")
            for i, pair in enumerate(similar_facts[:3]):  # Show first 3 examples
                logger.info(f"Pair {i+1} (similarity: {pair['similarity']:.4f}):")
                logger.info(f"  Fact 1: {pair['fact1'][:100]}...")
                logger.info(f"  Fact 2: {pair['fact2'][:100]}...")

    # Remove duplicate edges if requested
    if args.remove_duplicate_edges:
        logger.info(
            f"Removing duplicate edges with similarity threshold {args.similarity_threshold}..."
        )
        result = await remove_duplicate_facts(
            graphiti.driver, group_id=args.group_id, threshold=args.similarity_threshold
        )
        logger.info(f"Duplicate edge removal result: {result}")

    # Remove duplicate nodes if requested
    if args.remove_duplicate_nodes:
        logger.info(
            f"Removing duplicate nodes with similarity threshold {args.similarity_threshold}..."
        )
        result = await remove_duplicate_nodes(
            graphiti.driver,
            group_id=args.group_id,
            node_labels=args.node_labels,
            threshold=args.similarity_threshold,
        )
        logger.info(f"Duplicate node removal result: {result}")

    # Perform search if requested
    if args.search_query:
        logger.info(
            f"Searching with query: '{args.search_query}'"
            f"{f', focal node: {args.focal_node_uuid}' if args.focal_node_uuid else ''}"
            f", num_results: {args.num_results}"
        )
        search_results = await graphiti.search(
            args.search_query,
            center_node_uuid=args.focal_node_uuid,
            num_results=args.num_results,
        )
        if search_results:
            logger.info("Search results:")
            logger.info(search_results)
            # print(edges_to_facts_string(search_results))
        else:
            logger.info("No results found for your query.")

    await close_graphiti_client()


if __name__ == "__main__":
    asyncio.run(main())
