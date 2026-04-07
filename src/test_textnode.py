import unittest

from textnode import TextType, TextNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a test node", TextType.ITALIC, None)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a test node", TextType.TEXT)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is also a test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

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
        
        

if __name__ == "__main__()":
    unittest.main()