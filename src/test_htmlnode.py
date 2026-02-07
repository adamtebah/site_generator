import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode



class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        """props None or empty dict returns empty string."""
        node_none = HtmlNode("a", value="link", props=None)
        self.assertEqual(node_none.props_to_html(), "")

        node_empty = HtmlNode("a", value="link", props={})
        self.assertEqual(node_empty.props_to_html(), "")

    def test_props_to_html_single(self):
        """Single attribute has leading space and key=\"value\" format."""
        node = HtmlNode("a", value="link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple(self):
        """Multiple attributes are space-separated with leading space."""
        node = HtmlNode(
            "a",
            value="link",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_to_html_not_implemented(self):
        """to_html raises NotImplementedError (for subclasses to override)."""
        node = HtmlNode("p", value="hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Raw text only")
        self.assertEqual(node.to_html(), "Raw text only")

    def test_leaf_no_value_raises(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_leaf_repr_no_children(self):
        node = LeafNode("span", "hi", {"class": "greeting"})
        self.assertIn("LeafNode", repr(node))
        self.assertNotIn("children", repr(node))

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        children = [
            LeafNode("p", "First"),
            LeafNode("p", "Second"),
            LeafNode("p", "Third"),
        ]
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>First</p><p>Second</p><p>Third</p></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_nested_parents(self):
        inner = ParentNode("span", [LeafNode("b", "bold")])
        middle = ParentNode("p", [inner, LeafNode(None, " and text")])
        outer = ParentNode("div", [middle])
        self.assertEqual(
            outer.to_html(),
            "<div><p><span><b>bold</b></span> and text</p></div>",
        )

    def test_parent_no_tag_raises(self):
        with self.assertRaises(ValueError) as ctx:
            ParentNode(None, [LeafNode("span", "x")]).to_html()
        self.assertIn("tag", str(ctx.exception).lower())

    def test_parent_no_children_raises(self):
        with self.assertRaises(ValueError) as ctx:
            ParentNode("div", None).to_html()
        self.assertIn("children", str(ctx.exception).lower())

    def test_parent_with_props(self):
        parent_node = ParentNode("div", [LeafNode("span", "child")], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

if __name__ == "__main__":
    unittest.main()