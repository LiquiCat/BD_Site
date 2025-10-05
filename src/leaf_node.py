from html_node import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag=tag, value=value, props=props)

        if self.props and not self.tag:
            raise ValueError("Props should be provided only with the tag not None")

    def to_html(self):

        if not self.value:
            raise ValueError("Leaf Node should contain a value")

        if self.tag:
            if self.props:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return self.value