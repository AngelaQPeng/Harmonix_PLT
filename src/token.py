from enum import Enum


class TokenType(Enum):
    IDENTIFIER = "Identifier"
    NOTE = "Note"
    DURATION = "Duration"
    KEYWORD = "Keyword"
    STRINGLITERAL = "StringLiteral"
    OPERATOR = "Operator"
    DELIMITER = "Delimiter"
    INTLITERAL = "IntLiteral"
    COMMENT = "Comment"
    WHITESPACE = "Whitespace"


class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f"[{self.type}, {self.value}]"
