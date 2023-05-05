from enum import Enum

class SSToken:
    def __init__(self, sstype, value):
        self.type = sstype
        self.value = value

    def __repr__(self):
        return f"{self.type} => {self.value}"

class SSTokens(Enum):
    LetKwToken = 0,
    FuncKwToken = 0,
    ReturnKwToken = 0,
    IfKwToken = 0,
    ElifKwToken = 0,
    ElseKwToken = 0,
    ForKwToken = 0,
    WhileKwToken = 0,
    DoKwToken = 0,
    BreakKwToken = 0,
    ContinueKwToken = 0,
    IdentifierToken = 1,
    AssignOperatorToken = 2,
    UnaryOperatorToken = 3,
    BinaryOperatorToken = 4,
    ColonToken = 9,
    SemicolonToken = 10,
    LParenToken = 11,
    RParenToken = 12,
    NumberToken = 13,
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
    "continue": SSTokens.ContinueKwToken
}
