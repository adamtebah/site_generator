import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    """Return the BlockType for a single block of markdown. Assumes block is already stripped."""
    lines = block.split("\n")

    if not block:
        return BlockType.PARAGRAPH

    # Code: starts with ```\n and ends with ```
    if block.startswith("```\n") and block.endswith("```") and len(block) > 7:
        return BlockType.CODE

    # Heading: 1-6 # then space
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Quote: every line starts with >
    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with "N. " for N = 1, 2, 3, ...
    if lines and all(
        len(line) >= 3 and line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
