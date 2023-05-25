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

            #parse if
            node = self.parseIf()
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

            #parse struct declaration
            node = self.parseStruct()
            if node != None:
                program.appendChild(node)
                continue

            #parse impl declaration
            node = self.parseImpl()
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
                    raise SSParserException(SSTokens.CommaToken, self.peak())
                child = self.parseUnaryExpression()
            c.setParams(params)
            
            return c
                    
    """
    factor -> [IdentifierNode, NumberNode, BoolNode, NullNode, StringNode, unaryexpression, arithmeticexpression]:
        numbertoken | identifiertoken
    """
    def parseFactor(self) -> Node:
        #check for exp inside paren
        if self.peak().type == SSTokens.LParenToken:
            self.get()
            n = self.parseUnaryExpression()
            if self.get().type != SSTokens.RParenToken:
                raise SSParserException(SSTokens.RParenToken, self.peak())
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
                raise SSParserException(SSTokens.QuoteToken, self.peak())
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

        if self.peak().type == SSTokens.UnaryOperatorToken or self.peak().value in "-+":
            u = UnaryExpressionNode()
            u.setOperator(self.get().value)

            child = self.parseLogicalExpression()
            
            u.setChild(child)
            return u

        return None

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
        while self.peak().value in "|&<<>>^":
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
        if self.peak().type == SSTokens.UnaryOperatorToken or self.peak().value in "-+":
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
                    raise SSParserException(SSTokens.AssignOperatorToken, self.peak())
            else:
                raise SSParserException(SSTokens.IdentifierToken, self.peak())
    
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
                raise SSParserException(SSTokens.AssignOperatorToken, self.peak())

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
                    raise SSParserException(SSTokens.RParenToken, self.peak())
            else:
                raise SSParserException(SSTokens.LParenToken, self.peak())
    
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
                    raise SSParserException(SSTokens.RParenToken, self.peak())
            else:
                raise SSParserException(SSTokens.LParenToken, self.peak())
    
    """
    returnvalue -> [unaryexpression]:
        returnkwtoken (unaryexpression)
    """
    def parseReturnValue(self) -> Node:
        if self.peak().type == SSTokens.ReturnKwToken:
            self.get()
            r = ReturnNode()
            exp = self.parseUnaryExpression()
            if exp != None:
                r.setValue(exp)
            return r
    
    """
    body [DeclareVariableAssignNode, VariableAssignNode, ForLoopNode, LogLnNode, LogNode]:
        declarevariableassignnode |
        variableassignnode |
        functiondeclarationnode |
        forloopnode |
        loglnnode |
        lognode

    """
    def parseBody(self) -> list[Node]:
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

            #parse if
            node = self.parseIf()
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
                            children = self.parseBody()
                            f.setChild(children)
                            if self.peak().type == SSTokens.RBracketToken:
                                self.get()
                                return f
                            else:
                                raise SSParserException(SSTokens.RBracketToken, self.peak())
                        else:
                            raise SSParserException(SSTokens.LBracketToken, self.peak())
                    else:
                        raise SSParserException(SSTokens.RParenToken, self.peak())
                else:
                    raise SSParserException(SSTokens.LParenToken, self.peak())
            else:
                raise SSParserException(SSTokens.IdentifierToken, self.peak())

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
                    raise SSParserException("DeclareVariableAssignNode", self.peak())
                if self.peak().type != SSTokens.SemicolonToken:
                    raise SSParserException(SSTokens.SemicolonToken, self.peak())
                self.get()
                lexp = self.parseUnaryExpression()
                if lexp == None:
                    raise SSParserException("UnaryExpressionNode", self.peak())
                if self.peak().type != SSTokens.SemicolonToken:
                    raise SSParserException(SSTokens.SemicolonToken, self.peak())
                self.get()
                mexp = self.parseVariableAssign()
                if mexp == None:
                    raise SSParserException("DeclareVariableAssignNode", self.peak())
                if self.peak().type == SSTokens.RParenToken:
                    self.get()
                    if self.peak().type == SSTokens.LBracketToken:
                        self.get()
                        children = self.parseBody()
                        if self.peak().type == SSTokens.RBracketToken:
                            self.get()
                            f = ForLoopNode()
                            f.setStartExpression(sexp)
                            f.setLogicExpression(lexp)
                            f.setModExpression(mexp)
                            f.setBody(children)
                            return f
                        else:
                            raise SSParserException(SSTokens.RBracketToken, self.peak())
                else:
                    raise SSParserException(SSTokens.RParenToken, self.peak())
            else:
                raise SSParserException(SSTokens.LParenToken, self.peak())
            
    def parseWhileLoop(self) -> Node:
        if self.peak().type == SSTokens.WhileKwToken:
            self.get()
            if self.peak().type == SSTokens.LParenToken:
                self.get()
                lexp = self.parseUnaryExpression()
                if lexp == None:
                    raise SSParserException("UnaryExpressionNode", self.peak())
                if self.peak().type == SSTokens.RParenToken:
                    self.get()
                    if self.peak().type == SSTokens.LBracketToken:
                        self.get()
                        children = self.parseBody()
                        if self.peak().type == SSTokens.RBracketToken:
                            self.get()
                            f = WhileLoopNode()
                            f.setLogicExpression(lexp)
                            f.setBody(children)
                            return f
                        else:
                            raise SSParserException(SSTokens.RBracketToken, self.peak())
                else:
                    raise SSParserException(SSTokens.RParenToken, self.peak())
            else:
                raise SSParserException(SSTokens.LParenToken, self.peak())

    def parseDoWhileLoop(self) -> Node:
        if self.peak().type == SSTokens.DoKwToken:
            self.get()
            if self.peak().type == SSTokens.LBracketToken:
                self.get()
                children = self.parseBody()
                if self.peak().type == SSTokens.RBracketToken:  
                    self.get()                  
                    if self.peak().type == SSTokens.WhileKwToken:
                        self.get()                        
                        if self.peak().type == SSTokens.LParenToken:
                            self.get()
                            l = DoWhileLoopNode()
                            lexp = self.parseUnaryExpression()
                            if lexp == None:
                                raise SSParserException("UnaryExpressionNode", self.peak())
                            if self.peak().type == SSTokens.RParenToken:
                                self.get()
                                l.setLogicExpression(lexp)
                                l.setBody(children)
                                return l
                            else:
                                raise SSParserException(SSTokens.RParenToken, self.peak())
                        else:
                            raise SSParserException(SSTokens.LParenToken, self.peak())
                    else:
                        raise SSParserException(SSTokens.WhileKwToken, self.peak())
                else:
                    raise SSParserException(SSTokens.RBracketToken, self.peak())
            else:
                raise SSParserException(SSTokens.LBracketToken, self.peak())
            
    def parseIf(self) -> Node:
        if self.peak().type == SSTokens.IfKwToken:
            self.get()
            i = IfNode()
            if self.peak().type == SSTokens.LParenToken:
                self.get()
                lexp = self.parseUnaryExpression()
                if lexp == None:
                    raise SSParserException("UnaryExpressionNode", self.peak())
                i.setLogicExpression(lexp)
                if self.peak().type == SSTokens.RParenToken:    
                    self.get()                
                    if self.peak().type == SSTokens.LBracketToken:
                        self.get()
                        body = self.parseBody()
                        i.setBody(body)
                        if self.peak().type == SSTokens.RBracketToken:
                            self.get()
                            child = self.parseElif()
                            if child != None:
                                i.setChild(child)
                            else:
                                child = self.parseElse()
                                if child != None:
                                    i.setChild(child)
                            return i
                        else:
                            raise SSParserException(SSTokens.RBracketToken, self.peak())
                    else:
                        raise SSParserException(SSTokens.LBracketToken, self.peak())
                else:
                    raise SSParserException(SSTokens.RParenToken, self.peak())
            else:
                raise SSParserException(SSTokens.LParenToken, self.peak())
            
    def parseElif(self) -> Node:
        if self.peak().type == SSTokens.ElifKwToken:
            self.get()
            i = ElifNode()
            if self.peak().type == SSTokens.LParenToken:
                self.get()
                lexp = self.parseUnaryExpression()
                if lexp == None:
                    raise SSParserException("UnaryExpressionNode", self.peak())
                i.setLogicExpression(lexp)
                if self.peak().type == SSTokens.RParenToken:    
                    self.get()                
                    if self.peak().type == SSTokens.LBracketToken:
                        self.get()
                        body = self.parseBody()
                        i.setBody(body)
                        if self.peak().type == SSTokens.RBracketToken:
                            self.get()
                            child = self.parseElif()
                            if child != None:
                                i.setChild(child)
                            else:
                                child = self.parseElse()
                                if child != None:
                                    i.setChild(child)
                            return i
                        else:
                            raise SSParserException(SSTokens.RBracketToken, self.peak())
                    else:
                        raise SSParserException(SSTokens.LBracketToken, self.peak())
                else:
                    raise SSParserException(SSTokens.RParenToken, self.peak())
            else:
                raise SSParserException(SSTokens.LParenToken, self.peak())
            
    def parseElse(self) -> Node:
        if self.peak().type == SSTokens.ElseKwToken:
            self.get()
            i = ElseNode()                
            if self.peak().type == SSTokens.LBracketToken:
                self.get()
                body = self.parseBody()
                i.setBody(body)
                if self.peak().type == SSTokens.RBracketToken:
                    self.get()
                    return i
                else:
                    raise SSParserException(SSTokens.RBracketToken, self.peak())
            else:
                raise SSParserException(SSTokens.LBracketToken, self.peak())

    def parseFieldDeclarationAssign(self) -> Node:
        if self.peak().type == SSTokens.AccessModifierToken:
            kw = DeclareFieldAssignNode()
            kw.setAccess(self.get().value)
            if self.peak().type == SSTokens.LetKwToken or self.peak().type == SSTokens.ConstKwToken:
                t = self.get() #skip let/const
                if self.peak().type == SSTokens.IdentifierToken:
                    kw.setIdentifier(self.get().value)
                    if t.type == SSTokens.ConstKwToken:
                        kw.isConst()
                    if self.peak().type == SSTokens.AssignOperatorToken:
                        self.get()
                        exp = self.parseUnaryExpression()
                        kw.setChild(exp)
                        return kw
                    else:
                        raise SSParserException(SSTokens.AssignOperatorToken, self.peak())
                else:
                    raise SSParserException(SSTokens.IdentifierToken, self.peak())
            else:
                raise SSParserException([SSTokens.LetKwToken, SSTokens.ConstKwToken], self.peak())

    def parseStructBody(self) -> list[Node]:
        childs = []

        while self.peak().type != SSTokens.RBracketToken:
            node = None

            #parse declaration variable assign
            node = self.parseFieldDeclarationAssign()
            if node != None:
                childs.append(node)
            
        return childs   

    def parseStruct(self) -> Node:
        if self.peak().type == SSTokens.StructKwToken:
            self.get()
            if self.peak().type == SSTokens.IdentifierToken:
                struct = StructNode()
                struct.setName(self.get().value)
                if self.peak().type == SSTokens.LParenToken:
                    self.get()
                    if self.peak().type == SSTokens.IdentifierToken:
                        struct.setParent(self.get().value)
                        if self.get().type != SSTokens.RParenToken:
                            raise SSParserException(SSTokens.RParenToken, self.peak())
                    else:
                        raise SSParserException(SSTokens.IdentifierToken, self.peak())
                if self.peak().type == SSTokens.LBracketToken:
                    self.get()
                    body = self.parseStructBody()
                    struct.setBody(body)
                    if self.peak().type == SSTokens.RBracketToken:
                        self.get()
                        return struct
                    else:
                        raise SSParserException(SSTokens.RBracketToken, self.peak())
            else:
                raise SSParserException(SSTokens.IdentifierToken, self.peak())
            
    def parseMethodDefinition(self, struct: str) -> Node:
        if self.peak().type == SSTokens.AccessModifierToken:
            f = MethodDeclarationNode()
            f.setStructName(struct)
            f.setAccess(self.get())    
            if self.peak().type == SSTokens.FuncKwToken:
                self.get()
                if self.peak().type == SSTokens.IdentifierToken:
                    f.setIdentifier(self.get().value)
                    if self.peak().type == SSTokens.LParenToken:
                        self.get()
                        params = self.parseFunctionParams()
                        f.setParams(params)
                        if self.peak().type == SSTokens.RParenToken:
                            self.get()
                            if self.peak().type == SSTokens.LBracketToken:
                                self.get()
                                children = self.parseBody()
                                f.setChild(children)
                                if self.peak().type == SSTokens.RBracketToken:
                                    self.get()
                                    return f
                                else:
                                    raise SSParserException(SSTokens.RBracketToken, self.peak())
                            else:
                                raise SSParserException(SSTokens.LBracketToken, self.peak())
                        else:
                            raise SSParserException(SSTokens.RParenToken, self.peak())
                    else:
                        raise SSParserException(SSTokens.LParenToken, self.peak())
                else:
                    raise SSParserException(SSTokens.IdentifierToken, self.peak())
            else:
                raise SSParserException(SSTokens.FuncKwToken, self.peak())
    
    def parseImplBody(self, struct: str) -> list[Node]:
        childs = []

        while self.peak().type != SSTokens.RBracketToken:
            node = None

            #parse declaration variable assign
            node = self.parseMethodDefinition(struct)
            if node != None:
                childs.append(node)
            
        return childs 

    def parseImpl(self) -> Node:
        if self.peak().type == SSTokens.ImplKwToken:
            self.get()
            if self.peak().type == SSTokens.IdentifierToken:
                impl = ImplNode()
                impl.setName(self.get().value)
                if self.peak().type == SSTokens.LParenToken:
                    self.get()
                    if self.peak().type == SSTokens.IdentifierToken:
                        impl.setParent(self.get().value)
                        if self.get().type != SSTokens.RParenToken:
                            raise SSParserException(SSTokens.RParenToken, self.peak())
                    else:
                        raise SSParserException(SSTokens.IdentifierToken, self.peak())
                if self.peak().type == SSTokens.LBracketToken:
                    self.get()
                    body = self.parseImplBody(impl.name)
                    impl.setBody(body)
                    if self.peak().type == SSTokens.RBracketToken:
                        self.get()
                        return impl
                    else:
                        raise SSParserException(SSTokens.RBracketToken, self.peak())
            else:
                raise SSParserException(SSTokens.IdentifierToken, self.peak())