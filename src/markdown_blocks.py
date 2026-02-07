def markdown_to_blocks(markdown):
    """Split a markdown document into blocks by double newlines. Strips each block and removes empty blocks."""
    blocks = markdown.split("\n\n")
    return [b.strip() for b in blocks if b.strip()]
