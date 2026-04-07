from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
             return LeafNode("b", text_node.text)
        elif text_node.text_type == TextType.ITALIC:
             return LeafNode("i", text_node.text)
        elif text_node.text_type == TextType.CODE:
             return LeafNode("code", text_node.text)
        elif text_node.text_type == TextType.LINK:
             return LeafNode("a", text_node.text, {"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
             return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        else:
             raise Exception(f"Invalid text type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splits = node.text.split(delimiter)
        temp_nodes = []
        i = 1
        if len(splits) % 2 == 0:
             raise Exception("invalid markdown syntax")
        for split in splits:
            if split != "":
                if i % 2 == 1:
                    temp_nodes.append(TextNode(split, TextType.TEXT))
                else:
                    temp_nodes.append(TextNode(split, text_type))   
            i += 1
        new_nodes.extend(temp_nodes)
    return new_nodes

def extract_markdown_images(text):
     matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)   
     return matches

def extract_markdown_links(text):
     matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)   
     return matches
     
