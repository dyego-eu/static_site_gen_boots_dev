import pytest

from md_to_html import TextNode, TextNodeType, TextNodeList


def test_textnodelist_equality():
    nodelist_1 = TextNodeList(
        TextNode("normal text", TextNodeType.NORMAL),
        TextNode("bold text", TextNodeType.BOLD),
    )
    nodelist_2 = TextNodeList(
        TextNode("normal text", TextNodeType.NORMAL),
        TextNode("bold text", TextNodeType.BOLD),
    )
    assert nodelist_1 == nodelist_2


def test_textnodelist_inequality_error():
    node = TextNode("normal text", TextNodeType.NORMAL)
    nodelist = TextNodeList(node)

    with pytest.raises(ValueError):
        nodelist == node

def test_complex_parse_delimiter():
    example = (
        "This is **some very bold claims** that you seem to be making. *It is"
        " almost as you are italian*. Let me `Throw some Code at you.`"
        " Psheew, psheew, **BOLD PSHEEW**"
    )
    node = TextNode(example, TextNodeType.NORMAL)
    expected = TextNodeList(
        TextNode("This is ", TextNodeType.NORMAL),
        TextNode("some very bold claims", TextNodeType.BOLD),
        TextNode(" that you seem to be making. ", TextNodeType.NORMAL),
        TextNode("It is almost as you are italian", TextNodeType.ITALIC),
        TextNode(". Let me ", TextNodeType.NORMAL),
        TextNode("Throw some Code at you.", TextNodeType.CODE),
        TextNode(" Psheew, psheew, ", TextNodeType.NORMAL),
        TextNode("BOLD PSHEEW", TextNodeType.BOLD),
        TextNode("", TextNodeType.NORMAL),
    )
    assert (
        node.parse_delimiter("**", TextNodeType.BOLD)
        .parse_delimiter("*", TextNodeType.ITALIC)
        .parse_delimiter("`", TextNodeType.CODE)
    ) == expected
