from parser.nodes import *
from runtime.values import *
from runtime.ssscope import *

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
            result = int(lvalue.value) | int(rvalue.value)
        elif operator == "&":
            result = int(lvalue.value) & int(rvalue.value)
        elif operator == "^":
            result = int(lvalue.value) ^ int(rvalue.value)
        elif operator == "<":
            result = int(lvalue.value) << int(rvalue.value)
        elif operator == ">":
            result = int(lvalue.value) >> int(rvalue.value)

        ret = NumberRuntimeValue()
        ret.setValue(result)
        return ret

    def evalBinaryExpressionBool(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = False

        if operator == "or":
            result = lvalue.value or rvalue.value
        elif operator == "and":
            result = lvalue.value and rvalue.value
        else:
            raise Exception(f"SSRuntime: Bool expression not support this operator {operator}")

        ret = BoolRuntimeValue()
        ret.setValue(result)
        return ret

    def evalBinaryExpressionComparasion(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = False

        if operator == "eq":
            result = lvalue.value == rvalue.value
        elif operator == "neq":
            result = lvalue.value != rvalue.value
        elif operator == "gr":
            result = lvalue.value > rvalue.value
        elif operator == "ge":
            result = lvalue.value >= rvalue.value
        elif operator == "ls":
            result = lvalue.value < rvalue.value
        elif operator == "le":
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
    
    def identifierNode(self, node: Node, scope: SSRuntimeScope):
        value = scope.peakValueSymbol(node.identifier)
        return value

    def programNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        last = NullNode()
        for child in node.children:
            l = self.execute(child, scope)
            if l != None:
                last = l
        return last

    def binaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        left = self.execute(node.lChild, scope)
        right = self.execute(node.rChild, scope)

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
        #comparasion operators
        elif node.operator in ["eq", "neq", "gr", "ge", "ls", "le"]:
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                #convert right bool to number
                r = NumberRuntimeValue()
                r.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                #convert left bool to number
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                #convert left bool to number
                l = NumberRuntimeValue()
                l.setValue(1 if left.value else 0)
                #convert right bool to number
                r = NumberRuntimeValue()
                r.setValue(1 if left.value else 0)
                return self.evalBinaryExpressionComparasion(l, r, node.operator)
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

    def unaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)

        if node.operator == "not":
            if child.type == ValueTypes.Number:
                r = BoolRuntimeValue()
                r.setValue(True if child.value == 0 else False)
                return r
            elif child.type == ValueTypes.Bool:
                r = BoolRuntimeValue()
                r.setValue(not child.value)
                return r
            
    def declareVariableAssignNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        if node.const:
            scope.declareValueConstSymbol(node.identifier, exp)
        else:
            scope.declareValueSymbol(node.identifier, exp)

    def variableAssignNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        scope.assignValueSymbol(node.identifier, exp)

    def logNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        print(f"{exp}",end="")

    def loglnNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        print(f"{exp}")

    def execute(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:

        if type(node).__name__ == "NullNode":
            return self.nullNode(node)
        elif type(node).__name__ == "NumberNode":
            return self.numberNode(node)
        elif type(node).__name__ == "BoolNode":
            return self.boolNode(node)
        elif type(node).__name__ == "IdentifierNode":
            return self.identifierNode(node, scope)
        elif type(node).__name__ == "BinaryExpressionNode":
            return self.binaryExpressionNode(node, scope)
        elif type(node).__name__ == "UnaryExpressionNode":
            return self.unaryExpressionNode(node, scope)
        elif type(node).__name__ == "VariableAssignNode":
            self.variableAssignNode(node, scope)
        elif type(node).__name__ == "DeclareVariableAssignNode":
            self.declareVariableAssignNode(node, scope)
        elif type(node).__name__ == "FunctionDeclarationNode":
            pass
        elif type(node).__name__ == "LogNode":
            self.logNode(node, scope)
        elif type(node).__name__ == "LoglnNode":
            self.loglnNode(node, scope)
        elif type(node).__name__ == "ProgramNode":
            return self.programNode(node, scope)
        else:
            raise Exception(f"SSRuntime: Failed to evaluate node {type(node).__name__}")
