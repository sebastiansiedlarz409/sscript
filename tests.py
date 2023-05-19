from lexer.sslexer import *
from misc.exceptions import *
from parser.ssparser import *
from runtime.ssscope import *
from runtime.ssruntime import *

def execute(source, db = False):
    lexer = SSLexer()
    parser = SSParser()
    runtime = SSRuntime()

    tokens = lexer.tokenize(source)
    if db == True:
        for t in tokens: print(t)

    program = parser.parseProgram(tokens)
    if db == True:
        print(program)

    globalScope = SSRuntimeScope()
    result = runtime.execute(program, globalScope)
    if db == True:
        print(result)

    return str(result)

def t1():
    s = ""
    with open("tests\\t1.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "0":
            print("T1 OK")
            return
    except Exception as x:
        print(x)

    result = execute(s, True)
    print("T1 NOT OK")

def t2():
    s = ""
    with open("tests\\t2.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "false":
            print("T2 OK")
            return
    except Exception as x:
        print(x)

    result = execute(s, True)
    print("T2 NOT OK")

def t3():
    s = ""
    with open("tests\\t3.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "EBAtrue99":
            print("T3 OK")
            return
    except Exception as x:
        print(x)

    result = execute(s, True)
    print("T3 NOT OK")

def t4():
    s = ""
    with open("tests\\t4.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "true":
            print("T4 OK")
            return
    except Exception as x:
        print(x)

    result = execute(s, True)
    print("T4 NOT OK")

def t5():
    s = ""
    with open("tests\\t5.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "100":
            print("T5 OK")
            return
    except Exception as x:
        print(x)

    result = execute(s, True)
    print("T5 NOT OK")

def t6():
    s = ""
    with open("tests\\t6.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "512":
            print("T6 OK")
            return
    except Exception as x:
        print(x)

    result = execute(s, True)
    print("T6 NOT OK")

def t6():
    s = ""
    with open("tests\\t7.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "10":
            print("T7 OK")
            return
    except Exception as x:
        print(x)

    result = execute(s, True)
    print("T7 NOT OK")

print()
print("TEST TEST TEST")
t1()
t2()
t3()
t4()
t5()
t6()