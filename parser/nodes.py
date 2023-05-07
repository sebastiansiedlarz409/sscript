class Node:
    def __init__(self):
        pass

class ProgramNode(Node):
    def __init__(self):
        self.children: list[Node] = []

    def appendChild(self, child: Node):
        self.children.append(child)

    def __repr__(self) -> str:
        ret = f"Program:\n"
        for child in self.children:
            ret += "\t"
            ret += f"{child}"
            ret += "\n"
        return ret
    
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
        self.value: str = None

    def setValue(self, value: str):
        self.value = value

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
    
class FunctionDeclarationNode(Node):
    def __init__(self):
        self.identifier: str = None
        self.params: list[Node] = [] #params
        self.child: list[Node] = [] #body

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

    def appendParams(self, param: Node):
        self.params.append(param)

    def appendChild(self, child: Node):
        self.child.append(child)

    def __repr__(self) -> str:
        ret = f"{self.identifier}: ("
        for p in self.params:
            ret += f"{p} "
        ret+=f")\n"
        for c in self.child:
            ret += f"\t{c}"

        return ret
    
class VariableAssignNode(Node):
    def __init__(self):
        self.identifier: str = None
        self.child: Node = None

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"{self.identifier} <= ({self.child})"
        return ret
    
class DeclareVariableAssignNode(Node):
    def __init__(self):
        self.identifier: str = None
        self.child: Node = None
        self.const: bool = False

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

    def setChild(self, child: Node):
        self.child = child

    def isConst(self):
        self.const = True

    def __repr__(self) -> str:
        if self.const:
            ret = f"(const) {self.identifier} <= ({self.child})"
            return ret
        else:
            ret = f"{self.identifier} <= ({self.child})"
            return ret