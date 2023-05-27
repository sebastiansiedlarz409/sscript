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
        last = NullNode()
        for child in node.children:
            l = self.execute(child, scope)
            if l != None:
                last = l
        return last

    def binaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        left = self.execute(node.lChild, scope)
        right = self.execute(node.rChild, scope)

        return self.expressions.binaryExpressionNode(node, left, right, scope)

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
            l = self.execute(child, functionScope)
            if l != None:
                ret = l
        return ret
    
    def returnNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        return self.execute(node.value, scope)
    
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

        while self.execute(test, loopScope).value == True:
            loopBodyScope = SSRuntimeScope()
            loopBodyScope.setParentScope(loopScope)
            for c in node.body:
                self.execute(c, loopBodyScope)
            self.execute(node.mod, loopScope)

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

        while self.execute(test, loopScope).value == True:
            loopBodyScope = SSRuntimeScope()
            loopBodyScope.setParentScope(loopScope)
            for c in node.body:
                self.execute(c, loopBodyScope)

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
        for c in node.body:
            self.execute(c, loopBodyScope)

        while self.execute(test, loopScope).value == True:
            loopBodyScope = SSRuntimeScope()
            loopBodyScope.setParentScope(loopScope)
            for c in node.body:
                self.execute(c, loopBodyScope)

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
        elif type(node).__name__ == "UnaryExpressionNode":
            return self.unaryExpressionNode(node, scope)
        elif type(node).__name__ == "VariableAssignNode":
            self.variableAssignNode(node, scope)
        elif type(node).__name__ == "DeclareVariableAssignNode":
            self.declareVariableAssignNode(node, scope)
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
