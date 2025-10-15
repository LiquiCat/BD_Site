from __future__ import annotations
from enum import Enum
from typing import List, Tuple
import copy
import re

from leaf_node import LeafNode

class TextType(Enum):
    PLAIN = "plain text"
    BOLD = "Bold text"
    ITALIC = "Italic"
    LINK = "Link"
    IMAGE = "Image"
    CODE = "Code"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: TextNode) -> bool:
        return \
            self.text == value.text and \
            self.text_type == value.text_type and \
            self.url == value.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt":text_node.text})
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case _:
            raise ValueError("Unsupported type")
        
def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:

    resulting = []

    for node in old_nodes:
        is_text = True

        if node.text_type != TextType.PLAIN:
            resulting.append(node)
            continue
        
        delim_count = node.text.count(delimiter)
        delim_count = delim_count if delim_count%2==0 else delim_count-1

        node_split = node.text.split(delimiter, delim_count)

        for part in node_split:
            if part:
                if not is_text:
                        resulting.append(TextNode(part, text_type))
                else:
                    resulting.append(TextNode(part, TextType.PLAIN))
            is_text = False if is_text else True

    return resulting
                
def extract_markdown_images(text: str) -> Tuple[str, str]:
    reg = r"!\[([A-Za-z0-9 _]*)\]\((https?:\/\/[A-Za-z0-9 _./@]+)\)"
    imgs = re.findall(reg, text)
    return imgs

def extract_markdown_links(text: str) -> Tuple[str, str]:
    reg = r"(?<!!)\[([A-Za-z0-9 _]+)\]\((https?:\/\/[A-Za-z0-9 _./@]+)\)"
    links = re.findall(reg, text)
    return links

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    res = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        extracted = [copy.deepcopy(node)]

        if not images:
            res.append(node)
            continue
        
        for img in images:
            img_name = f"![{img[0]}]({img[1]})"
            around_img = extracted[-1].text.split(img_name, 1)

            if around_img[0]:
                extracted.insert(-1, TextNode(around_img[0], TextType.PLAIN))
            extracted.insert(-1, TextNode(img[0], TextType.IMAGE, img[1]))
            extracted[-1].text = around_img[-1]

        if not extracted[-1].text:
            extracted.pop()

        res.extend(extracted)
    return res
        
def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    res = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        extracted = [copy.deepcopy(node)]

        if not links:
            res.append(node)
            continue
        
        for lnk in links:
            lnk_name = f"[{lnk[0]}]({lnk[1]})"
            around_lnk = extracted[-1].text.split(lnk_name, 1)

            if around_lnk[0]:
                extracted.insert(-1, TextNode(around_lnk[0], TextType.PLAIN))
            extracted.insert(-1, TextNode(lnk[0], TextType.LINK, lnk[1]))
            extracted[-1].text = around_lnk[-1]

        if not extracted[-1].text:
            extracted.pop()
        res.extend(extracted)
    return res

def text_to_textnodes(text:str) -> List[TextNode]:

    node = [TextNode(text, TextType.PLAIN)]
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "_", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)

    return node

