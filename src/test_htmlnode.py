import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to(self):
        test_props = {
    "href": "https://www.google.com",
    "target": "_blank",
    }
        node = HTMLNode(props = test_props)
        test_string = node.props_to_html()
        format = ' href="https://www.google.com" target="_blank"' 
        self.assertEqual(test_string, format)

    def test_props_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_init_values(self):
        children = [HTMLNode("b", "bold")]
        props = {"class": "intro"}
        node = HTMLNode("p", "hello", children, props)

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_to_html_raises(self):
        node = HTMLNode("p", "hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, child_node)
        with self.assertRaises(ValueError):
            parent_node.to_html()

        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph")
        formatted = node.__repr__()
        self.assertEqual(formatted, 'HTMLNode(p, This is a paragraph, None, None)')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold!")
        self.assertEqual(node.to_html(), "<b>This is bold!</b>")

    def test_leaf_to_html_a(self):
        node  = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!" )

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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

if __name__ == "__main__()":
    unittest.main()





