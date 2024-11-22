from textnode import TextNode, TextNodeTypes


def test_node_equality():
    node_1 = TextNode(content="abc 123", node_type = TextNodeTypes.BOLD, url="www.google.com")
    node_2 = TextNode(content="abc 123", node_type = TextNodeTypes.BOLD, url="www.google.com")
    assert node_1 == node_2


def test_node_inequality_types():
    node_1 = TextNode(content="abc 123", node_type = TextNodeTypes.BOLD, url="www.google.com")
    node_2 = TextNode(content="abc 123", node_type = TextNodeTypes.NORMAL, url="www.google.com")
    assert node_1 != node_2


def test_node_inequality_content():
    node_1 = TextNode(content="ABC 123", node_type = TextNodeTypes.NORMAL, url="www.google.com")
    node_2 = TextNode(content="abc 123", node_type = TextNodeTypes.NORMAL, url="www.google.com")
    assert node_1 != node_2


def test_node_inequality_url():
    node_1 = TextNode(content="abc 123", node_type = TextNodeTypes.NORMAL, url="www.gmail.com")
    node_2 = TextNode(content="abc 123", node_type = TextNodeTypes.NORMAL, url="www.google.com")
    assert node_1 != node_2


def test_node_equality_url_null():
    node_1 = TextNode(content="abc 123", node_type = TextNodeTypes.NORMAL, url=None)
    node_2 = TextNode(content="abc 123", node_type = TextNodeTypes.NORMAL)
    assert node_1 == node_2

