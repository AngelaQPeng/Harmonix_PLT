import sys
import json
from python_generator import PythonCodeGenerator

def main():
    if len(sys.argv) != 3:
        print("Usage: python python_generator_runner.py <input_ast.json> <output_python.py>")
        sys.exit(1)

    input_ast_file = sys.argv[1]
    output_python_file = sys.argv[2]

    try:
        with open(input_ast_file, 'r') as infile:
            ast = json.load(infile)

        generator = PythonCodeGenerator(ast)
        python_code = generator.generate()

        with open(output_python_file, 'w') as outfile:
            outfile.write(python_code)

        print(f"Python code successfully generated and written to {output_python_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
