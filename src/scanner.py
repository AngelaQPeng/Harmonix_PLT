from token import Token, TokenType
import warnings

class Scanner:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current_pos = 0
        self.tokens = []

    def peek(self):
        if self.current_pos + 1 >= len(self.source_code):
            return None
        return self.source_code[self.current_pos + 1]

    def scan(self):
        while self.current_pos < len(self.source_code):
            char = self.source_code[self.current_pos]
            if char.isspace():
                self.current_pos += 1
            elif char == '"':
                self.scan_string_literal()
            elif char == '/':
                self.scan_comment()
            elif char in '{};,':
                self.scan_delimiter()
            elif char in ':=+-*':
                self.scan_operator()
            elif char == '@':
                self.scan_key_signature()
            elif char.isalpha():
                if self.is_potential_key_signature():
                    self.scan_key_signature()
                else:
                    self.scan_letter()
            elif char.isdigit():
                self.scan_digit()

    def scan_letter(self):
        start_pos = self.current_pos
        while self.current_pos < len(self.source_code) and (
                self.source_code[self.current_pos].isalnum() or self.source_code[self.current_pos] == '_' or self.source_code[self.current_pos] == '#'):
            self.current_pos += 1
        value = self.source_code[start_pos:self.current_pos]
        if value in ['clef', 'timeSig', 'keySig', 'pattern', 'repeat', 'end', 'staff', 'duration', 'note', 'title', 'composer']:
            self.tokens.append(Token(TokenType.KEYWORD, value))
        elif value in ['whole', 'half', 'quarter', 'eighth', 'sixteenth']:
            self.tokens.append(Token(TokenType.DURATION, value))
        elif len(value) == 2 and value[0] in 'ABCDEFG'and value[1] in '1234567':
            self.tokens.append(Token(TokenType.NOTE, value))
        elif len(value) == 3 and value[0] in 'ABCDEFG' and value[1] in 'b#' and value[2] in '01234567':
            self.tokens.append(Token(TokenType.NOTE, value))
        elif '#' in value:
            self.raise_lexical_error("Identifier Error")
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value))

    def scan_key_signature(self):
        start_pos = self.current_pos
        # self.current_pos += 1

        if self.source_code[self.current_pos] == '@':
            self.current_pos += 1  # Move past the '@'
        else:
            warnings.warn("Missing '@' symbol in key signature. Assuming '@' and continuing...", UserWarning)

        if self.current_pos < len(self.source_code) and self.source_code[self.current_pos] in 'ABCDEFG':
            letter = self.source_code[self.current_pos]
            self.current_pos += 1

            optional = ''
            if self.current_pos < len(self.source_code) and self.source_code[self.current_pos] in '#b':
                optional = self.source_code[self.current_pos]
                self.current_pos += 1

            if self.current_pos < len(self.source_code) and self.source_code[self.current_pos] == ' ':
                self.current_pos += 1

                if self.source_code.startswith("Major", self.current_pos):
                    self.current_pos += len("Major")
                    value = '@' + letter + optional + " Major"
                    self.tokens.append(Token(TokenType.KEYSIG, value))
                elif self.source_code.startswith("Minor", self.current_pos):
                    self.current_pos += len("Minor")
                    value = '@' + letter + optional + " Minor"
                    self.tokens.append(Token(TokenType.KEYSIG, value))
                else:
                    self.raise_lexical_error("KeySig Error")
            else:
                self.raise_lexical_error("KeySig Error")
        else:
            self.raise_lexical_error("KeySig Error")

    def scan_digit(self):
        start_pos = self.current_pos
        while self.current_pos < len(self.source_code) and self.source_code[self.current_pos].isdigit():
            self.current_pos += 1
        value = self.source_code[start_pos:self.current_pos]
        self.tokens.append(Token(TokenType.INTLITERAL, value))

    def scan_operator(self):
        if self.peek() == '=':
            if self.source_code[self.current_pos] != ':':
                self.raise_lexical_error("Wrong Operator")
            self.tokens.append(Token(TokenType.OPERATOR, ":="))
            self.current_pos += 2
        else:
            self.tokens.append(Token(TokenType.OPERATOR, self.source_code[self.current_pos]))
            self.current_pos += 1

    def scan_string_literal(self):
        start_pos = self.current_pos
        self.current_pos += 1
        while self.current_pos < len(self.source_code) and self.source_code[self.current_pos] != '"':
            self.current_pos += 1
        if self.current_pos >= len(self.source_code):
            self.raise_lexical_error("Unterminated string literal")
            return
        self.current_pos += 1
        value = self.source_code[start_pos:self.current_pos]
        self.tokens.append(Token(TokenType.STRINGLITERAL, value))


    def scan_delimiter(self):
        self.tokens.append(Token(TokenType.DELIMITER, self.source_code[self.current_pos]))
        self.current_pos += 1

    def scan_comment(self):
        if self.peek() != '/':
            self.raise_lexical_error("Wrong Comment Format")
        while self.current_pos < len(self.source_code) and self.source_code[self.current_pos] != '\n':
            self.current_pos += 1
        if self.current_pos < len(self.source_code):  # Move past the newline if it exists
            self.current_pos += 1

    def raise_lexical_error(self, message):
        raise Exception(f"Lexical Error: {message}")

    def print_error(self, message):
        # Print error and continue scanning
        print(f"ERROR, {message}.")

    def is_potential_key_signature(self):
        lookahead_pos = self.current_pos

        if self.source_code[lookahead_pos] in 'ABCDEFG':
            lookahead_pos += 1

            if lookahead_pos < len(self.source_code) and self.source_code[lookahead_pos] in '#b':
                lookahead_pos += 1

            if lookahead_pos < len(self.source_code) and self.source_code[lookahead_pos] == ' ':
                lookahead_pos += 1

                if self.source_code.startswith("Major", lookahead_pos) or self.source_code.startswith("Minor", lookahead_pos):
                    return True

        return False
