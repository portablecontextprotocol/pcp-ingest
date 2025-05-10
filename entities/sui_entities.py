# Import necessary base classes from Pydantic
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any

# --- Core Sui & Move Language Entities ---


class SuiGeneralConcept(BaseModel):
    """Represents a fundamental concept, principle, or mechanism within the Sui ecosystem.

    These are often high-level ideas that explain how Sui works, distinct from specific code constructs
    but essential for understanding the platform (e.g., Object Model, Consensus, Gas, Programmable Transaction Blocks).

    Instructions for identifying and extracting SuiGeneralConcept:
    1. Look for introductory sections, overviews, or glossaries defining key terms.
    2. Identify headings or paragraphs explaining core Sui mechanics, architecture, or economic models.
    3. Extract the name of the concept (e.g., "Shared Objects", "Owned Objects", "Epochs", "Validators", "Gas Fees").
    4. Capture a detailed explanation of the concept, its purpose, and its implications within Sui.
    5. Note any explicitly mentioned trade-offs, benefits, or limitations.
    6. Identify the source document and relevant section.
    """

    concept_name: str = Field(
        ...,
        description="The name of the Sui general concept (e.g., 'Shared Objects', 'Programmable Transaction Blocks', 'Consensus').",
    )
    description: str = Field(
        ...,
        description="A comprehensive explanation of the concept, its significance in the Sui ecosystem, and its key characteristics.",
    )
    category: Optional[str] = Field(
        None,
        description="A high-level category for the concept (e.g., 'Object Model', 'Transaction Lifecycle', 'Network Architecture', 'Tokenomics').",
    )
    key_properties_or_implications: List[str] = Field(
        default_factory=list,
        description="A list of key properties, implications, benefits, or trade-offs associated with this concept. Each item should be a JSON string representing the property or implication.",
    )
    related_concepts: List[str] = Field(
        default_factory=list,
        description="List of other SuiGeneralConcept names that are closely related or often discussed in conjunction.",
    )
    source_file: Optional[str] = Field(
        None,
        description="The name of the source documentation file or URL where this concept is primarily described.",
    )


class MoveModuleDefinition(BaseModel):
    """Represents a Move module, which is a collection of struct and function definitions.

    Modules are the basic unit of code organization and deployment in Move.

    Instructions for identifying and extracting MoveModuleDefinition:
    1. Look for `module <address>::<name> { ... }` declarations in code blocks.
    2. Identify sections describing the purpose and contents of a specific Move module.
    3. Extract the module name and its (optional) on-chain address if specified.
    4. Summarize the module's overall purpose or domain.
    5. List any other modules it explicitly uses or depends on (e.g., `use sui::coin::Coin;`).
    """

    module_name: str = Field(
        ..., description="The name of the Move module (e.g., 'coin', 'escrow', 'capy')."
    )
    full_address_and_name: Optional[str] = Field(
        None,
        description="The full module identifier including its address if published (e.g., '0x2::coin', '0x...::my_module'). If only name is present, use name.",
    )
    description: str = Field(
        ...,
        description="A summary of the module's purpose, responsibilities, and the domain it models.",
    )
    dependencies: List[str] = Field(
        default_factory=list,
        description="A list of other modules this module uses (e.g., ['sui::tx_context', 'sui::transfer']).",
    )
    source_file: Optional[str] = Field(
        None,
        description="The source file or documentation page where this module is defined or primarily discussed.",
    )


class MoveStructDefinition(BaseModel):
    """Represents a custom data type (struct) defined within a Move module.

    Structs are user-defined types that group named fields, similar to structs or classes in other languages.

    Instructions for identifying and extracting MoveStructDefinition:
    1. Look for `struct <Name> <abilities?> { ... }` declarations in Move code.
    2. Identify sections detailing the structure and purpose of a specific data type.
    3. Extract the struct name and the module it belongs to.
    4. List its abilities (e.g., 'key', 'store', 'copy', 'drop').
    5. Detail its fields: name, type, and any comments explaining the field.
    6. Capture the overall purpose or role of the struct.
    """

    struct_name: str = Field(
        ...,
        description="The name of the struct (e.g., 'Coin', 'Capy', 'Escrow', 'Key').",
    )
    module_name: str = Field(
        ..., description="The name of the Move module where this struct is defined."
    )
    description: str = Field(
        ...,
        description="An explanation of what this struct represents, its purpose, and how it's used.",
    )
    abilities: List[str] = Field(
        default_factory=list,
        description="A list of abilities associated with the struct (e.g., ['key', 'store']).",
    )
    fields: List[str] = Field(
        default_factory=list,
        description='A list of fields within the struct. Each item should be a JSON string with \'name\', \'type\', and \'description\' keys (e.g., \'{"name": "id", "type": "UID", "description": "Unique identifier."}\').',
    )
    is_object_type: Optional[bool] = Field(  # Sui specific addition
        None,
        description="Indicates if this struct typically represents a Sui Object (often having an 'id: UID' field as the first field and 'key' ability).",
    )
    generic_parameters: Optional[str] = Field(
        None,
        description="Description of generic type parameters if the struct is generic (e.g., 'T: store', 'K: copy + drop, V: store').",
    )
    source_file: Optional[str] = Field(
        None,
        description="The source file or documentation page where this struct is defined.",
    )


class MoveFunctionDefinition(BaseModel):
    """Represents a function defined within a Move module.

    Functions contain the logic for manipulating structs and interacting with the Sui state.

    Instructions for identifying and extracting MoveFunctionDefinition:
    1. Look for `fun <name><generics?>(<params>): <return_type?> { ... }` declarations.
    2. Identify explanations of a function's behavior, parameters, and return values.
    3. Extract the function name, its module, visibility (public, private, friend), and if it's an 'entry' function.
    4. Detail its parameters: name, type, and description.
    5. Specify the return type(s).
    6. Describe the function's purpose, logic, and any side effects (e.g., emitting events, transferring objects).
    7. Note any generic type parameters and their constraints (e.g., `T: key + store`).
    """

    function_name: str = Field(
        ...,
        description="The name of the function (e.g., 'split', 'transfer', 'create_escrow').",
    )
    module_name: str = Field(
        ..., description="The name of the Move module where this function is defined."
    )
    description: str = Field(
        ...,
        description="A detailed explanation of the function's purpose, its core logic, what it accomplishes, and any important pre/post conditions.",
    )
    visibility: str = Field(
        ...,
        description="The visibility of the function (e.g., 'public', 'public(friend)', 'private').",
    )
    is_entry_function: bool = Field(
        default=False,
        description="True if the function is an 'entry' function, callable directly in a transaction.",
    )
    parameters: List[str] = Field(
        default_factory=list,
        description='A list of parameters. Each item should be a JSON string with \'name\', \'type\', and \'description\' (e.g., \'{"name": "coin", "type": "Coin<SUI>", "description": "The coin to split."}\').',
    )
    return_type: Optional[str] = Field(
        None,
        description="The return type(s) of the function. If multiple, represent as a tuple string e.g., '(Coin<SUI>, Coin<SUI>)' or describe.",
    )
    generic_parameters: Optional[str] = Field(
        None,
        description="Description of generic type parameters and their constraints if the function is generic (e.g., 'T: store', 'CoinType: drop').",
    )
    emits_events: List[str] = Field(
        default_factory=list,
        description="A list of event types (struct names) that this function may emit.",
    )
    aborts_with: List[str] = Field(
        default_factory=list,
        description="A list of custom error names or conditions under which this function explicitly aborts.",
    )
    usage_notes_or_examples: Optional[str] = Field(
        None,
        description="Specific notes on how to use this function, common patterns, or brief textual examples if code examples are separate.",
    )
    source_file: Optional[str] = Field(
        None,
        description="The source file or documentation page where this function is defined.",
    )


class SuiEventDefinition(BaseModel):
    """Represents an event struct that can be emitted by Move functions in Sui.

    Events provide a way for on-chain activities to signal off-chain listeners.

    Instructions for identifying and extracting SuiEventDefinition:
    1. Look for struct definitions that are used in `sui::event::emit<EventType>(...)` calls.
    2. Identify documentation sections describing specific events, their fields, and when they are emitted.
    3. Extract the event name (which is a struct name).
    4. Detail its fields: name, type, and description.
    5. Describe the purpose of the event and the circumstances under which it is emitted.
    """

    event_name: str = Field(
        ...,
        description="The name of the event struct (e.g., 'EscrowCreated', 'CoinMinted').",
    )
    module_name: str = Field(
        ...,
        description="The name of the Move module where this event struct is defined.",
    )
    description: str = Field(
        ...,
        description="An explanation of what this event signifies and the context in which it's emitted.",
    )
    fields: List[str] = Field(
        default_factory=list,
        description="A list of fields within the event struct. Each item should be a JSON string with 'name', 'type', and 'description'.",
    )
    emitted_by_functions: List[str] = Field(
        default_factory=list,
        description="A list of function names (e.g., 'module_name::function_name') that are known to emit this event.",
    )
    source_file: Optional[str] = Field(
        None,
        description="The source file or documentation page where this event is defined or discussed.",
    )


class MoveErrorCodeDefinition(BaseModel):
    """Represents a custom error code defined in Move, typically as a constant used in `assert!` or `abort`.

    Error codes help in diagnosing transaction failures.

    Instructions for identifying and extracting MoveErrorCodeDefinition:
    1. Look for `const <ERROR_NAME>: u64 = <value>;` declarations, especially if they are used in `abort <ERROR_NAME>` or `assert!(..., <ERROR_NAME>)`.
    2. Identify sections in documentation that list or explain custom error codes for a module.
    3. Extract the error name (constant name) and its numeric value.
    4. Describe the condition or reason this error signifies.
    """

    error_name: str = Field(
        ...,
        description="The constant name of the error code (e.g., 'EIncorrectSigner', 'EAmountCannotBeZero').",
    )
    module_name: str = Field(
        ..., description="The name of the Move module where this error code is defined."
    )
    error_value: Optional[int] = (
        Field(  # Error codes are u64 in Move, but often represented as int.
            None, description="The numeric value of the error code."
        )
    )
    description: str = Field(
        ...,
        description="A clear explanation of what condition this error code represents and why a transaction might abort with it.",
    )
    source_file: Optional[str] = Field(
        None,
        description="The source file or documentation page where this error is defined or discussed.",
    )


# --- Sui Ecosystem & Tooling Entities ---


class SuiClientCommand(BaseModel):
    """Represents a command for the Sui Client CLI.

    The CLI is a primary tool for developers to interact with the Sui network.

    Instructions for identifying and extracting SuiClientCommand:
    1. Look for documentation sections dedicated to the Sui CLI.
    2. Identify headings or descriptions of specific commands (e.g., `sui client object <OBJECT_ID>`, `sui client publish`).
    3. Extract the base command and any subcommands.
    4. Describe what the command does.
    5. Capture example usage, including common flags and arguments.
    6. List key options/flags and their purpose.
    """

    command_string: str = Field(
        ...,
        description="The full command string, including subcommands (e.g., 'sui client object', 'sui client publish').",
    )
    description: str = Field(
        ...,
        description="An explanation of what the CLI command does and its common use cases.",
    )
    example_usage: Optional[str] = Field(
        None,
        description="A typical example of how to use the command, including placeholders for arguments.",
    )
    key_options_flags: List[str] = Field(
        default_factory=list,
        description="A list of important options/flags. Each item should be a JSON string with 'flag' (e.g., '--gas-budget', '--json') and 'description'.",
    )
    related_concepts_or_tasks: List[str] = Field(
        default_factory=list,
        description="Concepts or tasks this command is typically used for (e.g., 'Object Inspection', 'Package Deployment').",
    )
    source_file: Optional[str] = Field(
        None, description="The documentation page detailing this CLI command."
    )


class SuiRPCMethodDefinition(BaseModel):
    """Represents a Sui JSON-RPC API method.

    RPC methods allow applications to interact with a Sui node programmatically.

    Instructions for identifying and extracting SuiRPCMethodDefinition:
    1. Look for API reference documentation listing JSON-RPC methods.
    2. Identify specific method names (e.g., `sui_getObject`, `sui_executeTransactionBlock`).
    3. Describe the purpose of the RPC method.
    4. Detail its request parameters (name, type, required, description).
    5. Describe the structure of its JSON response.
    6. Capture example requests and responses if provided.
    """

    method_name: str = Field(
        ...,
        description="The name of the JSON-RPC method (e.g., 'sui_getObject', 'sui_tryExecuteTransactionBlock').",
    )
    description: str = Field(
        ...,
        description="A detailed explanation of what the RPC method does, its purpose, and any important considerations for its use.",
    )
    request_parameters: List[str] = Field(
        default_factory=list,
        description="A list of request parameters. Each item should be a JSON string with 'name', 'type', 'required' (bool), and 'description'.",
    )
    response_description: str = Field(
        ...,
        description="A description of the JSON response structure, including key fields and their meanings.",
    )
    example_request_json: Optional[str] = Field(
        None, description="An example JSON payload for the request."
    )
    example_response_json: Optional[str] = Field(
        None, description="An example JSON payload for the response."
    )
    source_file: Optional[str] = Field(
        None,
        description="The API documentation page where this RPC method is described.",
    )


class DeveloperGuide(BaseModel):
    """Represents a walkthrough, tutorial, or instructional document within the Sui documentation.

    Guides typically provide step-by-step instructions for setup, specific tasks, or understanding complex workflows.
    This is similar to your original Guide but tailored for how Sui docs might structure extensive guides.

    Instructions for identifying and extracting DeveloperGuide:
    1. Look for documentation pages or sections explicitly labeled as "Guides," "Tutorials," or "Walkthroughs."
    2. Identify documents that provide sequential steps or explanations for achieving a specific goal (e.g., "Building your first dApp", "Understanding PTBs", "Custom NFT Tutorial").
    3. Extract the main title or topic of the guide.
    4. Capture a brief description summarizing the guide's objective and target audience.
    5. List the key learning objectives or topics covered.
    """

    title: str = Field(
        ...,
        description="The primary title of the guide or tutorial (e.g., 'Getting Started with Sui Move', 'Building a DeFi Application').",
    )
    description: str = Field(
        ...,
        description="A concise summary of the guide's purpose, what the reader will learn, and its target audience.",
    )
    category: Optional[str] = Field(  # e.g., "Smart Contracts", "Client SDK", "Tooling"
        None,
        description="A category for the guide, if applicable (e.g., 'Smart Contracts', 'Tooling', 'Application Development').",
    )
    key_topics_or_steps_covered: List[str] = Field(
        default_factory=list,
        description="A list of major topics, concepts, or high-level steps covered in the guide.",
    )
    prerequisites: List[str] = Field(
        default_factory=list,
        description="Any prerequisite knowledge or setup mentioned for following the guide.",
    )
    source_file: Optional[str] = Field(
        None, description="The name of the source markdown file or URL for the guide."
    )


# Dictionary mapping entity names to their corresponding Pydantic models
SUI_ENTITY_TYPES: Dict[str, Any] = {
    "SuiGeneralConcept": SuiGeneralConcept,
    "MoveModuleDefinition": MoveModuleDefinition,
    "MoveStructDefinition": MoveStructDefinition,
    "MoveFunctionDefinition": MoveFunctionDefinition,
    "SuiEventDefinition": SuiEventDefinition,
    "MoveErrorCodeDefinition": MoveErrorCodeDefinition,
    "SuiClientCommand": SuiClientCommand,
    "SuiRPCMethodDefinition": SuiRPCMethodDefinition,
    "DeveloperGuide": DeveloperGuide,
}

print("Sui/Move entity definitions created successfully.")

# # You can optionally print the schema for verification
# import json
# for name, model in SUI_ENTITY_TYPES.items():
#     print(f"\nSchema for {name}:")
#     # Pydantic V2 uses model_json_schema()
#     print(json.dumps(model.model_json_schema(), indent=2))
