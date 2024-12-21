import sys
import ast
from optimizer import MusicPatternOptimizer

def main():
    if len(sys.argv) != 3:
        print("Usage: python music_optimizer_runner.py <input_python_file> <output_python_file>")
        sys.exit(1)

    input_python_file = sys.argv[1]
    output_python_file = sys.argv[2]

    try:
        with open(input_python_file, 'r') as infile:
            input_code = infile.read()

        optimizer = MusicPatternOptimizer()
        optimized_code = optimizer.optimize(input_code)

        with open(output_python_file, 'w') as outfile:
            outfile.write(optimized_code)

        print(f"Optimized Python code has been written to {output_python_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()