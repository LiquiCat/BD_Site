import unittest

from block import BlockType, block_to_block_type

class TestTextNode(unittest.TestCase):

    def test_b2b_paragraph(self):
        md = """This is a regular
paragraph
Nothing strange"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_heading_single(self):
        md = """# This is just a header"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.HEADING)

    def test_b2b_heading_six(self):
        md = """###### This is just a header"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.HEADING)

    def test_b2b_code(self):
        md = """```
def main():
    print("Hello world")
```"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.CODE)
                        
    def test_b2b_quote(self):
        md = """> This is a quote from a Einstein
> This is a quote from a Einstein
> This is a quote from a Einstein
> This is a quote from a Einstein"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.QUOTE)

    def test_b2b_unordered(self):
        md = """- milk
- sugar
- eggs
- meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.UNORDERED_LIST)

    def test_b2b_ordered(self):
        md = """1. milk
2. sugar
3. eggs
4. meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.ORDERED_LIST)

    def test_b2b_ordered_error_missing_space(self):
        md = """1. milk
2.sugar
3. eggs
4. meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_ordered_error_index_skip(self):
        md = """1. milk
2. sugar
3. eggs
5. meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_unordered_error_missing_space(self):
        md = """- milk
- sugar
-eggs
- meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_quote_error_missing_space(self):
        md = """> milk
> sugar
>eggs
> meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_quote_error_missing_line(self):
        md = """> milk
> sugar
eggs
> meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_code_error_missing_closing(self):
        md = """```milk
> sugar
eggs
> meth"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_heading_error_seven(self):
        md = """####### milk"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

    def test_b2b_heading_error_space_missing(self):
        md = """###milk"""
        b_type = block_to_block_type(md)
        self.assertTrue(b_type, BlockType.PARAGRAPH)

