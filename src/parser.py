class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = self.tokens[0]
        self.index = 0
        self.ast = dict()

    def parse_program(self):
        """Parse the entire program"""
        self.ast["type"] = "program"
        self.ast["statements"] = list()
        while not self.match("KEYWORD", "end"):
            self.ast["statements"].append(self.parse_statement())

    def parse_statement(self):
        """Parse a statement according to the type of the current token."""
        if self.match("KEYWORD", "title"):
            return self.parse_title_statement()
        elif self.match("KEYWORD", "composer"):
            return self.parse_composer_statement()
        elif self.match("KEYWORD", "staff"):
            return self.parse_staff_statement()
        elif self.match("KEYWORD", "clef"):
            return self.parse_clef_statement()
        elif self.match("KEYWORD", "timeSig"):
            return self.parse_time_sig_statement()
        elif self.match("KEYWORD", "keySig"):
            return self.parse_key_sig_statement()
        elif self.match("KEYWORD", "pattern"):
            return self.parse_pattern_definition()
        elif self.check("IDENTIFIER") and self.peek("OPERATOR", ":="):
            return self.parse_assignment_statement()
        else:
            self.raise_error("Unexpected token in statement")

    def parse_title_statement(self):
        pass

    def parse_composer_statement(self):
        pass

    def parse_staff_statement(self):
        pass

    def parse_clef_statement(self):
        pass

    def parse_time_sig_statement(self):
        pass

    def parse_key_sig_statement(self):
        pass

    def parse_pattern_definition(self):
        pass

    def parse_assignment_statement(self):
        pass

    def advance(self):
        """Advance to the next token in the token list."""
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def check(self, expected_type, expected_value=None):
        """Check if the current token matches the expected token's type and value."""
        return (self.current_token and self.current_token[0] == expected_type and
                (expected_value is None or self.current_token[1] == expected_value))

    def consume(self, expected_type, expected_value=None):
        """Consume a token if it matches the expected token."""
        if self.check(expected_type, expected_value):
            token = self.current_token
            self.advance()
            return token
        else:
            self.raise_error(f"Expected {expected_type} {expected_value if expected_value else ''}")

    def match(self, expected_type, expected_value=None):
        """Advance if the current token matches the expected token."""
        if self.check(expected_type, expected_value):
            self.advance()
            return True
        return False

    def peek(self, expected_type, expected_value=None):
        """Look ahead to check if the next token matches the token."""
        if self.index + 1 < len(self.tokens):
            next_token = self.tokens[self.index + 1]
            typeMatch = next_token.type == expected_type
            valueMatch = expected_value is None or next_token.value == expected_value
            return typeMatch and valueMatch
        return False

    def raise_error(self, message):
        """Raise syntax error."""
        raise SyntaxError(f"Syntax error: {message} at token {self.current_token}")
