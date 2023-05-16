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
        forloopnode |
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

            #function calls
            node = self.parseFunctionCall()
            if node != None:
                program.appendChild(node)
                continue
            
            #parse for loop
            node = self.parseForLoop()
            if node != None:
                program.appendChild(node)
                continue

            #parse while loop
            node = self.parseWhileLoop()
            if node != None:
                program.appendChild(node)
                continue

            #parse do while loop
            node = self.parseDoWhileLoop()
            if node != None:
                program.appendChild(node)
                continue

            #parse return value
            node = self.parseReturnValue()
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
    functioncall -> [FunctionCallNode]:
        Identifier LParen (UnaryExpression CommaToken)* RParen
    """
    def parseFunctionCall(self) -> Node:
        if self.peak().type == SSTokens.IdentifierToken and self.peak(1).type == SSTokens.LParenToken:
            c = FunctionCallNode()
            c.setIdentifier(self.get().value)
            self.get() #lparen
            if self.peak().type == SSTokens.RParenToken:
                self.get()
                return c
            params = []
            child = self.parseUnaryExpression()
            while child != None:
                params.append(child)
                if self.peak().type == SSTokens.RParenToken:
                    self.get()
                    break
                elif self.peak().type == SSTokens.CommaToken:
                    self.get()
                else:
                    raise SSException(f"SSParser: Expected CommaToken or RParenToken")
                child = self.parseUnaryExpression()
            c.setParams(params)
            
            return c
                    
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
        
        #function call
        n = self.parseFunctionCall()
        if n != None:
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
                    raise SSException(f"SSParser: Expected AssignOperatorToken")
            else:
                raise SSException(f"SSParser: Expected IdentifierToken")

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
                raise SSException(f"SSParser: Expected AssignOperatorToken")

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
                    raise SSException(f"SSParser: Expected RParenToken")
            else:
                raise SSException(f"SSParser: Expected LParenToken")

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
                    raise SSException(f"SSParser: Expected RParenToken")
            else:
                raise SSException(f"SSParser: Expected LParenToken")

        return None
    
    """
    returnvalue -> [unaryexpression]:
        returnkwtoken unaryexpression
    """
    def parseReturnValue(self) -> Node:
        if self.peak().type == SSTokens.ReturnKwToken:
            self.get()
            exp = self.parseUnaryExpression()
            if exp != None:
                r = ReturnNode()
                r.setValue(exp)
                return r
            else:
                raise SSException(f"SSParser: Expected return expression")
    
    """
    functionbody [DeclareVariableAssignNode, VariableAssignNode, ForLoopNode, LogLnNode, LogNode]:
        declarevariableassignnode |
        variableassignnode |
        functiondeclarationnode |
        forloopnode |
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

            #parse for loop
            node = self.parseForLoop()
            if node != None:
                childs.append(node)
                continue

            #parse while loop
            node = self.parseWhileLoop()
            if node != None:
                childs.append(node)
                continue
            
            #parse do while loop
            node = self.parseDoWhileLoop()
            if node != None:
                childs.append(node)
                continue

            #parse return value
            node = self.parseReturnValue()
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
                                raise SSException(f"SSParser: Expected RBracketToken")
                        else:
                            raise SSException(f"SSParser: Expected LBracketToken")
                    else:
                        raise SSException(f"SSParser: Expected RParenToken")
                else:
                    raise SSException(f"SSParser: Expected LParenToken")
            else:
                raise SSException(f"SSParser: Expected IdentifierToken")
            
        return None

    """
    forloopbody -> [DeclareVariableAssignNode, VariableAssignNode, ForLoopNode, LogLnNode, LogNode]:
        declarevariableassignnode |
        variableassignnode |
        functiondeclarationnode |
        forloopnode |
        loglnnode |
        lognode
    """
    def parseLoopBody(self) -> list[Node]:
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

            #parse for loop
            node = self.parseForLoop()
            if node != None:
                childs.append(node)
                continue

            #parse while loop
            node = self.parseWhileLoop()
            if node != None:
                childs.append(node)
                continue

            #parse do while loop
            node = self.parseDoWhileLoop()
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
    forloop -> [ForLoopNode]:
        forkwtoken, lparentoken, variabledeclarationassign, commatoken, unaryexpression, commatoken, unaryexpression rparent
        lbracket loopbody rbracket
    """
    def parseForLoop(self) -> Node:
        if self.peak().type == SSTokens.ForKwToken:
            self.get()
            if self.peak().type == SSTokens.LParenToken:
                self.get()
                sexp = self.parseVariableDeclarationAssign()
                if sexp == None:
                    raise SSException(f"SSParser: Expected starting declaration")
                if self.peak().type != SSTokens.SemicolonToken:
                    raise SSException(f"SSParser: Expected SemicolonToken")
                self.get()
                lexp = self.parseUnaryExpression()
                if lexp == None:
                    raise SSException(f"SSParser: Expected testing expression")
                if self.peak().type != SSTokens.SemicolonToken:
                    raise SSException(f"SSParser: Expected SemicolonToken")
                self.get()
                mexp = self.parseVariableAssign()
                if mexp == None:
                    raise SSException(f"SSParser: Expected mod expression")
                if self.peak().type == SSTokens.RParenToken:
                    self.get()
                    if self.peak().type == SSTokens.LBracketToken:
                        self.get()
                        children = self.parseLoopBody()
                        if self.peak().type == SSTokens.RBracketToken:
                            self.get()
                            f = ForLoopNode()
                            f.setStartExpression(sexp)
                            f.setLogicExpression(lexp)
                            f.setModExpression(mexp)
                            f.setBody(children)
                            return f
                        else:
                            raise SSException(f"SSParser: Expected RBracketToken")
                else:
                    raise SSException(f"SSParser: Expected RParenToken")
            else:
                raise SSException(f"SSParser: Expected LParenToken")
            
    def parseWhileLoop(self) -> Node:
        if self.peak().type == SSTokens.WhileKwToken:
            self.get()
            if self.peak().type == SSTokens.LParenToken:
                self.get()
                lexp = self.parseUnaryExpression()
                if lexp == None:
                    raise SSException(f"SSParser: Expected testing expression")
                if self.peak().type == SSTokens.RParenToken:
                    self.get()
                    if self.peak().type == SSTokens.LBracketToken:
                        self.get()
                        children = self.parseLoopBody()
                        if self.peak().type == SSTokens.RBracketToken:
                            self.get()
                            f = WhileLoopNode()
                            f.setLogicExpression(lexp)
                            f.setBody(children)
                            return f
                        else:
                            raise SSException(f"SSParser: Expected RBracketToken")
                else:                
                    raise SSException(f"SSParser: Expected RParenToken")
            else:
                raise SSException(f"SSParser: Expected LParenToken")

    def parseDoWhileLoop(self) -> Node:
        if self.peak().type == SSTokens.DoKwToken:
            self.get()
            if self.peak().type == SSTokens.LBracketToken:
                self.get()
                children = self.parseLoopBody()
                if self.peak().type == SSTokens.RBracketToken:  
                    self.get()                  
                    if self.peak().type == SSTokens.WhileKwToken:
                        self.get()                        
                        if self.peak().type == SSTokens.LParenToken:
                            self.get()
                            l = DoWhileLoopNode()
                            lexp = self.parseUnaryExpression()
                            if lexp == None:
                                raise SSException(f"SSParser: Expected testing expression")
                            if self.peak().type == SSTokens.RParenToken:
                                self.get()
                                l.setLogicExpression(lexp)
                                l.setBody(children)
                                return l
                            else:
                                raise SSException(f"SSParser: Expected RParenToken")
                        else:
                            raise SSException(f"SSParser: Expected LParenToken")
                    else:
                        raise SSException(f"SSParser: Expected WhileKwToken")
                else:
                    raise SSException(f"SSParser: Expected RBracketToken")
            else:
                raise SSException(f"SSParser: Expected LBracketToken")