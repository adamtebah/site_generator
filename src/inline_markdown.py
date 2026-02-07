import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    """Extract markdown images ![alt](url) from text. Returns list of (alt_text, url) tuples."""
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """Extract markdown links [anchor](url) from text (not images). Returns list of (anchor_text, url) tuples."""
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    """Split TEXT nodes by markdown images ![alt](url). Non-TEXT nodes are passed through."""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining = node.text
        for alt, url in images:
            delimiter = f"![{alt}]({url})"
            sections = remaining.split(delimiter, 1)
            before = sections[0]
            after = sections[1] if len(sections) > 1 else ""
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = after
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    """Split TEXT nodes by markdown links [anchor](url). Non-TEXT nodes are passed through."""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining = node.text
        for anchor, url in links:
            delimiter = f"[{anchor}]({url})"
            sections = remaining.split(delimiter, 1)
            before = sections[0]
            after = sections[1] if len(sections) > 1 else ""
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining = after
        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown: no matching closing delimiter '{delimiter}'")
        split_result = []
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                split_result.append(TextNode(part, TextType.TEXT))
            else:
                split_result.append(TextNode(part, text_type))
        new_nodes.extend(split_result)
    return new_nodes


def text_to_textnodes(text):
    """Convert raw markdown text into a list of TextNodes (TEXT, BOLD, ITALIC, CODE, IMAGE, LINK)."""
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
