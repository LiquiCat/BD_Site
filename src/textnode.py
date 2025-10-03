from __future__ import annotations
from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "plain text"
    BOLD_TEXT = "bold text"
    ITALIC_TEXT = "italic text"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text:str, text_type:TextType, url:str):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value:TextNode):
        return \
            self.text == value.text and \
            self.text_type == value.text_type and \
            self.url == value.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"