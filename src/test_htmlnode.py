import unittest

from html_node import HTMLNode
from leaf_node import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_node_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), None)

    def test_tag_node(self):
        node = HTMLNode("<b>", "Test bold line")
        self.assertEqual(str(node), "<b>, Test bold line, None, None")

    def test_node_with_children(self):
        node_chid_1 = HTMLNode("<b>", "Test bold line")
        node_chid_2 = HTMLNode("<i>", "Test italic line")
        node_parent = HTMLNode("div", "", [node_chid_1, node_chid_2])
        self.assertEqual(str(node_parent), "div, , [<b>, Test bold line, None, None, <i>, Test italic line, None, None], None")
    
    def test_leaf_node_to_html_p(self):
        node = LeafNode("p", "Just text")
        self.assertTrue(node.to_html(),"<p>Just text</p>")

    def test_leaf_node_to_html_a_props(self):
        node = LeafNode("a", "Just text", {"href": "https://www.google.com"})
        self.assertTrue(node.to_html(),'<a href="https://www.google.com">Just text</a>')

    def test_leaf_node_to_html_no_value(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        self.assertRaises(ValueError, node.to_html)

def main():
    unittest.main()

if __name__ == "__main__":
    main()