from lexer.tokens import *
from parser.nodes import *
from misc.exceptions import *

class SSParser:
    def __init__(self):
        self.tokens = []

    def iseof(self) -> bool:
        return self.tokens[0].type == SSTokens.EOFToken
    
    def get(self) -> str:
        t = self.tokens[0]
        self.tokens.pop(0)
        return t
    
    def peak(self, offset: int = 0) -> str:
        return self.tokens[offset]

    """
    program -> ProgramNode:
        declarevariableassignnode
        variableassignnode |
        functiondeclarationnode |
        loglnnode |
        lognode
    """
    def parseProgram(self, tokens: list[SSToken]) -> Node:
        self.tokens = tokens

        #prepare main node
        program = ProgramNode()

        while not self.iseof():
            node = None

            #parse declaration variable assign
            node = self.parseVariableDeclarationAssign()
            if node != None:
                program.appendChild(node)
                continue
            
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
            node = self.parseLog()
            if node != None:
                program.appendChild(node)
                continue
            node = self.parseLogln()
            if node != None:
                program.appendChild(node)
                continue

        return program
    
    """
    factor -> [IdentifierNode, NumberNode, arithmeticexpression]:
        numbertoken | identifiertoken
    """
    def parseFactor(self) -> Node:
        #check for exp inside paren
        if self.peak().type == SSTokens.LParenToken:
            self.get()
            n = self.parseUnaryExpression()
            if self.get().type != SSTokens.RParenToken:
                raise SSException(f"SSParser: Expected RParenToken")
            return n

        #string
        if self.peak().type == SSTokens.QuoteToken:
            self.get()
            n = StringNode()
            n.setValue(self.get().value)
            if self.get().type != SSTokens.QuoteToken:
                raise SSException(f"SSParser: Expected QuoteToken")
            return n

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
        
        #null
        if self.peak().type == SSTokens.NullKwToken:
            n = NullNode()
            self.get().value
            return n
        
        #true false
        if self.peak().type == SSTokens.TrueKwToken or self.peak().type == SSTokens.FalseKwToken:
            n = BoolNode()
            n.setValue(self.get().value)
            return n
        
        raise SSException(f"SSParser: Unexpected token {self.peak().value}")

    """
    term -> [BinaryOperatorNode, factor]:
        factor (binaryoperatortoken(mul, div, mod) factor)
    """
    def parseMulArithmeticExpression(self) -> Node:
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
    arithmeticexpression -> [BinaryOperatorNode, mularithmeticexpression]:
        mularithmeticexpression (binaryoperatortoken(add, sub) mularithmeticexpression)
    """
    def parseAddArithmeticExpression(self) -> Node:
        left = self.parseMulArithmeticExpression()
        while self.peak().value in "+-":
            operator = self.get().value #operator
            right = self.parseMulArithmeticExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    comparasionexpression -> [BinaryOperatorNode, addarithmeticexpression]:
        addarithmeticexpression (binaryoperatortoken(comparasion) addarithmeticexpression)
    """
    def parseComparasionExpression(self) -> Node:
        left = self.parseAddArithmeticExpression()
        while self.peak().value in ["eq", "neq", "gr", "ge", "ls", "le"]:
            operator = self.get().value #operator
            right = self.parseAddArithmeticExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    bitewiseexpression -> [BinaryOperatorNode, camparasionexpression]:
        comparasionexpression (binaryoperatortoken(comparasion) comparasionexpression)
    """
    def parseBitewiseExpression(self) -> Node:
        left = self.parseComparasionExpression()
        while self.peak().value in "|&<>^":
            operator = self.get().value #operator
            right = self.parseComparasionExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left

    """
    logicalexpression -> [BinaryOperatorNode, bitewiseexpression]:
        bitewisexpression (binaryoperatortoken(comparasion) bitewisexpression)
    """
    def parseLogicalExpression(self) -> Node:
        left = self.parseBitewiseExpression()
        while self.peak().value in ["and", "or"]:
            operator = self.get().value #operator
            right = self.parseBitewiseExpression()
            temp = BinaryExpressionNode()
            temp.lChild = left
            temp.rChild = right
            temp.operator = operator
            left = temp

        return left
    
    """
    unaryexpression -> [UnaryExpressionNode, logicalexpression]
        (unaryoperatortoken) logicalexpression
    """
    def parseUnaryExpression(self) -> Node:
        if self.peak().type == SSTokens.UnaryOperatorToken:
            u = UnaryExpressionNode()
            u.setOperator(self.get().value)

            child = self.parseLogicalExpression()
            
            u.setChild(child)
            return u
        
        return self.parseLogicalExpression()

    """
    variabledeclarationassign -> [VariableAssignNode]:
        (letkwtoken | constkwtoken) identifiertoken assignoperatortoken unaryexpression
    """
    def parseVariableDeclarationAssign(self) -> Node:
        if self.peak().type == SSTokens.LetKwToken or self.peak().type == SSTokens.ConstKwToken:
            t = self.get() #skip let/const
            if self.peak().type == SSTokens.IdentifierToken:
                kw = DeclareVariableAssignNode()
                kw.setIdentifier(self.get().value)
                if t.type == SSTokens.ConstKwToken:
                    kw.isConst()
                if self.peak().type == SSTokens.AssignOperatorToken:
                    self.get()
                    exp = self.parseUnaryExpression()
                    kw.setChild(exp)
                    return kw
                else:
                    raise SSException(f"SSLexer: Expected AssignOperatorToken")
            else:
                raise SSException(f"SSLexer: Expected IdentifierToken")

        return None
    
    """
    variableassign -> [VariableAssignNode]:
        identifiertoken assignoperatortoken unaryexpression
    """
    def parseVariableAssign(self) -> Node:
        if self.peak().type == SSTokens.IdentifierToken:
            kw = VariableAssignNode()
            kw.setIdentifier(self.get().value)
            if self.peak().type == SSTokens.AssignOperatorToken:
                self.get()
                exp = self.parseUnaryExpression()
                kw.setChild(exp)
                return kw
            else:
                raise SSException(f"SSLexer: Expected AssignOperatorToken")

        return None

    """
    parselog -> [LogNode]:
        logkw unaryexpression
    """
    def parseLog(self) -> Node:
        if self.peak().type == SSTokens.LogKwToken:
            self.get()
            if self.peak().type == SSTokens.LParenToken:
                self.get()
                log = LogNode()
                exp = self.parseUnaryExpression()
                log.setChild(exp)
                if self.peak().type == SSTokens.RParenToken:
                    self.get()
                    return log
                else:
                    raise SSException(f"SSLexer: Expected RParenToken")
            else:
                raise SSException(f"SSLexer: Expected LParenToken")

        return None
    
    """
    parselogln -> [LoglnNode]:
        loglnkw unaryexpression
    """
    def parseLogln(self) -> Node:
        if self.peak().type == SSTokens.LoglnKwToken:
            self.get()
            if self.peak().type == SSTokens.LParenToken:
                self.get()
                log = LoglnNode()
                exp = self.parseUnaryExpression()
                log.setChild(exp)
                if self.peak().type == SSTokens.RParenToken:
                    self.get()
                    return log
                else:
                    raise SSException(f"SSLexer: Expected RParenToken")
            else:
                raise SSException(f"SSLexer: Expected LParenToken")

        return None
    
    """
    functionbody [DeclareVariableAssignNode, VariableAssignNode, LogLnNode, LogNode]:
        declarevariableassignnode |
        variableassignnode |
        functiondeclarationnode |
        loglnnode |
        lognode

    """
    def parseFunctionBody(self) -> list[Node]:
        childs = []

        while self.peak().type != SSTokens.RBracketToken:
            node = None

            #parse declaration variable assign
            node = self.parseVariableDeclarationAssign()
            if node != None:
                childs.append(node)
                continue
            
            #parse variable assign
            node = self.parseVariableAssign()
            if node != None:
                childs.append(node)
                continue

            #testing only
            node = self.parseLog()
            if node != None:
                childs.append(node)
                continue
            node = self.parseLogln()
            if node != None:
                childs.append(node)
                continue

        return childs
    
    """
    functionparams -> [DeclareVariableAssignNode*]:
        (IdentifierToken) (CommaToken, IdentifierToken)
    """
    def parseFunctionParams(self) -> list[Node]:
        params = []
        while self.peak().type == SSTokens.IdentifierToken:
            p = DeclareVariableAssignNode()
            p.setIdentifier(self.get().value)
            p.setChild(NullNode())
            params.append(p)
            if self.peak().type != SSTokens.CommaToken:
                return params
            else:
                self.get()
        return params
    
    """
    functiondeclaration -> [FunctionDeclarationNode]:
        FuncKwToken IdentifierToken FunctionParams FunctionBody
    """
    def parseFunctionDeclaration(self) -> Node:
        if self.peak().type == SSTokens.FuncKwToken:
            self.get()
            if self.peak().type == SSTokens.IdentifierToken:
                f = FunctionDeclarationNode()
                f.setIdentifier(self.get().value)
                if self.peak().type == SSTokens.LParenToken:
                    self.get()
                    params = self.parseFunctionParams()
                    f.setParams(params)
                    if self.peak().type == SSTokens.RParenToken:
                        self.get()
                        if self.peak().type == SSTokens.LBracketToken:
                            self.get()
                            children = self.parseFunctionBody()
                            f.setChild(children)
                            if self.peak().type == SSTokens.RBracketToken:
                                self.get()
                                return f
                            else:
                                raise SSException(f"SSLexer: Expected RBracketToken")
                        else:
                            raise SSException(f"SSLexer: Expected LBracketToken")
                    else:
                        raise SSException(f"SSLexer: Expected RParenToken")
                else:
                    raise SSException(f"SSLexer: Expected LParenToken")
            else:
                raise SSException(f"SSLexer: Expected IdentifierToken")
            
        return None