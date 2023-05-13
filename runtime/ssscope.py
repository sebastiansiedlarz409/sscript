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
        self.value: RuntimeValue = None
    
    def setValue(self, value: RuntimeValue):
        self.value = value

    def __repr__(self) -> str:
        ret = f"{self.identifier} = () => {self.value}"
        return ret
    
#scope
class SSRuntimeScope:
    def __init__(self): 
        #parent in type Runtimescope
        self.parent = None
        self.symbols: list[RuntimeIdentifier] = []

    def setParentScope(self, parent):
        self.parent = parent

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
        
        return None
    
    #alway declare inside myself
    def declareFunction(self, symbol: str, value: RuntimeValue):
        #check if already symbol exists
        if self.checkIfFunctionExists(symbol, False) != None:
            raise SSException(f"SSRuntime: Function '{symbol}' has already been declared")
        
        s = FunctionRuntimeIdentifier()
        s.setIdentifier(symbol)
        s.setValue(value)

        self.symbols.append(s)

    #return function value
    def peakFunctionSymbol(self, symbol: str) -> RuntimeValue:
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
        
        return None

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