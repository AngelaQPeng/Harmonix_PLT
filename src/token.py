from enum import Enum


class TokenType(Enum):
    KEYWORD = "Keyword"
    NOTE = "Note"
    DURATION = "Duration"
    IDENTIFIER = "Identifier"
    INTLITERAL = "IntLiteral"
    STRINGLITERAL = "StringLiteral"
    OPERATOR = "Operator"
    DELIMITER = "Delimiter"
    COMMENT = "Comment"
    WHITESPACE = "Whitespace"


class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f"[{self.type}, {self.value}]"
