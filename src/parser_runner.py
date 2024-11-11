import json
import sys
import re
from parser import Parser

from token import Token


def parse_token_line(line):
    """Parse a line in the format <TOKEN_TYPE, lexeme> and return a tuple (TOKEN_TYPE, lexeme)."""
    match = re.match(r"<(\w+),\s*(.+?)>", line.strip())
    if not match:
        raise ValueError(f"Invalid token format: {line}")
    token_type, lexeme = match.groups()
    lexeme = lexeme.strip('"')
    return token_type, lexeme

def main(input_file, output_file):
    tokens = []
    try:
        with open(input_file, 'r') as file:
            for line in file:
                if line.strip():
                    token = parse_token_line(line)
                    tokens.append(Token(token[0], token[1])) # convert to token
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error parsing tokens: {e}")
        sys.exit(1)

    parser = Parser(tokens)

    try:
        parser.parse_program()
        ast = parser.ast
    except Exception as e:
        print(f"Parser error: {e}")
        sys.exit(1)

    with open(output_file, "w") as file:
        json.dump(ast, file, indent=4)

    print(f"Parsing complete. AST written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parser_runner.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
