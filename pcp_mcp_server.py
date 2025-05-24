from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from dotenv import load_dotenv
import asyncio
import json
import os
import logging

# Imports from the PCP ingest application
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI compatible provider configuration
api_key = os.environ.get("OPENAI_API_KEY")
api_base = "https://api.groq.com/openai/v1"
model = "llama-3.1-8b-instant"

if not api_key or not api_base:
    raise ValueError(
        "OPENAI_API_KEY and OPENAI_API_BASE environment variables must be set"
    )


# Create a dataclass for our application context
@dataclass
class PCPMCPContext:
    """Context for the PCP MCP server."""

    graphiti_client: object


def edges_to_facts_string(entities: list):
    """Convert edges to a formatted facts string."""
    if not entities:
        return "No facts found."
    return "- " + "\n- ".join([edge.fact for edge in entities])


@asynccontextmanager
async def pcp_lifespan(server: FastMCP) -> AsyncIterator[PCPMCPContext]:
    """
    Manages the Graphiti client lifecycle.

    Args:
        server: The FastMCP server instance.

    Yields:
        PCPMCPContext: The context containing the Graphiti client.
    """
    print("Initializing Graphiti client...")

    # Initialize Graphiti client with the same config as rag.py
    groq_config = create_openai_config(
        api_key=api_key,
        api_base=api_base,
        model=model,
    )

    groq_embedder_config = create_openai_embedder_config(
        api_key=os.environ.get("OPENAI_API_KEY"),
        api_base=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
        embedding_model="text-embedding-nomic-embed-text-v1.5:2",
    )

    graphiti_client = get_graphiti_client(
        openai_config=groq_config,
        embedder_config=groq_embedder_config,
    )

    print("Graphiti client initialized.")
    try:
        yield PCPMCPContext(graphiti_client=graphiti_client)
    finally:
        print("Graphiti client lifespan ending.")
        await close_graphiti_client()


# Initialize FastMCP server
mcp = FastMCP(
    "pcp-graph-mcp-server",
    description="MCP server for searching and managing the PCP knowledge graph built with Graphiti.",
    lifespan=pcp_lifespan,
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8052")),  # Different port from axiom server
)


@mcp.tool()
async def search_graph(
    ctx: Context, query: str, num_results: int = 10, focal_node_uuid: str | None = None
) -> str:
    """
    Search the PCP knowledge graph for relevant facts and entities.

    This tool queries the knowledge graph built from ingested PCP content using Graphiti.
    It returns relevant facts and relationships based on the search query.

    Args:
        ctx: The MCP server provided context, including the Graphiti client.
        query: The search query describing what you're looking for.
        num_results: Maximum number of results to return (default: 10).
        focal_node_uuid: Optional UUID of a focal node for distance-based reranking.

    Returns:
        A JSON formatted string containing search results.
    """
    try:
        graphiti_client = ctx.request_context.lifespan_context.graphiti_client

        logger.info(
            f"Searching graph with query: '{query}', num_results: {num_results}"
            f"{f', focal node: {focal_node_uuid}' if focal_node_uuid else ''}"
        )

        # Only pass center_node_uuid if focal_node_uuid is provided and not empty
        search_kwargs = {
            "query": query,
            "num_results": num_results,
        }

        if focal_node_uuid and focal_node_uuid.strip():
            search_kwargs["center_node_uuid"] = focal_node_uuid

        search_results = await graphiti_client.search(**search_kwargs)

        if search_results:
            # Format results as structured data
            formatted_results = []
            for edge in search_results:
                result = {
                    "fact": edge.fact,
                    "source_node": edge.source_node_uuid,
                    "target_node": edge.target_node_uuid,
                    "created_at": str(edge.created_at) if edge.created_at else None,
                    "valid_at": str(edge.valid_at) if edge.valid_at else None,
                }
                formatted_results.append(result)

            response_data = {
                "query": query,
                "num_results": len(formatted_results),
                "results": formatted_results,
                "facts_summary": edges_to_facts_string(search_results),
            }
        else:
            response_data = {
                "query": query,
                "num_results": 0,
                "results": [],
                "facts_summary": "No results found for your query.",
            }

        return json.dumps(response_data, indent=2)

    except Exception as e:
        logger.error(f"Error searching graph: {str(e)}")
        return json.dumps({"error": f"Error searching graph: {str(e)}"}, indent=2)


@mcp.tool()
async def check_duplicates(
    ctx: Context, group_id: str = "sui-docs", similarity_threshold: float = 0.95
) -> str:
    """
    Check for duplicate content and facts in the knowledge graph.

    This tool analyzes the knowledge graph to find exact duplicates and near-duplicates
    based on embedding similarity.

    Args:
        ctx: The MCP server provided context, including the Graphiti client.
        group_id: Group ID to check for duplicates (default: "sui-docs").
        similarity_threshold: Similarity threshold for near-duplicates (0.0-1.0, default: 0.95).

    Returns:
        A JSON formatted string containing duplicate analysis results.
    """
    try:
        graphiti_client = ctx.request_context.lifespan_context.graphiti_client

        logger.info(
            f"Checking duplicates for group_id: {group_id}, threshold: {similarity_threshold}"
        )

        # Find exact duplicate content across all node types
        duplicates = await count_duplicate_content_all_nodes(
            graphiti_client.driver, group_id
        )

        # Find near-duplicate facts using embedding similarity
        similar_facts = await find_similar_facts(
            graphiti_client.driver,
            group_id=group_id,
            threshold=similarity_threshold,
            limit=1000,
        )

        # Format examples of similar facts
        examples = []
        for i, pair in enumerate(similar_facts[:5]):  # Show first 5 examples
            examples.append(
                {
                    "similarity": pair["similarity"],
                    "fact1": (
                        pair["fact1"][:200] + "..."
                        if len(pair["fact1"]) > 200
                        else pair["fact1"]
                    ),
                    "fact2": (
                        pair["fact2"][:200] + "..."
                        if len(pair["fact2"]) > 200
                        else pair["fact2"]
                    ),
                }
            )

        response_data = {
            "group_id": group_id,
            "similarity_threshold": similarity_threshold,
            "exact_duplicates": len(duplicates),
            "near_duplicate_pairs": len(similar_facts),
            "examples": examples,
        }

        return json.dumps(response_data, indent=2)

    except Exception as e:
        logger.error(f"Error checking duplicates: {str(e)}")
        return json.dumps({"error": f"Error checking duplicates: {str(e)}"}, indent=2)


@mcp.tool()
async def clean_duplicates(
    ctx: Context,
    group_id: str = "sui-docs",
    similarity_threshold: float = 0.95,
    remove_edges: bool = True,
    remove_nodes: bool = False,
    node_labels: list = None,
) -> str:
    """
    Remove duplicate facts and/or nodes from the knowledge graph.

    This tool removes duplicate content from the knowledge graph based on similarity analysis.
    Use with caution as this operation modifies the graph.

    Args:
        ctx: The MCP server provided context, including the Graphiti client.
        group_id: Group ID to clean (default: "sui-docs").
        similarity_threshold: Similarity threshold for duplicates (0.0-1.0, default: 0.95).
        remove_edges: Whether to remove duplicate edges/facts (default: True).
        remove_nodes: Whether to remove duplicate nodes (default: False).
        node_labels: List of node labels to clean when removing nodes (default: ["Entity", "Episodic"]).

    Returns:
        A JSON formatted string containing cleanup results.
    """
    try:
        graphiti_client = ctx.request_context.lifespan_context.graphiti_client

        if node_labels is None:
            node_labels = ["Entity", "Episodic"]

        logger.info(
            f"Cleaning duplicates for group_id: {group_id}, threshold: {similarity_threshold}"
        )

        results = {}

        # Remove duplicate edges if requested
        if remove_edges:
            logger.info("Removing duplicate edges...")
            edge_result = await remove_duplicate_facts(
                graphiti_client.driver,
                group_id=group_id,
                threshold=similarity_threshold,
            )
            results["edges_removed"] = edge_result

        # Remove duplicate nodes if requested
        if remove_nodes:
            logger.info("Removing duplicate nodes...")
            node_result = await remove_duplicate_nodes(
                graphiti_client.driver,
                group_id=group_id,
                node_labels=node_labels,
                threshold=similarity_threshold,
            )
            results["nodes_removed"] = node_result

        response_data = {
            "group_id": group_id,
            "similarity_threshold": similarity_threshold,
            "operations_performed": {
                "remove_edges": remove_edges,
                "remove_nodes": remove_nodes,
                "node_labels": node_labels if remove_nodes else None,
            },
            "results": results,
        }

        return json.dumps(response_data, indent=2)

    except Exception as e:
        logger.error(f"Error cleaning duplicates: {str(e)}")
        return json.dumps({"error": f"Error cleaning duplicates: {str(e)}"}, indent=2)


async def main():
    transport = os.getenv("MCP_TRANSPORT", "sse")
    print(f"Starting PCP Graph MCP Server with {transport} transport...")
    if transport == "sse":
        await mcp.run_sse_async()
    elif transport == "stdio":
        await mcp.run_stdio_async()
    else:
        print(f"Unsupported transport type: {transport}. Please use 'sse' or 'stdio'.")


if __name__ == "__main__":
    asyncio.run(main())
