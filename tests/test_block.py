import pytest

from md_to_html.textblock import Block, BlockList


def test_simple_block_conversion():
    example_text = "this is a block\n\nthis is other block"
    expected = BlockList(
        Block("this is a block"),
        Block("this is other block"),
    )

    computed = BlockList.from_text(example_text)

    assert computed == expected


def test_multiple_block_conversion():
    example_text = (
        "this is one block"
        "\n\nother block"
        "\n\n\n\n\nhighly separated block"
        "\n\nfinal block"
    )

    expected = BlockList(
        Block("this is one block"),
        Block("other block"),
        Block("highly separated block"),
        Block("final block"),
    )

    computed = BlockList.from_text(example_text)
    print(computed.blocks)
    print(expected.blocks)

    assert computed == expected


def test_blocklist_comparison_fail():
    block = Block("some text")
    blocklist = BlockList(block)
    with pytest.raises(ValueError):
        blocklist == block


def test_extract_title():
    markdown = "# This is title"

    title = BlockList.get_title(markdown)
    assert title == "This is title"


def test_extract_title_more_complex_markdown():
    markdown = (
        "#            Title: This is a Serious Markdown"
        "\n\n## Subtitle: yeah! I mean it"
        "\n\nThis is some text explaining why this markdown is so serious"
    )
    title = BlockList.get_title(markdown)
    assert title == "Title: This is a Serious Markdown"


def test_extract_title_error():
    markdown = (
        "This markdown doesnt start with title"
        "\n# It comes later"
        "\n but is too little, too late"
    )
    with pytest.raises(ValueError):
        BlockList.get_title(markdown)
