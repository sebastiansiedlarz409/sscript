from enum import Enum
from parser.nodes.nodes import *

class ValueTypes(Enum):
    Number = 0,
    Null = 1,
    Bool = 2,
    String = 3

class RuntimeValue:
    def __init__(self):
        self.type: ValueTypes = None
        self.value = None

    def setType(self, t: ValueTypes):
        self.type = t

    def setValue(self, value):
        self.value = value

    def __repr__(self):
        ret = f"{self.value}"
        return ret


class NullRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.Null)

class NumberRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.Number)

class StringRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.String)

class BoolRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.Bool)

    def __repr__(self):
        ret = f"{str(self.value).lower()}"
        return ret
    
class FunctionRuntimeValue(RuntimeValue):
    def __init__(self):
        self.params: list[Node] = []
        self.body: list[Node] = []

    def setParams(self, params: list[Node]):
        self.params = params

    def setBody(self, body: list[Node]):
        self.body = body

    def __repr__(self):
        ret = f"{{...}}"
        return ret