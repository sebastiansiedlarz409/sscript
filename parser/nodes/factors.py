from parser.nodes.nodes import *

class IdentifierNode(Node):
    def __init__(self):
        self.identifier: str = None

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

    def __repr__(self) -> str:
        ret = f"{self.identifier}"
        return ret
    
class NumberNode(Node):
    def __init__(self):
        self.number: str = None

    def setValue(self, number: str):
        self.number = number

    def __repr__(self) -> str:
        ret = f"{self.number}"
        return ret
    
class NullNode(Node):
    def __init__(self):
        self.value: str = "null"

    def __repr__(self) -> str:
        ret = f"{self.value}"
        return ret
    
class BoolNode(Node):
    def __init__(self):
        self.value: str = None

    def setValue(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        ret = f"{self.value}"
        return ret

class StringNode(Node):
    def __init__(self):
        self.value: str = None

    def setValue(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        ret = f'"{self.value}"'
        return ret