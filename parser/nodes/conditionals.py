from parser.nodes.nodes import *

class IfNode(Node):
    def __init__(self):
        self.body: list[Node] = [] #if body
        self.logic: Node = None #test exression
        self.child: Node = None #else/elif

    def setBody(self, body: list[Node]):
        self.body = body

    def setLogicExpression(self, expression: Node):
        self.logic = expression

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"if({self.logic}){{\n"
        for b in self.body:
            ret += f"{b}\n"
        ret += "}"
        if self.child != None:
            ret += f"\n{self.child}"
        return ret

class ElifNode(Node):
    def __init__(self):
        self.body: list[Node] = [] #if body
        self.logic: Node = None #test exression
        self.child: Node = None #else/elif

    def setBody(self, body: list[Node]):
        self.body = body

    def setLogicExpression(self, expression: Node):
        self.logic = expression

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"elif({self.logic}){{\n"
        for b in self.body:
            ret += f"{b}\n"
        ret += "}"
        if self.child != None:
            ret += f"\n{self.child}"
        return ret

class ElseNode(Node):
    def __init__(self):
        self.body: list[Node] = [] #if body

    def setBody(self, body: list[Node]):
        self.body = body

    def __repr__(self) -> str:
        ret = f"else{{\n"
        for b in self.body:
            ret += f"{b}\n"
        ret += "}"
        return ret