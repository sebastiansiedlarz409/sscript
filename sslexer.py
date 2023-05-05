from tokens.tokens import SSToken, SSTokens, SSKEYWORDS

import string

class SSLexer:
    def __init__(self):
        pass

    def isalphabetic(self, char):
        chars = string.ascii_letters + "_"
        return char in chars
    
    def isnumber(self, char):
        return char in string.digits

    def tokenize(self, source):
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
            elif chars[0] == '=':
                tokens.append(SSToken(SSTokens.AssignOperatorToken, chars[0]))
                chars.pop(0)
            elif chars[0] == ',':
                tokens.append(SSToken(SSTokens.ColonToken, chars[0]))
                chars.pop(0)
            elif chars[0] == ';':
                tokens.append(SSToken(SSTokens.SemicolonToken, chars[0]))
                chars.pop(0)
            elif chars[0] in '!':
                tokens.append(SSToken(SSTokens.UnaryOperatorToken, chars[0]))
                chars.pop(0)
            elif chars[0] in '+-*/%|&':
                tokens.append(SSToken(SSTokens.BinaryOperatorToken, chars[0]))
                chars.pop(0)
            else:
                #here we handle multicharacter tokens

                #build number token
                if(self.isnumber(chars[0])):
                    value = ""
                    while(len(chars) > 0 and self.isnumber(chars[0])):
                        value+=chars[0]
                        chars.pop(0)
                    tokens.append(SSToken(SSTokens.NumberToken, value))

                elif(self.isalphabetic(chars[0])):
                    value = ""
                    while(len(chars) > 0 and self.isalphabetic(chars[0])):
                        value+=chars[0]
                        chars.pop(0)

                    if value in SSKEYWORDS.keys():
                        tokens.append(SSToken(SSKEYWORDS[value], value))
                    else:
                        tokens.append(SSToken(SSTokens.IdentifierToken, value))
                
                else:
                    raise Exception(f"SSLexer: Unknown token {chars[0]}")

        #add EOF
        tokens.append(SSToken(SSTokens.EOFToken, "EOF"))

        return tokens