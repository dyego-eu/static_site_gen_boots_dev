from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: list[HTMLNode] | None = None
    props: dict[str, str] | None = None

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        return " " + " ".join([f'{prop}="{value}"' for prop, value in self.props.items()])


class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            value: str,
            props: dict[str, str] | None=None
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
