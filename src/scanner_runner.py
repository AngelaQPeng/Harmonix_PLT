import sys
from scanner import Scanner

def main(input_file, output_file):
    # read the input txt file
    with open(input_file, 'r') as file:
        source_code = file.read()

    # run the scaner
    scanner = Scanner(source_code)
    scanner.scan()

    # write the output file
    with open(output_file, 'w+') as file:
        for token in scanner.tokens:
            file.write(f"<{token.type.value}, {token.value}>\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scanner_executable.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    main(input_file, output_file)
