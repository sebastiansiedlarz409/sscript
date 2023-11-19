#runtime values for struct and variable allocation
from runtime.values import *

#exceptions
from misc.exceptions import *

#parser node
from parser.nodes.oop import StructNode

class ScopeVariable:
    def __init__(self, name: str = None, value: RuntimeValue = None, isConst: bool = False):
        self.name: str = name
        self.isConst: bool = isConst
        self.value: RuntimeValue = value

    def setConst(self):
        self.isConst = True
    
class ScopeFunction:
    def __init__(self, name: str = None, params: list[Node] = [], body: list[Node] = []):
        self.name: str = name
        self.params: list[Node] = params
        self.body: list[Node] = body

class ScopeType:
    def __init__(self, name: str = None, parentName: str = None, fields: list[Node] = [], methods: list[Node] = []):
        self.name: str = name
        self.parent: str = parentName #its only for impl validation purpose
        self.fields: list[Node] = fields
        self.methods: list[Node] = fields
        self.impl: bool = False
    
#scope
class SSRuntimeScope:
    def __init__(self, parent = None):
        self.parentScope = parent #parent scope
        self.variables: list[ScopeVariable] = []
        self.functions: list[ScopeFunction] = []
        self.types: list[ScopeType] = []

    #VARIABLE SECTION

    #check if variable exists
    #check self and higher level scopes if checkParent is true
    #if exist returns it
    #otherwise returns None
    def checkIfVariableExist(self, name: str, checkParent: bool) -> ScopeVariable:
        test = [x for x in self.variables if x.name == name]

        #there should be allways one var with given name but lets check it
        if len(test) == 1:
            return test[0]
        elif len(test) > 1:
            #this should never happend
            raise SSException(f"SSRuntime: Identifier '{name}' found multiple times")
        
        #check parent scope
        if checkParent:
            if self.parentScope:
                return self.parentScope.checkIfVariableExist(name, True)

    #alway declare inside myself
    def declareVariable(self, name: str, value: RuntimeValue):
        #check if already symbol exists
        if self.checkIfVariableExist(name, False) != None:
            raise SSException(f"SSRuntime: Identifier '{name}' has already been declared")
        
        var = ScopeVariable(name, value)

        self.variables.append(var)

    #alway declare inside myself
    def declareConstant(self, name: str, value: RuntimeValue):
        #check if already symbol exists
        if self.checkIfVariableExist(name, False) != None:
            raise SSException(f"SSRuntime: Identifier '{name}' has already been declared")
        
        var = ScopeVariable(name, value)

        self.variables.append(var)
    
    #override can reassign in myself or in my ancestor
    def assignVariable(self, name: str, value: RuntimeValue):
        #check if variable exist
        var = self.checkIfVariableExist(name, True)
        if var == None:
            raise SSException(f"SSRuntime: Identifier '{name}' has not been declered yet")
        
        #throw if try to override constant
        if var.isConst:
            raise SSException(f"SSRuntime: Identifier '{name}' is constant")

        #override 
        var.value = value

    #return symbol value
    #it checks all scope above as well
    def getVariableValue(self, name: str) -> ScopeVariable:
        #check if already symbol exists
        var = self.checkIfVariableExist(name, True)
        if var == None:
            raise SSException(f"SSRuntime: Identifier '{name}' has not been declered yet")
        
        return var
    
    #VARIABLE SECTION ENDS

    #FUNCTION SECTION

    #check if function exists
    #check self and higher level scopes if checkParent is true
    #if exist returns it
    #otherwise returns None
    def checkIfFunctionExists(self, name: str, checkParent: bool) -> ScopeFunction:
        test = [x for x in self.functions if x.name == name]

        #there should be always 1 but check
        if len(test) == 1:
            return test[0]
        elif len(test) > 1:
            raise SSException(f"SSRuntime: Function '{name}' found multiple times")
        
        if checkParent:
            if self.parent != None:
                return self.parent.checkIfFunctionExists(name, True)
    
    #alway declare inside myself
    def declareFunction(self, name: str, params: list[Node], body: list[Node]):
        #check if already symbol exists
        if self.checkIfFunctionExists(name, False) != None:
            raise SSException(f"SSRuntime: Function '{name}' has already been declared")
        
        func = ScopeFunction(name, params, body)

        self.functions.append(func)

    #return function value
    def getFunction(self, name: str) -> ScopeFunction:
        #check if already symbol exists
        func = self.checkIfFunctionExists(name, True)
        if func == None:
            raise SSException(f"SSRuntime: Function '{name}' has not been declered yet")
        
        return func

    #FUNCTION SECTION ENDS

    #STRUCT AND IMPL SECTION

    def getRootScope(self):
        #find root scope
        scope = self
        while scope.parentScope:
            scope = scope.parentScope

        return scope

    def checkIfTypeExists(self, name: str) -> ScopeType:
        root = self.getRootScope()        
        test = [x for x in root.types if x.name == name.upper()]

        #there always should be 1 by check
        if len(test) == 1:
            return test[0]
        elif len(test) > 1:
            raise SSException(f"SSRuntime: Type '{name}' found multiple times")
        
    #alawys declare in the root scope
    def declareStruct(self, name: str, parent: str = None, fields: list[Node] = []):
        if self.checkIfTypeExists(name) != None:
            raise SSException(f"SSRuntime: Type '{name}' has already been declared")
        
        if parent:
            if self.checkIfTypeExists(parent) == None:
                raise SSException(f"SSRuntime: Parent type '{parent}' has not been declared yet")
        
        #get parent
        if parent:
            parent = self.peakTypeSymbol(parent)

        #get root scope        
        scope = self.getRootScope()

        methods = []
        if parent:
            fields += parent.fields
            methods += parent.methods
        
        t = ScopeType(name, parent, fields, methods)

        scope.types.append(t)

    #alawys declare in the root scope
    def declareStructImpl(self, name: str, parent: str = None, methods: list[Node] = []):
        struct = self.checkIfTypeExists(name)

        #if struct not exist declare
        if struct == None:
            self.declareStruct(name, parent, [])
            struct = self.peakTypeSymbol(name)

        #if already has implementation throw
        if struct.impl:
            raise SSException(f"SSRuntime: Type '{name}' has already been implemented")
        
        if parent:
            if self.checkIfTypeExists(parent) == None:
                raise SSException(f"SSRuntime: Parent type '{parent}' has not been declared yet")
            else:
                if parent != struct.parent:
                    raise SSException(f"SSRuntime: Parent has to be the same for struct and implementation")

        struct.impl = True #mark as struct with impl

        if parent:
            parent = self.peakTypeSymbol(parent)
            struct.methods += parent.methods
        struct.methods += methods #IMPORTANT OTDER IN CONTEXT OF OVERRIDE
    
    #return struct node from main scope
    def peakTypeSymbol(self, name: str) -> ScopeType:
        t = self.checkIfTypeExists(name)
        if not t:
            raise SSException(f"SSRuntime: Struct '{name}' has not been declered yet")
        return t

    #STRUCT AND IMPL SECTION ENDS