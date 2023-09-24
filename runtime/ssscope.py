#every scope has list of identifiers
#identifier can be value type (variables, consts) or function type (functions)

from runtime.values import *
from misc.exceptions import *

class RuntimeIdentifier:
    def __init__(self):
        self.identifier: str = None

    def setIdentifier(self, identifier: str):
        self.identifier = identifier

class ValueRuntimeIdentifier(RuntimeIdentifier):
    def __init__(self):
        self.value: RuntimeValue = None
        self.const: bool = False

    def setValue(self, value: RuntimeValue):
        self.value = value

    def isConst(self):
        self.const = True

    def __repr__(self) -> str:
        ret = f"{self.identifier} = {self.value}"
        return ret
    
class FunctionRuntimeIdentifier(RuntimeIdentifier):
    def __init__(self):
        self.value: Node = None
    
    def setValue(self, value: Node):
        self.value = value

    def __repr__(self) -> str:
        ret = f"{self.identifier} = {self.value}"
        return ret
    
class TypeRuntimeIdentifier(RuntimeIdentifier):
    def __init__(self):
        self.struct: Node = None
        self.impl: Node = None
        self.parent: str = None

    def setParent(self, parent: str):
        self.parent = parent
    
    def setFields(self, struct: Node):
        self.struct = struct

    def setImpl(self, impl: Node):
        self.impl = impl

    def __repr__(self) -> str:
        ret = f"{self.struct}\n{self.impl}"
        return ret
    
#scope
class SSRuntimeScope:
    def __init__(self): 
        #parent in type Runtimescope
        self.parent = None
        self.symbols: list[RuntimeIdentifier] = []
        self.types: list[RuntimeIdentifier] = []

    def setParentScope(self, parent):
        self.parent = parent

    def checkIfTypeExists(self, symbol: str):
        scope = self
        #find root due to root type allocation
        while scope.parent:
            scope = scope.parent

        test = [x for x in self.types if x.identifier == symbol.upper()]
        if len(test) == 1:
            return test[0]
        
    #olawys declare in the root scope
    def declareType(self, symbol: str, value: Node):
        if self.checkIfTypeExists(symbol) != None:
            raise SSException(f"SSRuntime: Type '{symbol}' has already been declared")
        
        #find parent
        parent = None
        if value.parent:
            parent = self.checkIfTypeExists(value.parent)
            if not parent:
                raise SSException(f"SSRuntime: Parent type '{value.parent}' has not been declared yet")
        
        scope = self
        #find root (always declare in root scope)
        while scope.parent:
            scope = scope.parent

        t = TypeRuntimeIdentifier()
        t.setIdentifier(symbol)
        t.setFields(value)
        if parent:
            t.setParent(parent.struct.name)

        scope.types.append(t)

    #alawys declare in the root scope
    def declareTypeImpl(self, symbol: str, value: Node):
        struct = self.checkIfTypeExists(symbol)
        if struct != None:
            if struct.impl != None:
                raise SSException(f"SSRuntime: Type '{symbol}' has already been implemented")
        else: #declare empty type
            scope = self
            #find root (always declare in root scope)
            while scope.parent:
                scope = scope.parent

            t = TypeRuntimeIdentifier()
            t.setIdentifier(symbol)

            scope.types.append(t)
        
        struct = self.checkIfTypeExists(symbol)
        struct.setImpl(value)
        
        #check if inherit
        if value.parent:
            parent = self.checkIfTypeExists(value.parent)
            if not parent:
                raise SSException(f"SSRuntime: Parent type '{value.parent}' has not been declared yet")

            #check if inherit type is same as coresponding struct
            if value.parent != struct.parent.identifier:
                raise SSException(f"SSRuntime: Parent has to be the same for type and implementation")
    
    #return struct node from main scope
    def peakTypeSymbol(self, symbol: str) -> Node:
        struct = self.checkIfTypeExists(symbol)
        if not struct:
            raise SSException(f"SSRuntime: Struct '{symbol}' has not been declered yet")
        return struct.struct

    #check if function exist in myself or in my ancestor
    #if exist returns it
    #otherwise returns None
    def checkIfFunctionExists(self, symbol: str, par: bool) -> RuntimeIdentifier:
        test = [x for x in self.symbols if x.identifier == symbol and isinstance(x, FunctionRuntimeIdentifier)]
        if len(test) == 1:
            return test[0]
        
        if par:
            if self.parent != None:
                return self.parent.checkIfFunctionExists(symbol, True)
    
    #alway declare inside myself
    def declareFunction(self, symbol: str, value: Node):
        #check if already symbol exists
        if self.checkIfFunctionExists(symbol, False) != None:
            raise SSException(f"SSRuntime: Function '{symbol}' has already been declared")
        
        s = FunctionRuntimeIdentifier()
        s.setIdentifier(symbol)
        s.setValue(value)

        self.symbols.append(s)

    #return function value
    def peakFunctionSymbol(self, symbol: str) -> Node:
        #check if already symbol exists
        s = self.checkIfFunctionExists(symbol, True)
        if s == None:
            raise SSException(f"SSRuntime: Function '{symbol}' has not been declered yet")
        
        return s.value

    #check if symbol exist in myself or in my ancestor
    #if exist returns it
    #otherwise returns None
    def checkIfSymbolExists(self, symbol: str, par: bool) -> RuntimeIdentifier:
        test = [x for x in self.symbols if x.identifier == symbol and isinstance(x, ValueRuntimeIdentifier)]
        if len(test) == 1:
            return test[0]
        
        if par:
            if self.parent != None:
                return self.parent.checkIfSymbolExists(symbol, True)

    #alway declare inside myself
    def declareValueSymbol(self, symbol: str, value: RuntimeValue):
        #check if already symbol exists
        if self.checkIfSymbolExists(symbol, False) != None:
            raise SSException(f"SSRuntime: Identifier '{symbol}' has already been declared")
        
        s = ValueRuntimeIdentifier()
        s.setIdentifier(symbol)
        s.setValue(value)

        self.symbols.append(s)

    #alway declare inside myself
    def declareValueConstSymbol(self, symbol: str, value: RuntimeValue):
        #check if already symbol exists
        if self.checkIfSymbolExists(symbol, False) != None:
            raise SSException(f"SSRuntime: Identifier '{symbol}' has already been declared")
        
        s = ValueRuntimeIdentifier()
        s.setIdentifier(symbol)
        s.setValue(value)
        s.isConst()

        self.symbols.append(s)
    
    #override can reassign in myself or in my ancestor
    def assignValueSymbol(self, symbol: str, value: RuntimeValue):
        #check if already symbol exists
        s = self.checkIfSymbolExists(symbol, True)
        if s == None:
            raise SSException(f"SSRuntime: Identifier '{symbol}' has not been declered yet")
        
        #throw if try to override constant
        if s.const:
            raise SSException(f"SSRuntime: Identifier '{symbol}' is constant")

        #override 
        s.setValue(value)

    #return symbol value
    def peakValueSymbol(self, symbol: str) -> RuntimeValue:
        #check if already symbol exists
        s = self.checkIfSymbolExists(symbol, True)
        if s == None:
            raise SSException(f"SSRuntime: Identifier '{symbol}' has not been declered yet")
        
        return s.value