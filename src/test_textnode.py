import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_default_url(self):
        node = TextNode("plain text", TextType.TEXT)
        node2 = TextNode("plain text", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq_differnt_text_type(self):
        node = TextNode("plain text", TextType.TEXT)
        node2 = TextNode("plain text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_differnt_url(self):
        node = TextNode("link", TextType.LINK, "https://www.github.com")
        node2 = TextNode("link", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_differnt_text(self):
        node = TextNode("text", TextType.TEXT)
        node2 = TextNode("text2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_link_with_url(self):
        node = TextNode("link", TextType.LINK, "https://www.github.com")
        node2 = TextNode("link", TextType.LINK, "https://www.github.com")
        self.assertEqual(node, node2)

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code snippet")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("alt description", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/img.png", "alt": "alt description"})

    def test_link_without_url_raises(self):
        node = TextNode("anchor", TextType.LINK, url=None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_without_url_raises(self):
        node = TextNode("alt", TextType.IMAGE, url=None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_unknown_text_type_raises(self):
        node = TextNode("x", TextType.TEXT)
        node.text_type = "unknown"  # not a valid TextType enum value
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()