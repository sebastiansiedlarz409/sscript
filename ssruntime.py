from nodes.nodes import *
from values.values import *

class SSRuntime:
    def __init__(self):
        pass

    def evalBinaryExpressionNumberNumber(self, lvalue, rvalue, operator):
        result = 0

        if operator == "+":
            result = lvalue.value + rvalue.value
        elif operator == "-":
            result = lvalue.value - rvalue.value
        elif operator == "*":
            result = lvalue.value * rvalue.value
        elif operator == "/":
            result = lvalue.value / rvalue.value
        elif operator == "%":
            result = lvalue.value % rvalue.value
        elif operator == "|":
            result = lvalue.value | rvalue.value
        elif operator == "&":
            result = lvalue.value & rvalue.value
        elif operator == "^":
            result = lvalue.value ^ rvalue.value
        elif operator == "<":
            result = lvalue.value << rvalue.value
        elif operator == ">":
            result = lvalue.value >> rvalue.value

        ret = NumberRuntimeValue()
        ret.setValue(result)
        return ret

    def evalBinaryExpressionBool(self, lvalue, rvalue, operator):
        result = False

        if operator == "or":
            result = lvalue.value or rvalue.value
        elif operator == "and":
            result = lvalue.value and rvalue.value
        elif operator == "eq":
            result = lvalue.value == rvalue.value
        elif operator == "neq":
            result = lvalue.value != rvalue.value
        elif operator == "gr":
            result = lvalue.value > rvalue.value
        elif operator == "ge":
            result = lvalue.value >= rvalue.value
        elif operator == "gr":
            result = lvalue.value < rvalue.value
        elif operator == "gr":
            result = lvalue.value <= rvalue.value
        else:
            raise Exception(f"SSRuntime: Bool expression not support this operator {operator}")

        ret = BoolRuntimeValue()
        ret.setValue(result)
        return ret
    
    def boolNode(self, node):
        value = BoolRuntimeValue()
        value.setValue(True if node.value == "true" else False)
        return value

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
        elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
            #convert right number to bool
            r = BoolRuntimeValue()
            r.setValue(False if right.value == 0 else True)
            return self.evalBinaryExpressionBool(left, r, node.operator)
        elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
            #convert left number to bool
            l = BoolRuntimeValue()
            l.setValue(False if left.value == 0 else True)
            return self.evalBinaryExpressionBool(l, right, node.operator)
        elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
            return self.evalBinaryExpressionBool(bool(left), bool(right), node.operator)
        else:
            raise Exception(f"SSRuntime: Cant evaluate binary node when one of child is 'null'")

    def execute(self, node):
        if type(node).__name__ == "NullNode":
            return self.nullNode(node)
        elif type(node).__name__ == "NumberNode":
            return self.numberNode(node)
        elif type(node).__name__ == "BoolNode":
            return self.boolNode(node)
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
