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
            ret += f"{child}"
            ret += "\n"
        return ret[0:len(ret)-1]
        
class LogNode(Node):
    def __init__(self):
        self.child: Node = None

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"log({self.child})"
        return ret
    
class LoglnNode(Node):
    def __init__(self):
        self.child: Node = None

    def setChild(self, child: Node):
        self.child = child

    def __repr__(self) -> str:
        ret = f"logln({self.child})"
        return ret