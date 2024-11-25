from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Literal

from .htmlnode import HTMLNode, ParentNode
from .textnode import TextNode, TextNodeType


@dataclass
class Block:
    content: str

    def to_html_node(self) -> HTMLNode:
        if self.is_code():
            return self._code_to_html_node()
        elif self.is_heading():
            return self._heading_to_html_node()
        elif self.is_ordered_list():
            return self._ordered_list_to_html_node()
        elif self.is_unordered_list():
            return self._unordered_list_to_html_node()
        elif self.is_quote():
            return self._quote_to_html_node()

        return self._paragraph_to_html_node()

    def _paragraph_to_html_node(self) -> HTMLNode:
        return ParentNode(
            tag="p",
            children=TextNode(self.content).parse_all().to_html_nodes(),
        )

    def _heading_to_html_node(self) -> HTMLNode:
        match = re.match(r"^(#{1,6}) (.*)", self.content)

        if match is None:
            raise ValueError("heading type wrongly detected")  # pragma: no cover

        h_level, content = len(match[1]), match[2]
        return ParentNode(
            tag=f"h{h_level}",
            children=TextNode(content).parse_all().to_html_nodes(),
        )

    def _code_to_html_node(self) -> HTMLNode:
        language_match = re.match(r"^```(\w+)\s*", self.lines[0])
        language = "plain" if language_match is None else language_match[1]
        return ParentNode(
            tag="pre",
            children=[
                ParentNode(
                    tag="code",
                    children=[TextNode("\n".join(self.lines[1:-1])).to_html_node()],
                    props=({"class": f"language-{language}"}),
                )
            ],
        )

    def _quote_to_html_node(self) -> HTMLNode:
        return ParentNode(
            tag="blockquote",
            children=TextNode(self.content).remove_marker().parse_all().to_html_nodes(),
        )

    def _unordered_list_to_html_node(self) -> HTMLNode:
        return self._list_to_html_node("ul")

    def _ordered_list_to_html_node(self) -> HTMLNode:
        return self._list_to_html_node("ol")

    def _list_to_html_node(self, tag: Literal["ol", "ul"]) -> HTMLNode:
        children = []
        for line in self.lines:
            line = self.remove_marker(line).rstrip()
            child = (
                TextNode(content=re.sub(r"^\[[ x]?\]", "", line))
                .parse_all()
                .to_html_nodes()
            )
            if re.match(r"^\[ ?\]", line):
                child = [
                    TextNode(
                        content="", node_type=TextNodeType.UNMARKED_CHECKBOX
                    ).to_html_node()
                ] + child
            elif re.match(r"^\[x\]", line):
                child = [
                    TextNode(
                        content="", node_type=TextNodeType.MARKED_CHECKBOX
                    ).to_html_node()
                ] + child

            children.append(child)

        return ParentNode(
            tag=tag,
            children=[ParentNode(tag="li", children=child) for child in children],
        )

    @staticmethod
    def remove_marker(line: str) -> str:
        return line.strip().split(" ", 1)[1]

    @property
    def lines(self) -> list[str]:
        return self.content.split("\n")

    def is_code(self) -> bool:
        has_start = self.lines[0].startswith("```")
        has_end = self.lines[-1].startswith("```")
        has_enough_lines = len(self.lines) >= 2

        return has_start and has_end and has_enough_lines

    def is_ordered_list(self) -> bool:
        return all(
            line.startswith(f"{line_no}. ")
            for line_no, line in enumerate(self.lines, 1)
        )

    def is_unordered_list(self) -> bool:
        return all(line.startswith("* ") for line in self.lines) or all(
            line.startswith("- ") for line in self.lines
        )

    def is_heading(self) -> bool:
        has_heading_mark = re.match(r"^#{1,6} ", self.content) is not None
        has_single_line = len(self.lines) == 1
        return has_heading_mark and has_single_line

    def is_quote(self) -> bool:
        return all(line.startswith("> ") for line in self.lines)


class BlockList:
    def __init__(self, *blocks: Block):
        self.blocks = list(blocks)

    @classmethod
    def from_text(cls, text: str) -> BlockList:
        preprocessed_text = re.sub(r"\n{2,}", "\n\n", text).strip()
        return cls(
            *[Block(block_text) for block_text in preprocessed_text.split("\n\n")]
        )

    @staticmethod
    def get_title(text: str) -> str:
        first_line, _ = (text + "\n").split("\n", 1)
        if not first_line.startswith("# "):
            raise ValueError("First line of markdown file should contain title")

        return re.split(r"# ", first_line)[1].strip()

    def to_html_node(self) -> HTMLNode:
        return ParentNode(
            tag="div", children=[block.to_html_node() for block in self.blocks]
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BlockList):
            raise ValueError("BlockList can only be compared to BlockList")

        is_equalsize = len(self.blocks) == len(other.blocks)
        is_matched = all(
            my_block == your_block
            for my_block, your_block in zip(self.blocks, other.blocks)
        )

        return is_equalsize and is_matched
