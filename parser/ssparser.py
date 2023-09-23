from lexer.tokens import *
from misc.exceptions import *
from parser.nodes.conditionals import *
from parser.nodes.expressions import *
from parser.nodes.factors import *
from parser.nodes.loops import *
from parser.nodes.functions import *
from parser.nodes.nodes import *
from parser.nodes.oop import *
from parser.nodes.variables import *

class SSParser:
    def __init__(self):
        self.tokens = []

    def iseof(self, offset: int = 0) -> bool:
        return self.tokens[offset].type == SSTokens.EOFToken
    
    #return token and pops it from source
    def get(self, offset: int = 0) -> SSToken:
        t = self.tokens[offset]
        self.tokens.pop(offset)
        return t
    
    #return token
    def peak(self, offset: int = 0) -> SSToken:
        return self.tokens[offset]
    
    #return token but if not matching throws
    def expect(self, expected: SSTokens, offset: int = 0) -> SSToken:
        if offset >= len(self.tokens):
            raise SSParserException(expected, SSToken(SSTokens.EOFToken, "EOF"))
        if self.peak(offset).type != expected:
            raise SSParserException(expected, self.peak())
        return self.get(offset)
    
    #test if token matching expected, not throw, move poiter only when token match
    def test(self, expected: SSTokens, offset: int = 0) -> SSTokens:
        if offset >= len(self.tokens):
            return None
        if self.peak(offset).type == expected:
            return self.get(offset)
        else:
            return None

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
            
            #pre or post fix
            node = self.parsePrefixExpression()
            if node != None:
                program.appendChild(node)
                continue

            
            #array item assing
            node = self.parseArrayElementOverride()
            if node != None:
                program.appendChild(node)
                continue

            #parse struct member assign
            node = self.parseStructMemberWrite()
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

            raise SSParserUnexpectedException(self.peak())

        return program
    

    def parseFunctionCall(self) -> Node:
        if self.peak().type != SSTokens.IdentifierToken or self.peak(1).type != SSTokens.LParenToken:
            return
        
        identifier = self.get()
        self.get() #lparen

        c = FunctionCallNode()
        c.setIdentifier(identifier.value)

        if self.test(SSTokens.RParenToken):
            return c
        
        params = []
        child = self.parseExpression()
        while child != None:
            params.append(child)
            if self.test(SSTokens.RParenToken):
                break
            elif self.expect(SSTokens.CommaToken):
                pass
            child = self.parseExpression()
        c.setParams(params)
        
        return c
    
    def parseArrayReference(self) -> Node:
        if self.test(SSTokens.LSquareBracketToken, 1):
            identifier = self.expect(SSTokens.IdentifierToken)
            index = self.parseExpression()
            self.expect(SSTokens.RSquareBracketToken)

            a = ArrayReferenceNode()
            a.setIdentifier(identifier.value)
            a.setIndex(index)

            return a
                    
    def parseFactor(self) -> Node:
        #check for exp inside paren
        if self.test(SSTokens.LParenToken):
            n = self.parseExpression()
            self.expect(SSTokens.RParenToken)
            return n
        
        #array indexer
        node = self.parseArrayReference()
        if node:
            return node
        
        #function call
        node = self.parseFunctionCall()
        if node:
            return node

        #string
        if self.test(SSTokens.QuoteToken):
            n = StringNode()
            n.setValue(self.get().value)
            self.expect(SSTokens.QuoteToken)
            return n

        #number token
        number = self.test(SSTokens.NumberToken)
        if number:
            n = NumberNode()
            n.setValue(number.value)
            return n

        #struct.field
        #struct.method()
        structMember = self.parseStructMemberAccess()
        if structMember:
            return structMember

        #identifier
        identifier = self.test(SSTokens.IdentifierToken)
        if identifier:
            n = IdentifierNode()
            n.setIdentifier(identifier.value)
            return n
        
        #true false
        if self.peak().type == SSTokens.TrueKwToken or self.peak().type == SSTokens.FalseKwToken:
            n = BoolNode()
            n.setValue(self.get().value)
            return n

        if self.peak().type == SSTokens.UnaryOperatorToken or self.peak().value in "-+":
            u = UnaryExpressionNode()
            u.setOperator(self.get().value)

            child = self.parseLogicalExpression() #for ex. -2
            
            u.setChild(child)
            return u

        #null
        if self.test(SSTokens.NullKwToken):
            n = NullNode()
            return n
        
        return None

    def parseMulArithmeticExpression(self) -> Node:
        left = self.parseFactor()
        if left:
            while self.peak().value in "*/%":
                operator = self.get().value #operator
                right = self.parseFactor()
                if not right:
                    raise SSParserUnexpectedException(self.peak())
                temp = BinaryExpressionNode()
                temp.lChild = left
                temp.rChild = right
                temp.operator = operator
                left = temp

            return left

    def parseAddArithmeticExpression(self) -> Node:
        left = self.parseMulArithmeticExpression()
        if left:
            while self.peak().value in "+-":
                operator = self.get().value #operator
                right = self.parseMulArithmeticExpression()
                if not right:
                    raise SSParserUnexpectedException(self.peak())
                temp = BinaryExpressionNode()
                temp.lChild = left
                temp.rChild = right
                temp.operator = operator
                left = temp

        return left

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
    
    def parseUnaryExpression(self) -> Node:
        if self.peak().type == SSTokens.UnaryOperatorToken or self.peak().value in "-+":
            u = UnaryExpressionNode()
            u.setOperator(self.get().value)

            child = self.parseLogicalExpression()
            
            u.setChild(child)
            return u
    
    def parsePrefixExpression(self) -> Node:
        #prefix ++a
        operator = self.test(SSTokens.PrefixOperatorToken)
        if operator:
            identifer = self.expect(SSTokens.IdentifierToken)
            i = IdentifierNode()
            i.setIdentifier(identifer.value)
            e = PrefixExpressionNode()
            e.setChild(i)
            e.setOperator(operator.value)
            return e
        
        #postfix a++
        operator = self.test(SSTokens.PrefixOperatorToken, 1)
        if operator:
            identifer = self.expect(SSTokens.IdentifierToken)
            i = IdentifierNode()
            i.setIdentifier(identifer.value)
            e = PostfixExpressionNode()
            e.setChild(i)
            e.setOperator(operator.value)
            return e

    def parseExpression(self) -> Node:
        node = self.parseUnaryExpression()
        if node:
            return node
        
        node = self.parsePrefixExpression()
        if node:
            return node
        
        return self.parseLogicalExpression()

    def parseArray(self) -> Node:
        children = []
        
        node = self.parseFactor()
        while node:
            children.append(node)

            if not self.test(SSTokens.CommaToken):
                break

            node = self.parseFactor()
        
        a = ArrayNode()
        a.setChildren(children)
        return a
    
    def parseAlloc(self):
        if not self.test(SSTokens.AllocKwToken):
            return
        
        self.expect(SSTokens.LParenToken)
        identifier = self.expect(SSTokens.IdentifierToken)
        self.expect(SSTokens.CommaToken)
        expression = self.parseExpression()
        
        if expression:
            self.expect(SSTokens.RParenToken)

            v = StructAllocNode()
            v.setStructName(identifier.value)
            v.setCount(expression)

            return v

    def parseVariableDeclarationAssign(self) -> Node:
        t = self.test(SSTokens.LetKwToken)
        if not t:
            t = self.test(SSTokens.ConstKwToken)
            if not t:
                return
            
        identifier = self.expect(SSTokens.IdentifierToken)
        self.expect(SSTokens.AssignOperatorToken)

        alloc = self.parseAlloc()
        if alloc:
            v = DeclareVariableAssignNode()
            v.setIdentifier(identifier.value)
            v.setChild(alloc)
            if t.type == SSTokens.ConstKwToken:
                v.isConst()
            
            return v

        expression = self.parseExpression()
        if expression:
            v = DeclareVariableAssignNode()
            v.setIdentifier(identifier.value)
            v.setChild(expression)
            if t.type == SSTokens.ConstKwToken:
                v.isConst()

            return v
        
        self.expect(SSTokens.LSquareBracketToken)
        child = self.parseArray()
        self.expect(SSTokens.RSquareBracketToken)
        
        v = DeclareVariableAssignNode()
        v.setIdentifier(identifier.value)
        v.setChild(child)
        if t.type == SSTokens.ConstKwToken:
            v.isConst()

        return v

    def parseVariableAssign(self) -> Node:
        identifier = self.test(SSTokens.IdentifierToken)
        if not identifier:
            return
        
        self.expect(SSTokens.AssignOperatorToken)
        expression = self.parseExpression()
        if expression:
            v = VariableAssignNode()
            v.setIdentifier(identifier.value)
            v.setChild(expression)

            return v
        
        self.expect(SSTokens.LSquareBracketToken)
        child = self.parseArray()
        self.expect(SSTokens.RSquareBracketToken)
        
        v = VariableAssignNode()
        v.setIdentifier(identifier.value)
        v.setChild(child)

        return v
    
    def parseArrayElementOverride(self) -> Node:
        if not self.test(SSTokens.LSquareBracketToken, 1):
            return
        
        identifier = self.expect(SSTokens.IdentifierToken)
        index = self.parseExpression()
        self.expect(SSTokens.RSquareBracketToken)

        self.expect(SSTokens.AssignOperatorToken)
        expression = self.parseExpression()

        v = ArrayElementOverrideNode()
        v.setIdentifier(identifier.value)
        v.setIndex(index)
        v.setChild(expression)

        return v

    def parseLog(self) -> Node:
        if not self.test(SSTokens.LogKwToken):
            return
        
        self.expect(SSTokens.LParenToken)
        expression = self.parseExpression()
        self.expect(SSTokens.RParenToken)

        log = LogNode()
        log.setChild(expression)

        return log
    
    def parseLogln(self) -> Node:
        if not self.test(SSTokens.LoglnKwToken):
            return
        
        self.expect(SSTokens.LParenToken)
        expression = self.parseExpression()
        self.expect(SSTokens.RParenToken)

        log = LoglnNode()
        log.setChild(expression)

        return log
    
    def parseReturnValue(self) -> Node:
        if not self.test(SSTokens.ReturnKwToken):
            return
        
        expression = self.parseExpression()

        r = ReturnNode()
        if expression:
            r.setValue(expression)

        return r
    
    def parseBody(self) -> list[Node]:
        childs = []

        while self.peak().type != SSTokens.RBracketToken:
            node = None
            
            #parse declaration variable assign
            node = self.parseVariableDeclarationAssign()
            if node != None:
                childs.append(node)
                continue

            #array item assing
            node = self.parseArrayElementOverride()
            if node != None:
                childs.append(node)
                continue
            
            #parse struct member assign
            node = self.parseStructMemberWrite()
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

            #continue kw
            c = self.test(SSTokens.ContinueKwToken)
            if c:
                childs.append(ContinueNode())
                continue

            #break kw
            b = self.test(SSTokens.BreakKwToken)
            if b:
                childs.append(BreakNode())
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
            
            raise SSParserUnexpectedException(self.peak())

        return childs
    
    def parseFunctionParams(self) -> list[Node]:
        params = []

        identifier = self.test(SSTokens.IdentifierToken)
        while identifier:
            p = DeclareVariableAssignNode()
            p.setIdentifier(identifier.value)
            p.setChild(NullNode())
            params.append(p)

            if not self.test(SSTokens.CommaToken):
                return params
            
            identifier = self.test(SSTokens.IdentifierToken)

        return params

    def parseFunctionDeclaration(self) -> Node:
        if not self.test(SSTokens.FuncKwToken):
            return
        
        identifier = self.expect(SSTokens.IdentifierToken)
        self.expect(SSTokens.LParenToken)
        params = self.parseFunctionParams()
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)
        
        func = FunctionDeclarationNode()
        func.setIdentifier(identifier.value)
        func.setParams(params)
        func.setChild(body)

        return func

    def parseForLoopStarter(self) -> Node:
        declaration = self.parseVariableDeclarationAssign()
        if declaration:
            return declaration
        
        return self.parseVariableAssign()
    
    def parseForLoopModifier(self) -> Node:
        node = self.parsePrefixExpression()
        if node:
            return node
        
        return self.parseVariableAssign()

    def parseForLoop(self) -> Node:
        if not self.test(SSTokens.ForKwToken):
            return
        
        self.expect(SSTokens.LParenToken)
        sexpression = self.parseForLoopStarter()
        self.expect(SSTokens.SemicolonToken)
        lexpression = self.parseExpression()
        self.expect(SSTokens.SemicolonToken)
        mexpression = self.parseForLoopModifier()
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)

        f = ForLoopNode()
        f.setStartExpression(sexpression)
        f.setLogicExpression(lexpression)
        f.setModExpression(mexpression)
        f.setBody(body)

        return f

    def parseWhileLoop(self) -> Node:
        if not self.test(SSTokens.WhileKwToken):
            return
        
        self.expect(SSTokens.LParenToken)
        lexpression = self.parseExpression()
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)

        w = WhileLoopNode()
        w.setLogicExpression(lexpression)
        w.setBody(body)

        return w

    def parseDoWhileLoop(self) -> Node:
        if not self.test(SSTokens.DoKwToken):
            return
        
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)
        self.expect(SSTokens.WhileKwToken)
        self.expect(SSTokens.LParenToken)
        lexpression = self.parseExpression()
        self.expect(SSTokens.RParenToken)

        do = DoWhileLoopNode()
        do.setLogicExpression(lexpression)
        do.setBody(body)

        return do

    def parseIf(self) -> Node:
        if not self.test(SSTokens.IfKwToken):
            return
        
        self.expect(SSTokens.LParenToken)
        lexpression = self.parseExpression()
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)

        child = self.parseElif()
        if not child:
            child = self.parseElse()
        
        e = IfNode()
        e.setLogicExpression(lexpression)
        e.setBody(body)
        if child:
            e.setChild(child)

        return e
                
    def parseElif(self) -> Node:
        if not self.test(SSTokens.ElifKwToken):
            return
        
        self.expect(SSTokens.LParenToken)
        lexpression = self.parseExpression()
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)

        child = self.parseElif()
        if not child:
            child = self.parseElse()
        
        e = ElifNode()
        e.setLogicExpression(lexpression)
        e.setBody(body)
        if child:
            e.setChild(child)

        return e
                
    def parseElse(self) -> Node:
        if not self.test(SSTokens.ElseKwToken):
            return
        
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)
        
        e = ElseNode()
        e.setBody(body)
        
        return e

    def parseFieldDeclarationAssign(self) -> Node:
        access = self.test(SSTokens.AccessModifierKwToken)
        if not access:
            return
        
        self.expect(SSTokens.LetKwToken)
        identifier = self.expect(SSTokens.IdentifierToken)
        const = self.test(SSTokens.ConstKwToken)
        self.expect(SSTokens.AssignOperatorToken)
        expression = self.parseExpression()

        field = DeclareFieldAssignNode()
        field.setAccess(access.value)
        field.setIdentifier(identifier.value)
        if const:
            field.isConst()
        field.setChild(expression)

        return field

    def parseStructBody(self) -> list[Node]:
        childs = []

        while self.peak().type != SSTokens.RBracketToken:
            node = None

            #parse declaration variable assign
            node = self.parseFieldDeclarationAssign()
            if node != None:
                childs.append(node)
                continue

            raise SSParserUnexpectedException(self.peak())
            
        return childs   

    def parseStruct(self) -> Node:
        if not self.test(SSTokens.StructKwToken):
            return

        identifier = self.expect(SSTokens.IdentifierToken)
        self.expect(SSTokens.LParenToken)
        parent = self.test(SSTokens.IdentifierToken)
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseStructBody()
        self.expect(SSTokens.RBracketToken)

        struct = StructNode()
        struct.setName(identifier.value)
        if parent:
            struct.setParent(parent.value)
        struct.setBody(body)

        return struct
            
    def parseMethodDefinition(self, struct: str) -> Node:
        access = self.test(SSTokens.AccessModifierKwToken)
        if not access:
            return
        
        self.expect(SSTokens.FuncKwToken)
        identifier = self.expect(SSTokens.IdentifierToken)
        self.expect(SSTokens.LParenToken)
        params = self.parseFunctionParams()
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseBody()
        self.expect(SSTokens.RBracketToken)

        met = MethodDeclarationNode()
        met.setAccess(access.value)
        met.setIdentifier(identifier.value)
        met.setStructName(struct)
        met.setParams(params)
        met.setChild(body)
        
        return met
    
    def parseImplBody(self, struct: str) -> list[Node]:
        childs = []

        while self.peak().type != SSTokens.RBracketToken:
            node = None

            #parse declaration variable assign
            node = self.parseMethodDefinition(struct)
            if node != None:
                childs.append(node)
                continue

            raise SSParserUnexpectedException(self.peak())
            
        return childs 

    def parseImpl(self) -> Node:
        if not self.test(SSTokens.ImplKwToken):
            return

        identifier = self.expect(SSTokens.IdentifierToken)
        self.expect(SSTokens.LParenToken)
        parent = self.test(SSTokens.IdentifierToken)
        self.expect(SSTokens.RParenToken)
        self.expect(SSTokens.LBracketToken)
        body = self.parseImplBody(identifier)
        self.expect(SSTokens.RBracketToken)

        impl = ImplNode()
        impl.setName(identifier.value)
        if parent:
            impl.setParent(parent.value)
        impl.setBody(body)

        return impl
    
    def parseStructMemberAccess(self):
        if self.peak().type == SSTokens.IdentifierToken != None and self.peak(1).type == SSTokens.DotToken:
            identifier = self.expect(SSTokens.IdentifierToken)
            self.expect(SSTokens.DotToken)
            member = self.expect(SSTokens.IdentifierToken)

            v = StructMemberAccess()
            v.setStruct(identifier.value)
            v.setMember(member.value)
            return v
        
    def parseStructMemberWrite(self):
        if self.peak().type == SSTokens.IdentifierToken != None and self.peak(1).type == SSTokens.DotToken:
            identifier = self.expect(SSTokens.IdentifierToken)
            self.expect(SSTokens.DotToken)
            member = self.expect(SSTokens.IdentifierToken)
            self.expect(SSTokens.AssignOperatorToken)

            expression = self.parseExpression()

            if expression:
                v = StructMemberWrite()
                v.setStruct(identifier.value)
                v.setMember(member.value)
                v.setChild(expression)
                return v