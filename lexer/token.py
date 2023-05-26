from lexer.tokens import *

class SSToken:
    def __init__(self, sstype: SSTokens, value: str, line: int = 0, column: int = 0):
        self.type: SSTokens = sstype
        self.value: str = value
        self.line: int = line
        self.column: int = column

    def __repr__(self) -> str:
        return f"[{self.line}:{self.column}] {self.type} => {self.value}"