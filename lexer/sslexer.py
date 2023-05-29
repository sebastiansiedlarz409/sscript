from lexer.tokens import *
from lexer.token import *
from misc.exceptions import *

import string

class SSLexer:
    def __init__(self):
        self.line: int = 1
        self.column: int = 1 #current position in line
        self.current: int = 1 #currently testing token start position
        self.chars: list[str] = [] #list of characters from source

    #return [length] characters from [offset] without removing them
    def peak(self, offset: int = 0, length: int = 1):
        return ''.join(self.chars[offset:offset+length])

    #return [length] characters from [offset] and pop them from source
    def get(self, offset: int = 0, length: int = 1):
        ret = ''.join(self.chars[offset: offset+length])
        for i in range(0, length): self.chars.pop(offset)
        self.column += length
        return ret

    def isalphabetic(self, char: str) -> bool:
        return char in (string.ascii_letters + "_")
    
    def isnumber(self, char: str) -> bool:
        return char in string.digits
    
    def ishexnumber(self, char: str) -> bool:
        return char.lower() in (string.digits+"abcdef")
    
    def isbinnumber(self, char: str) -> bool:
        return char.lower() in ("01")
    
    #if numeric literal was dectected, builts it and returns it
    def getNumericValue(self) -> str:
        value = ""

        #if hex
        if len(self.chars) > 1:
            if self.peak(0,2) == "0x":
                value+="0x"
                self.get()
                self.get()
                while(len(self.chars) > 0 and (self.ishexnumber(self.peak()))):
                    value+=self.peak()
                    self.get()
                return value
        
        #if bin
        if len(self.chars) > 1:
            if self.peak(0,2) == "0b":
                value+="0b"
                self.get()
                self.get()
                while(len(self.chars) > 0 and (self.isbinnumber(self.peak()))):
                    value+=self.peak()
                    self.get()
                return value

        #if decimal
        dot = False
        while(len(self.chars) > 0 and (self.isnumber(self.peak()) or self.peak() == ".")):
            #throw if there is more than one dot
            if self.peak() == "." and dot:
                raise SSLexerException(self.peak(), self.line, self.column)
            #mark first dot
            if self.peak() == ".":
                dot = True
            value+=self.peak()
            self.get()
        return value
    
    #builts and returns string literal without quotes
    def getStringValue(self) -> str:
        value = ""
        while self.peak() in string.printable and self.peak() != '"':
            value += self.peak()
            self.get()
        return value

    #tokenize source
    def tokenize(self, source: str) -> list[SSToken]:
        #buffer for tokens
        tokens = []

        #get all characters
        self.chars = [x for x in source]
        
        #self.line and self.column tracking for errors
        self.line = 1
        self.column = 1
        self.current = 1

        while(len(self.chars) > 0):
            #here analyze of new token begin
            #align column pointers
            self.current = self.column

            if self.peak() in '\t\n\r ':
                if self.peak() == '\n':
                    self.line+=1
                    self.column=0
                self.get()
            elif self.peak() == '(':
                tokens.append(SSToken(SSTokens.LParenToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == ')':
                tokens.append(SSToken(SSTokens.RParenToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == '{':
                tokens.append(SSToken(SSTokens.LBracketToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == '}':
                tokens.append(SSToken(SSTokens.RBracketToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == '[':
                tokens.append(SSToken(SSTokens.LSquareBracketToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == ']':
                tokens.append(SSToken(SSTokens.RSquareBracketToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == '=':
                tokens.append(SSToken(SSTokens.AssignOperatorToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == ',':
                tokens.append(SSToken(SSTokens.CommaToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak() == ';':
                tokens.append(SSToken(SSTokens.SemicolonToken, self.peak(),self.line, self.current))
                self.get()
            elif self.peak(0,2) == '<<':
                tokens.append(SSToken(SSTokens.BinaryOperatorToken, self.peak(0,2),self.line, self.current))
                self.get()
                self.get()
            elif self.peak(0,2) == '>>':
                tokens.append(SSToken(SSTokens.BinaryOperatorToken, self.peak(0,2),self.line, self.current))
                self.get()
                self.get()
            elif self.peak(0,2) == '++':
                tokens.append(SSToken(SSTokens.PrefixOperatorToken, self.peak(0,2),self.line, self.current))
                self.get()
                self.get()
            elif self.peak(0,2) == '--':
                tokens.append(SSToken(SSTokens.PrefixOperatorToken, self.peak(0,2),self.line, self.current))
                self.get()
                self.get()
            elif self.peak() in '+-*/%|&^':
                tokens.append(SSToken(SSTokens.BinaryOperatorToken, self.peak(),self.line, self.current))
                self.get()
            else:
                #here we handle multicharacter tokens
                #strings
                if self.peak() == '"':
                    tokens.append(SSToken(SSTokens.QuoteToken, self.peak(),self.line, self.current))
                    self.get()
                    self.current = self.column
                    value = self.getStringValue()
                    tokens.append(SSToken(SSTokens.StringToken, value,self.line, self.current))
                    self.current = self.column
                    if self.peak() == '"':
                        tokens.append(SSToken(SSTokens.QuoteToken, self.peak(),self.line, self.current))
                        self.get()
                    continue

                #number token
                if(self.isnumber(self.peak())):
                    value = self.getNumericValue()
                    tokens.append(SSToken(SSTokens.NumberToken, value,self.line, self.current))

                #identifier or keyword
                elif(self.isalphabetic(self.peak())):
                    value = ""
                    while(len(self.chars) > 0 and self.isalphabetic(self.peak())):
                        value+=self.peak()
                        self.get()

                    if value.lower() in SSKEYWORDS.keys():
                        tokens.append(SSToken(SSKEYWORDS[value], value.lower(),self.line, self.current))
                    else:
                        tokens.append(SSToken(SSTokens.IdentifierToken, value.lower(),self.line, self.current))
                
                else:
                    raise SSLexerException(self.peak(), self.line, self.column)

        #add EOF
        tokens.append(SSToken(SSTokens.EOFToken, "EOF",self.line, self.column))

        return tokens