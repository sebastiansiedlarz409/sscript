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
        self.expressions = Expressions()
    
    def boolNode(self, node: Node) -> RuntimeValue:
        value = BoolRuntimeValue()
        value.setValue(True if node.value == "true" else False)
        return value

    def numberNode(self, node: Node) -> RuntimeValue:
        value = NumberRuntimeValue()
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
        f = FunctionRuntimeValue()
        f.setParams(node.params)
        f.setBody(node.child)

        scope.declareFunction(node.identifier, f)

    def functionCallNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        function = scope.peakFunctionSymbol(node.identifier)

        if len(function.params) != len(node.params):
            raise SSException(f"SSRuntime: Function '{node.identifier}' expect {len(function.params)} params, but {len(node.params)} was given")

        functionScope = SSRuntimeScope()
        functionScope.setParentScope(scope) #create scope for function
        for i in range(0, len(node.params)):
            exp = self.execute(node.params[i], scope) #eval param with global scope
            functionScope.declareValueSymbol(function.params[i].identifier, exp)

        ret = NullRuntimeValue()
        for child in function.body:
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
                except SSRuntimeContinue:
                    self.execute(node.mod, loopScope)
                    continue
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
                except SSRuntimeContinue:
                    continue
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
                except SSRuntimeContinue:
                    continue
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
        elif type(node).__name__ == "ProgramNode":
            return self.programNode(node, scope)
        elif type(node).__name__ == "NoneType":
            return None
        else:
            raise SSException(f"SSRuntime: Failed to evaluate node {type(node).__name__}")
