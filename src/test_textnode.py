import unittest

from textnode import TextNode,TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)
    
    def test_eq_with_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("This is a text node 1", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node 2", TextType.BOLD_TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.youtube.com")

        self.assertNotEqual(node1, node2)

def main():
    unittest.main()

if __name__ == "__main__":
    main()