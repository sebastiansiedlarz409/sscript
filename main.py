from lexer.sslexer import SSLexer
from parser.ssparser import SSParser
from runtime.ssruntime import SSRuntime

lexer = SSLexer()
parser = SSParser()
runtime = SSRuntime()

#open source file
source = ""
with open("_s2.ss", "r") as f:
    source = f.read()

#tokenize
print("Lexer:")
tokens = lexer.tokenize(source)
for t in tokens: print(t)
print()

#parse
print("Parser:")
program = parser.parseProgram(tokens)
print(program)
print()
exit()

#runtime
print("Runtime:")
result = runtime.execute(program)
print(result)