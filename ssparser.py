from tokens.tokens import *
from nodes.nodes import *

class SSParser:
    def __init__(self):
        self.tokens = []

    def iseof(self):
        return self.tokens[0].type == SSTokens.EOFToken
    
    def get(self):
        t = self.tokens[0]
        self.tokens.pop(0)
        return t
    
    def peak(self, offset = 0):
        return self.tokens[offset]

    """
    program:
        variableassignnode |
        functiondeclarationnode
    """
    def parseProgram(self, tokens):
        self.tokens = tokens

        #prepare main node
        program = ProgramNode()

        while not self.iseof():
            node = None

            #parse variable assign
            node = self.parseVariableAssign()
            if node != None:
                program.appendChild(node)
                continue
            
            #parse function declaration
            node = self.parseFunctionDeclaration()
            if node != None:
                program.appendChild(node)
                continue

            #testing only
            node = self.parserArithmeticExpression()
            if node != None:
                program.appendChild(node)
                continue

        return program
    
    """
    factor -> [IdentifierNode, NumberNode]:
        numbertoken | identifiertoken
    """
    def parseFactor(self):
        #number token
        if self.peak().type == SSTokens.NumberToken:
            n = NumberNode()
            n.setValue(self.get().value)
            return n
        
        #identifier
        if self.peak().type == SSTokens.IdentifierToken:
            n = IdentifierNode()
            n.setIdentifier(self.get().value)
            return n
        
        raise Exception(f"SSParser: Unexpected token {self.peak().value}")

    """
    term -> [BinaryOperatorNode, factor]:
        factor (binaryoperatortoken(mul, div, mod) factor)
    """
    def parseTerm(self):
        left = self.parseFactor()
        while self.peak().value in "*/%":
            operator = self.get().value #operator
            right = self.parseFactor()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    arithmeticexpression -> [BinaryOperatorNode, term]:
        term (binaryoperatortoken(add, sub) term)
    """
    def parserArithmeticExpression(self):
        left = self.parseTerm()
        while self.peak().value in "+-":
            operator = self.get().value #operator
            right = self.parseTerm()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    logicalexpression -> [UnaryOperatorNode, BinaryOperatorNode, arithmeticexpression]:
        (unaryoperatortoken) arithmeticexpression (binaryoperatortoken(logical) arithmeticexpression)
    """
    def parserLogicalExpression(self):
        pass

    """
    variableassign -> [VariableAssignNode]:
        letkwtoken identifiertoken assignoperatortoken logicalexpression
    """
    def parseVariableAssign(self):
        pass

    
    def parseFunctionDeclaration(self):
        pass