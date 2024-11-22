from enum import Enum, auto
from typing import Optional

from dataclasses import dataclass

from htmlnode import LeafNode

class TextNodeType(Enum):
    NORMAL = auto()
    BOLD = auto()
    ITALIC  = auto()
    CODE = auto()
    LINK = auto()
    IMG = auto()
    
@dataclass
class TextNode:
    content: str
    node_type: TextNodeType
    url: Optional[str] = None

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
                return LeafNode(tag="img", value="", props={"src": self.url, "alt":self.content})

            case _:
                raise ValueError()  # pragma: no cover

