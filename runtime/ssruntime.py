#runtime values
from runtime.values import *

#expression helper class
from runtime.expressions import *

#scope stuff
from runtime.ssscope import *

#exceptions
from misc.exceptions import *

#parser nodes
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
    
    def boolNode(self, node: Node) -> RuntimeValue:
        return BoolRuntimeValue(True if node.value == "true" else False)

    def numberNode(self, node: Node) -> RuntimeValue:
        value = 0
        
        #try to handle diffrent numeric system base on prefix
        if node.number[0:2] == "0x":
            value = float(int(node.number, 16))
        elif node.number[0:2] == "0b":
            value = float(int(node.number, 2))
        else:
            value = float(node.number)

        #check if value is integer
        #if so cut decimal part of it
        if value%1 == 0:
            value = int(value)
        return NumberRuntimeValue(value)
    
    def nullNode(self, node: Node) -> RuntimeValue:
        return NullRuntimeValue()
    
    def stringNode(self, node: Node) -> RuntimeValue:
        return StringRuntimeValue(node.value)
    
    def identifierNode(self, node: Node, scope: SSRuntimeScope):
        return scope.getVariableValue(node.identifier).value

    def programNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        #return value from whole program
        #by default its null
        last = NullRuntimeValue()

        #eval each child
        #catch sepcial exceptions for return, break and continue
        for child in node.children:
            try:
                self.execute(child, scope)
            except SSRuntimeReturn as result:
                if result.value:
                    last = result.value
                break
            except SSRuntimeContinue:
                raise SSException(f"SSRuntime: Keyword 'continue' cant be used outside loop")
            except SSRuntimeBreak:
                raise SSException(f"SSRuntime: Keyword 'break' cant be used outside loop")
            
        return last

    def binaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        left = self.execute(node.lChild, scope)
        right = self.execute(node.rChild, scope)

        return self.expressions.binaryExpressionNode(node, left, right, scope)

    def prefixExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)

        if type(child) == NumberRuntimeValue:
            if node.operator == "++":
                child.value+=1
            else:
                child.value-=1
        else:
            raise SSException(f"SSRuntime: Cannot use operator '{node.operator}' with value of type '{type(child)}'")

        return child
    
    def postfixExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)
        org = deepcopy(child)

        if type(child) == NumberRuntimeValue:
            if node.operator == "++":
                child.value+=1
            else:
                child.value-=1
        else:
            raise SSException(f"SSRuntime: Cannot use operator '{node.operator}' with value of type '{type(child)}'")

        return org

    def unaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)

        return self.expressions.unaryExpressionNode(node, child, scope)
            
    def declareVariableAssignNode(self, node: Node, scope: SSRuntimeScope):
        #get value for variable
        exp = self.execute(node.child, scope)

        #declare
        if node.const:
            scope.declareConstant(node.identifier, exp)
        else:
            scope.declareVariable(node.identifier, exp)

    def variableAssignNode(self, node: Node, scope: SSRuntimeScope):
        #get value for variable
        exp = self.execute(node.child, scope)

        #override value
        scope.assignVariable(node.identifier, exp)

    def logNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        if exp == None: exp = ""
        print(f"{exp}",end="")

    def loglnNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
        if exp == None: exp = ""
        print(f"{exp}")

    def functionDeclarationNode(self, node: Node, scope: SSRuntimeScope):
        scope.declareFunction(node.identifier, node.params, node.child)

    def functionCallNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        #get function from scope
        function = scope.getFunction(node.identifier)

        #check if params count is ok
        if len(function.params) != len(node.params):
            raise SSException(f"SSRuntime: Function '{node.identifier}' expect {len(function.params)} params, but {len(node.params)} was given")

        #create scope for function
        functionScope = SSRuntimeScope(scope)

        #eval params using base scope
        #declare them in function scope
        for i in range(0, len(node.params)):
            exp = self.execute(node.params[i], scope) #eval param with global scope
            functionScope.declareVariable(function.params[i].identifier, exp)

        #execute body
        ret = NullRuntimeValue()
        for child in function.body:
            try:
                self.execute(child, functionScope)
            except SSRuntimeReturn as result:
                if result.value:
                    ret = result.value
        return ret
    
    def returnNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        expression = self.execute(node.value, scope)
        raise SSRuntimeReturn(expression)
    
    def forLoopNode(self, node: Node, scope: SSRuntimeScope):
        #create scope for loop header
        loopScope = SSRuntimeScope(scope)

        #eval loop start expression e.g let i = 0
        self.execute(node.start, loopScope)

        #prepare test expression
        #test if node.logic && true is true
        #ist important because node.logic may not be type of BoolRuntimeExpression
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        try:
            while self.execute(test, loopScope).value == True:
                try:
                    #create scope for this iteration of body items
                    loopBodyScope = SSRuntimeScope(loopScope)
                    #eval boyd
                    for c in node.body:
                        self.execute(c, loopBodyScope)
                    #eval mod expression e.g i++
                    self.execute(node.mod, loopScope)
                #special exception created to break or continue loop
                except SSRuntimeContinue:
                    #eval mod expression e.g i++
                    #to avoid infinity loop
                    self.execute(node.mod, loopScope)
                    continue
        #special exception created to break or continue loop
        except SSRuntimeBreak:
            return

    def whileLoopNode(self, node: Node, scope: SSRuntimeScope):
        #create scope for loop header
        loopScope = SSRuntimeScope(scope)

        #prepare test expression
        #test if node.logic && true is true
        #ist important because node.logic may not be type of BoolRuntimeExpression
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        try:
            while self.execute(test, loopScope).value == True:
                try:
                    #create scope for this iteration of body items
                    loopBodyScope = SSRuntimeScope(loopScope)
                    #eval body
                    for c in node.body:
                        self.execute(c, loopBodyScope)
                #special exception created to break or continue loop
                except SSRuntimeContinue:
                    continue
        #special exception created to break or continue loop
        except SSRuntimeBreak:
            return

    def dowhileLoopNode(self, node: Node, scope: SSRuntimeScope):
        #create scope for loop header
        loopScope = SSRuntimeScope(scope)
        
        #prepare test expression
        #test if node.logic && true is true
        #ist important because node.logic may not be type of BoolRuntimeExpression
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)
        
        #create scope for first iteration
        loopBodyScope = SSRuntimeScope(loopScope)
        
        try:            
            #execute first iteration always
            for c in node.body:
                try:
                    self.execute(c, loopBodyScope)
                except SSRuntimeContinue:
                    return

            #execute next iterations
            while self.execute(test, loopScope).value == True:
                try:
                    #create scope for iterations
                    loopBodyScope = SSRuntimeScope(loopScope)
                    #eval body
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
        #ist important because node.logic may not be type of BoolRuntimeExpression
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        if self.execute(test, scope).value == True:
            #create scope for if
            ifBodyScope = SSRuntimeScope(scope)
            for c in node.body:
                self.execute(c, ifBodyScope)
        else:
            #go to elif/else if exist
            if node.child != None:
                self.execute(node.child, scope)

    def elifNode(self, node: Node, scope: SSRuntimeScope):
        #prepare test expression
        #test if node.logic && true is true
        #ist important because node.logic may not be type of BoolRuntimeExpression
        true = BoolNode()
        true.setValue("true")
        test = BinaryExpressionNode()
        test.setOperator("and")
        test.setLChild(true)
        test.setRChild(node.logic)

        if self.execute(test, scope).value == True:
            #create scope for body
            elifBodyScope = SSRuntimeScope(scope)
            for c in node.body:
                self.execute(c, elifBodyScope)
        else:
            #go to elif/else if exist
            if node.child != None:
                self.execute(node.child, scope)

    def elseNode(self, node: Node, scope: SSRuntimeScope):
        #create scope for body
        elseBodyScope = SSRuntimeScope(scope)
        for c in node.body:
            self.execute(c, elseBodyScope)

    def arrayNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        array = []
        for c in node.children:
            array.append(self.execute(c, scope))

        return ArrayRuntimeValue(array)
    
    def arrayElementOverrideNode(self, node: Node, scope: SSRuntimeScope):
        array = self.execute(node.array, scope)

        value = self.execute(node.child, scope)
        index = self.execute(node.index, scope)

        if index.value >= len(array.value):
            raise SSException("SSRuntime: Array index out of range")

        array.value[index.value] = value
    
    def arrayReferenceNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        array = self.execute(node.array, scope)
        
        index = self.execute(node.index, scope)

        if index.value >= len(array.value):
            raise SSException("SSRuntime: Array index out of range")

        return array.value[index.value]
        
    def structNode(self, node: Node, scope: SSRuntimeScope):
        scope.declareStruct(node.name, node.parent, node.body)

    def implNode(self, node: Node, scope: SSRuntimeScope):
        scope.declareStructImpl(node.name, node.parent, node.body)

    def declareFieldAssignNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        return self.execute(node.child, scope)

    def structAllocNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        #get struct declaration
        struct = scope.peakTypeSymbol(node.struct)

        #init object with struct data
        symbol = None
        if struct.parent:
            symbol = StructRuntimeValue(struct.name, struct.parent)
        else:
            symbol = StructRuntimeValue(struct.name)

        for field in struct.fields:
            if type(field).__name__ == "DeclareFieldAssignNode": #in case i add something other in future
                symbol.createField(field.identifier, field.const, self.execute(field, scope))

        return symbol
    
    def structMemberAccess(self, node: Node, scope: SSRuntimeScope, parent: RuntimeValue = None) -> RuntimeValue:
        if parent == None:
            parent = self.execute(node.parent, scope)
        
        if type(parent) != StructRuntimeValue:
            raise SSException(f"SSRuntime: '{node.parent}' is not an object")
        
        print(node.child)
        if node.child:
            member = self.execute(node.child.parent, scope)
            print(member)
    
    def structMemberWrite(self, node: Node, scope: SSRuntimeScope, parent = None):
        if parent: #composition
            obj = parent.peakField(node.symbol)
        else:
            obj = scope.getVariableValue(node.symbol).value #get obj

        if type(node.member).__name__ == "StructMemberWrite": #when member is call to another object field (composite)
            self.structMemberWrite(node.member, scope, obj)
            return
        elif type(node.member).__name__ == "ArrayElementOverrideNode":
            member = obj.peakField(node.member.identifier)
            self.arrayElementOverrideNode(node.member, scope, member)
            return 
        
        if obj.isConst(node.member):
            raise SSException(f"SSRuntime: Field '{node.member}' is constant")
        
        obj.overrideField(node.member, self.execute(node.child, scope))

    def implMemberCall(self, node: Node, scope: SSRuntimeScope, parent: RuntimeValue) -> RuntimeValue:
        symbol = None #for errors
        methodToCall = node.symbol
        methodToCallParams = node.params

        #list of methods in type (include multilevel inheritance)
        objMethods = {}

        #get all method from called type
        struct = scope.checkIfTypeExists(parent.structName) #get struct by struct name
        impl = struct.impl
        if impl:
            for method in struct.methods:
                objMethods[method.identifier] = method

        #if there is 0 methods
        if len(objMethods) == 0:
            raise SSException(f"SSRuntime: Struct '{symbol}' type of {parent.structName} has not any implementation")

        #get method from above dict
        if not methodToCall in objMethods.keys():
            raise SSException(f"SSRuntime: Struct '{symbol}' type of {parent.structName} has not '{methodToCall}' method")
        method = objMethods[methodToCall]

        #here check params
        if len(method.params) != len(methodToCallParams):
            raise SSException(f"SSRuntime: Method '{node.member}' from {parent.structName} impl expect {len(methodToCallParams)} params, but {len(node.params)} was given")

        methodScope = SSRuntimeScope(scope)

        #here eval params
        methodScope.declareVariable("self", parent) #here insert self hidden param
        for i in range(0, len(methodToCallParams)):
            exp = self.execute(methodToCallParams[i], scope) #eval param with global scope
            methodScope.declareVariable(method.params[i].identifier, exp)

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

        if type(node) == NullNode:
            return self.nullNode(node)
        elif type(node) == NumberNode:
            return self.numberNode(node)
        elif type(node) == BoolNode:
            return self.boolNode(node)
        elif type(node) == StringNode:
            return self.stringNode(node)
        elif type(node) == IdentifierNode:
            return self.identifierNode(node, scope)
        elif type(node) == BinaryExpressionNode:
            return self.binaryExpressionNode(node, scope)
        elif type(node) == PrefixExpressionNode:
            return self.prefixExpressionNode(node, scope)
        elif type(node) == PostfixExpressionNode:
            return self.postfixExpressionNode(node, scope)
        elif type(node) == UnaryExpressionNode:
            return self.unaryExpressionNode(node, scope)
        elif type(node) == VariableAssignNode:
            self.variableAssignNode(node, scope)
        elif type(node) == DeclareVariableAssignNode:
            self.declareVariableAssignNode(node, scope)
        elif type(node) == ArrayNode:
            return self.arrayNode(node, scope)
        elif type(node) == ArrayReferenceNode:
            return self.arrayReferenceNode(node, scope)
        elif type(node) == ArrayElementOverrideNode:
            self.arrayElementOverrideNode(node, scope)
        elif type(node) == FunctionDeclarationNode:
            self.functionDeclarationNode(node, scope)
        elif type(node) == FunctionCallNode:
            return self.functionCallNode(node, scope)
        elif type(node) == ReturnNode:
            return self.returnNode(node, scope)
        elif type(node) == ForLoopNode:
            self.forLoopNode(node, scope)
        elif type(node) == WhileLoopNode:
            self.whileLoopNode(node, scope)
        elif type(node) == DoWhileLoopNode:
            self.dowhileLoopNode(node, scope)
        elif type(node) == ContinueNode:
            raise SSRuntimeContinue()
        elif type(node) == BreakNode:
            raise SSRuntimeBreak()
        elif type(node) == IfNode:
            self.ifNode(node, scope)
        elif type(node) == ElifNode:
            self.elifNode(node, scope)
        elif type(node) == ElseNode:
            self.elseNode(node, scope)
        elif type(node) == LogNode:
            self.logNode(node, scope)
        elif type(node) == LoglnNode:
            self.loglnNode(node, scope)
        elif type(node) == StructNode:
            self.structNode(node, scope)
        elif type(node) == ImplNode:
            self.implNode(node, scope)
        elif type(node) == StructAllocNode:
            return self.structAllocNode(node, scope)
        elif type(node) == DeclareFieldAssignNode:
            return self.declareFieldAssignNode(node, scope)
        elif type(node) == StructMemberAccess:
            return self.structMemberAccess(node, scope)
        elif type(node) == StructMemberWrite:
            self.structMemberWrite(node, scope)
        #elif type(node) == ImplMemberCall:
        #    return self.implMemberCall(node, scope)
        elif type(node) == ProgramNode:
            return self.programNode(node, scope)
        elif node == None:
            return None
        else:
            raise SSException(f"SSRuntime: Failed to evaluate node {type(node).__name__}")
