class HTMLNode():

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self): 
        raise NotImplementedError
    
    def props_to_html(self):
        formatted_string = ""

        if self.props is None or self.props == {}:
            return formatted_string
        
        for key in self.props:
            formatted_string += " "
            formatted_string += f'{key}="{self.props[key]}"'

        return formatted_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        
        if self.value is None:
            raise ValueError("Value cannot be empty or None")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            string += child.to_html()
        string += f"</{self.tag}>"
        return string
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        