from typing import Optional, List, Dict, Any
import logging
from pydantic import BaseModel
import openai
import time
import random
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from models.snippet_extraction_model import SnippetList

logger = logging.getLogger(__name__)


class OpenAIConfig(BaseModel):
    """Configuration for OpenAI client"""

    api_key: str
    base_url: str = "http://127.0.0.1:1234/v1"
    model: str = "gpt-4-turbo-preview"
    max_tokens: int = 8192
    temperature: float = 0.0
    max_retries: int = 5
    initial_retry_delay: float = 1.0
    max_retry_delay: float = 60.0


class OpenAIClient:
    """Direct OpenAI API client implementation"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = openai.AsyncOpenAI(
            api_key=config.api_key, base_url=config.base_url
        )
        logger.info(f"OpenAI client initialized with base URL: {self.client.base_url}")

    @retry(
        retry=retry_if_exception_type(
            (openai.APIConnectionError, openai.APITimeoutError)
        ),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        reraise=True,
    )
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_model: Optional[Any] = None,
        max_tokens: Optional[int] = None,
    ) -> Any:
        """Generate a response using OpenAI's API with proper error handling and retries"""
        try:
            response_schema = {
                "type": "json_schema",
                "json_schema": {
                    "name": "snippet_schema",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "snippets": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "source": {"type": "string", "format": "uri"},
                                        "language": {"type": "string"},
                                        "code": {"type": "string"},
                                        "mentions": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                    },
                                    "required": [
                                        "title",
                                        "description",
                                        "source",
                                        "language",
                                        "code",
                                        "mentions",
                                    ],
                                    "additionalProperties": False,
                                },
                                "minItems": 1,
                            }
                        },
                        "required": ["snippets"],
                    },
                },
            }

            response = await self.client.beta.chat.completions.parse(
                model=self.config.model,
                messages=messages,
                temperature=0,
                max_tokens=max_tokens or self.config.max_tokens,
                response_format=response_schema,
            )

            # Extract the response content
            content = response.choices[0].message.content
            return content

        except openai.APIConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise
        except openai.APITimeoutError as e:
            logger.error(f"Timeout error: {str(e)}")
            raise
        except openai.RateLimitError as e:
            logger.error(f"Rate limit error: {str(e)}")
            raise
        except openai.APIError as e:
            logger.error(f"API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
