from lexer.sslexer import *
from parser.ssparser import *
from runtime.ssruntime import *
from runtime.ssscope import *
from misc.exceptions import *

lexer = SSLexer()
parser = SSParser()
runtime = SSRuntime()

try:
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
    globalScope = SSRuntimeScope()
    result = runtime.execute(program, globalScope)
    print(result)
except SSException as x:
    print(x)
