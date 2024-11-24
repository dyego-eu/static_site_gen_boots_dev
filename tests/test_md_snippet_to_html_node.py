import pytest

from md_to_html import Block
from md_to_html import HTMLNode
from md_to_html.textblock import BlockList


@pytest.mark.parametrize(
    "snippet,expected_html_node",
    [
        ("code", "code"),
        ("language_code", "language_code"),
        ("heading", "heading"),
        ("deep_heading", "deep_heading"),
        ("quote", "quote"),
        ("ul", "ul"),
        ("ol", "ol"),
        ("paragraph", "paragraph"),
    ],
    indirect=["snippet", "expected_html_node"],
)
def test_code_block_to_html_node(snippet: str, expected_html_node: HTMLNode):
    print(snippet)
    block = Block(snippet)
    result = block.to_html_node()
    assert result == expected_html_node


def test_full_markdown_conversion(
    full_markdown: str, full_markdown_html_node: HTMLNode
):
    calculated = BlockList.from_text(full_markdown).to_html_node()
    assert calculated == full_markdown_html_node
