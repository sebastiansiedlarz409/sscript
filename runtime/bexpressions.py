from misc.exceptions import *
from runtime.values import *

class BExpressions():
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