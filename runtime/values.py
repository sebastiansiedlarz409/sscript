from enum import Enum

class ValueTypes(Enum):
    Number = 0,
    Null = 1,
    Bool = 2

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

class BoolRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.Bool)