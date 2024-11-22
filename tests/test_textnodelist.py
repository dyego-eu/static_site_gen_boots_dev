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
    )
    assert node.parse_bold().parse_italic().parse_code() == expected


def test_complex_parse_multinode():
    nodelist = TextNodeList(
        TextNode(
            "This is **some very bold claims** that you seem to be making. ",
            TextNodeType.NORMAL,
        ),
        TextNode(
            "*It is almost as you are italian*. Let me `Throw some Code at you.`",
            TextNodeType.NORMAL,
        ),
        TextNode(" Psheew, psheew, **BOLD PSHEEW**", TextNodeType.NORMAL),
    )

    expected = TextNodeList(
        TextNode("This is ", TextNodeType.NORMAL),
        TextNode("some very bold claims", TextNodeType.BOLD),
        TextNode(" that you seem to be making. ", TextNodeType.NORMAL),
        TextNode("It is almost as you are italian", TextNodeType.ITALIC),
        TextNode(". Let me ", TextNodeType.NORMAL),
        TextNode("Throw some Code at you.", TextNodeType.CODE),
        TextNode(" Psheew, psheew, ", TextNodeType.NORMAL),
        TextNode("BOLD PSHEEW", TextNodeType.BOLD),
    )
    assert nodelist.parse_bold().parse_italic().parse_code() == expected


def test_simple_image_parse():
    node = TextNode(
        "this is a simple markdown ![alt_text for image](www.image.com) with text after image",
        TextNodeType.NORMAL,
    )
    expected = TextNodeList(
        TextNode("this is a simple markdown ", TextNodeType.NORMAL),
        TextNode("alt_text for image", TextNodeType.IMG, url="www.image.com"),
        TextNode(" with text after image", TextNodeType.NORMAL),
    )
    assert node.parse_image() == expected


def test_simple_link_parse():
    node = TextNode(
        "this is a simple markdown [this is a hyperlink](www.image.com) with text after image",
        TextNodeType.NORMAL,
    )
    expected = TextNodeList(
        TextNode("this is a simple markdown ", TextNodeType.NORMAL),
        TextNode("this is a hyperlink", TextNodeType.LINK, url="www.image.com"),
        TextNode(" with text after image", TextNodeType.NORMAL),
    )
    assert node.parse_link() == expected


def test_img_doesnt_parse_link():
    node = TextNode(
        "this is a simple markdown [this is a hyperlink](www.image.com) with text after image",
        TextNodeType.NORMAL,
    )
    assert node.parse_image() == TextNodeList(node)


def test_link_doesnt_parse_img():
    node = TextNode(
        "this is a simple markdown ![alt_text](www.image.com) with text after image",
        TextNodeType.NORMAL,
    )
    assert node.parse_link() == TextNodeList(node)


def test_full_complex_parse():
    example_text = (
        "This is an **example** of a markdown file that *contains italics*"
        " **bold in multiple places**, contains some `code_variables` and"
        " even some ![images](www.url.com) and [hyperlinks](www.url2.com)."
        " In fact, there are [multiple](www.link_to_multiple.com) links and"
        " multiple ![cat image](www.cat_image.com). Even some more `code`"
    )
    expected = TextNodeList(
        TextNode("This is an ", TextNodeType.NORMAL),
        TextNode("example", TextNodeType.BOLD),
        TextNode(" of a markdown file that ", TextNodeType.NORMAL),
        TextNode("contains italics", TextNodeType.ITALIC),
        TextNode(" ", TextNodeType.NORMAL),
        TextNode("bold in multiple places", TextNodeType.BOLD),
        TextNode(", contains some ", TextNodeType.NORMAL),
        TextNode("code_variables", TextNodeType.CODE),
        TextNode(" and even some ", TextNodeType.NORMAL),
        TextNode("images", url="www.url.com", node_type=TextNodeType.IMG),
        TextNode(" and ", TextNodeType.NORMAL),
        TextNode("hyperlinks", url="www.url2.com", node_type=TextNodeType.LINK),
        TextNode(". In fact, there are ", TextNodeType.NORMAL),
        TextNode(
            "multiple", url="www.link_to_multiple.com", node_type=TextNodeType.LINK
        ),
        TextNode(" links and multiple ", TextNodeType.NORMAL),
        TextNode("cat image", url="www.cat_image.com", node_type=TextNodeType.IMG),
        TextNode(". Even some more ", TextNodeType.NORMAL),
        TextNode("code", TextNodeType.CODE),
    )

    assert TextNode(example_text, TextNodeType.NORMAL).parse_all() == expected


def test_create_from_text():
    example_text = (
        "This is an **example** of a markdown file that *contains italics*"
        " **bold in multiple places**, contains some `code_variables` and"
        " even some ![images](www.url.com) and [hyperlinks](www.url2.com)."
        " In fact, there are [multiple](www.link_to_multiple.com) links and"
        " multiple ![cat image](www.cat_image.com). Even some more `code`"
    )
    expected = TextNodeList(
        TextNode("This is an ", TextNodeType.NORMAL),
        TextNode("example", TextNodeType.BOLD),
        TextNode(" of a markdown file that ", TextNodeType.NORMAL),
        TextNode("contains italics", TextNodeType.ITALIC),
        TextNode(" ", TextNodeType.NORMAL),
        TextNode("bold in multiple places", TextNodeType.BOLD),
        TextNode(", contains some ", TextNodeType.NORMAL),
        TextNode("code_variables", TextNodeType.CODE),
        TextNode(" and even some ", TextNodeType.NORMAL),
        TextNode("images", url="www.url.com", node_type=TextNodeType.IMG),
        TextNode(" and ", TextNodeType.NORMAL),
        TextNode("hyperlinks", url="www.url2.com", node_type=TextNodeType.LINK),
        TextNode(". In fact, there are ", TextNodeType.NORMAL),
        TextNode(
            "multiple", url="www.link_to_multiple.com", node_type=TextNodeType.LINK
        ),
        TextNode(" links and multiple ", TextNodeType.NORMAL),
        TextNode("cat image", url="www.cat_image.com", node_type=TextNodeType.IMG),
        TextNode(". Even some more ", TextNodeType.NORMAL),
        TextNode("code", TextNodeType.CODE),
    )
    assert TextNodeList.from_text(example_text) == expected
