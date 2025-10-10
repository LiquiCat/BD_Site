import unittest

from textnode import TextNode, TextType, \
    text_node_to_html_node, split_nodes_delimiter, \
    extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)
    
    def test_eq_with_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("This is a text node 1", TextType.BOLD)
        node2 = TextNode("This is a text node 2", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.youtube.com")
        self.assertNotEqual(node1, node2)

    def test_text_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_text_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a text node</a>')

    def test_text_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="https://www.google.com" alt="This is a text node"></img>')

    def test_delimeter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, result)

    def test_delimeter_odd(self):
        node = TextNode("This is text with a `code block` word` and one tailing", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word` and one tailing", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, result)

    def test_delimeter_multiple(self):
        node = TextNode("This is text with a `code block` word` and one tailing` not anymore", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
            TextNode(" and one tailing", TextType.CODE),
            TextNode(" not anymore", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, result)

    def test_delimeter_bold(self):
        node = TextNode("This is text with a **bold part** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold part", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, result)

    def test_delimeter_italic(self):
        node = TextNode("This is text with a _italic part_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("italic part", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, result)

    def test_delimeter_empty(self):
        node = TextNode("This is text with an __ empty part", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode(" empty part", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, result)
    
    def test_delimeter_multiple(self):
        node1 = TextNode("This is text with _italic_ part", TextType.PLAIN)
        node2 = TextNode("Second _text with italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        result = [
            TextNode("This is text with ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" part", TextType.PLAIN),
            TextNode("Second ", TextType.PLAIN),
            TextNode("text with italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, result)

    def test_extract_images_2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_imgs = extract_markdown_images(text)
        res = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extracted_imgs, res)

    def test_extract_images_1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and None"
        extracted_imgs = extract_markdown_images(text)
        res = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extracted_imgs, res)

    def test_extract_images_no_img(self):
        text = "This is text with a (https://i.imgur.com/aKaOqIh.gif) and (https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_imgs = extract_markdown_images(text)
        res = []
        self.assertEqual(extracted_imgs, res)

    def test_extract_images_no_text(self):
        text = "This is text with a ![](https://i.imgur.com/aKaOqIh.gif) and ![](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_imgs = extract_markdown_images(text)
        res = [("", "https://i.imgur.com/aKaOqIh.gif"), ("", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extracted_imgs, res)

    def test_extract_images_no_link(self):
        text = "This is text with a ![rick roll]() and ![obi wan]()"
        extracted_imgs = extract_markdown_images(text)
        res = []
        self.assertEqual(extracted_imgs, res)

    def test_extract_links_2(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_imgs = extract_markdown_links(text)
        res = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extracted_imgs, res)

    def test_extract_links_1(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and None"
        extracted_imgs = extract_markdown_links(text)
        res = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extracted_imgs, res)

    def test_extract_links_no_text(self):
        text = "This is text with a (https://i.imgur.com/aKaOqIh.gif) and (https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_imgs = extract_markdown_links(text)
        res = []
        self.assertEqual(extracted_imgs, res)

    def test_extract_links_empty_text(self):
        text = "This is text with a [](https://i.imgur.com/aKaOqIh.gif) and [](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_imgs = extract_markdown_links(text)
        res = []
        self.assertEqual(extracted_imgs, res)

    def test_extract_links_no_link(self):
        text = "This is text with a [rick roll]() and [obi wan]()"
        extracted_imgs = extract_markdown_links(text)
        res = []
        self.assertEqual(extracted_imgs, res)

def main():
    unittest.main()

if __name__ == "__main__":
    main()