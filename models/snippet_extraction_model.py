from typing import List, Optional
from pydantic import BaseModel, Field, RootModel


class Snippet(BaseModel):
    """
    Represents a single extracted snippet from code documentation.
    """

    title: str = Field(
        ...,
        description="A concise, descriptive title for the snippet.",
        examples=["Installing Optimizely Axiom React using npm"],
    )
    description: str = Field(
        ...,
        description="A short summary explaining what the snippet is about.",
        examples=[
            "This shell command uses the npm package manager to install the `@optiaxiom/react` library."
        ],
    )
    source: str = (
        Field(  # Using str as the example output is "[Text](URL)", not just the URL
            ...,
            description="The Markdown link (e.g., [Text](URL)) or just URL pointing to the source of the snippet.",
            examples=[
                "[https://github.com/optimizely-axiom/optiaxiom/blob/main/packages/react/README.md#_snippet_0](https://github.com/optimizely-axiom/optiaxiom/blob/main/packages/react/README.md#_snippet_0)"
            ],
        )
    )
    language: Optional[str] = Field(
        default=None,
        description="The programming language of the code block (e.g., sh, tsx).",
        examples=["sh", "tsx"],
    )
    code: Optional[str] = Field(
        default=None,
        description="The actual code example related to the snippet, as a string.",
        examples=["npm install @optiaxiom/react"],
    )
    mentions: List[str] = Field(
        default_factory=list,
        description="A list of other key entities, libraries, or concepts mentioned.",
        examples=[["Node.js", "npm"], ["@optiaxiom/web-components"]],
    )
    source_path: Optional[str] = Field(
        default=None,
        description="The path to the source Markdown file from which this snippet was extracted.",
        examples=["assets/sui-docs/docs_guides/write-package.md"],
    )


class SnippetList(BaseModel):
    snippets: List[Snippet]


# ——— 1) Generate the full Pydantic JSON Schema ———
full = SnippetList.model_json_schema()

# full looks like:
# {
#   'type':'object',
#   'properties': {
#     'snippets': {
#       'type':'array',
#       'items': {'$ref':'#/definitions/Snippet'}
#     }
#   },
#   'required':['snippets'],
#   'additionalProperties': False,
#   '$defs': {
#     'Snippet': { ... the snippet schema ... }
#   }
# }

# ——— 2) Extract and inline the Snippet definition ———
snippet_def = full["$defs"]["Snippet"]

# Build a clean, minimal wrapper
clean_schema = {
    "type": "object",
    "properties": {"snippets": {"type": "array", "items": snippet_def, "minItems": 1}},
    "required": ["snippets"],
    "additionalProperties": False,
}

# ——— 3) Wrap it for the API ———
payload_schema = {
    "type": "json_schema",
    "json_schema": {"name": "snippet_schema", "strict": True, "schema": clean_schema},
}
