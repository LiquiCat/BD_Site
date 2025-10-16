import unittest

from block import BlockType, block_to_block_type, \
    markdown_to_html_node, extract_title

class TestBlock(unittest.TestCase):

    def test_b2b_paragraph(self):
        md = """This is a regular
paragraph
Nothing strange"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_heading_single(self):
        md = """# This is just a header"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.HEADING)

    def test_b2b_heading_six(self):
        md = """###### This is just a header"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.HEADING)

    def test_b2b_code(self):
        md = """```
def main():
    print("Hello world")
```"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.CODE)

    def test_b2b_code_with_new_line(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        b_type = block_to_block_type(md)

        self.assertEqual(b_type, BlockType.CODE)
                        
    def test_b2b_quote(self):
        md = """> This is a quote from a Einstein
> This is a quote from a Einstein
> This is a quote from a Einstein
> This is a quote from a Einstein"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.QUOTE)

    def test_b2b_unordered(self):
        md = """- milk
- sugar
- eggs
- meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.UNORDERED_LIST)

    def test_b2b_ordered(self):
        md = """1. milk
2. sugar
3. eggs
4. meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.ORDERED_LIST)

    def test_b2b_ordered_error_missing_space(self):
        md = """1. milk
2.sugar
3. eggs
4. meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_ordered_error_index_skip(self):
        md = """1. milk
2. sugar
3. eggs
5. meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_unordered_error_missing_space(self):
        md = """- milk
- sugar
-eggs
- meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_quote_error_missing_space(self):
        md = """> milk
> sugar
>eggs
> meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_quote_error_missing_line(self):
        md = """> milk
> sugar
eggs
> meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_code_error_missing_closing(self):
        md = """```milk
> sugar
eggs
> meth"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_heading_error_seven(self):
        md = """####### milk"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_b2b_heading_error_space_missing(self):
        md = """###milk"""
        b_type = block_to_block_type(md)
        self.assertEqual(b_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        print(f"{html=}")
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_title(self):
        md = """# title here"""
        title = extract_title(md)
        self.assertEqual(title, "title here")
    
    def test_title_more_rows(self):
        md = """# title here
but not here
and not here"""
        title = extract_title(md)
        self.assertEqual(title, "title here")

    def test_title_multiple_rows(self):
        md = """# title here
# but not here
# and not here"""
        title = extract_title(md)
        self.assertEqual(title, "title here")

    def test_title_error(self):
        md = """## title here
# but not here
# and not here"""
        with self.assertRaises(ValueError):
            extract_title(md)