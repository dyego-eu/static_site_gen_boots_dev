from pathlib import Path

import pytest

from md_to_html import ParentNode
from md_to_html.htmlnode import LeafNode

FIX = Path(__file__).parent / "fixtures"


@pytest.fixture
def snippet(request) -> str:
    with open(FIX / "code_snippet.md") as f:
        code_md = f.read().strip()
    with open(FIX / "code_w_language_snippet.md") as f:
        language_code_md = f.read().strip()
    with open(FIX / "heading_snippet.md") as f:
        heading_md = f.read().strip()
    with open(FIX / "deep_heading_snippet.md") as f:
        deep_heading_md = f.read().strip()
    with open(FIX / "quote_snippet.md") as f:
        quote_md = f.read().strip()
    with open(FIX / "unordered_list_snippet.md") as f:
        ul_md = f.read().strip()
    with open(FIX / "ordered_list_snippet.md") as f:
        ol_md = f.read().strip()
    with open(FIX / "regular_paragraph.md") as f:
        paragraph_md = f.read().strip()
    OPTIONS = {
        "code": code_md,
        "heading": heading_md,
        "deep_heading": deep_heading_md,
        "language_code": language_code_md,
        "quote": quote_md,
        "ul": ul_md,
        "ol": ol_md,
        "paragraph": paragraph_md,
    }

    return OPTIONS[request.param]


@pytest.fixture
def expected_html_node(request) -> ParentNode:
    code_html_node = ParentNode(
        tag="pre",
        children=[
            ParentNode(
                tag="code",
                props={"class": "language-plain"},
                children=[
                    LeafNode(
                        value=(
                            "code_snippet\nignores **bold**\n\n> and quotes\n> with"
                            " multilines"
                        )
                    )
                ],
            ),
        ],
    )
    language_code_html_node = ParentNode(
        tag="pre",
        children=[
            ParentNode(
                tag="code",
                props={"class": "language-python"},
                children=[
                    LeafNode(
                        value=(
                            "import pandas as pd\n\n"
                            'pd.set_option("display.max_rows", None)'
                        )
                    )
                ],
            ),
        ],
    )
    paragraph_md = ParentNode(
        tag="p",
        children=[
            LeafNode("this is just a regular paragraph in md\nI will add some "),
            LeafNode("italics", tag="i"),
            LeafNode(" and\nsome "),
            LeafNode("inline code", tag="code"),
            LeafNode(" just to be cool"),
        ],
    )
    quote_html_node = ParentNode(
        tag="blockquote",
        children=[
            LeafNode(value="this is a quote\nthat has multiple lines"),
        ],
    )
    heading_html_node = ParentNode(
        tag="h1", children=[LeafNode(value="Basic ass title")]
    )
    deep_heading_html_node = ParentNode(
        tag="h3", children=[LeafNode(value="deep heading")]
    )
    ul_html_node = ParentNode(
        tag="ul",
        children=[
            ParentNode(tag="li", children=[LeafNode("item 1")]),
            ParentNode(tag="li", children=[LeafNode("item 2")]),
            ParentNode(tag="li", children=[LeafNode("item 3")]),
        ],
    )
    ol_html_node = ParentNode(
        tag="ol",
        children=[
            ParentNode(tag="li", children=[LeafNode("first item")]),
            ParentNode(tag="li", children=[LeafNode("second item")]),
            ParentNode(tag="li", children=[LeafNode("third item")]),
        ],
    )

    OPTIONS = {
        "code": code_html_node,
        "language_code": language_code_html_node,
        "heading": heading_html_node,
        "deep_heading": deep_heading_html_node,
        "quote": quote_html_node,
        "ul": ul_html_node,
        "ol": ol_html_node,
        "paragraph": paragraph_md,
    }

    return OPTIONS[request.param]


@pytest.fixture
def full_markdown() -> str:
    with open(FIX / "example_markdown.md") as f:
        return f.read()


@pytest.fixture
def full_markdown_html_node():
    return ParentNode(
        tag="div",
        children=[
            ParentNode(tag="h1", children=[LeafNode(value="Main Header")]),
            ParentNode(
                tag="p",
                children=[
                    LeafNode(value="This is a normal paragraph. It will contain "),
                    LeafNode(tag="b", value="some bold text"),
                    LeafNode(value="\nand maybe some "),
                    LeafNode(tag="code", value="inline code"),
                    LeafNode(value=" tags."),
                ],
            ),
            ParentNode(
                tag="ul",
                children=[
                    ParentNode(tag="li", children=[LeafNode(value="list item 1")]),
                    ParentNode(tag="li", children=[LeafNode(value="list item 2")]),
                    ParentNode(tag="li", children=[LeafNode(value="list item 3")]),
                ],
            ),
            ParentNode(
                tag="ol",
                children=[
                    ParentNode(tag="li", children=[LeafNode(value="ordered item 1")]),
                    ParentNode(tag="li", children=[LeafNode(value="ordered item 2")]),
                ],
            ),
            ParentNode(
                tag="p",
                children=[
                    LeafNode(
                        value="Now, this paragraph will have a more complex markdown. It will contain:\n"
                    ),
                    LeafNode(
                        tag="img",
                        value="",
                        props={"src": "images", "alt": "describe this image"},
                    ),
                    LeafNode(value="\nand maybe some "),
                    LeafNode(tag="b", value="bold"),
                    LeafNode(value=" text, some "),
                    LeafNode(tag="code", value="code_snippets"),
                    LeafNode(value=" and some "),
                    LeafNode(tag="i", value="italics"),
                    LeafNode(value=" even.\nI might even add a "),
                    LeafNode(
                        tag="a", value="hyperlink", props={"href": "www.google.com"}
                    ),
                    LeafNode(value=" here and there, just to throw\nsome spice"),
                ],
            ),
            ParentNode(tag="h2", children=[LeafNode(value="Subheader")]),
            ParentNode(
                tag="p", children=[LeafNode(value="Testing writing under subheader")]
            ),
        ],
    )
