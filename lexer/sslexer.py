from lexer.tokens import SSToken, SSTokens, SSKEYWORDS

import string

class SSLexer:
    def __init__(self):
        pass

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
                raise Exception(f"SSLexer: Floating point value cant contains only one dot")
            #get dot once
            if chars[0] == ".":
                dot = True
            value+=chars[0]
            chars.pop(0)
        return value

    def tokenize(self, source: str) -> list[SSToken]:
        #buffer for tokens
        tokens = []

        #get all characters
        chars = [x for x in source.lower()]

        while(len(chars) > 0):
            if chars[0] in '\t\n\r ':
                chars.pop(0)
            elif chars[0] == '(':
                tokens.append(SSToken(SSTokens.LParenToken, chars[0]))
                chars.pop(0)
            elif chars[0] == ')':
                tokens.append(SSToken(SSTokens.RParenToken, chars[0]))
                chars.pop(0)
            elif chars[0] == '{':
                tokens.append(SSToken(SSTokens.LBracketToken, chars[0]))
                chars.pop(0)
            elif chars[0] == '}':
                tokens.append(SSToken(SSTokens.RBracketToken, chars[0]))
                chars.pop(0)
            elif chars[0] == '[':
                tokens.append(SSToken(SSTokens.LSquareBracketToken, chars[0]))
                chars.pop(0)
            elif chars[0] == ']':
                tokens.append(SSToken(SSTokens.RSquareBracketToken, chars[0]))
                chars.pop(0)
            elif chars[0] == '=':
                tokens.append(SSToken(SSTokens.AssignOperatorToken, chars[0]))
                chars.pop(0)
            elif chars[0] == ',':
                tokens.append(SSToken(SSTokens.ColonToken, chars[0]))
                chars.pop(0)
            elif chars[0] == ';':
                tokens.append(SSToken(SSTokens.SemicolonToken, chars[0]))
                chars.pop(0)
            elif chars[0] in '+-*/%|&^<>':
                tokens.append(SSToken(SSTokens.BinaryOperatorToken, chars[0]))
                chars.pop(0)
            else:
                #here we handle multicharacter tokens

                #build number token
                if(self.isnumber(chars[0])):
                    value = self.getNumericValue(chars)
                    tokens.append(SSToken(SSTokens.NumberToken, value))

                elif(self.isalphabetic(chars[0])):
                    value = ""
                    while(len(chars) > 0 and self.isalphabetic(chars[0])):
                        value+=chars[0]
                        chars.pop(0)

                    if value.lower() in SSKEYWORDS.keys():
                        tokens.append(SSToken(SSKEYWORDS[value], value))
                    else:
                        tokens.append(SSToken(SSTokens.IdentifierToken, value))
                
                else:
                    raise Exception(f"SSLexer: Unknown token {chars[0]}")

        #add EOF
        tokens.append(SSToken(SSTokens.EOFToken, "EOF"))

        return tokens