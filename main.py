from lexer.sslexer import SSLexer
from parser.ssparser import SSParser
from runtime.ssruntime import SSRuntime

lexer = SSLexer()
parser = SSParser()
runtime = SSRuntime()

# here i test scoping
# from runtime.ssscope import SSRuntimeScope
# from runtime.values import *
# mainScope = SSRuntimeScope()
# av = NumberRuntimeValue()
# av.setValue(10)
# bv = NumberRuntimeValue()
# bv.setValue(22)
# mainScope.declareValueSymbol("a", av)
# mainScope.declareValueSymbol("b", bv)
# print(mainScope.peakValueSymbol("a"))
# print(mainScope.peakValueSymbol("b"))
# mainScope.assignValueSymbol("a", bv)
# print(mainScope.peakValueSymbol("a"))
# childScope = SSRuntimeScope()
# childScope.setParentScope(mainScope)
# #childScope.declareValueSymbol("a", av) #ok, failed
# print(childScope.peakValueSymbol("a"))
# childScope.assignValueSymbol("a", av)
# print(mainScope.peakValueSymbol("a"))
# print(childScope.peakValueSymbol("a"))
# exit()

# open source file
source = ""
with open("_s2.ss", "r") as f:
    source = f.read()

# tokenize
print("Lexer:")
tokens = lexer.tokenize(source)
for t in tokens: print(t)
print()

# parse
print("Parser:")
program = parser.parseProgram(tokens)
print(program)
print()

# runtime
print("Runtime:")
result = runtime.execute(program)
print(result)