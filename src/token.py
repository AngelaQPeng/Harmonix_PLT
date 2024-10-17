from enum import Enum


class TokenType(Enum):
    KEYWORD = "KEYWORD"
    KEYSIG = "KEYSIG"
    NOTE = "NOTE"
    DURATION = "DURATION"
    IDENTIFIER = "IDENTIFIER"
    INTLITERAL = "INTLITERAL"
    STRINGLITERAL = "STRINGLITERAL"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"


class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f"[{self.type}, {self.value}]"
