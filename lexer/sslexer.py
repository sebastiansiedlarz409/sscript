from lexer.tokens import *
from misc.exceptions import *

import string

class SSLexer:
    def __init__(self):
        self.line = 1
        self.column = 1

    def isalphabetic(self, char: str) -> bool:
        chars = string.ascii_letters + "_"
        return char in chars
    
    def isnumber(self, char: str) -> bool:
        return char in string.digits
    
    def ishexnumber(self, char: str) -> bool:
        return char.lower() in (string.digits+"abcdef")
    
    def isbinnumber(self, char: str) -> bool:
        return char.lower() in (string.digits+"abcdef")
    
    def getNumericValue(self, chars: list[str]) -> str:
        value = ""

        #if hex
        if len(chars) > 1:
            if chars[0] == "0" and chars[1] == "x":
                value+="0x"
                chars.pop(0)
                chars.pop(0)
                while(len(chars) > 0 and (self.ishexnumber(chars[0]) or chars[0] == ".")):
                    #get dot once
                    value+=chars[0]
                    chars.pop(0)
                return value
        
        #if bin
        if len(chars) > 1:
            if chars[0] == "0" and chars[1] == "b":
                value+="0b"
                chars.pop(0)
                chars.pop(0)
                while(len(chars) > 0 and (self.isbinnumber(chars[0]) or chars[0] == ".")):
                    #get dot once
                    value+=chars[0]
                    chars.pop(0)
                return value

        dot = False
        while(len(chars) > 0 and (self.isnumber(chars[0]) or chars[0] == ".")):
            if chars[0] == "." and dot:
                raise SSLexerException(chars[0], self.line, self.column)
            #get dot once
            if chars[0] == ".":
                dot = True
            value+=chars[0]
            chars.pop(0)
        return value
    
    def getStringValue(self, chars: list[str]) -> str:
        value = ""
        while chars[0] in string.printable and chars[0] != '"':
            value += chars[0]
            chars.pop(0)
        return value

    def tokenize(self, source: str) -> list[SSToken]:
        #buffer for tokens
        tokens = []

        #get all characters
        chars = [x for x in source]
        
        #self.line and self.column tracking for errors
        self.line = 1
        self.column = 1

        while(len(chars) > 0):
            if chars[0] in '\t\n\r ':
                self.column+=1
                if chars[0] == '\n':
                    self.line+=1
                    self.column=1
                chars.pop(0)
            elif chars[0] == '(':
                tokens.append(SSToken(SSTokens.LParenToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == ')':
                tokens.append(SSToken(SSTokens.RParenToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == '{':
                tokens.append(SSToken(SSTokens.LBracketToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == '}':
                tokens.append(SSToken(SSTokens.RBracketToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == '[':
                tokens.append(SSToken(SSTokens.LSquareBracketToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == ']':
                tokens.append(SSToken(SSTokens.RSquareBracketToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == '=':
                tokens.append(SSToken(SSTokens.AssignOperatorToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == ',':
                tokens.append(SSToken(SSTokens.CommaToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] == ';':
                tokens.append(SSToken(SSTokens.SemicolonToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            elif chars[0] in '+-*/%|&^<>':
                tokens.append(SSToken(SSTokens.BinaryOperatorToken, chars[0],self.line, self.column))
                chars.pop(0)
                self.column+=1
            else:
                #here we handle multicharacter tokens
                #strings
                if chars[0] == '"':
                    tokens.append(SSToken(SSTokens.QuoteToken, chars[0],self.line, self.column))
                    chars.pop(0)
                    value = self.getStringValue(chars)
                    tokens.append(SSToken(SSTokens.StringToken, value,self.line, self.column))
                    if chars[0] == '"':
                        tokens.append(SSToken(SSTokens.QuoteToken, chars[0],self.line, self.column))
                        chars.pop(0)
                        self.column+=(len(value)+2)
                    continue

                #build number token
                if(self.isnumber(chars[0])):
                    value = self.getNumericValue(chars)
                    tokens.append(SSToken(SSTokens.NumberToken, value,self.line, self.column))
                    self.column+=len(value)

                #build identifier or keyword
                elif(self.isalphabetic(chars[0])):
                    value = ""
                    while(len(chars) > 0 and self.isalphabetic(chars[0])):
                        value+=chars[0]
                        chars.pop(0)

                    if value.lower() in SSKEYWORDS.keys():
                        tokens.append(SSToken(SSKEYWORDS[value], value.lower(),self.line, self.column))
                        self.column+=len(value)
                    else:
                        tokens.append(SSToken(SSTokens.IdentifierToken, value.lower(),self.line, self.column))
                        self.column+=len(value)
                
                else:
                    raise SSLexerException(chars[0], self.line, self.column)

        #add EOF
        tokens.append(SSToken(SSTokens.EOFToken, "EOF",self.line, self.column))

        return tokens