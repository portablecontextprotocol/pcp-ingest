import os


async def process_markdown_file(file_path: str) -> str:
    """Read and process a markdown file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


async def get_markdown_files(base_dir: str) -> list[tuple[str, dict]]:
    """
    Recursively get all markdown files from the base directory and their metadata.
    Returns a list of tuples containing (file_path, metadata).
    """
    markdown_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                # Get the relative path components to determine section
                rel_path = os.path.relpath(file_path, base_dir)
                path_parts = rel_path.split(os.sep)

                # Determine section from the first directory level
                section = path_parts[0].replace("docs_", "")

                metadata = {
                    "file_path": file_path,
                    "file_type": "markdown",
                    "section": section,
                    "document_type": path_parts[-1].replace(".md", ""),
                }
                markdown_files.append((file_path, metadata))
    return markdown_files
