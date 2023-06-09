from parser.nodes.nodes import *

class ReturnNode(Node):
    def __init__(self):
        self.value: str = None

    def setValue(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        ret = f"return {self.value}"
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
        ret = f"func {self.identifier}("
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
        ret = f"{self.identifier}("
        for p in self.params:
            ret += f"[{p}]"
        ret+=f")\n"
        ret+=f"{{\n"
        for c in self.child:
            ret += f"{c}\n"
        ret+=f"}}"

        return ret