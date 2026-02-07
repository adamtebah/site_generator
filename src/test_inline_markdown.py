import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_images_empty_text(self):
        self.assertListEqual(extract_markdown_images(""), [])

    def test_extract_images_no_images(self):
        self.assertListEqual(
            extract_markdown_images("Just plain text and [a link](https://example.com)"),
            [],
        )

    def test_extract_images_alt_with_spaces(self):
        matches = extract_markdown_images("See ![my cool image](https://example.com/img.png)")
        self.assertListEqual([("my cool image", "https://example.com/img.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_links_excludes_images(self):
        text = "An ![image](https://example.com/img.png) and a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_links_empty_text(self):
        self.assertListEqual(extract_markdown_links(""), [])

    def test_extract_links_no_links(self):
        self.assertListEqual(
            extract_markdown_links("Just plain text and ![image](https://example.com)"),
            [],
        )

    def test_extract_links_anchor_with_spaces(self):
        matches = extract_markdown_links("Check [this page out](https://example.com)")
        self.assertListEqual([("this page out", "https://example.com")], matches)

    def test_extract_links_single_link(self):
        matches = extract_markdown_links("Go to [home](https://example.com) for more.")
        self.assertListEqual([("home", "https://example.com")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single_image(self):
        node = TextNode(
            "Before ![pic](https://example.com/p.png) after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://example.com/p.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_images_returns_original(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_empty_list(self):
        self.assertListEqual(split_nodes_image([]), [])

    def test_split_images_non_text_node_passed_through(self):
        bold_node = TextNode("bold", TextType.BOLD)
        text_node = TextNode("Text with ![x](https://x.com)", TextType.TEXT)
        new_nodes = split_nodes_image([bold_node, text_node])
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("x", TextType.IMAGE, "https://x.com"),
            ],
            new_nodes,
        )

    def test_split_images_image_at_start(self):
        node = TextNode("![first](https://a.com) and rest", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://a.com"),
                TextNode(" and rest", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_image_at_end(self):
        node = TextNode("start and ![last](https://b.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start and ", TextType.TEXT),
                TextNode("last", TextType.IMAGE, "https://b.com"),
            ],
            new_nodes,
        )

    def test_split_images_only_image_no_extra_text(self):
        node = TextNode("![solo](https://solo.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo", TextType.IMAGE, "https://solo.com")],
            new_nodes,
        )

    def test_split_images_multiple_text_nodes(self):
        nodes = [
            TextNode("No image here", TextType.TEXT),
            TextNode("Here is ![one](https://one.com) ok", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("No image here", TextType.TEXT),
                TextNode("Here is ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://one.com"),
                TextNode(" ok", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single_link(self):
        node = TextNode(
            "Go to [home](https://example.com) for more.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("home", TextType.LINK, "https://example.com"),
                TextNode(" for more.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_no_links_returns_original(self):
        node = TextNode("Just plain text and ![img](https://x.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_empty_list(self):
        self.assertListEqual(split_nodes_link([]), [])

    def test_split_links_non_text_node_passed_through(self):
        code_node = TextNode("code", TextType.CODE)
        text_node = TextNode("See [link](https://l.com) here", TextType.TEXT)
        new_nodes = split_nodes_link([code_node, text_node])
        self.assertListEqual(
            [
                TextNode("code", TextType.CODE),
                TextNode("See ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://l.com"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_start(self):
        node = TextNode("[first](https://a.com) and rest", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://a.com"),
                TextNode(" and rest", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_end(self):
        node = TextNode("start and [last](https://b.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start and ", TextType.TEXT),
                TextNode("last", TextType.LINK, "https://b.com"),
            ],
            new_nodes,
        )

    def test_split_links_only_link_no_extra_text(self):
        node = TextNode("[solo](https://solo.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("solo", TextType.LINK, "https://solo.com")],
            new_nodes,
        )

    def test_split_links_excludes_images(self):
        node = TextNode(
            "![img](https://img.com) and [link](https://link.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![img](https://img.com) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_text_nodes(self):
        nodes = [
            TextNode("No link here", TextType.TEXT),
            TextNode("Here is [one](https://one.com) ok", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("No link here", TextType.TEXT),
                TextNode("Here is ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://one.com"),
                TextNode(" ok", TextType.TEXT),
            ],
            new_nodes,
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode("Plain and **bold part** and plain", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Plain and ", TextType.TEXT),
                TextNode("bold part", TextType.BOLD),
                TextNode(" and plain", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("Start _italic_ end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_multiple_code_blocks(self):
        node = TextNode("A `one` B `two` C", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("one", TextType.CODE),
                TextNode(" B ", TextType.TEXT),
                TextNode("two", TextType.CODE),
                TextNode(" C", TextType.TEXT),
            ],
        )

    def test_non_text_node_passed_through(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        node = TextNode("text with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([bold_node, node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_only_non_text_nodes(self):
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, nodes)

    def test_no_delimiter_in_text(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("Just plain text", TextType.TEXT)])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("Text with `unclosed code", TextType.TEXT)
        with self.assertRaises(ValueError) as ctx:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("no matching closing delimiter", str(ctx.exception))
        self.assertIn("`", str(ctx.exception))

    def test_unclosed_bold_raises(self):
        node = TextNode("Start **bold no end", TextType.TEXT)
        with self.assertRaises(ValueError) as ctx:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("**", str(ctx.exception))

    def test_delimiter_at_edges(self):
        node = TextNode("`only code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("only code", TextType.CODE)],
        )

    def test_empty_list(self):
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_multiple_text_nodes_split(self):
        nodes = [
            TextNode("`a`", TextType.TEXT),
            TextNode("x **b** y", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("`a`", TextType.TEXT),
                TextNode("x ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" y", TextType.TEXT),
            ],
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_plain_text(self):
        nodes = text_to_textnodes("Just plain text")
        self.assertListEqual(nodes, [TextNode("Just plain text", TextType.TEXT)])

    def test_text_to_textnodes_bold_only(self):
        nodes = text_to_textnodes("Hello **world**")
        self.assertListEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
            ],
        )

    def test_text_to_textnodes_image_and_link(self):
        text = "See ![pic](https://img.com) and [here](https://link.com)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("See ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://img.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://link.com"),
            ],
        )

    def test_text_to_textnodes_code_and_italic(self):
        text = "Use `code` and _italic_ together"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("Use ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" together", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual(nodes, [])


if __name__ == "__main__":
    unittest.main()
