import argparse
from scanner import Scanner

def main():
    parser = argparse.ArgumentParser(description="Run the scanner on input files.")
    parser.add_argument("input_file", help="Input file to scan")
    parser.add_argument("output_file", help="File to write output tokens")

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

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
    main()



