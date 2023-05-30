from parser.nodes.nodes import *

class VariableAssignNode(Node):
    def __init__(self):
        self.identifier: str = None
        self.child: Node = None

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"{self.identifier} <= {self.child}"
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
            ret = f"const {self.identifier} <= {self.child}"
            return ret
        else:
            ret = f"let {self.identifier} <= {self.child}"
            return ret