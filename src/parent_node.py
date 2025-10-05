from html_node import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):

        if not self.tag:
            raise ValueError("Tag is not optional for the Parent node")
        
        if not self.children:
            raise ValueError("Children are not optional for the Parent node")
        
        if self.props:
            res_html = f"<{self.tag}{self.props_to_html()}>"
        else:
            res_html = f"<{self.tag}>"

        for child in self.children:
            res_html += child.to_html()

        res_html += f"</{self.tag}>"

        return res_html