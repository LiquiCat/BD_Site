from __future__ import annotations
from enum import Enum
from typing import List
import re

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered list"
    ORDERED_LIST = "Ordered list"


def block_to_block_type(markdown: str) -> BlockType:
    if re.findall(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    if markdown[0: 3] == "```" and markdown[-3] == "```":
        return BlockType.CODE
    
    all_lines =  markdown.split("\n")

    if verify_lines_start_with(r"^> ", all_lines):
        return BlockType.QUOTE
    if verify_lines_start_with(r"^- ", all_lines):
        return BlockType.UNORDERED_LIST
    
    index = 1
    for line in all_lines:
        if not line.startswith(f"{index}. "): 
            break
        index += 1
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def verify_lines_start_with(beg, lines):
    reg = re.compile(beg)
    return all(map(lambda x: reg.search(x), lines))