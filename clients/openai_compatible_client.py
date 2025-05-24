import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from logging import INFO, DEBUG
from urllib.parse import urlparse

from graphiti_core.llm_client.openai_generic_client import (
    OpenAIGenericClient,
    LLMConfig,
)

from dotenv import load_dotenv
import openai


# Enable debug logging for OpenAI
openai.log = "debug"

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
api_base = os.environ.get("OPENAI_API_BASE", "http://127.0.0.1:1234/v1")
model = os.environ.get(
    "OPENAI_MODEL", "qwen3-30b-a3b"
)  # Default to gpt-4.1-mini if not specified

if not api_key or not api_base:
    raise ValueError(
        "OPENAI_API_KEY and OPENAI_API_BASE environment variables must be set"
    )

# Ensure api_base has a protocol
parsed_url = urlparse(api_base)
if not parsed_url.scheme:
    api_base = f"https://{api_base}"  # Default to https if no protocol specified
elif parsed_url.scheme not in ["http", "https"]:
    raise ValueError("OPENAI_API_BASE must use either http:// or https:// protocol")

# Log the configuration for debugging
logger.info(f"Using API base URL: {api_base}")
logger.info(f"Using model: {model}")


class OpenAIGenericClientJSONResponse(OpenAIGenericClient):
    """OpenAI-compatible client with working _generate_response and constructor."""

    def __init__(self, config=None, cache=False, client=None):
        load_dotenv()
        if config is None:
            # Fallback to environment variables if config is not provided
            api_key = os.environ.get("OPENAI_API_KEY")
            api_base = os.environ.get("OPENAI_API_BASE", "http://127.0.0.1:1234/v1")
            model = os.environ.get("OPENAI_MODEL", "qwen3-30b-a3b")
            if not api_key or not api_base:
                raise ValueError(
                    "OPENAI_API_KEY and OPENAI_API_BASE environment variables must be set"
                )
            config = type(
                "LLMConfig",
                (),
                {
                    "api_key": api_key,
                    "base_url": api_base,
                    "model": model,
                    "max_tokens": 8192,
                    "temperature": 0.0,
                },
            )()
        super().__init__(config, cache, client)
        # Ensure the OpenAI client is set up correctly
        if client is None:
            self.client = openai.AsyncOpenAI(
                api_key=config.api_key, base_url=config.base_url
            )
        else:
            self.client = client
        self.model = getattr(config, "model", "qwen3-30b-a3b")
        self.max_tokens = getattr(config, "max_tokens", 8192)
        self.temperature = getattr(config, "temperature", 0.0)
        logger.info(f"Using API base URL: {config.base_url}")
        logger.info(f"Using model: {self.model}")

    async def _generate_response(
        self,
        messages,
        response_model=None,
        max_tokens=8192,
        model_size="medium",
    ):
        openai_messages = []
        for m in messages:
            # Assume m has 'role' and 'content' attributes
            if hasattr(m, "content"):
                content = m.content
            else:
                content = m.get("content")
            if hasattr(m, "role"):
                role = m.role
            else:
                role = m.get("role")
            openai_messages.append({"role": role, "content": content})
        try:
            logger.debug(f"Sending messages: {json.dumps(openai_messages, indent=2)}")
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=openai_messages,
                temperature=self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                response_format=response_model,
            )
            logger.debug(f"LLM response: {response}")
            result = response.choices[0].message.content
            return json.loads(result)
        except Exception as e:
            logger.error(f"Error in generating LLM response: {e}")
            raise
