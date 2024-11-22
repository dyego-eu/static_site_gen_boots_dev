import pytest

from md_to_html.textnode import TextNode, TextNodeType
from md_to_html.htmlnode import LeafNode


def test_node_equality():
    node_1 = TextNode(
        content="abc 123", node_type=TextNodeType.BOLD, url="www.google.com"
    )
    node_2 = TextNode(
        content="abc 123", node_type=TextNodeType.BOLD, url="www.google.com"
    )
    assert node_1 == node_2


def test_node_inequality_types():
    node_1 = TextNode(
        content="abc 123", node_type=TextNodeType.BOLD, url="www.google.com"
    )
    node_2 = TextNode(
        content="abc 123", node_type=TextNodeType.NORMAL, url="www.google.com"
    )
    assert node_1 != node_2


def test_node_inequality_content():
    node_1 = TextNode(
        content="ABC 123", node_type=TextNodeType.NORMAL, url="www.google.com"
    )
    node_2 = TextNode(
        content="abc 123", node_type=TextNodeType.NORMAL, url="www.google.com"
    )
    assert node_1 != node_2


def test_node_inequality_url():
    node_1 = TextNode(
        content="abc 123", node_type=TextNodeType.NORMAL, url="www.gmail.com"
    )
    node_2 = TextNode(
        content="abc 123", node_type=TextNodeType.NORMAL, url="www.google.com"
    )
    assert node_1 != node_2


def test_node_equality_url_null():
    node_1 = TextNode(content="abc 123", node_type=TextNodeType.NORMAL, url=None)
    node_2 = TextNode(content="abc 123", node_type=TextNodeType.NORMAL)
    assert node_1 == node_2


@pytest.mark.parametrize(
    "node_type,html_node",
    [
        (
            TextNodeType.NORMAL,
            LeafNode(value="this is some text"),
        ),
        (
            TextNodeType.BOLD,
            LeafNode(tag="b", value="this is some text"),
        ),
        (
            TextNodeType.LINK,
            LeafNode(
                tag="a", value="this is some text", props={"href": "www.hyperlink.com"}
            ),
        ),
        (
            TextNodeType.ITALIC,
            LeafNode(tag="i", value="this is some text"),
        ),
        (
            TextNodeType.IMG,
            LeafNode(
                tag="img",
                value="",
                props={"src": "www.hyperlink.com", "alt": "this is some text"},
            ),
        ),
        (
            TextNodeType.CODE,
            LeafNode(tag="code", value="this is some text"),
        ),
    ],
)
def test_textnode_to_htmlnode(node_type, html_node):
    text_node = TextNode(
        content="this is some text", node_type=node_type, url="www.hyperlink.com"
    )
    assert text_node.to_html_node() == html_node
