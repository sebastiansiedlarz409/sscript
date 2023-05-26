from lexer.tokens import *
from lexer.token import *

class SSException(Exception):
    def __init__ (self, message: str):
        super().__init__(message)

class SSLexerException(SSException):
    def __init__ (self, got: str, line: int, column: int):
        self.got = got
        self.line = line
        self.column = column
        message = f"SSLexer: Unexpected token '{got}' at [{line}:{column}]"
        super().__init__(message)

class SSParserException(SSException):
    def __init__ (self, expected, got: SSToken):
        self.expected = expected
        self.got = got
        message = f"SSParser: Expected {expected} but got {got.type} ({got.value}) at [{got.line}:{got.column}]"
        super().__init__(message)