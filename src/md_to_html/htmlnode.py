from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence


@dataclass
class HTMLNode:
    tag: str | None = None
    value: str | None = None
    children: Sequence[HTMLNode] | None = None
    props: dict[str, str] | None = None

    def to_html(self) -> str:
        raise NotImplementedError()  # pragma: no cover

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        return " " + " ".join(
            [f'{prop}="{value}"' for prop, value in self.props.items()]
        )


class LeafNode(HTMLNode):
    def __init__(
        self, value: str, tag: str | None = None, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.tag:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Sequence[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:

        if self.children is None:
            raise Exception()  # pragma: no cover

        return (
            f"<{self.tag}{self.props_to_html()}>"
            + "".join(child.to_html() for child in self.children)
            + f"</{self.tag}>"
        )
