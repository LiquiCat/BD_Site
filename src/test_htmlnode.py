import unittest

from html_node import HTMLNode
from leaf_node import LeafNode
from parent_node import ParentNode

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

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>")

    def test_parent_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("a", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(parent_node.to_html(), '<a href="https://www.google.com"><span>child</span></a>')

    def test_parent_to_html_with_child_with_props(self):
        child_node = LeafNode("span", "child", {"href": "https://www.google.com"})
        parent_node = ParentNode("a", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(parent_node.to_html(), '<a href="https://www.google.com"><span href="https://www.google.com">child</span></a>')

def main():
    unittest.main()

if __name__ == "__main__":
    main()