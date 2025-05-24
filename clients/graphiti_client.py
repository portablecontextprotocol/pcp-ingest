import os
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse

from graphiti_core import Graphiti
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig
from graphiti_core.llm_client.openai_generic_client import LLMConfig
from graphiti_core.utils.maintenance.graph_data_operations import clear_data
from clients.openai_compatible_client import OpenAIGenericClientJSONResponse

# Configure logging
logger = logging.getLogger(__name__)

# Singleton instance
_graphiti_instance = None


def validate_api_base(api_base: str) -> str:
    """
    Ensure the API base URL has a valid protocol.

    Args:
        api_base: The API base URL to validate

    Returns:
        A validated API base URL with proper protocol
    """
    parsed_url = urlparse(api_base)
    if not parsed_url.scheme:
        api_base = f"https://{api_base}"
    elif parsed_url.scheme not in ["http", "https"]:
        raise ValueError("API base URL must use either http:// or https:// protocol")
    return api_base


def create_openai_config(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
) -> LLMConfig:
    """
    Create an OpenAI configuration with appropriate defaults.

    Args:
        api_key: The OpenAI API key (defaults to environment variable)
        api_base: The API base URL (defaults to localhost for local models)
        model: The model name to use (defaults to environment variable or fallback)

    Returns:
        Configured OpenAIConfig instance
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    api_base = api_base or os.environ.get("OPENAI_API_BASE", "http://127.0.0.1:1234/v1")
    model = model or os.environ.get("OPENAI_MODEL", "qwen3-30b-a3b")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY must be provided or set as environment variable"
        )

    # Validate API base URL
    api_base = validate_api_base(api_base)

    return LLMConfig(
        api_key=api_key,
        base_url=api_base,
        model=model,
        temperature=0,  # Set to 0 for deterministic responses
        max_tokens=32768,
    )


def create_openai_embedder_config(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    embedding_model: Optional[str] = None,
) -> OpenAIEmbedderConfig:
    """
    Create an OpenAI Embedder configuration with appropriate defaults.

    Args:
        api_key: The OpenAI API key (defaults to environment variable)
        api_base: The API base URL (defaults to localhost for local models)
        embedding_model: The embedding model name (defaults to environment variable or fallback)

    Returns:
        Configured OpenAIEmbedderConfig instance
    """
    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    api_base = api_base or os.environ.get("OPENAI_API_BASE", "http://127.0.0.1:1234/v1")
    embedding_model = embedding_model or os.environ.get(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-nomic-embed-text-v1.5"
    )

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY must be provided or set as environment variable for embedder"
        )

    # Validate API base URL
    api_base = validate_api_base(api_base)

    return OpenAIEmbedderConfig(
        embedding_model=embedding_model,
        api_key=api_key,
        base_url=api_base,
    )


def get_graphiti_client(
    openai_config: Optional[LLMConfig] = None,
    embedder_config: Optional[OpenAIEmbedderConfig] = None,
    neo4j_uri: Optional[str] = None,
    neo4j_user: Optional[str] = None,
    neo4j_password: Optional[str] = None,
    cache: bool = False,
    force_new: bool = False,
) -> Graphiti:
    """
    Initialize and return a configured Graphiti client using a singleton pattern.

    The first call to this function will create the instance with the provided parameters.
    Subsequent calls will return the existing instance unless force_new=True.

    Args:
        openai_config: OpenAI configuration, will be created if not provided
        embedder_config: OpenAI Embedder configuration, will be created if not provided
        neo4j_uri: Neo4j URI (defaults to environment variable)
        neo4j_user: Neo4j username (defaults to environment variable)
        neo4j_password: Neo4j password (defaults to environment variable)
        cache: Whether to enable LLM caching
        force_new: Force creation of a new instance, even if one already exists

    Returns:
        Configured Graphiti instance (singleton)
    """
    global _graphiti_instance

    # Return existing instance if we have one and not forcing a new one
    if _graphiti_instance is not None and not force_new:
        logger.debug("Returning existing Graphiti client instance")
        return _graphiti_instance

    # Handle OpenAI configuration
    if openai_config is None:
        openai_config = create_openai_config()

    # Handle Embedder configuration
    if embedder_config is None:
        embedder_config = create_openai_embedder_config(
            api_key=openai_config.api_key,
            api_base=openai_config.base_url,
        )

    # Handle Neo4j configuration
    neo4j_uri = neo4j_uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = neo4j_user or os.environ.get("NEO4J_USER", "neo4j")
    neo4j_password = neo4j_password or os.environ.get("NEO4J_PASSWORD", "pass123abcd")

    if not neo4j_uri or not neo4j_user or not neo4j_password:
        raise ValueError(
            "NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be provided or set as environment variables"
        )

    # Create Graphiti client
    logger.info(f"Creating new Graphiti client instance (NEO4J URI: {neo4j_uri})")
    _graphiti_instance = Graphiti(
        neo4j_uri,
        neo4j_user,
        neo4j_password,
        llm_client=OpenAIGenericClientJSONResponse(
            config=openai_config,
            cache=cache,
        ),
        embedder=OpenAIEmbedder(
            config=embedder_config,
        ),
    )

    return _graphiti_instance


async def clear_graph():
    """
    Clear the Graphiti graph.
    """
    global _graphiti_instance

    await clear_data(_graphiti_instance.driver)
    await _graphiti_instance.build_indices_and_constraints()


async def close_graphiti_client():
    """
    Close the Graphiti client connection if it exists.
    Should be called when shutting down the application.
    """
    global _graphiti_instance

    if _graphiti_instance is not None:
        logger.info("Closing Graphiti client connection")
        await _graphiti_instance.close()
        _graphiti_instance = None
