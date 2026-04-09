from enum import Enum
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote" 
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
            
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for i in range(len(blocks)):
        if blocks[i].strip() != "":
            new_blocks.append(blocks[i].strip())
    return new_blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        if block_to_block_type(block) != BlockType.CODE:
            node = block_to_node(block)
        else:
            node = TextNode(block.lstrip("\n```").rstrip("```"), TextType.CODE)
            node = text_node_to_html_node(node)
            node = ParentNode("pre", [node])
        block_nodes.append(node)
    html_node = ParentNode("div", block_nodes)
    return html_node

def header_type_check(header_block):
    if header_block.startswith("# "):
        return "h1", "# "
    elif header_block.startswith("## "):
        return "h2", "## "
    elif header_block.startswith("### "):
        return "h3", "### "
    elif header_block.startswith("#### "):
        return "h4", "#### "
    elif header_block.startswith("##### "):
        return "h5", "##### "
    elif header_block.startswith("###### "):
        return "h6", "###### "
    else:
        raise Exception("Error, argument is not a header")
    
def block_to_node(block):
    type = block_to_block_type(block)
    if type == BlockType.PARAGRAPH:
        children = text_to_children(block.replace("\n"," "))
        node = ParentNode("p", children)
    elif type == BlockType.HEADING:
        children = text_to_children(block.replace(f"{header_type_check(block)[1]}", ""))
        node = ParentNode(header_type_check(block)[0], children)
    elif type == BlockType.QUOTE:
        children = text_to_children(block.replace("> ", "").replace(">", ""))
        node = ParentNode("blockquote", children)
    elif type == BlockType.UNORDERED_LIST:
        children = text_to_children(block.replace("- ", "<li>").replace("\n", "</li>") + "</li>")
        node = ParentNode("ul", children)
    elif type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        i = 1
        stripped_lines = []
        for line in lines:
            if line != "":
                line = line.replace(f"{i}. ", "<li>")
                i += 1
                stripped_lines.append(line + "</li>")
        block = "\n".join(stripped_lines)
        children = text_to_children(block)
        node = ParentNode("ol", children)
    return node

def text_to_children(text):
    nodes = text_to_textnodes(text)
    htmlnodes = []
    for node in nodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("# ").strip()
        else:
            continue
    raise Exception("markdown does not contain h1 header")



