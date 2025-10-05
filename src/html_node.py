from __future__ import annotations
from typing import List, Dict

class HTMLNode():
    def __init__(self, tag:str = None, value:str = None, children:List[HTMLNode] = None, props:Dict[str,str] = None):
        self.tag: str = tag
        self.value: str = value
        self.children: List[HTMLNode] = children
        self.props: Dict[str,str] = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):

        if not self.props:
            return None

        html_str = ""
        for key, val in self.props.values:
            html_str += f' {key}="{val}"'
        return html_str
    
    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"
    
