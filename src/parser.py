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
        while not self.check("KEYWORD", "end"):
            self.ast["statements"].append(self.parse_statement())

    def parse_statement(self):
        """Parse a statement according to the type of the current token."""
        if self.check("KEYWORD", "title"):
            return self.parse_title_statement()
        elif self.check("KEYWORD", "composer"):
            return self.parse_composer_statement()
        elif self.check("KEYWORD", "staff"):
            return self.parse_staff_statement()
        elif self.check("KEYWORD", "clef"):
            return self.parse_clef_statement()
        elif self.check("KEYWORD", "timeSig"):
            return self.parse_time_sig_statement()
        elif self.check("KEYWORD", "keySig"):
            return self.parse_key_sig_statement()
        elif self.check("KEYWORD", "pattern"):
            return self.parse_pattern_definition()
        elif self.check("IDENTIFIER") and self.peek("OPERATOR", ":="):
            return self.parse_assignment_statement()
        else:
            self.raise_error("Unexpected token in statement")

    def parse_title_statement(self):
        self.consume("KEYWORD", "title")
        title = self.consume("STRINGLITERAL").value
        return {"type": "title_statement", "title": title}

    def parse_composer_statement(self):
        self.consume("KEYWORD", "composer")
        composer = self.consume("STRINGLITERAL").value
        return {"type": "composer_statement", "composer": composer}

    def parse_staff_statement(self):
        self.consume("KEYWORD", "staff")
        staff = self.consume("IDENTIFIER").value
        return {"type": "staff_statement", "staff": staff}

    def parse_clef_statement(self):
        self.consume("KEYWORD", "clef")
        clef = self.consume("IDENTIFIER").value
        return {"type": "clef_statement", "clef": clef}

    def parse_time_sig_statement(self):
        self.consume("KEYWORD", "timeSig")
        time_sig = self.consume("STRINGLITERAL").value
        return {"type": "time_sig_statement", "timeSig": time_sig}

    def parse_key_sig_statement(self):
        self.consume("KEYWORD", "keySig")
        key_sig = self.consume("KEYSIG").value
        return {"type": "key_sig_statement", "keySig": key_sig}

    def parse_pattern_definition(self):
        self.consume("KEYWORD", "pattern")
        pattern_name = self.consume("IDENTIFIER").value
        self.consume("DELIMITER", "{")
        pattern_body = self.parse_pattern_body()
        self.consume("DELIMITER", "}")
        return {"type": "pattern_definition", "name": pattern_name, "body": pattern_body}

    def parse_pattern_body(self):
        body = []
        while not self.check("DELIMITER", "}"):
            body.append(self.parse_note_sequence())
        return body

    def parse_note_sequence(self):
        if self.check("KEYWORD", "note"):
            return self.parse_note_statement()
        elif self.check("KEYWORD", "repeat"):
            return self.parse_repeat_statement()
        elif self.check("KEYWORD", "pattern"):
            return self.parse_pattern_definition()
        else:
            self.raise_error("Unexpected token in note sequence")

    def parse_note_statement(self):
        self.consume("KEYWORD", "note")
        note = self.consume("NOTE").value
        self.consume("KEYWORD", "duration")
        duration = self.consume("DURATION").value
        return {"type": "note_statement", "note": note, "duration": duration}

    def parse_repeat_statement(self):
        self.consume("KEYWORD", "repeat")
        count = int(self.consume("INTLITERAL").value)
        self.consume("DELIMITER", "{")
        repeat_body = self.parse_pattern_body()
        self.consume("DELIMITER", "}")
        return {"type": "repeat_statement", "count": count, "body": repeat_body}

    def parse_assignment_statement(self):
        name = self.consume("IDENTIFIER").value
        self.consume("OPERATOR", ":=")
        expression = self.parse_expression()
        return {"type": "assignment_statement", "name": name, "expression": expression}

    def parse_expression(self):
        term = self.parse_term()
        if self.peek("OPERATOR", "+"):
            self.consume("OPERATOR", "+")
            right_expression = self.parse_expression()
            return {
                "type": "addition_expression",
                "operator": "+",
                "left": term,
                "right": right_expression
            }
        else:
            return term

    def parse_term(self):
        if self.check("IDENTIFIER"):
            return {"type": "identifier", "name": self.consume("IDENTIFIER").value}
        elif self.check("KEYWORD", "pattern"):
            return self.parse_pattern_definition()
        elif self.check("KEYWORD", "repeat"):
            return self.parse_repeat_statement()
        else:
            self.raise_error("Expected a pattern, repeat, or identifier in expression")

    def advance(self):
        """Advance to the next token in the token list."""
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def check(self, expected_type, expected_value=None):
        """Check if the current token matches the expected token's type and value."""
        return (self.current_token and self.current_token.type == expected_type and
                (expected_value is None or self.current_token.value == expected_value))

    def consume(self, expected_type, expected_value=None):
        """Consume a token if it matches the expected token."""
        if self.check(expected_type, expected_value):
            token = self.current_token
            self.advance()
            return token
        else:
            self.raise_error(f"Expected {expected_type} {expected_value if expected_value else ''}")

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
