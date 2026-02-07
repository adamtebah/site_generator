import unittest

from block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_one_to_six(self):
        for i in range(1, 7):
            block = "#" * i + " Heading text"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_heading_requires_space_after_hashes(self):
        self.assertEqual(block_to_block_type("##no space"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\ncode line 1\ncode line 2\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_with_one_line(self):
        block = "```\nsingle line\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_no_newline_after_opening_is_paragraph(self):
        block = "```code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_does_not_end_with_backticks_is_paragraph(self):
        block = "```\ncode only"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_with_space_after_gt(self):
        block = "> quote with space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_mixed_without_gt_is_paragraph(self):
        block = "> first line\nsecond without gt"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_requires_space_after_dash(self):
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    def test_unordered_list_mixed_is_paragraph(self):
        block = "- item one\nnot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one(self):
        block = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment(self):
        block = "1. first\n3. skip two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_requires_dot_and_space(self):
        self.assertEqual(block_to_block_type("1 not list"), BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. only item"), BlockType.ORDERED_LIST)

    def test_paragraph_plain_text(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)

    def test_paragraph_empty(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_paragraph_looks_like_list_but_wrong_format(self):
        self.assertEqual(block_to_block_type("1. item\n2 wrong"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
