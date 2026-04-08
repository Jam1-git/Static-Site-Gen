import re

from textnode import TextNode, TextType

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        section = old_node.text
        images = extract_markdown_images(section)
        if images == []:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = section.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            section = sections[1]
        if section != "":
            new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        section = old_node.text
        links = extract_markdown_links(section)
        if links == []:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = section.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            section = sections[1]
        if section != "":
            new_nodes.append(TextNode(section, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes