from sslexer import SSLexer
from ssparser import SSParser

lexer = SSLexer()
parser = SSParser()

#open source file
source = ""
with open("_s2.ss", "r") as f:
    source = f.read()

#tokenize
print("Lexer:")
tokens = lexer.tokenize(source)
for t in tokens: print(t)
print()

print("Parser:")
#parse
program = parser.parseProgram(tokens)
print(program)
print()