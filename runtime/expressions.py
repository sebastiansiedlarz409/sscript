from misc.exceptions import *
from runtime.values import *
from runtime.ssscope import *

class Expressions():
    def __init__(self):
        pass

    def evalBinaryExpressionArithmetic(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = 0

        try:
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
            elif operator == "<<":
                result = int(lvalue.value) << int(rvalue.value)
            elif operator == ">>":
                result = int(lvalue.value) >> int(rvalue.value)
        except TypeError:
            raise SSException(f"SSRuntime: Cant {operator} this type of values")

        if lvalue.type == ValueTypes.Number:
            ret = NumberRuntimeValue()
            ret.setValue(result)
            return ret
        elif lvalue.type == ValueTypes.String:
            ret = StringRuntimeValue()
            ret.setValue(str(result))
            return ret
        else:
            raise SSException(f"SSRuntime: Cant handle binary expression")
            

    def evalBinaryExpressionLogical(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = False
        
        try:
            if operator == "or":
                result = lvalue.value or rvalue.value
            elif operator == "and":
                result = lvalue.value and rvalue.value
            else:
                raise SSException(f"SSRuntime: Bool expression not support this operator {operator}")
        except TypeError:
            raise SSException(f"SSRuntime: Cant {operator} this type of values")

        ret = BoolRuntimeValue()
        ret.setValue(result)
        return ret

    def evalBinaryExpressionComparasion(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = False

        try:
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
                raise SSException(f"SSRuntime: Bool expression not support this operator {operator}")
        except TypeError:
            raise SSException(f"SSRuntime: Cant {operator} this type of values")

        ret = BoolRuntimeValue()
        ret.setValue(result)
        return ret
    
    def binaryExpressionNode(self, node: Node, left: RuntimeValue, right: RuntimeValue, scope: SSRuntimeScope) -> RuntimeValue:
        #not logical operator
        if node.operator in "+-*/%&|<<>>^":
            #NUMBER <> NUMBER
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionArithmetic(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                r = NumberRuntimeValue()
                r.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #NUMBER <> STRING
            elif left.type == ValueTypes.Number and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue(str(left.value))
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #BOOL <> BOOL
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                l = NumberRuntimeValue()
                l.setValue(1 if left.value else 0)
                r = NumberRuntimeValue()
                r.setValue(1 if left.value else 0)
                return self.evalBinaryExpressionArithmetic(l, r, node.operator)
            
            #BOOL <> STRING
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue("true" if left.value else "false")
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #STRING <> NUMBER
            elif left.type == ValueTypes.String and right.type == ValueTypes.Number:
                r = StringRuntimeValue()
                r.setValue(str(right.value))
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #STRING <> BOOL
            elif left.type == ValueTypes.String and right.type == ValueTypes.Bool:
                r = StringRuntimeValue()
                r.setValue("true" if right.value else "false")
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #STRING <> STRING
            elif left.type == ValueTypes.String and right.type == ValueTypes.String:
                return self.evalBinaryExpressionArithmetic(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")
            
        #comparasion operators
        elif node.operator in ["eq", "neq", "gr", "ge", "ls", "le"]:
            #NUMBER <> NUMBER
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                r = NumberRuntimeValue()
                r.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #NUMBER <> STRING
            elif left.type == ValueTypes.Number and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue(str(left.value))
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #BOOL <> BOOL
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            #BOOL <> STRING
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue("true" if left.value else "false")
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #STRING <> NUMBER
            elif left.type == ValueTypes.String and right.type == ValueTypes.Number:
                r = StringRuntimeValue()
                r.setValue(str(right.value))
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #STRING <> BOOL
            elif left.type == ValueTypes.String and right.type == ValueTypes.Bool:
                r = StringRuntimeValue()
                r.setValue("true" if right.value else "false")
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #STRING <> STRING
            elif left.type == ValueTypes.String and right.type == ValueTypes.String:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")

        #logical operator
        else:
            #NUMBER <> NUMBER
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                r = NumberRuntimeValue()
                r.setValue(False if left.value == 0 else True)
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #NUMBER <> STRING
            elif left.type == ValueTypes.Number and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue(str(left.value))
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #BOOL <> BOOL
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #BOOL <> STRING
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue("true" if left.value else "false")
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #STRING <> NUMBER
            elif left.type == ValueTypes.String and right.type == ValueTypes.Number:
                r = StringRuntimeValue()
                r.setValue(str(right.value))
                return self.evalBinaryExpressionLogical(left, r, node.operator)
            
            #STRING <> BOOL
            elif left.type == ValueTypes.String and right.type == ValueTypes.Bool:
                r = StringRuntimeValue()
                r.setValue("true" if right.value else "false")
                return self.evalBinaryExpressionLogical(left, r, node.operator)
            
            #STRING <> STRING
            elif left.type == ValueTypes.String and right.type == ValueTypes.String:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")

    def unaryExpressionNode(self, node: Node, child: RuntimeValue, scope: SSRuntimeScope) -> RuntimeValue:
        if node.operator == "not":
            if child.type == ValueTypes.Number:
                r = BoolRuntimeValue()
                r.setValue(True if child.value == 0 else False)
                return r
            elif child.type == ValueTypes.Bool:
                r = BoolRuntimeValue()
                r.setValue(not child.value)
                return r
            elif child.type == ValueTypes.String:
                r = BoolRuntimeValue()
                r.setValue(False if len(child.value) > 0 else True)
                return r
        elif node.operator == "+":
            if child.type == ValueTypes.Number:
                r = NumberRuntimeValue()
                r.setValue(child.value)
                return r
            elif child.type == ValueTypes.Bool:
                r = BoolRuntimeValue()
                r.setValue(1 if child.value else 0)
                return r
            elif child.type == ValueTypes.String:
                raise SSException(f"SSRuntime: Cant {node.operator} this type of values")
        elif node.operator == "-":
            if child.type == ValueTypes.Number:
                r = NumberRuntimeValue()
                r.setValue(child.value*(-1))
                return r
            elif child.type == ValueTypes.Bool:
                r = BoolRuntimeValue()
                r.setValue(-1 if child.value else 0)
                return r
            elif child.type == ValueTypes.String:
                raise SSException(f"SSRuntime: Cant {node.operator} this type of values")