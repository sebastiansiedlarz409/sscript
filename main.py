from sslexer import SSLexer

lexer = SSLexer()

#open source file
source = ""
with open("_s2.ss", "r") as f:
    source = f.read()

#tokenize
tokens = lexer.tokenize(source)
for t in tokens: print(t)