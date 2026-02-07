import unittest

from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_example(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_strips_whitespace(self):
        markdown = "  \n\n  block one  \n\n  block two  "
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, ["block one", "block two"])

    def test_markdown_to_blocks_removes_empty_blocks(self):
        markdown = "first\n\n\n\nsecond"
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(blocks, ["first", "second"])

    def test_markdown_to_blocks_single_block(self):
        blocks = markdown_to_blocks("Just one block")
        self.assertListEqual(blocks, ["Just one block"])

    def test_markdown_to_blocks_empty_document(self):
        self.assertListEqual(markdown_to_blocks(""), [])
        self.assertListEqual(markdown_to_blocks("   \n\n   \n\n   "), [])


if __name__ == "__main__":
    unittest.main()
