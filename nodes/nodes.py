class Node:
    def __init__(self):
        pass

class ProgramNode(Node):
    def __init__(self):
        self.children = []

    def appendChild(self, child):
        self.children.append(child)

    def __repr__(self):
        ret = ""
        for child in self.children:
            ret += "\t"
            ret += child
            ret += "\n"
        return ret
    
class IdentifierNode(Node):
    def __init__(self):
        self.identifier = None

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        ret = self.identifier
        return ret
    
class NumberNode(Node):
    def __init__(self):
        self.number = None

    def setIdentifier(self, number):
        self.number = number

    def __repr__(self):
        ret = self.number
        return ret
    
class VariableAssignNode(Node):
    def __init__(self):
        self.identifier = None
        self.child = None

    def setIdentifier(self, identifier):
        self.identifier = identifier

    def setChild(self, child):
        self.child = child

    def __repr__(self):
        ret = f"{self.identifier} <= ({self.child})"
        return ret

class UnaryExpressionNode(None):
    def __init__(self):
        self.child = None
        self.operator = None

    def setOperator(self, operator):
        self.operator = operator

    def setChild(self, child):
        self.child = child

    def __repr__(self):
        ret = f"({self.operator} {self.child})"
        return ret
    
class BinaryExpressionNode(Node):
    def __init__(self):
        self.lChild = None
        self.rChild = None
        self.operator = None

    def setOperator(self, operator):
        self.operator = operator
    
    def setLChild(self, child):
        self.lChild = child

    def setRChild(self, child):
        self.rChild = child

    def __repr__(self):
        ret = f"({self.lChild} {self.operator} {self.rChild})"
        return ret