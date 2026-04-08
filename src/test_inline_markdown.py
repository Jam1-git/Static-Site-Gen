import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import TextNode, TextType

class TestInlineDelimeter(unittest.TestCase):
    def test_delims(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                         ])
        
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word", TextType.TEXT),
                         ])
        
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word", TextType.TEXT),
                         ])
    
    def test_no_delim(self):
        node = TextNode("This text has no delimeters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_delim_start_or_end_or_empty(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
                         [
                          TextNode("Bold", TextType.BOLD),
                          TextNode(" at the start", TextType.TEXT)
                         ])
        
        node = TextNode("Italics at the _end_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
                         [
                          TextNode("Italics at the ", TextType.TEXT),
                          TextNode("end", TextType.ITALIC)
                         ])
        
        node = TextNode("Empty code `` segment", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
                         [
                          TextNode("Empty code ", TextType.TEXT),
                          TextNode(" segment", TextType.TEXT)
                         ])
        
    def test_mixed_nodes(self):
        nodes = [TextNode("This is a simple text node!", TextType.TEXT),
                 TextNode("This one is all code!", TextType.CODE),
                 TextNode("This one **contains** bold", TextType.TEXT),
                 TextNode("This one _contains_ italics", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes,"`", TextType.CODE)   
        self.assertEqual(new_nodes,
                         [
                           TextNode("This is a simple text node!", TextType.TEXT),
                           TextNode("This one is all code!", TextType.CODE),
                           TextNode("This one ", TextType.TEXT),
                           TextNode("contains", TextType.BOLD),
                           TextNode(" bold", TextType.TEXT),
                           TextNode("This one ", TextType.TEXT),
                           TextNode("contains", TextType.ITALIC),
                           TextNode(" italics", TextType.TEXT)
                         ])

class TestRegex(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_many(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
                            
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
        
    def test_extract_markdown_links_many(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

class TestSplitNodesImageAndLinks(unittest.TestCase):

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

        node = TextNode(
            "This text doesn't contain links or images",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

        node = TextNode(
            "![just](urls)![really just](image.urls)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("just", TextType.IMAGE, "urls"),
                TextNode("really just", TextType.IMAGE, "image.urls")
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node = TextNode(
            "This text doesn't contain links or images",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

        node = TextNode(
            "[just](links)[really just](link.urls)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("just", TextType.LINK, "links"),
                TextNode("really just", TextType.LINK, "link.urls")
            ],
            new_nodes
        )

class TestTextToNode(unittest.TestCase):

    def test_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_some(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) This contains some of the _text types_, **Yippee**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" This contains some of the ", TextType.TEXT),
                TextNode("text types", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("Yippee", TextType.BOLD)
            ],
            nodes
        )
        
if __name__ == "__main__()":
    unittest.main()