from nodes.nodes import *
from values.values import *

class SSRuntime:
    def __init__(self):
        pass

    def evalBinaryExpressionNumberNumber(self, lvalue, rvalue, operator):
        result = 0

        if operator == "+":
            result = lvalue.value + rvalue.value

        ret = NumberRuntimeValue()
        ret.setValue(result)
        return ret

    def numberNode(self, node):
        value = NumberRuntimeValue()
        value.setValue(float(node.number))
        return value
    
    def nullNode(self, node):
        value = NullRuntimeValue()
        return value

    def programNode(self, node):
        last = NullNode()
        for child in node.children:
            last = self.execute(child)
        return last

    def binaryExpressionNode(self, node):
        left = self.execute(node.lChild)
        right = self.execute(node.rChild)

        if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
            return self.evalBinaryExpressionNumberNumber(left, right, node.operator)
        else:
            raise Exception(f"SSRuntime: Cant evaluate binary node when one of child is 'null'")

    def execute(self, node):
        if type(node).__name__ == "NullNode":
            return self.nullNode(node)
        elif type(node).__name__ == "NumberNode":
            return self.numberNode(node)
        elif type(node).__name__ == "IdentifierNode":
            pass
        elif type(node).__name__ == "BinaryExpressionNode":
            return self.binaryExpressionNode(node)
        elif type(node).__name__ == "UnaryExpressionNode":
            pass
        elif type(node).__name__ == "VariableAssignNode":
            pass
        elif type(node).__name__ == "FunctionDeclarationNode":
            pass
        elif type(node).__name__ == "ProgramNode":
            return self.programNode(node)
        else:
            raise Exception(f"SSRuntime: Failed to evaluate node {type(node).__name__}")
