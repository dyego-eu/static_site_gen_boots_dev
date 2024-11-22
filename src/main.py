from textnode import TextNode, TextNodeTypes


def main():
    node = TextNode(
        content="this is some text",
        url="https://boot.dev/",
        node_type=TextNodeTypes.NORMAL,
    )
    print(node)


if __name__ == "__main__":
    main()

