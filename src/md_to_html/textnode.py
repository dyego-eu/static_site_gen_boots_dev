from __future__ import annotations

import re
from typing import Any, Callable, ClassVar, Pattern
from enum import Enum, auto
from typing import Optional

from dataclasses import dataclass

from .htmlnode import LeafNode


class TextNodeType(Enum):
    NORMAL = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMG = auto()


@dataclass
class TextNode:
    content: str
    node_type: TextNodeType
    url: Optional[str] = None

    img_regex: ClassVar[Pattern[str]] = re.compile(r"\!\[(.*?)\]\((.*?)\)")
    link_regex: ClassVar[Pattern[str]] = re.compile(r"(?<!\!)\[(.*?)\]\((.*?)\)")

    def to_html_node(self):
        match self.node_type:
            case TextNodeType.NORMAL:
                return LeafNode(value=self.content)

            case TextNodeType.BOLD:
                return LeafNode(tag="b", value=self.content)

            case TextNodeType.ITALIC:
                return LeafNode(tag="i", value=self.content)

            case TextNodeType.CODE:
                return LeafNode(tag="code", value=self.content)

            case TextNodeType.LINK:
                if self.url is None:
                    raise ValueError("TextNode with Link type MUST have url")
                return LeafNode(tag="a", value=self.content, props={"href": self.url})

            case TextNodeType.IMG:
                if self.url is None:
                    raise ValueError("TextNode with Image type MUST have url")
                return LeafNode(
                    tag="img", value="", props={"src": self.url, "alt": self.content}
                )

            case _:
                raise ValueError()  # pragma: no cover

    def parse_all(self) -> TextNodeList:
        return TextNodeList(self).parse_all()

    def parse_bold(self) -> TextNodeList:
        return self._parse_delimiter("**", TextNodeType.BOLD)

    def parse_italic(self) -> TextNodeList:
        return self._parse_delimiter("*", TextNodeType.ITALIC)

    def parse_code(self) -> TextNodeList:
        return self._parse_delimiter("`", TextNodeType.CODE)

    def parse_image(self) -> TextNodeList:
        return self._parse_regex(self.img_regex, TextNodeType.IMG)

    def parse_link(self) -> TextNodeList:
        return self._parse_regex(self.link_regex, TextNodeType.LINK)

    def _parse_delimiter(self, delimiter: str, node_type: TextNodeType) -> TextNodeList:
        if self.content == "":
            return TextNodeList()

        re_delim = delimiter.replace("*", r"\*")
        if re.search(rf"{re_delim}.*?{re_delim}", self.content) is None:
            return TextNodeList(self)

        start, delimited, rest = self.content.split(delimiter, 2)
        return TextNodeList(
            TextNode(content=start, node_type=self.node_type),
            TextNode(content=delimited, node_type=node_type),
            *(
                TextNode(content=rest, node_type=self.node_type)
                ._parse_delimiter(delimiter, node_type)
                .nodes
            ),
        )

    def _parse_regex(
        self, regex: Pattern[str], node_type: TextNodeType
    ) -> TextNodeList:
        regex_match = regex.search(self.content)
        if not regex_match:
            return TextNodeList(self)

        re_span = regex_match.span()
        return TextNodeList(
            TextNode(self.content[: re_span[0]], self.node_type),
            TextNode(regex_match[1], node_type, url=regex_match[2]),
            *(
                TextNode(self.content[re_span[1] :], self.node_type)
                ._parse_regex(regex, node_type)
                .nodes
            ),
        )


class TextNodeList:
    def __init__(
        self,
        *text_nodes: TextNode,
    ):
        self.nodes = list(text_nodes)

    @classmethod
    def from_text(cls, text:str):
        return TextNode(text, TextNodeType.NORMAL).parse_all()

    def parse_all(self) -> TextNodeList:
        return self.parse_image().parse_link().parse_bold().parse_italic().parse_code()

    def parse_bold(self) -> TextNodeList:
        return self._parse_nodes(TextNode.parse_bold)

    def parse_italic(self) -> TextNodeList:
        return self._parse_nodes(TextNode.parse_italic)

    def parse_code(self) -> TextNodeList:
        return self._parse_nodes(TextNode.parse_code)

    def parse_image(self) -> TextNodeList:
        return self._parse_nodes(TextNode.parse_image)

    def parse_link(self) -> TextNodeList:
        return self._parse_nodes(TextNode.parse_link)

    def _parse_nodes(
        self, parse_method: Callable[[TextNode], TextNodeList]
    ) -> TextNodeList:
        return TextNodeList(*sum([parse_method(node).nodes for node in self.nodes], []))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TextNodeList):
            raise ValueError("Can only compare TextNodeList with TextNodeList")

        is_equalsize = len(self.nodes) == len(other.nodes)
        is_matching = all(
            my_node == your_node for my_node, your_node in zip(self.nodes, other.nodes)
        )

        return is_equalsize and is_matching
