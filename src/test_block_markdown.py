import unittest

from block_markdown import (BlockType, 
                            markdown_to_blocks, 
                            block_to_block_type,
                            markdown_to_html_node,
                            extract_title)

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_space_filled(self):
        md = "Block one\n\n   \n\nBlock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two"
            ]
        )

    def test_markdown_excessive_newlines(self):
        md = "Block one\n\n\n\n\nBlock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block one",
                "Block two"
            ]
        )

class TestMarkdownBlockTypes(unittest.TestCase):

    def test_heading(self):

        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "###Heading"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):

        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "```code```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):

        block = ">'Quote 1'\n> Quote 2\n>'Quote 3'"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = ">'Quote 1'\n Quote 2\n>'Quote 3'"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

        block = ">'Quote 1'> Quote 2\n>'Quote 3'"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        
        block = "- item\n- other item\n- another item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "-item\n- other item\n- another item"
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):

        block = "1. first item\n2. second item\n3. third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "2. second item\n3. third item"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1.first item\n2. second item"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1. first item\n3. third item"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

class TestMarkdownToHTMLNode(unittest.TestCase):

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
        self.assertEqual(
            html,
         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_blockquote(self):
        md = """
> This is
>a
> quote block
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is\na\nquote block</blockquote></div>"
        )

    def test_heading(self):
        md = "# Heading!"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading!</h1></div>"
        )

        md = "### **Bold subheading!**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3><b>Bold subheading!</b></h3></div>"
        )

        md = "###### **Bold subheading** with _italics_!"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6><b>Bold subheading</b> with <i>italics</i>!</h6></div>" 
        )

    def test_unordered(self):
        md = """
- unsorted
- list
- of
- items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>unsorted</li><li>list</li><li>of</li><li>items</li></ul></div>"
        )

    def test_ordered(self):
        md = """
1. Sorted
2. List
"""
        node = markdown_to_html_node(md)
        html = node.to_html()  
        self.assertEqual(
            html,
            "<div><ol><li>Sorted</li>\n<li>List</li></ol></div>"
        )

    def test_extract_h1(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")

        md = "# Hello\n\nThis is my markdown file"
        title = extract_title(md)
        self.assertEqual(title, "Hello")

        md = "oops, no h1 header\n\n## but there is h2"
        with self.assertRaises(Exception):
            extract_title(md)
            
if __name__ == "__main__()":
    unittest.main()