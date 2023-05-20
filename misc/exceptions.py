from lexer.tokens import *

class SSException(Exception):
    def __init__ (self, message: str):
        super().__init__(message)

class SSParserException(SSException):
    def __init__ (self, expected, got: SSToken):
        self.expected = expected
        self.got = got
        message = f"Expected {expected} but got {got.type} ({got.value}) at at [{got.line}:{got.column}]"
        super().__init__(message)