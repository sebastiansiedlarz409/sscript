from parser.nodes.nodes import *

class UnaryExpressionNode(Node):
    def __init__(self):
        self.child: Node = None
        self.operator: str = None

    def setOperator(self, operator: str):
        self.operator = operator

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"({self.operator} {self.child})"
        return ret
    
class BinaryExpressionNode(Node):
    def __init__(self):
        self.lChild: Node = None
        self.rChild: Node = None
        self.operator: str = None

    def setOperator(self, operator: str):
        self.operator = operator
    
    def setLChild(self, child: Node):
        self.lChild = child

    def setRChild(self, child: Node):
        self.rChild = child

    def __repr__(self) -> str:
        ret = f"({self.lChild} {self.operator} {self.rChild})"
        return ret
    
class PrefixExpressionNode(Node):
    def __init__(self):
        self.operator: str = None
        self.child: Node = None

    def setOperator(self, operator: str):
        self.operator = operator

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"{self.operator}({self.child})"
        return ret

class PostfixExpressionNode(Node):
    def __init__(self):
        self.operator: str = None
        self.child: Node = None

    def setOperator(self, operator: str):
        self.operator = operator

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"({self.child}){self.operator}"
        return ret
    
class ArrayNode(Node):
    def __init__(self):
        self.children: list[Node] = []

    def setChildren(self, children: list[Node]):
        self.children = children

    def __repr__(self) -> str:
        children = ""
        for c in self.children:
            children += f"{c}, "
        if len(children) > 2:
            children = children[0:len(children)-2]
        ret = f"[{children}]"
        return ret
    
class ArrayReferenceNode(Node):
    def __init__(self):
        self.array: Node = None
        self.index = None

    def setArray(self, array: str):
        self.array = array
    
    def setIndex(self, index: Node):
        self.index = index

    def __repr__(self) -> str:
        ret = f"{self.array}[{self.index}]"
        return ret
    
class ArrayElementOverrideNode(Node):
    def __init__(self):
        self.array: Node = None
        self.index = None
        self.child = None

    def setArray(self, array: str):
        self.array = array
    
    def setIndex(self, index: Node):
        self.index = index

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"{self.array}[{self.index}] = {self.child}"
        return ret