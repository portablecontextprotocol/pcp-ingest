# Import necessary base classes from Pydantic
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Define the custom entities based on the software documentation structure


class ComponentJSX(BaseModel):
    """Represents a specific UI component within the design library (e.g., Banner, Button, Box).

    Components are the building blocks of the UI. Extract information about their purpose,
    how they are used, and their available configurations (props).

    Instructions for identifying and extracting Components:
    1. Look for headings or sections explicitly named after a component (e.g., "# Banner", "# Button").
    2. Identify definitions describing a reusable UI element.
    3. Extract the primary name of the component.
    4. Capture a concise description of the component's purpose or function, often found near the heading.
    5. Note the source document/page where the component is defined.
    6. Pay attention to mentions of related components, which can imply relationships.
    """

    component_name: str = Field(
        ...,
        description="The primary name of the component (e.g., 'Banner', 'Box', 'Flex').",
    )
    description: str = Field(
        ...,
        description="A brief summary of what the component does or is used for. Use information directly stated in the documentation.",
    )
    source_file: Optional[str] = Field(
        None,
        description="The name of the source markdown file where this component is primarily documented (e.g., 'banner.md').",
    )
    # Note: Props are defined as a separate entity and linked via relationships in the graph.
    # Note: Usage examples are captured in CodeExample entities and linked.


class Prop(BaseModel):
    """Represents a property (prop) that configures a Component.

    Props are attributes passed to components to modify their behavior or appearance.

    Instructions for identifying and extracting Props:
    1. Look for tables or lists explicitly labeled "Props" or describing component attributes.
    2. Identify attributes mentioned within code examples being passed to a component (e.g., `<Banner intent="success">`).
    3. Extract the prop name (e.g., 'intent', 'onDismiss', 'flex', 'bg').
    4. Capture the description of what the prop does.
    5. Note the data type(s) the prop accepts (e.g., 'string', 'boolean', '() => void', specific enum values like '"information" | "success"').
    6. Extract the default value if specified.
    7. Identify the Component to which this prop belongs. An edge should link this Prop to its Component.
    """

    propName: str = Field(
        ..., description="The name of the prop (e.g., 'intent', 'flex', 'color')."
    )
    component_name: str = Field(
        ...,
        description="The name of the Component this prop belongs to (e.g., 'Banner', 'Box').",
    )
    description: str = Field(
        ..., description="Explanation of what the prop controls or modifies."
    )
    type: str = Field(
        ...,
        description="The data type or allowed values for the prop (e.g., 'string', 'boolean', '\"information\" | \"success\" | ...').",
    )
    default_value: Optional[str] = Field(
        None, description="The default value of the prop, if specified."
    )
    source_file: Optional[str] = Field(
        None,
        description="The name of the source markdown file where this prop definition is found.",
    )


class StylingConcept(BaseModel):
    """Represents a concept related to styling, theming, or layout within the design system.

    These are principles or features related to appearance, distinct from specific components,
    though they might be applied via components or props (e.g., Colors, Flexbox, CSS Layers, Design Tokens).

    Instructions for identifying and extracting Styling Concepts:
    1. Look for documentation pages or sections under headings like "Styling".
    2. Identify topics explaining how to control visual aspects like color, space, layout, or theming.
    3. Extract the name of the concept (e.g., 'Colors', 'Flex', 'CSS Layers', 'Dark Mode').
    4. Capture the core explanation or definition of the concept.
    5. Note specific CSS variables, classes, or utility props associated with the concept if central to its definition.
    6. Identify the source document detailing this concept.
    """

    propName: str = Field(
        ...,
        description="The name of the styling concept (e.g., 'Colors', 'Flex', 'CSS Layers').",
    )
    description: str = Field(
        ...,
        description="A summary explaining the styling concept and its purpose or usage.",
    )
    category: str = Field(
        "Styling",
        description="The high-level category this concept belongs to, typically 'Styling'.",
    )
    source_file: Optional[str] = Field(
        None,
        description="The name of the source markdown file where this concept is primarily described (e.g., 'colors.md', 'flex.md').",
    )


class Guide(BaseModel):
    """Represents a walkthrough, tutorial, or instructional document.

    Guides typically provide step-by-step instructions for setup, configuration, or troubleshooting tasks.

    Instructions for identifying and extracting Guides:
    1. Look for documentation pages or sections under headings like "Guides".
    2. Identify documents that provide sequential steps or explanations for achieving a specific goal (e.g., Installation, Setup, Troubleshooting).
    3. Extract the main title or topic of the guide (e.g., 'Installation', 'CSS Imports', 'CSS Layers').
    4. Capture a brief description summarizing the guide's objective.
    5. Note the key steps or procedures mentioned within the guide if easily summarized (detailed steps might be better as relationships or properties).
    6. Identify the source document for the guide.
    """

    title: str = Field(
        ...,
        description="The primary title of the guide (e.g., 'Getting Started', 'Installation', 'CSS Layers').",
    )
    description: str = Field(
        ...,
        description="A brief summary of the guide's purpose or the task it helps accomplish.",
    )
    category: str = Field(
        "Guides",
        description="The high-level category this documentation belongs to, typically 'Guides'.",
    )
    source_file: Optional[str] = Field(
        None,
        description="The name of the source markdown file containing the guide (e.g., 'guides.md', 'css-layers.md').",
    )


class CodeExample(BaseModel):
    """Represents a specific code snippet provided in the documentation.

    Code examples illustrate how to use components, apply styling concepts, or implement procedures described in guides.

    Instructions for identifying and extracting Code Examples:
    1. Look for fenced code blocks (```) within the documentation.
    2. Extract the code content itself.
    3. Identify the programming language (e.g., 'tsx', 'css', 'bash', 'javascript'). If not specified, infer from syntax or context.
    4. Determine what the code example demonstrates (e.g., "Basic usage of Banner", "Setting up CSS Layers for Tailwind 3.0", "Installing the package using npm"). This forms the description.
    5. Identify the main Component, Styling Concept, or Guide that this code example relates to. An edge should link this CodeExample to the relevant entity/entities.
    6. Note the source document and approximate location (e.g., section heading) if possible.
    """

    description: str = Field(
        ...,
        description="A description of what the code example demonstrates or is used for (e.g., 'Basic usage of Button component', 'How to import CSS', 'Applying flex prop').",
    )
    code: str = Field(..., description="The actual code snippet.")
    language: Optional[str] = Field(
        None,
        description="The programming or markup language of the code snippet (e.g., 'tsx', 'css', 'bash', 'markdown').",
    )
    context_description: str = Field(
        ...,
        description="Briefly describe the context: Which component, guide, or concept does this example illustrate?",
    )
    source_file: Optional[str] = Field(
        None,
        description="The name of the source markdown file where this code example appears.",
    )


class CSSToken(BaseModel):
    """Represents a specific design token, often exposed as a CSS variable or utility class.

    Tokens are named entities representing specific design decisions (e.g., a color value, a spacing unit).

    Instructions for identifying and extracting CSS Tokens:
    1. Look for tables or lists defining named values, especially under styling sections like 'Colors', 'Spacing', 'Typography'.
    2. Identify items with a specific name (e.g., `fg.accent`, `bg.success.subtle`, `--ax-colors-fg-accent`) and a corresponding value (e.g., `#0037FF`, `light-dark(#0037FF, #6A8FFC)`).
    3. Extract the token name.
    4. Extract the token value(s). Include light/dark mode variations if specified.
    5. Categorize the token based on its usage (e.g., 'Text Color', 'Background Color', 'Border Color', 'Spacing').
    6. Note the source document where the token is defined.
    7. These often relate to a StylingConcept (e.g., 'Colors'). An edge should be created.
    """

    tokenName: str = Field(
        ...,
        description="The name of the CSS token (e.g., 'fg.accent', 'bg.success.subtle', '--ax-colors-bg-default').",
    )
    value: str = Field(
        ...,
        description="The CSS value(s) associated with the token, including light/dark mode variations if present (e.g., 'light-dark(#0037FF, #6A8FFC)', '16px').",
    )
    category: str = Field(
        ...,
        description="The functional category of the token (e.g., 'Text Color', 'Background Color', 'Border Color', 'Spacing', 'Font Size').",
    )
    source_file: Optional[str] = Field(
        None,
        description="The name of the source markdown file where this token definition is found (e.g., 'colors.md').",
    )


# Dictionary mapping entity names to their corresponding Pydantic models
# This is used by the graph memory library to know which entities to extract.
REACT_ENTITY_TYPES: Dict[str, Any] = {
    "ComponentJSX": ComponentJSX,
    "Prop": Prop,
    "StylingConcept": StylingConcept,
    "Guide": Guide,
    "CodeExample": CodeExample,
    "CSSToken": CSSToken,
}

print("Entity definitions created successfully.")
# You can optionally print the schema for verification
# import json
# for name, model in ENTITY_TYPES.items():
#     print(f"\nSchema for {name}:")
#     print(json.dumps(model.model_json_schema(), indent=2))
