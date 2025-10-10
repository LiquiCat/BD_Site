from __future__ import annotations
from enum import Enum
from typing import List

from leaf_node import LeafNode

class TextType(Enum):
    PLAIN = ""
    BOLD = "b"
    ITALIC = "i"
    LINK = "a"
    IMAGE = "img"
    CODE = "code"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: TextNode):
        return \
            self.text == value.text and \
            self.text_type == value.text_type and \
            self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node: TextNode):
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
        case _:
            raise ValueError("Unsupported type")
        

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):

    resulting = []
    is_text = True

    for node in old_nodes:

        if node.text_type != TextType.PLAIN:
            resulting.append(node)
            continue
        
        delim_count = node.text.count(delimiter)
        delim_count = delim_count if delim_count%2==0 else delim_count-1

        node_split = node.text.split(delimiter, delim_count)

        for part in node_split:
            if part:
                if (not is_text):
                    resulting.append(TextNode(part, text_type))
                else:
                    resulting.append(TextNode(part, TextType.PLAIN))
            is_text = False if is_text else True

    return resulting
                