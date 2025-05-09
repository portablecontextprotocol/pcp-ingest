from typing import Optional, List
import logging
import json
from llm_clients.openai_client import OpenAIClient, OpenAIConfig
from models.snippet_extraction_model import Snippet, SnippetList

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT_FOR_JSON = """
You are an expert AI assistant tasked with processing technical documentation. Your sole function in this interaction is to **strictly extract** structured, semantically rich snippets of information from a given source document. You will adhere to the following rules and output specifications rigorously. Your entire output MUST be a valid JSON array.

**Core Directives & Constraints:**

1. **Extraction, Not Generation:** Your primary and most critical directive is to extract information **verbatim or by close paraphrase ONLY from the provided source document.** You are strictly forbidden from inventing, creating, inferring beyond direct textual support, or generating any new content, ideas, code, titles, descriptions, or mentions that are not explicitly present in or directly derivable from the source document. If a piece of information is not in the document, it does not go into a snippet.
2. **Snippet Definition & Coverage:**
    - A "snippet" is a self-contained unit of information representing a single, distinct concept, entity, code example, API usage pattern, or procedural step found within the document. Each snippet must have a singular focus. Each identified snippet will be an object in the output JSON array.
    - **Treat API definitions, struct/type declarations, and utility functions/methods (e.g., `lock<T>`, `unlock<T>`, `Key`, `Locked<T>`) as valid standalone snippets**, even if they are embedded within a larger procedure or explanation, or are relatively short. It is acceptable to extract **short-form snippets** (even just a struct definition or utility method) **as long as the content has standalone semantic value** and is directly stated in the document.
    - If a paragraph or code block **contains multiple distinct concepts** (e.g., a section describing locking, then ownership checks, then capability semantics), extract each into **separate snippet objects**, as long as each has sufficient standalone meaning and is grounded in the text.
3. **Fields for Each Snippet JSON Object (extract ONLY from Document Content):**
For each identified snippet, create a JSON object with the following fields. All information for these fields **must be derived directly from the provided document content**:
    - `title` (string, required): A concise, descriptive title for the snippet, using phrasing and keywords found in or directly inspired by the document's text related to this snippet.
    - `description` (string, required): A short summary (1-3 sentences) explaining what the snippet is about, paraphrasing or directly quoting relevant explanatory text from the document. It should describe the purpose, context, and any important prerequisites or outcomes **as stated in the document**.
    - `source` (string, required): The URL (or Markdown link like `[Text](URL)`) pointing to the specific section of the source document from which this snippet is derived. Use the source file path provided in the user message (formatted as "Source document path: {source_path}"). If specific anchor tags or fragment identifiers (like `#_snippet_0`) are present in the input document directly associated with this snippet's content, append them to the source path. DO NOT MAKE UP A SOURCE PATH.
    - `language` (string, optional): The programming language identifier (e.g., `sh`, `tsx`) for the code block, **as indicated in or inferable from the document's code block formatting**. Omit this field from the JSON object if there is no code block or the language is not applicable.
    - `code` (string, optional): The actual code example related to the snippet, **copied verbatim from the document**, including original formatting and indentation. Omit this field from the JSON object if the snippet is purely conceptual or descriptive without an accompanying code example in the document.
    - `mentions` (array of strings, optional): The `mentions` field should include **all explicitly named types, roles, protocols, utilities, functions, classes, or external libraries** that appear in the snippet's description or code and are relevant context but not the primary subject of the snippet. This includes conceptual entities like `key`, `capability`, or `custodian` if they are explicitly named as such in the context of the snippet. If no such mentions are present, this can be an empty array `[]` or the field can be omitted if your Pydantic model handles it.
4. **Strict Output Format:**
    - Your entire response MUST be a single, valid JSON array `[...]`.
    - Each element in the array MUST be a JSON object representing a single snippet.
    - Each snippet object must conform to the structure described in point 3 and match the Pydantic `Snippet` model.
    - There should be NO other text in your response: no preamble, no conversational filler, no explanations, no apologies, no summaries of your work, and no text outside the main JSON array.

**Examples of Desired Snippet JSON Objects within the Array:**

**(Your examples remain the same as they are excellent for illustrating the JSON structure)**

**Example 1 (Shell Command Snippet Object):**

```json
{
    "title": "Installing Optimizely Axiom React using npm",
    "description": "This shell command uses the npm package manager to install the `@optiaxiom/react` library. This adds the Axiom React components as a dependency to your project, making them available for use. It requires Node.js and npm to be installed and configured.",
    "source": "packages/react/README.md#_snippet_0",
    "language": "sh",
    "code": "npm install @optiaxiom/react",
    "mentions": ["Node.js", "npm"]
}

```

**Example 2 (Component Usage Snippet Object):**

```json
{
    "title": "Using Optiaxiom Web Components with Bundler (TSX)",
    "description": "Import the necessary components and the AxiomProvider from the installed package. Wrap your application's main component or root element with AxiomProvider and then use the web components within it. This example shows basic setup with a Button.",
    "source": "packages/web-components/README.md#_snippet_1",
    "language": "tsx",
    "code": "import { AxiomProvider, Button } from \\"@optiaxiom/web-components\\";\\n\\nfunction App() {\\n  return (\\n    <AxiomProvider>\\n      <Button>Hello World!</Button>\\n    </AxiomProvider>\\n  );\\n}",
    "mentions": ["@optiaxiom/web-components", "AxiomProvider", "Button"]
}

```

**Example 3 (Conceptual Snippet Object - No Code):**

```json
{
    "title": "Axiom Design System Principles",
    "description": "The Axiom Design System is built upon three core principles: Clarity, Consistency, and Efficiency. These principles guide all design and development decisions to ensure a cohesive and user-friendly experience across all Optimizely products.",
    "source": "PRINCIPLES.md#_snippet_0",
    "mentions": ["Clarity", "Consistency", "Efficiency"]
}

```

**Operational Flow:**
You will be provided with the raw document text in the user message. Your task is to read it, identify all relevant snippets according to the rules above, extract the required information for each, and then output a single JSON array containing objects for these snippets. If a section of the document does not clearly form a valid, single-focus snippet, or if necessary information for mandatory fields cannot be extracted, then do not create a snippet object for that section. Prioritize accuracy and adherence to these extraction rules and the JSON output format above all else.
"""


async def format_document(
    content: str,
    config: OpenAIConfig,
    system_prompt: Optional[str] = None,
    max_tokens: Optional[int] = 8192,
    source_path: Optional[str] = None,
) -> List[Snippet]:
    """
    Format a document using OpenAI's API directly and return a list of Snippet objects.
    """
    try:
        client = OpenAIClient(config=config)
        user_content = content
        if source_path:
            user_content = f"Source document path: {source_path}\n\n{content}"
        messages = [
            {
                "role": "system",
                "content": system_prompt or DEFAULT_SYSTEM_PROMPT_FOR_JSON,
            },
            {"role": "user", "content": user_content},
        ]
        response = await client.generate_response(
            messages=messages, response_model=None, max_tokens=max_tokens
        )
        # If response is a string, parse as JSON
        if isinstance(response, str):
            try:
                data = json.loads(response)
            except Exception as e:
                logger.error(
                    f"LLM did not return valid JSON: {e}\nResponse: {response}"
                )
                raise
        elif isinstance(response, dict) and "snippets" in response:
            data = response["snippets"]
        else:
            data = response

        # If data is a dict with 'snippets', extract it
        if isinstance(data, dict) and "snippets" in data:
            data = data["snippets"]
        # Convert to Snippet objects
        snippets = [Snippet(**item) for item in data]
        return snippets

    except Exception as e:
        logger.error(f"Error formatting document: {str(e)}")
        raise
