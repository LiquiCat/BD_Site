from __future__ import annotations
from enum import Enum
from typing import List
import re

from textnode import text_to_textnodes, text_node_to_html_node
from leaf_node import LeafNode
from parent_node import ParentNode

class BlockType(Enum):
    PARAGRAPH = "Paragraph"
    HEADING = "Heading"
    CODE = "Code"
    QUOTE = "Quote"
    UNORDERED_LIST = "Unordered list"
    ORDERED_LIST = "Ordered list"

def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    blocks = map(str.strip, blocks)
    blocks = filter(lambda x: x, blocks)
    blocks = list(blocks)

    return blocks

def block_to_block_type(markdown: str) -> BlockType:
    if re.findall(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    if markdown.strip()[0: 3] == "```" and markdown.strip()[-3:] == "```":
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

def verify_lines_start_with(beg: str, lines: List[str]) -> bool:
    reg = re.compile(beg)
    return all(map(lambda x: reg.search(x), lines))

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    parent = ParentNode("div", [])

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                block_parag = block.replace("\n", " ")
                block_parag = re.sub(" +", " ", block_parag)
                node = ParentNode("p", text_to_children(block_parag))

            case BlockType.HEADING:
                hash_count = 0

                while block[hash_count] == "#":
                    hash_count += 1

                block_no_header = block[hash_count+1:]
                node = ParentNode(f"h{hash_count}", text_to_children(block_no_header))

            case BlockType.CODE:
                block_no_code_tag = re.sub(r"^\s?```\s?", "", block)
                block_no_code_tag = re.sub(r"```$", "", block_no_code_tag)
                child_node = LeafNode("code", block_no_code_tag)
                node = ParentNode(f"pre", [child_node])

            case BlockType.QUOTE:
                block_quote = block.replace("\n>",">")[2:]
                node = ParentNode(f"blockquote", text_to_children(block_quote))

            case BlockType.UNORDERED_LIST:
                list_items = block.split("\n")
                node = ParentNode(f"ul", [])

                for line in list_items:
                    child = LeafNode("li", text_to_children(line[:2]))
                    node.add_child(child)

            case BlockType.ORDERED_LIST:
                list_items = block.split("\n")
                node = ParentNode(f"ol", [])

                for line in list_items:
                    i = 0
                    while line[i].isdigit():
                        i += 1

                    child = LeafNode("li", text_to_children(line[:i+2]))
                    node.add_child(child)

        parent.add_child(node)
    return parent

def text_to_children(line: str) -> List[LeafNode]:
    nodes = text_to_textnodes(line)
    res = []

    for node in nodes:
        res.append(text_node_to_html_node(node))
    return res

def extract_title(markdown: str):
    line = markdown.split("\n")[0]
    if line[0:2] == "# ":
        title = line[2:]
        return title
    raise ValueError("Markdown file should contain a title as a first line")
    
