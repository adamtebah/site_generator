import re

from block_type import BlockType, block_to_block_type
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from markdown_blocks import markdown_to_blocks
from textnode import text_node_to_html_node


def text_to_children(text):
    """Convert inline markdown text to a list of HTML nodes (LeafNodes)."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def block_to_html_node(block):
    """Convert a single markdown block to an HTML node (ParentNode or LeafNode)."""
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        text = block.replace("\n", " ")
        children = text_to_children(text)
        return ParentNode("p", children)

    if block_type == BlockType.HEADING:
        match = re.match(r"^(#{1,6}) ", block)
        level = len(match.group(1))
        content = block[match.end() :]
        children = text_to_children(content)
        return ParentNode(f"h{level}", children)

    if block_type == BlockType.CODE:
        # Content between ```\n and ```; no inline parsing
        content = block[4:-3]
        code_node = LeafNode("code", content)
        return ParentNode("pre", [code_node])

    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        content = " ".join(line.lstrip(">").lstrip() for line in lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)

    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            item_content = line[2:]  # strip "- "
            item_children = text_to_children(item_content)
            items.append(ParentNode("li", item_children))
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        items = []
        for i, line in enumerate(lines):
            # strip "N. " (number + ". ")
            prefix_len = len(str(i + 1)) + 2
            item_content = line[prefix_len:]
            item_children = text_to_children(item_content)
            items.append(ParentNode("li", item_children))
        return ParentNode("ol", items)

    # fallback paragraph
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    """Convert a full markdown document to a single parent HTMLNode (div) containing block nodes."""
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
