from runtime.values import *
from runtime.expressions import *
from runtime.ssscope import *
from misc.exceptions import *
from parser.nodes.conditionals import *
from parser.nodes.expressions import *
from parser.nodes.factors import *
from parser.nodes.loops import *
from parser.nodes.functions import *
from parser.nodes.nodes import *
from parser.nodes.oop import *
from parser.nodes.variables import *

from copy import deepcopy

class SSRuntime:
    def __init__(self):
        #its just helper class created only because
        #i dont want make this file billion line long
        self.expressions = Expressions()
    
    #every possible node comming from parse has dedicated metod
    def boolNode(self, node: Node) -> RuntimeValue:
        value = BoolRuntimeValue()
        value.setValue(True if node.value == "true" else False)
        return value

    def numberNode(self, node: Node) -> RuntimeValue:
        value = NumberRuntimeValue()
        
        #try to handle diffrent numeric system base on prefix
        if node.number[0:2] == "0x":
            value.setValue(float(int(node.number, 16)))
        elif node.number[0:2] == "0b":
            value.setValue(float(int(node.number, 2)))
        else:
            value.setValue(float(node.number))

        if value.value%1 == 0:
            value.value = int(value.value)
        return value
    
    def nullNode(self, node: Node) -> RuntimeValue:
        value = NullRuntimeValue()
        return value
    
    def stringNode(self, node: Node) -> RuntimeValue:
        value = StringRuntimeValue()
        value.setValue(node.value)
        return value
    
    def identifierNode(self, node: Node, scope: SSRuntimeScope):
        value = scope.peakValueSymbol(node.identifier)
        return value

    def programNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        last = NullRuntimeValue()
        for child in node.children:
            try:
                self.execute(child, scope)
            except SSRuntimeReturn as r:
                if r.value:
                    last = r.value
                break
            except SSRuntimeContinue:
                raise SSException(f"Keyword 'continue' cant be used outside loop")
            except SSRuntimeBreak:
                raise SSException(f"Keyword 'break' cant be used outside loop")
        return last

    def binaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        left = self.execute(node.lChild, scope)
        right = self.execute(node.rChild, scope)

        return self.expressions.binaryExpressionNode(node, left, right, scope)

    def prefixExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)

        if node.operator == "++":
            child.value+=1
        else:
            child.value-=1

        return child
    
    def postfixExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)
        org = deepcopy(child)

        if node.operator == "++":
            child.value+=1
        else:
            child.value-=1

        return org

    def unaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)

        return self.expressions.unaryExpressionNode(node, child, scope)
            
    def declareVariableAssignNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        if node.const:
            scope.declareValueConstSymbol(node.identifier, exp)
        else:
            scope.declareValueSymbol(node.identifier, exp)

    def variableAssignNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        scope.assignValueSymbol(node.identifier, exp)

    def logNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        if exp == None: exp = ""
        print(f"{exp}",end="")

    def loglnNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        if exp == None: exp = ""
        print(f"{exp}")

    def functionDeclarationNode(self, node: Node, scope: SSRuntimeScope):
        scope.declareFunction(node.identifier, node)

    def functionCallNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        function = scope.peakFunctionSymbol(node.identifier)

        #check if params count is ok
        if len(function.params) != len(node.params):
            raise SSException(f"SSRuntime: Function '{node.identifier}' expect {len(function.params)} params, but {len(node.params)} was given")

        functionScope = SSRuntimeScope()
        functionScope.setParentScope(scope) #create scope for function
        #eval params
        for i in range(0, len(node.params)):
            exp = self.execute(node.params[i], scope) #eval param with global scope
            functionScope.declareValueSymbol(function.params[i].identifier, exp)

        #execute body
        ret = NullRuntimeValue()
        for child in function.child:
            try:
                self.execute(child, functionScope)
            except SSRuntimeReturn as r:
                if r.value:
                    ret = r.value
        return ret
    
    def returnNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        expression = self.execute(node.value, scope)
        raise SSRuntimeReturn(expression)
    
    def forLoopNode(self, node: Node, scope: SSRuntimeScope):
        loopScope = SSRuntimeScope()
        loopScope.setParentScope(scope) #create scope for function

        self.execute(node.start, loopScope)

        #prepare test expression
        #test if node.logic && true is true
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        try:
            while self.execute(test, loopScope).value == True:
                try:
                    loopBodyScope = SSRuntimeScope()
                    loopBodyScope.setParentScope(loopScope)
                    for c in node.body:
                        self.execute(c, loopBodyScope)
                    self.execute(node.mod, loopScope)
                #special exception created to break or continue loop
                except SSRuntimeContinue:
                    self.execute(node.mod, loopScope)
                    continue
        #special exception created to break or continue loop
        except SSRuntimeBreak:
            return

    def whileLoopNode(self, node: Node, scope: SSRuntimeScope):
        loopScope = SSRuntimeScope()
        loopScope.setParentScope(scope) #create scope for function

        #prepare test expression
        #test if node.logic && true is true
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        try:
            while self.execute(test, loopScope).value == True:
                try:
                    loopBodyScope = SSRuntimeScope()
                    loopBodyScope.setParentScope(loopScope)
                    for c in node.body:
                        self.execute(c, loopBodyScope)
                #special exception created to break or continue loop
                except SSRuntimeContinue:
                    continue
        #special exception created to break or continue loop
        except SSRuntimeBreak:
            return

    def dowhileLoopNode(self, node: Node, scope: SSRuntimeScope):
        loopScope = SSRuntimeScope()
        loopScope.setParentScope(scope) #create scope for function
        
        #prepare test expression
        #test if node.logic && true is true
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        loopBodyScope = SSRuntimeScope()
        loopBodyScope.setParentScope(loopScope)
        
        try:            
            for c in node.body:
                try:
                    self.execute(c, loopBodyScope)
                except SSRuntimeContinue:
                    return

            while self.execute(test, loopScope).value == True:
                try:
                    loopBodyScope = SSRuntimeScope()
                    loopBodyScope.setParentScope(loopScope)
                    for c in node.body:
                        self.execute(c, loopBodyScope)
                #special exception created to break or continue loop
                except SSRuntimeContinue:
                    continue
        #special exception created to break or continue loop
        except SSRuntimeBreak:
            return

    def ifNode(self, node: Node, scope: SSRuntimeScope):
        #prepare test expression
        #test if node.logic && true is true
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        if self.execute(test, scope).value == True:
            ifBodyScope = SSRuntimeScope()
            ifBodyScope.setParentScope(scope)
            for c in node.body:
                self.execute(c, ifBodyScope)
        else:
            #go to elif/else if exist
            if node.child != None:
                self.execute(node.child, scope)

    def elifNode(self, node: Node, scope: SSRuntimeScope):
        #prepare test expression
        #test if node.logic && true is true
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        if self.execute(test, scope).value == True:
            elifBodyScope = SSRuntimeScope()
            elifBodyScope.setParentScope(scope)
            for c in node.body:
                self.execute(c, elifBodyScope)
        else:
            #go to elif/else if exist
            if node.child != None:
                self.execute(node.child, scope)

    def elseNode(self, node: Node, scope: SSRuntimeScope):
        elseBodyScope = SSRuntimeScope()
        elseBodyScope.setParentScope(scope)
        for c in node.body:
            self.execute(c, elseBodyScope)

    def arrayNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        array = []
        for c in node.children:
            array.append(self.execute(c, scope))

        a = ArrayRuntimeValue()
        a.setValue(array)
        return a
    
    def arrayElementOverrideNode(self, node: Node, scope: SSRuntimeScope):
        array = scope.peakValueSymbol(node.identifier)
        value = self.execute(node.child, scope)
        index = self.execute(node.index, scope)

        if index.value >= len(array.value):
            raise SSException("SSRuntime: Index out of range")

        array.value[index.value] = value
    
    def arrayReferenceNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        array = scope.peakValueSymbol(node.identifier)
        
        try:
            value =  array.value[self.execute(node.index, scope).value]
            return value
        except IndexError:
            raise SSException("SSRuntime: Array index error")
        
    def structNode(self, node: Node, scope: SSRuntimeScope):
        scope.declareType(node.name, node)

    def implNode(self, node: Node, scope: SSRuntimeScope):
        scope.declareTypeImpl(node.name, node)

    def declareFieldAssignNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        return self.execute(node.child, scope)

    def structAllocNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        #get struct node
        struct = scope.peakTypeSymbol(node.struct)

        symbol = StructRuntimeValue()
        symbol.setStruct(struct.name) #set type/struct name
        if struct.parent:
            symbol.setParent(struct.parent)

        #get and alloc all fields (multilevel inheritance)
        tempParent = struct.parent
        while tempParent:
            parent = scope.peakTypeSymbol(tempParent)
            if parent:
                for child in parent.body:
                    if type(child).__name__ == "DeclareFieldAssignNode": #check in case i add something other in future
                        symbol.allocField(child.identifier, child.const, self.execute(child, scope))
            tempParent = parent.parent

        for child in struct.body:
            if type(child).__name__ == "DeclareFieldAssignNode": #in case i add something other in future
                symbol.allocField(child.identifier, child.const, self.execute(child, scope))

        return symbol
    
    def structMemberAccess(self, node: Node, scope: SSRuntimeScope, parent = None) -> RuntimeValue:
        if type(node.member).__name__ == "StructMemberAccess": #when member is call to another object field (composite)
            obj = scope.peakValueSymbol(node.symbol) #get object
            member = self.structMemberAccess(node.member, scope, obj)
        else: #when call to own field
            if parent: #if composition dont scan global scope for object but parent object
                childObj = parent.peakField(node.symbol)
                member = childObj.peakField(node.member)
            else:
                obj = scope.peakValueSymbol(node.symbol) #get object
                member = obj.peakField(node.member)

        if not member:
            raise SSException(f"SSRuntime: Struct '{node.symbol}' has not '{node.member}' field")
        return member
    
    def structMemberWrite(self, node: Node, scope: SSRuntimeScope):
        obj = scope.peakValueSymbol(node.symbol) #get obj

        if obj.isConst(node.member):
            raise SSException(f"SSRuntime: Field '{node.member}' is constant")
        
        obj.overrideField(node.member, self.execute(node.child, scope))

    def implMemberCall(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        selfObj = scope.peakValueSymbol(node.symbol) #get struct object

        #list of methods in type (include multilevel inheritance)
        objMethods = {}

        #get all method from called type
        struct = scope.checkIfTypeExists(selfObj.struct) #get struct by struct name
        impl = struct.impl
        if impl:
            for method in impl.body:
                objMethods[method.identifier] = method
        parent = selfObj.parent
        while parent:
            struct = scope.checkIfTypeExists(parent) #get struct by struct name
            impl = struct.impl
            if impl:
                for method in impl.body:
                    if not method.identifier in objMethods.keys(): #add if note exist (child impl override base impl)
                        objMethods[method.identifier] = method
            parent = struct.parent

        #if there is 0 methods
        if len(objMethods) == 0:
            raise SSException(f"SSRuntime: Struct '{node.symbol}' type of {selfObj.struct} has not any implementation")

        #get method from above dict
        if not node.member in objMethods.keys():
            raise SSException(f"SSRuntime: Struct '{node.symbol}' type of {selfObj.struct} has not '{node.member}' method")
        method = objMethods[node.member]

        #here check params
        if len(method.params) != len(node.params):
            raise SSException(f"SSRuntime: Method '{node.member}' from {selfObj.struct} impl expect {len(method.params)} params, but {len(node.params)} was given")

        methodScope = SSRuntimeScope()
        methodScope.setParentScope(scope)
        #here eval params
        methodScope.declareValueSymbol("self", selfObj) #here insert self hidden param
        for i in range(0, len(node.params)):
            exp = self.execute(node.params[i], scope) #eval param with global scope
            methodScope.declareValueSymbol(method.params[i].identifier, exp)

        #execute body
        ret = NullRuntimeValue()
        for child in method.child:
            try:
                self.execute(child, methodScope)
            except SSRuntimeReturn as r:
                if r.value:
                    ret = r.value
        return ret

    #state machine for each type of node
    def execute(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:

        if type(node).__name__ == "NullNode":
            return self.nullNode(node)
        elif type(node).__name__ == "NumberNode":
            return self.numberNode(node)
        elif type(node).__name__ == "BoolNode":
            return self.boolNode(node)
        elif type(node).__name__ == "StringNode":
            return self.stringNode(node)
        elif type(node).__name__ == "IdentifierNode":
            return self.identifierNode(node, scope)
        elif type(node).__name__ == "BinaryExpressionNode":
            return self.binaryExpressionNode(node, scope)
        elif type(node).__name__ == "PrefixExpressionNode":
            return self.prefixExpressionNode(node, scope)
        elif type(node).__name__ == "PostfixExpressionNode":
            return self.postfixExpressionNode(node, scope)
        elif type(node).__name__ == "UnaryExpressionNode":
            return self.unaryExpressionNode(node, scope)
        elif type(node).__name__ == "VariableAssignNode":
            self.variableAssignNode(node, scope)
        elif type(node).__name__ == "DeclareVariableAssignNode":
            self.declareVariableAssignNode(node, scope)
        elif type(node).__name__ == "ArrayNode":
            return self.arrayNode(node, scope)
        elif type(node).__name__ == "ArrayReferenceNode":
            return self.arrayReferenceNode(node, scope)
        elif type(node).__name__ == "ArrayElementOverrideNode":
            self.arrayElementOverrideNode(node, scope)
        elif type(node).__name__ == "FunctionDeclarationNode":
            self.functionDeclarationNode(node, scope)
        elif type(node).__name__ == "FunctionCallNode":
            return self.functionCallNode(node, scope)
        elif type(node).__name__ == "ReturnNode":
            return self.returnNode(node, scope)
        elif type(node).__name__ == "ForLoopNode":
            self.forLoopNode(node, scope)
        elif type(node).__name__ == "WhileLoopNode":
            self.whileLoopNode(node, scope)
        elif type(node).__name__ == "DoWhileLoopNode":
            self.dowhileLoopNode(node, scope)
        elif type(node).__name__ == "ContinueNode":
            raise SSRuntimeContinue()
        elif type(node).__name__ == "BreakNode":
            raise SSRuntimeBreak()
        elif type(node).__name__ == "IfNode":
            self.ifNode(node, scope)
        elif type(node).__name__ == "ElifNode":
            self.elifNode(node, scope)
        elif type(node).__name__ == "ElseNode":
            self.elseNode(node, scope)
        elif type(node).__name__ == "LogNode":
            self.logNode(node, scope)
        elif type(node).__name__ == "LoglnNode":
            self.loglnNode(node, scope)
        elif type(node).__name__ == "StructNode":
            self.structNode(node, scope)
        elif type(node).__name__ == "ImplNode":
            self.implNode(node, scope)
        elif type(node).__name__ == "StructAllocNode":
            return self.structAllocNode(node, scope)
        elif type(node).__name__ == "DeclareFieldAssignNode":
            return self.declareFieldAssignNode(node, scope)
        elif type(node).__name__ == "StructMemberAccess":
            return self.structMemberAccess(node, scope)
        elif type(node).__name__ == "StructMemberWrite":
            self.structMemberWrite(node, scope)
        elif type(node).__name__ == "ImplMemberCall":
            return self.implMemberCall(node, scope)
        elif type(node).__name__ == "ProgramNode":
            return self.programNode(node, scope)
        elif type(node).__name__ == "NoneType":
            return None
        else:
            raise SSException(f"SSRuntime: Failed to evaluate node {type(node).__name__}")
