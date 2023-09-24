from enum import Enum
from parser.nodes.nodes import *

class ValueTypes(Enum):
    Number = 0,
    Null = 1,
    Bool = 2,
    String = 3,
    Array = 4,
    Struct = 5

#runtime values are used as result
#when runtime evaluate each node
#used only in runtime
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
        self.setValue("null")

class NumberRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.Number)

class StringRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.String)

class ArrayRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.Array)

class BoolRuntimeValue(RuntimeValue):
    def __init__(self):
        self.setType(ValueTypes.Bool)

    def __repr__(self):
        ret = f"{str(self.value).lower()}"
        return ret
    
class StructRuntimeValue(RuntimeValue):
    def __init__(self):
        self.struct: str = None #type of struct
        self.parent: str = None
        self.data: dict = {}
        self.setType(ValueTypes.Struct)

    def setStruct(self, struct: str):
        self.struct = struct

    def setParent(self, parent: str):
        self.parent = parent

    def allocField(self, name: str, const: bool, value: RuntimeValue):
        self.data[name] = [value, const]

    def peakField(self, name: str):
        try:
            return self.data[name][0]
        except KeyError:
            return None

    def __repr__(self):
        ret = f"{self.struct.upper()}:{self.data}"
        return ret