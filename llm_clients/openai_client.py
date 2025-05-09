from typing import Optional, List, Dict, Any
import logging
from pydantic import BaseModel
import openai
from models.snippet_extraction_model import SnippetList

logger = logging.getLogger(__name__)


class OpenAIConfig(BaseModel):
    """Configuration for OpenAI client"""

    api_key: str
    base_url: str = "http://127.0.0.1:/v1"
    model: str = "gpt-4-turbo-preview"
    max_tokens: int = 8192
    temperature: float = 0.0


class OpenAIClient:
    """Direct OpenAI API client implementation"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = openai.AsyncOpenAI(
            api_key=config.api_key, base_url=config.base_url
        )
        print(self.client.base_url)

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        response_model: Optional[Any] = None,
        max_tokens: Optional[int] = None,
    ) -> Any:
        """Generate a response using OpenAI's API with proper error handling and retries"""
        try:
            # response = await self.client.chat.completions.create(
            #     model=self.config.model,
            #     messages=messages,
            #     temperature=self.config.temperature,
            #     max_tokens=max_tokens or self.config.max_tokens,
            #     # response_format=response_model,
            # )

            # response_schema = {
            #     "$schema": "http://json-schema.org/draft-07/schema#",
            #     "type": "array",
            #     "items": {
            #         "type": "object",
            #         "required": [
            #             "title",
            #             "description",
            #             "source",
            #             "language",
            #             "code",
            #             "mentions",
            #         ],
            #         "properties": {
            #             "title": {"type": "string"},
            #             "description": {"type": "string"},
            #             "source": {"type": "string", "format": "uri"},
            #             "language": {"type": "string"},
            #             "code": {"type": "string"},
            #             "mentions": {"type": "array", "items": {"type": "string"}},
            #         },
            #         "additionalProperties": "false",
            #     },
            # }

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

            # response_schema = {
            #     "type": "json_schema",
            #     "json_schema": {
            #         "name": "snippet_schema",
            #         "strict": True,
            #         "schema": payload_schema,
            #     },
            # }

            response = await self.client.beta.chat.completions.parse(
                model=self.config.model,
                messages=messages,
                temperature=0,
                max_tokens=max_tokens or self.config.max_tokens,
                # response_format={"type": "json_object"},
                response_format=response_schema,
            )

            # Extract the response content
            content = response.choices[0].message.content

            # If a response model is provided, validate the response
            # if response_model and content:
            #     return response_model.model_validate_json(content)

            return content

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
