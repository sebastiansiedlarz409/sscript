from enum import Enum

class SSToken:
    def __init__(self, sstype, value):
        self.type = sstype
        self.value = value

    def __repr__(self):
        return f"{self.type} => {self.value}"

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
    NotKwToken = 13,
    EqKwToken = 21,
    NeqKwToken = 22,
    GrKwToken = 23,
    GeKwToken = 24,
    LsKwToken = 25,
    LeKwToken = 26,
    NullKwToken = 27,
    IdentifierToken = 31,
    AssignOperatorToken = 41,
    UnaryOperatorToken = 42,
    BinaryOperatorToken = 43,
    ColonToken = 51,
    SemicolonToken = 52,
    LParenToken = 53,
    RParenToken = 54,
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
    "not": SSTokens.NotKwToken,
    "eq": SSTokens.EqKwToken,
    "neq": SSTokens.NeqKwToken,
    "gr": SSTokens.GrKwToken,
    "ge": SSTokens.GeKwToken,
    "ls": SSTokens.LsKwToken,
    "le": SSTokens.LeKwToken,
    "null": SSTokens.NullKwToken
}
