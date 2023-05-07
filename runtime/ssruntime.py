from parser.nodes import *
from runtime.values import *

class SSRuntime:
    def __init__(self):
        pass

    def evalBinaryExpressionNumber(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
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

    def evalBinaryExpressionBool(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
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
    
    def boolNode(self, node: Node) -> RuntimeValue:
        value = BoolRuntimeValue()
        value.setValue(True if node.value == "true" else False)
        return value

    def numberNode(self, node: Node) -> RuntimeValue:
        value = NumberRuntimeValue()
        value.setValue(float(node.number))
        return value
    
    def nullNode(self, node: Node) -> RuntimeValue:
        value = NullRuntimeValue()
        return value

    def programNode(self, node: Node) -> RuntimeValue:
        last = NullNode()
        for child in node.children:
            last = self.execute(child)
        return last

    def binaryExpressionNode(self, node: Node) -> RuntimeValue:
        left = self.execute(node.lChild)
        right = self.execute(node.rChild)

        #not logical operator
        if node.operator in "+-*/%&|<>^":
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionNumber(left, right, node.operator)
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                #convert right bool to number
                r = NumberRuntimeValue()
                r.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionNumber(left, r, node.operator)
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                #convert left bool to number
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionNumber(l, right, node.operator)
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                #convert left bool to number
                l = NumberRuntimeValue()
                l.setValue(1 if left.value else 0)
                #convert right bool to number
                r = NumberRuntimeValue()
                r.setValue(1 if left.value else 0)
                return self.evalBinaryExpressionNumber(l, r, node.operator)
            else:
                raise Exception(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")
        #logical operator
        else:
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                #convert left number to bool
                l = BoolRuntimeValue()
                l.setValue(False if left.value == 0 else True)
                #convert right number to bool
                r = BoolRuntimeValue()
                r.setValue(False if right.value == 0 else True)
                return self.evalBinaryExpressionBool(l, r, node.operator)
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
                return self.evalBinaryExpressionBool(left, right, node.operator)
            else:
                raise Exception(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")

    def unaryExpressionNode(self, node: Node) -> RuntimeValue:
        child = self.execute(node.child)

        if node.operator == "not":
            if child.type == ValueTypes.Number:
                r = BoolRuntimeValue()
                r.setValue(True if child.value == 0 else False)
                return r
            elif child.type == ValueTypes.Bool:
                r = BoolRuntimeValue()
                r.setValue(not child.value)
                return r

    def execute(self, node: Node) -> RuntimeValue:
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
            return self.unaryExpressionNode(node)
        elif type(node).__name__ == "VariableAssignNode":
            pass
        elif type(node).__name__ == "FunctionDeclarationNode":
            pass
        elif type(node).__name__ == "ProgramNode":
            return self.programNode(node)
        else:
            raise Exception(f"SSRuntime: Failed to evaluate node {type(node).__name__}")
