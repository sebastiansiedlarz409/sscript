from enum import Enum

class SSTokens(Enum):
    LetKwToken = 0,
    FuncKwToken = 1,
    ReturnKwToken = 2,
    IfKwToken = 3,
    ElifKwToken = 4,
    ElseKwToken = 5,
    ForKwToken = 6,
    WhileKwToken = 7,
    DoKwToken = 8,
    BreakKwToken = 9,
    ContinueKwToken = 10,
    AndKwToken = 11,
    OrKwToken = 12,
    EqKwToken = 21,
    NeqKwToken = 22,
    GrKwToken = 23,
    GeKwToken = 24,
    LsKwToken = 25,
    LeKwToken = 26,
    NullKwToken = 27,
    TrueKwToken = 28,
    FalseKwToken = 29,
    IdentifierToken = 31,
    AssignOperatorToken = 41,
    UnaryOperatorToken = 42,
    BinaryOperatorToken = 43,
    ColonToken = 51,
    SemicolonToken = 52,
    LParenToken = 53,
    RParenToken = 54,
    LBracketToken = 55, #{}
    RBracketToken = 56,
    LSquareBracketToken = 57, #[]
    RSquareBracketToken = 58,
    NumberToken = 101,
    EOFToken = 9999

SSKEYWORDS = {
    "let" : SSTokens.LetKwToken,
    "func": SSTokens.FuncKwToken,
    "return": SSTokens.ReturnKwToken,
    "if": SSTokens.IfKwToken,
    "elif": SSTokens.ElifKwToken,
    "else": SSTokens.ElseKwToken,
    "for": SSTokens.ForKwToken,
    "while": SSTokens.WhileKwToken,
    "do": SSTokens.DoKwToken,
    "break": SSTokens.BreakKwToken,
    "continue": SSTokens.ContinueKwToken,
    "and": SSTokens.AndKwToken,
    "or": SSTokens.OrKwToken,
    "not": SSTokens.UnaryOperatorToken,
    "eq": SSTokens.EqKwToken,
    "neq": SSTokens.NeqKwToken,
    "gr": SSTokens.GrKwToken,
    "ge": SSTokens.GeKwToken,
    "ls": SSTokens.LsKwToken,
    "le": SSTokens.LeKwToken,
    "true": SSTokens.TrueKwToken,
    "false": SSTokens.FalseKwToken,
    "null": SSTokens.NullKwToken
}

class SSToken:
    def __init__(self, sstype: SSTokens, value: str):
        self.type: SSTokens = sstype
        self.value: str = value

    def __repr__(self) -> str:
        return f"{self.type} => {self.value}"