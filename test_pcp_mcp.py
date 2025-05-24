#!/usr/bin/env python3
"""
Test script for the PCP MCP Server.
This script tests the MCP server tools by making direct function calls.
"""

import asyncio
import json
from dotenv import load_dotenv

# Import the MCP server components
from pcp_mcp_server import pcp_lifespan, search_graph, check_duplicates


# Mock context class for testing
class MockContext:
    def __init__(self, lifespan_context):
        self.request_context = MockRequestContext(lifespan_context)


class MockRequestContext:
    def __init__(self, lifespan_context):
        self.lifespan_context = lifespan_context


class MockServer:
    pass


async def test_mcp_server():
    """Test the MCP server tools."""

    print("🚀 Starting PCP MCP Server Test")
    print("=" * 50)

    try:
        # Initialize the lifespan context (this sets up the Graphiti client)
        mock_server = MockServer()

        async with pcp_lifespan(mock_server) as context:
            print("✅ Graphiti client initialized successfully")

            # Create mock context for tool calls
            mock_ctx = MockContext(context)

            # Test 1: Search functionality
            print("\n📊 Test 1: Search Graph")
            print("-" * 30)

            test_query = "What is Sui?"
            print(f"Searching for: '{test_query}'")

            search_result = await search_graph(
                ctx=mock_ctx, query=test_query, num_results=5
            )

            print("Search Results:")
            # Parse and pretty print the JSON result
            result_data = json.loads(search_result)
            print(f"Query: {result_data['query']}")
            print(f"Number of results: {result_data['num_results']}")

            if result_data["num_results"] > 0:
                print("\nFacts found:")
                for i, result in enumerate(
                    result_data["results"][:3], 1
                ):  # Show first 3
                    print(f"{i}. {result['fact'][:100]}...")
            else:
                print("No results found")

            # Test 2: Check duplicates
            print("\n🔍 Test 2: Check Duplicates")
            print("-" * 30)

            duplicates_result = await check_duplicates(
                ctx=mock_ctx, group_id="sui-docs", similarity_threshold=0.95
            )

            dup_data = json.loads(duplicates_result)
            print(f"Group ID: {dup_data['group_id']}")
            print(f"Exact duplicates: {dup_data['exact_duplicates']}")
            print(f"Near-duplicate pairs: {dup_data['near_duplicate_pairs']}")

            if dup_data["examples"]:
                print("\nExample similar facts:")
                for i, example in enumerate(dup_data["examples"][:2], 1):
                    print(f"{i}. Similarity: {example['similarity']:.4f}")
                    print(f"   Fact 1: {example['fact1'][:80]}...")
                    print(f"   Fact 2: {example['fact2'][:80]}...")

            print("\n✅ All tests completed successfully!")

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback

        traceback.print_exc()


async def test_server_startup():
    """Test that the server can start up without errors."""
    print("\n🌐 Test 3: Server Startup")
    print("-" * 30)

    try:
        # Import the main server components
        from pcp_mcp_server import mcp

        print("✅ MCP server configuration loaded successfully")
        print(f"Server name: {mcp.name}")
        print("Server tools:")

        # List available tools
        tools = [
            "search_graph - Search the knowledge graph",
            "check_duplicates - Check for duplicate content",
            "clean_duplicates - Remove duplicate content",
        ]
        for tool in tools:
            print(f"  • {tool}")

    except Exception as e:
        print(f"❌ Error loading server configuration: {str(e)}")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    async def run_all_tests():
        await test_mcp_server()
        await test_server_startup()
        print("\n🎉 Testing completed!")

    asyncio.run(run_all_tests())
