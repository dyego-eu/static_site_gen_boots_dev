import pytest

from htmlnode import HTMLNode, LeafNode


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

