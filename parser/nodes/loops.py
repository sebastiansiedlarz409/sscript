from parser.nodes.nodes import *

class ContinueNode(Node):
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return "continue"

class BreakNode(Node):
    def __init__(self):
        pass
    
    def __repr__(self) -> str:
        return "break"

class ForLoopNode(Node):
    def __init(self):
        self.body: list[Node] = [] #body
        self.start: Node = None #start expression
        self.logic: Node = None #test expression
        self.mod: Node = None #modyfication expression

    def setBody(self, body: list[Node]):
        self.body = body

    def setStartExpression(self, expression: Node):
        self.start = expression

    def setLogicExpression(self, expression: Node):
        self.logic = expression

    def setModExpression(self, expression: Node):
        self.mod = expression

    def __repr__(self) -> str:
        ret = f"for({self.start};{self.logic};{self.mod}){{\n"
        for b in self.body:
            ret += f"{b}\n"
        ret += "}"
        return ret

class WhileLoopNode(Node):
    def __init(self):
        self.body: list[Node] = [] #body
        self.logic: Node = None #test expression

    def setBody(self, body: list[Node]):
        self.body = body

    def setLogicExpression(self, expression: Node):
        self.logic = expression

    def __repr__(self) -> str:
        ret = f"while({self.logic}){{\n"
        for b in self.body:
            ret += f"{b}\n"
        ret += "}"
        return ret
    
class DoWhileLoopNode(Node):
    def __init(self):
        self.body: list[Node] = [] #body
        self.logic: Node = None #test expression

    def setBody(self, body: list[Node]):
        self.body = body

    def setLogicExpression(self, expression: Node):
        self.logic = expression

    def __repr__(self) -> str:
        ret = f"do{{\n"
        for b in self.body:
            ret += f"{b}\n"
        ret += "}while({self.logic})"
        return ret