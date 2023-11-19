from enum import Enum

#parser nodes
from parser.nodes.nodes import *

#runtime values are used as result
#when runtime evaluate each node
#value member contains python value
class RuntimeValue:
    def __init__(self, value = None):
        self.value = value

    def __repr__(self):
        ret = f"{self.value if self.value is not None else 'null'}"
        return ret

class NullRuntimeValue(RuntimeValue):
    def __init__(self):
        super().__init__(None)

class NumberRuntimeValue(RuntimeValue):
    def __init__(self, value = None):
        super().__init__(value)

class StringRuntimeValue(RuntimeValue):
    def __init__(self, value = None):
        super().__init__(value)

class ArrayRuntimeValue(RuntimeValue):
    def __init__(self, value = None):
        super().__init__(value)

class BoolRuntimeValue(RuntimeValue):
    def __init__(self, value = None):
        super().__init__(value)

    def __repr__(self):
        ret = f"{str(self.value).lower()}"
        return ret
    
class StructRuntimeValue(RuntimeValue):
    def __init__(self, structName: str = None, parentName: str = None):
        self.structName: str = structName
        self.parent: str = parentName
        self.data: dict = {} #{key: [value, isConst],...}

    def createField(self, name: str, isConst: bool, value: RuntimeValue):
        if name in self.data.keys():
            return None
        
        self.data[name] = [value, isConst]

    def overrideField(self, name: str, value: RuntimeValue):
        if name in self.data.keys():
            return None
        
        if self.isConst(name):
            return None
        
        self.data[name][0] = value

    def isConst(self, name: str):
        if name not in self.data.keys():
            return None
        
        return self.data[name][1]

    def peakField(self, name: str):
        if name not in self.data.keys():
            return None
        
        return self.data[name][0]

    def __repr__(self):
        ret = f"{self.structName.upper()}->{self.data}"
        return ret