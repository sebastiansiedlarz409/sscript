from lexer import Lexer

lexer = Lexer()

#open source file
source = ""
with open("_s1.ss", "r") as f:
    source = f.read()

#tokenize
tokens = lexer.tokenize(source)
for t in tokens: print(t)