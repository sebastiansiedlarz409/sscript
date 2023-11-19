#exceptions
from misc.exceptions import *

#runtime values
from runtime.values import *

#scope stuff
from runtime.ssscope import *

class Expressions():
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
            raise SSException(f"SSRuntime: Cannot evaluate operator '{operator}' on this types of values")

        #try to adapt result to lvalue type
        if type(lvalue) == NumberRuntimeValue:
            return NumberRuntimeValue(result)
        elif type(lvalue) == StringRuntimeValue:
            return StringRuntimeValue(result)
        else:
            raise SSException(f"SSRuntime: Cannot adapt binary expression result to lvalue type of {type(lvalue)}")
            

    def evalBinaryExpressionLogical(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = False
        
        try:
            if operator == "or":
                result = lvalue.value or rvalue.value
            elif operator == "and":
                result = lvalue.value and rvalue.value
            else:
                raise SSException(f"SSRuntime: Bool expression not support this operator '{operator}'")
        except TypeError:
            raise SSException(f"SSRuntime: Cannot evaluate operator '{operator}' on this types of values")

        return BoolRuntimeValue(result)

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
                raise SSException(f"SSRuntime: Bool expression not support this operator '{operator}'")
        except TypeError:
            raise SSException(f"SSRuntime: Cannot evaluate operator '{operator}' on this types of values")

        return BoolRuntimeValue(result)
    
    def binaryExpressionNode(self, node: Node, left: RuntimeValue, right: RuntimeValue, scope: SSRuntimeScope) -> RuntimeValue:
        #not logical operator
        if node.operator in "+-*/%&|<<>>^":
            #NUMBER <> NUMBER
            if type(left) == NumberRuntimeValue and type(right) == NumberRuntimeValue:
                return self.evalBinaryExpressionArithmetic(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif type(left) == NumberRuntimeValue and type(right) == BoolRuntimeValue:
                r = NumberRuntimeValue(1 if right.value else 0)
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #NUMBER <> STRING
            elif type(left) == NumberRuntimeValue and type(right) == StringRuntimeValue:
                l = StringRuntimeValue(str(left.value))
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif type(left) == BoolRuntimeValue and type(right) == NumberRuntimeValue:
                l = NumberRuntimeValue(1 if left.value else 0)
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #BOOL <> BOOL
            elif type(left) == BoolRuntimeValue and type(right) == BoolRuntimeValue:
                l = NumberRuntimeValue(1 if left.value else 0)
                r = NumberRuntimeValue(1 if right.value else 0)
                return self.evalBinaryExpressionArithmetic(l, r, node.operator)
            
            #BOOL <> STRING
            elif type(left) == BoolRuntimeValue and type(right) == StringRuntimeValue:
                l = StringRuntimeValue("true" if left.value else "false")
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #STRING <> NUMBER
            elif type(left) == StringRuntimeValue and type(right) == NumberRuntimeValue:
                r = StringRuntimeValue(str(right.value))
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #STRING <> BOOL
            elif type(left) == StringRuntimeValue and type(right) == BoolRuntimeValue:
                r = StringRuntimeValue("true" if right.value else "false")
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #STRING <> STRING
            elif type(left) == StringRuntimeValue and type(right) == StringRuntimeValue:
                return self.evalBinaryExpressionArithmetic(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cannot use operator '{node.operator}' with this types of values")
            
        #comparasion operators
        elif node.operator in ["eq", "neq", "gr", "ge", "ls", "le"]:
            #NUMBER <> NUMBER
            if type(left) == NumberRuntimeValue and type(right) == NumberRuntimeValue:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif type(left) == NumberRuntimeValue and type(right) == BoolRuntimeValue:
                r = NumberRuntimeValue(1 if right.value else 0)
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #NUMBER <> STRING
            elif type(left) == NumberRuntimeValue and type(right) == StringRuntimeValue:
                l = StringRuntimeValue(str(left.value))
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif type(left) == BoolRuntimeValue and type(right) == NumberRuntimeValue:
                l = NumberRuntimeValue(1 if left.value else 0)
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #BOOL <> BOOL
            elif type(left) == BoolRuntimeValue and type(right) == BoolRuntimeValue:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            #BOOL <> STRING
            elif type(left) == BoolRuntimeValue and type(right) == StringRuntimeValue:
                l = StringRuntimeValue("true" if left.value else "false")
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #STRING <> NUMBER
            elif type(left) == StringRuntimeValue and type(right) == NumberRuntimeValue:
                r = StringRuntimeValue(str(right.value))
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #STRING <> BOOL
            elif type(left) == StringRuntimeValue and type(right) == BoolRuntimeValue:
                r = StringRuntimeValue("true" if right.value else "false")
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #STRING <> STRING
            elif type(left) == StringRuntimeValue and type(right) == StringRuntimeValue:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cannot use operator '{node.operator}' with this types of values")

        #logical operator
        else:
            #NUMBER <> NUMBER
            if type(left) == NumberRuntimeValue and type(right) == NumberRuntimeValue:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif type(left) == NumberRuntimeValue and type(right) == BoolRuntimeValue:
                r = NumberRuntimeValue(False if right.value == 0 else True)
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #NUMBER <> STRING
            elif type(left) == NumberRuntimeValue and type(right) == StringRuntimeValue:
                l = StringRuntimeValue(str(left.value))
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif type(left) == BoolRuntimeValue and type(right) == NumberRuntimeValue:
                l = NumberRuntimeValue(1 if left.value else 0)
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #BOOL <> BOOL
            elif type(left) == BoolRuntimeValue and type(right) == BoolRuntimeValue:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #BOOL <> STRING
            elif type(left) == BoolRuntimeValue and type(right) == StringRuntimeValue:
                l = StringRuntimeValue("true" if left.value else "false")
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #STRING <> NUMBER
            elif type(left) == StringRuntimeValue and type(right) == NumberRuntimeValue:
                r = StringRuntimeValue(str(right.value))
                return self.evalBinaryExpressionLogical(left, r, node.operator)
            
            #STRING <> BOOL
            elif type(left) == StringRuntimeValue and type(right) == BoolRuntimeValue:
                r = StringRuntimeValue("true" if right.value else "false")
                return self.evalBinaryExpressionLogical(left, r, node.operator)
            
            #STRING <> STRING
            elif type(left) == StringRuntimeValue and type(right) == StringRuntimeValue:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cannot evaluate binary node for lvalue type of '{type(left)}' and rvalue type of '{type(right)}'")

    def unaryExpressionNode(self, node: Node, child: RuntimeValue, scope: SSRuntimeScope) -> RuntimeValue:
        if node.operator == "not":
            if type(child) == NumberRuntimeValue:
                return BoolRuntimeValue(True if child.value == 0 else False)
            elif type(child) == BoolRuntimeValue:
                return BoolRuntimeValue(not child.value)
            elif type(child) == StringRuntimeValue:
                return BoolRuntimeValue(False if len(child.value) > 0 else True)
        elif node.operator == "+":
            if type(child) == NumberRuntimeValue:
                return NumberRuntimeValue(child.value)
            elif type(child) == BoolRuntimeValue:
                return BoolRuntimeValue(1 if child.value else 0)
            elif type(child) == StringRuntimeValue:
                raise SSException(f"SSRuntime: Cannot use operator '{node.operator}' with this types of values")
        elif node.operator == "-":
            if type(child) == NumberRuntimeValue:
                return NumberRuntimeValue(child.value*(-1))
            elif type(child) == BoolRuntimeValue:
                return BoolRuntimeValue(-1 if child.value else 0)
            elif type(child) == StringRuntimeValue:
                raise SSException(f"SSRuntime: Cannot use operator '{node.operator}' with this types of values")