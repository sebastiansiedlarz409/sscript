from parser.nodes import *
from runtime.values import *
from runtime.ssscope import *
from misc.exceptions import *

class SSRuntime:
    def __init__(self):
        pass

    def evalBinaryExpressionArithmetic(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = 0

        try:
            if operator == "+":
                result = lvalue.value + rvalue.value
            elif operator == "-":
                result = lvalue.value - rvalue.value
            elif operator == "*":
                result = lvalue.value * rvalue.value
            elif operator == "/":
                result = lvalue.value / rvalue.value
            elif operator == "%":
                result = lvalue.value % rvalue.value
            elif operator == "|":
                result = int(lvalue.value) | int(rvalue.value)
            elif operator == "&":
                result = int(lvalue.value) & int(rvalue.value)
            elif operator == "^":
                result = int(lvalue.value) ^ int(rvalue.value)
            elif operator == "<":
                result = int(lvalue.value) << int(rvalue.value)
            elif operator == ">":
                result = int(lvalue.value) >> int(rvalue.value)
        except TypeError:
            raise SSException(f"SSRuntime: Cant {operator} this type of values")

        if lvalue.type == ValueTypes.Number:
            ret = NumberRuntimeValue()
            ret.setValue(result)
            return ret
        elif lvalue.type == ValueTypes.String:
            ret = StringRuntimeValue()
            ret.setValue(str(result))
            return ret
        else:
            raise SSException(f"SSRuntime: Cant handle binary expression")
            

    def evalBinaryExpressionLogical(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = False
        
        try:
            if operator == "or":
                result = lvalue.value or rvalue.value
            elif operator == "and":
                result = lvalue.value and rvalue.value
            else:
                raise SSException(f"SSRuntime: Bool expression not support this operator {operator}")
        except TypeError:
            raise SSException(f"SSRuntime: Cant {operator} this type of values")

        ret = BoolRuntimeValue()
        ret.setValue(result)
        return ret

    def evalBinaryExpressionComparasion(self, lvalue: RuntimeValue, rvalue: RuntimeValue, operator: str) -> RuntimeValue:
        result = False

        try:
            if operator == "eq":
                result = lvalue.value == rvalue.value
            elif operator == "neq":
                result = lvalue.value != rvalue.value
            elif operator == "gr":
                result = lvalue.value > rvalue.value
            elif operator == "ge":
                result = lvalue.value >= rvalue.value
            elif operator == "ls":
                result = lvalue.value < rvalue.value
            elif operator == "le":
                result = lvalue.value <= rvalue.value
            else:
                raise SSException(f"SSRuntime: Bool expression not support this operator {operator}")
        except TypeError:
            raise SSException(f"SSRuntime: Cant {operator} this type of values")

        ret = BoolRuntimeValue()
        ret.setValue(result)
        return ret
    
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

        #not logical operator
        if node.operator in "+-*/%&|<>^":
            #NUMBER <> NUMBER
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionArithmetic(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                r = NumberRuntimeValue()
                r.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #NUMBER <> STRING
            elif left.type == ValueTypes.Number and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue(str(left.value))
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #BOOL <> BOOL
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                l = NumberRuntimeValue()
                l.setValue(1 if left.value else 0)
                r = NumberRuntimeValue()
                r.setValue(1 if left.value else 0)
                return self.evalBinaryExpressionArithmetic(l, r, node.operator)
            
            #BOOL <> STRING
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue("true" if left.value else "false")
                return self.evalBinaryExpressionArithmetic(l, right, node.operator)
            
            #STRING <> NUMBER
            elif left.type == ValueTypes.String and right.type == ValueTypes.Number:
                r = StringRuntimeValue()
                r.setValue(str(right.value))
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #STRING <> BOOL
            elif left.type == ValueTypes.String and right.type == ValueTypes.Bool:
                r = StringRuntimeValue()
                r.setValue("true" if right.value else "false")
                return self.evalBinaryExpressionArithmetic(left, r, node.operator)
            
            #STRING <> STRING
            elif left.type == ValueTypes.String and right.type == ValueTypes.String:
                return self.evalBinaryExpressionArithmetic(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")
            
        #comparasion operators
        elif node.operator in ["eq", "neq", "gr", "ge", "ls", "le"]:
            #NUMBER <> NUMBER
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                r = NumberRuntimeValue()
                r.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #NUMBER <> STRING
            elif left.type == ValueTypes.Number and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue(str(left.value))
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #BOOL <> BOOL
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            #BOOL <> STRING
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue("true" if left.value else "false")
                return self.evalBinaryExpressionComparasion(l, right, node.operator)
            
            #STRING <> NUMBER
            elif left.type == ValueTypes.String and right.type == ValueTypes.Number:
                r = StringRuntimeValue()
                r.setValue(str(right.value))
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #STRING <> BOOL
            elif left.type == ValueTypes.String and right.type == ValueTypes.Bool:
                r = StringRuntimeValue()
                r.setValue("true" if right.value else "false")
                return self.evalBinaryExpressionComparasion(left, r, node.operator)
            
            #STRING <> STRING
            elif left.type == ValueTypes.String and right.type == ValueTypes.String:
                return self.evalBinaryExpressionComparasion(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")

        #logical operator
        else:
            #NUMBER <> NUMBER
            if left.type == ValueTypes.Number and right.type == ValueTypes.Number:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #NUMBER <> BOOL
            elif left.type == ValueTypes.Number and right.type == ValueTypes.Bool:
                r = NumberRuntimeValue()
                r.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionLogical(left, r, node.operator)
            
            #NUMBER <> STRING
            elif left.type == ValueTypes.Number and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue(str(left.value))
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #BOOL <> NUMBER
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Number:
                l = NumberRuntimeValue()
                l.setValue(1 if right.value else 0)
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #BOOL <> BOOL
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.Bool:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            #BOOL <> STRING
            elif left.type == ValueTypes.Bool and right.type == ValueTypes.String:
                l = StringRuntimeValue()
                l.setValue("true" if left.value else "false")
                return self.evalBinaryExpressionLogical(l, right, node.operator)
            
            #STRING <> NUMBER
            elif left.type == ValueTypes.String and right.type == ValueTypes.Number:
                r = StringRuntimeValue()
                r.setValue(str(right.value))
                return self.evalBinaryExpressionLogical(left, r, node.operator)
            
            #STRING <> BOOL
            elif left.type == ValueTypes.String and right.type == ValueTypes.Bool:
                r = StringRuntimeValue()
                r.setValue("true" if right.value else "false")
                return self.evalBinaryExpressionLogical(left, r, node.operator)
            
            #STRING <> STRING
            elif left.type == ValueTypes.String and right.type == ValueTypes.String:
                return self.evalBinaryExpressionLogical(left, right, node.operator)
            
            else:
                raise SSException(f"SSRuntime: Cant evaluate binary node when lvalue or rvalue is 'null'")

    def unaryExpressionNode(self, node: Node, scope: SSRuntimeScope) -> RuntimeValue:
        child = self.execute(node.child, scope)

        if node.operator == "not":
            if child.type == ValueTypes.Number:
                r = BoolRuntimeValue()
                r.setValue(True if child.value == 0 else False)
                return r
            elif child.type == ValueTypes.Bool:
                r = BoolRuntimeValue()
                r.setValue(not child.value)
                return r
            elif child.type == ValueTypes.String:
                r = BoolRuntimeValue()
                r.setValue(False if len(child.value) > 0 else True)
                return r
            
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
        print(f"{exp}",end="")

    def loglnNode(self, node: Node, scope: SSRuntimeScope):
        exp = self.execute(node.child, scope)
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
        elif type(node).__name__ == "LogNode":
            self.logNode(node, scope)
        elif type(node).__name__ == "LoglnNode":
            self.loglnNode(node, scope)
        elif type(node).__name__ == "ProgramNode":
            return self.programNode(node, scope)
        else:
            raise SSException(f"SSRuntime: Failed to evaluate node {type(node).__name__}")
