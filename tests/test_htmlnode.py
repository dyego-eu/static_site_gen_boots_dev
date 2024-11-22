import pytest

from md_to_html.htmlnode import HTMLNode, LeafNode, ParentNode


def test_html_nodes_equal():
    node_1 = HTMLNode(
        tag="a",
        value="biroliro",
        children=None,
        props={"href": "www.google.com"}
    )
    node_2 = HTMLNode(
    tag="a",
    value="biroliro",
    children=None,
    props={"href": "www.google.com"}
)
    assert node_1 == node_2


@pytest.mark.parametrize(
    "parameter",
    ["tag", "value", "children", "props"],
)
def test_create_node_without_parameter(parameter):
    node_params = {
        "tag": "p",
        "value": "This is a paragraph",
        "children": [
            HTMLNode(tag="a", value="link", props={"href":"www.example.com"}),
        ],
        "props": {"style":"color: blue;", "class":"cool-paragraph"},
    }

    node_params.pop(parameter)

    HTMLNode(**node_params)


def test_props_to_html():
    props = {"style":"color: blue;", "class":"cool-div"}

    node = HTMLNode(tag="div", props=props)
    
    assert node.props_to_html() == ' style="color: blue;" class="cool-div"'


def test_leafnode_is_htmlnode():
    leafnode = LeafNode(value="I'm a Leaf!", tag="p")
    assert isinstance(leafnode, HTMLNode)


def test_render_leafnode_wo_props():
    leafnode = LeafNode(value="I'm a Leaf!", tag="p")
    assert leafnode.to_html() == "<p>I'm a Leaf!</p>"


def test_render_leafnode_w_props():
    leafnode = LeafNode(value="I'm a Leaf!", tag="p", props={"class":"cool-p", "style":"color:green;"})
    assert leafnode.to_html() == '<p class="cool-p" style="color:green;">I\'m a Leaf!</p>'


def test_render_leafnode_wo_tag():
    leafnode = LeafNode("I'm a Leaf!")
    assert leafnode.to_html() == "I'm a Leaf!"


def test_create_parent_node():
    node_1 = LeafNode(tag="b", value="This is bold")
    node_2 = LeafNode(value = "This is just normal text")
    parent_node = ParentNode(tag="div", children=[node_1, node_2])

    assert isinstance(parent_node, HTMLNode)


def test_render_simple_parent_node():

    node_1 = LeafNode(tag="b", value="This is bold")
    node_2 = LeafNode(value = "This is just normal text")
    parent_node = ParentNode(tag="div", children=[node_1, node_2])

    expected_html = "<div><b>This is bold</b>This is just normal text</div>"
    assert parent_node.to_html() == expected_html


def test_nested_parent_node():
    node_1 = LeafNode(tag="b", value="This is bold")
    node_2 = LeafNode(value = "This is just normal text")
    node_3 = LeafNode(tag="p", value="This is a paragraph", props={"class":"cool-p"})
    node_4 = LeafNode(tag="a", value="Hyperlink", props={"href":"www.boot.dev"})

    parent_1 = ParentNode(tag="div", props={"class":"paragraph-container"}, children=[node_1, node_2])
    parent_2 = ParentNode(tag="div", props={"class":"super-container"}, children=[parent_1, node_3])
    parent_3 = ParentNode(tag="div", children=[parent_2, node_4])

    expected_html = (
        '<div><div class="super-container"><div class="paragraph-container">'
        '<b>This is bold</b>This is just normal text'
        '</div><p class="cool-p">This is a paragraph</p>'
        '</div><a href="www.boot.dev">Hyperlink</a></div>'
    )
    assert parent_3.to_html() == expected_html
    
