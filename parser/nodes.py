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
    
class ReturnNode(Node):
    def __init__(self):
        self.value: str = None

    def setValue(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        ret = f"return {self.value}"
        return ret
    
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
            ret += f"\t{b}\n"
        ret += "\t}"
        return ret

class FunctionCallNode(Node):
    def __init__(self):
        self.identifier: str = None
        self.params: list[Node] = [] #params

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

    def setParams(self, param: list[Node]):
        self.params = param

    def __repr__(self) -> str:
        ret = f"{self.identifier}("
        for c in self.params:
            ret += f"{c},"
        ret = ret[:len(ret)-1] + ")" if ret[len(ret)-1] == "," else ret + ")"
        return ret

class FunctionDeclarationNode(Node):
    def __init__(self):
        self.identifier: str = None
        self.params: list[Node] = [] #params
        self.child: list[Node] = [] #body

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

    def setParams(self, param: list[Node]):
        self.params = param

    def setChild(self, child: list[Node]):
        self.child = child

    def __repr__(self) -> str:
        ret = f"{self.identifier}: ("
        for p in self.params:
            ret += f"{p} "
        ret+=f")\n"
        ret+=f"\t{{\n"
        for c in self.child:
            ret += f"\t{c}"
        ret+=f"\n\t}}"

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
        
class LogNode(Node):
    def __init__(self):
        self.child: Node = None

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"(log {self.child})"
        return ret
    
class LoglnNode(Node):
    def __init__(self):
        self.child: Node = None

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"(logln {self.child})"
        return ret