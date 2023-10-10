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
        else:
            print("T1 NOT OK")
    except Exception as x:
        print("T1 NOT OK")

def t2():
    s = ""
    with open("tests\\t2.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "false":
            print("T2 OK")
        else:
            print("T2 NOT OK")
    except Exception as x:
        print("T2 NOT OK")

def t3():
    s = ""
    with open("tests\\t3.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "EBAtrue99":
            print("T3 OK")
        else:
            print("T3 NOT OK")
    except Exception as x:
        print("T3 NOT OK")

def t4():
    s = ""
    with open("tests\\t4.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "true":
            print("T4 OK")
        else:
            print("T4 NOT OK")
    except Exception as x:
        print("T4 NOT OK")

def t5():
    s = ""
    with open("tests\\t5.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "100":
            print("T5 OK")
        else:
            print("T5 NOT OK")
    except Exception as x:
        print("T5 NOT OK")

def t6():
    s = ""
    with open("tests\\t6.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "512":
            print("T6 OK")
        else:
            print("T6 NOT OK")
    except Exception as x:
        print("T6 NOT OK")

def t7():
    s = ""
    with open("tests\\t7.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "10":
            print("T7 OK")
        else:
            print("T7 NOT OK")
    except Exception as x:
        print("T7 NOT OK")

def t8():
    s = ""
    with open("tests\\t8.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "false":
            print("T8 OK")
        else:
            print("T8 NOT OK")
    except Exception as x:
        print("T8 NOT OK")

def t9():
    s = ""
    with open("tests\\t9.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "false":
            print("T9 OK")
        else:
            print("T9 NOT OK")
    except Exception as x:
        print("T9 NOT OK")

def t10():
    s = ""
    with open("tests\\t10.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "-9":
            print("T10 OK")
        else:
            print("T10 NOT OK")
    except Exception as x:
        print("T10 NOT OK")

def t11():
    s = ""
    with open("tests\\t11.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "2":
            print("T11 OK")
        else:
            print("T11 NOT OK")
    except Exception as x:
        print("T11 NOT OK")

def t12():
    s = ""
    with open("tests\\t12.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "-1":
            print("T12 OK")
        else:
            print("T12 NOT OK")
    except Exception as x:
        print("T12 NOT OK")

def t13():
    s = ""
    with open("tests\\t13.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "null":
            print("T13 OK")
        else:
            print("T13 NOT OK")
    except Exception as x:
        print("T13 NOT OK")

def t14():
    s = ""
    with open("tests\\t14.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "4":
            print("T14 OK")
        else:
            print("T14 NOT OK")
    except Exception as x:
        print("T14 NOT OK")

def t15():
    s = ""
    with open("tests\\t15.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "255":
            print("T15 OK")
        else:    
            print("T15 NOT OK")
    except Exception as x:
        print("T15 NOT OK")

def t16():
    s = ""
    with open("tests\\t16.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "20":
            print("T16 OK")
        else:
            print("T16 NOT OK")
    except Exception as x:
        print("T16 NOT OK")

def t17():
    s = ""
    with open("tests\\t17.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "40":
            print("T17 OK")
        else:
            print("T17 NOT OK")
    except Exception as x:
        print("T17 NOT OK")

def t18():
    s = ""
    with open("tests\\t18.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "1":
            print("T18 OK")
        else:
            print("T18 NOT OK")
    except Exception as x:
        print("T18 NOT OK")

def t19():
    s = ""
    with open("tests\\t19.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "3":
            print("T19 OK")
        else:    
            print("T19 NOT OK")
    except Exception as x:
        print("T19 NOT OK")

def t20():
    s = ""
    with open("tests\\t20.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T20 NOT OK")
    except SSLexerException as x:
        if x.got == '`' and x.line == 2 and x.column == 1:
            print("T20 OK")
        else:
            print("T20 NOT OK")

def t21():
    s = ""
    with open("tests\\t21.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T21 NOT OK")
    except SSLexerException as x:
        if x.got == '.' and x.line == 1 and x.column == 12:
            print("T21 OK")
        else:
            print("T21 NOT OK")

def t22():
    s = ""
    with open("tests\\t22.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T22 NOT OK")
    except SSLexerException as x:
        if x.got == '~' and x.line == 1 and x.column == 42:
            print("T22 OK")
        else:
            print("T22 NOT OK")

def t23():
    s = ""
    with open("tests\\t23.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T23 NOT OK")
    except SSParserException as x:
        if x.got.type == SSTokens.NumberToken and x.got.line == 1 and x.got.column == 16:
            print("T23 OK")
        else:
            print("T23 NOT OK")

def t24():
    s = ""
    with open("tests\\t24.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T24 NOT OK")
    except SSParserException as x:
        if x.expected == SSTokens.IdentifierToken and x.got.line == 1 and x.got.column == 6:
            print("T24 OK")
        else:
            print("T24 NOT OK")

def t25():
    s = ""
    with open("tests\\t25.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T25 NOT OK")
    except SSParserException as x:
        if x.expected == SSTokens.SemicolonToken and x.got.line == 3 and x.got.column == 23:
            print("T25 OK")
        else:
            print("T25 NOT OK")

def t26():
    s = ""
    with open("tests\\t26.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T26 NOT OK")
    except SSParserUnexpectedException as x:
        if x.got.value == "=" and x.got.line == 3 and x.got.column == 5:
            print("T26 OK")
        else:
            print("T26 NOT OK")

def t27():
    s = ""
    with open("tests\\t27.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T27 NOT OK")
    except SSParserException as x:
        print("T27 OK")

def t28():
    s = ""
    with open("tests\\t28.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "1":
            print("T28 OK")
        else:
            print("T28 NOT OK")
    except Exception as x:
        print("T28 NOT OK")

def t29():
    s = ""
    with open("tests\\t29.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "0":
            print("T29 OK")
        else:
            print("T29 NOT OK")
    except Exception as x:
        print("T29 NOT OK")

def t30():
    s = ""
    with open("tests\\t30.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "13":
            print("T30 OK")
        else:    
            print("T30 NOT OK")
    except Exception as x:
        print("T30 NOT OK")

def t31():
    s = ""
    with open("tests\\t31.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "0":
            print("T31 OK")
        else:    
            print("T31 NOT OK")
    except Exception as x:
        print("T31 NOT OK")

def t32():
    s = ""
    with open("tests\\t32.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "3":
            print("T32 OK")
        else:
            print("T32 NOT OK")
    except Exception as x:
        print("T32 NOT OK")

def t33():
    s = ""
    with open("tests\\t33.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "3":
            print("T33 OK")
        else:
            print("T33 NOT OK")
    except Exception as x:
        print("T33 NOT OK")

def t34():
    s = ""
    with open("tests\\t34.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "0":
            print("T34 OK")
        else:
            print("T34 NOT OK")
    except Exception as x:
        print("T34 NOT OK")

def t35():
    s = ""
    with open("tests\\t35.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "2":
            print("T35 OK")
        else:
            print("T35 NOT OK")
    except Exception as x:
        print("T35 NOT OK")

def t36():
    s = ""
    with open("tests\\t36.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "10":
            print("T36 OK")
        else:
            print("T36 NOT OK")
    except Exception as x:
        print("T36 NOT OK")

def t37():
    s = ""
    with open("tests\\t37.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "3":
            print("T37 OK")
        else:
            print("T37 NOT OK")
    except Exception as x:
        print("T37 NOT OK")

def t38():
    s = ""
    with open("tests\\t38.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T38 NOT OK")
    except SSException as x:
        print("T38 OK")

def t39():
    s = ""
    with open("tests\\t39.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "88":
            print("T39 OK")
        else:
            print("T39 NOT OK")
    except Exception as x:
        print("T39 NOT OK")

def t40():
    s = ""
    with open("tests\\t40.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T40 NOT OK")
    except SSException as x:
        print("T40 OK")

def t41():
    s = ""
    with open("tests\\t41.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T41 NOT OK")
    except SSException as x:
        print("T41 OK")

def t42():
    s = ""
    with open("tests\\t42.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T42 NOT OK")
    except SSException as x:
        print("T42 OK")

def t43():
    s = ""
    with open("tests\\t43.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T43 NOT OK")
    except SSException as x:
        print("T43 OK")

def t44():
    s = ""
    with open("tests\\t44.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T44 OK")
    except SSException as x:
        print("T44 NOT OK")

def t45():
    s = ""
    with open("tests\\t45.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T45 OK")
    except SSException as x:
        print("T45 NOT OK")

def t46():
    s = ""
    with open("tests\\t46.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "1":
            print("T46 OK")
        else:
            print("T46 NOT OK")
    except SSException as x:
        print("T46 NOT OK")

def t47():
    s = ""
    with open("tests\\t47.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "3":
            print("T47 OK")
        else:
            print("T47 NOT OK")
    except SSException as x:
        print("T47 NOT OK")

def t48():
    s = ""
    with open("tests\\t48.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "10":
            print("T48 OK")
        else:
            print("T48 NOT OK")
    except SSException as x:
        print("T48 NOT OK")

def t49():
    s = ""
    with open("tests\\t49.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "Koko":
            print("T49 OK")
        else:
            print("T49 NOT OK")
    except SSException as x:
        print("T49 NOT OK")

def t50():
    s = ""
    with open("tests\\t50.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T50 NOT OK")
    except SSException as x:
        print("T50 OK")

def t51():
    s = ""
    with open("tests\\t51.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "12":
            print("T51 OK")
        else:
            print("T51 NOT OK")
    except SSException as x:
        print("T51 NOT OK")

def t52():
    s = ""
    with open("tests\\t52.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "18":
            print("T52 OK")
        else:
            print("T52 NOT OK")
    except SSException as x:
        print("T52 NOT OK")

def t53():
    s = ""
    with open("tests\\t53.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "Field is equal to: 18":
            print("T53 OK")
        else:
            print("T53 NOT OK")
    except SSException as x:
        print("T53 NOT OK")

def t54():
    s = ""
    with open("tests\\t54.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "Field is equal to: 18":
            print("T54 OK")
        else:
            print("T54 NOT OK")
    except SSException as x:
        print("T54 NOT OK")

def t55():
    s = ""
    with open("tests\\t55.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T55 NOT OK")
    except SSException as x:
        print("T55 OK")

def t56():
    s = ""
    with open("tests\\t56.ss", "r") as f:
        s = f.read()

    try:
        execute(s)
        print("T56 NOT OK")
    except SSException as x:
        print("T56 OK")

def t57():
    s = ""
    with open("tests\\t57.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "Field is equal to: 6":
            print("T57 OK")
        else:
            print("T57 NOT OK")
    except SSException as x:
        print("T57 NOT OK")

def t58():
    s = ""
    with open("tests\\t58.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "24 6":
            print("T58 OK")
        else:
            print("T58 NOT OK")
    except SSException as x:
        print("T58 NOT OK")

def t59():
    s = ""
    with open("tests\\t59.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "6":
            print("T59 OK")
        else:
            print("T59 NOT OK")
    except SSException as x:
        print("T59 NOT OK")

def t60():
    s = ""
    with open("tests\\t60.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "24":
            print("T60 OK")
        else:
            print("T60 NOT OK")
    except SSException as x:
        print("T60 NOT OK")

def t61():
    s = ""
    with open("tests\\t61.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "Im child":
            print("T61 OK")
        else:
            print("T61 NOT OK")
    except SSException as x:
        print("T61 NOT OK")

def t62():
    s = ""
    with open("tests\\t62.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "10":
            print("T62 OK")
        else:
            print("T62 NOT OK")
    except SSException as x:
        print("T62 NOT OK")

def t63():
    s = ""
    with open("tests\\t63.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "22":
            print("T63 OK")
        else:
            print("T63 NOT OK")
    except SSException as x:
        print("T63 NOT OK")

def t64():
    s = ""
    with open("tests\\t64.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "1":
            print("T64 OK")
        else:
            print("T64 NOT OK")
    except SSException as x:
        print("T64 NOT OK")

def t65():
    s = ""
    with open("tests\\t65.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "2":
            print("T65 OK")
        else:
            print("T65 NOT OK")
    except SSException as x:
        print("T65 NOT OK")

def t66():
    s = ""
    with open("tests\\t66.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "3":
            print("T66 OK")
        else:
            print("T66 NOT OK")
    except SSException as x:
        print("T66 NOT OK")

def t67():
    s = ""
    with open("tests\\t67.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "3":
            print("T67 OK")
        else:
            print("T67 NOT OK")
    except SSException as x:
        print("T67 NOT OK")

def t68():
    s = ""
    with open("tests\\t68.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "99":
            print("T68 OK")
        else:
            print("T68 NOT OK")
    except SSException as x:
        print("T68 NOT OK")

def t69():
    s = ""
    with open("tests\\t69.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "2":
            print("T69 OK")
        else:
            print("T69 NOT OK")
    except SSException as x:
        print("T69 NOT OK")

def t70():
    s = ""
    with open("tests\\t70.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "4":
            print("T70 OK")
        else:
            print("T70 NOT OK")
    except SSException as x:
        print("T70 NOT OK")

def t71():
    s = ""
    with open("tests\\t71.ss", "r") as f:
        s = f.read()

    try:
        result = execute(s)
        if result == "1":
            print("T71 OK")
        else:
            print("T71 NOT OK")
    except SSException as x:
        print("T71 NOT OK")

print()
print("TEST TEST TEST")

tests = list(filter(lambda x: str(x).startswith("t"), dir()))
tests.sort(key = lambda x: int(x[1:]))
for t in tests:
    globals()[t]()