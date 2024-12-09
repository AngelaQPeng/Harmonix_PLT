# Harmonix_PLT
We are creating a language for encoding musical notations into codes, which would translate musical scores into various formats of digital sheet music. This would allow musicians and music producers to compose in a consistent, readable format. Our harmonix will translate our language into the Python language.

## Team Members
Angela Peng (ap4636), Haoyuan Lu (hl3812)

## Dependency
- Python 3.12: To run the Harmonix Scanner locally, [Python 3.12](https://www.python.org/downloads/release/python-3120/) is required.

### Clone Repository and Install Dependencies

To get started, first clone this repository and navigate to the project directory:

```bash
# Clone the repository
git clone https://github.com/AngelaQPeng/Harmonix_PLT.git
cd Harmonix_PLT
```

# Part 1 - Lexical Scanner

## Program Overview - Lexical Analysis
- /src/token.py:
  - Defines the token types and token class itself
  
- /src/scanner.py: 
  - a lexical scanner that processes music notations codes and tokenizes it.
  - It can recognize 11 token types, including keywords, notes, durations, key signatures, operators, string literals, and more.
  - The lexer scans in a character by character manner, and works on the basis of DFA as discussed in class.
  - The program handles special cases like missing symbols (missing @ 
  in key signatures) by issuing warnings while continuing to scan. 
  - It is built to classify musical notation elements (like clefs, key signatures, and notes) 
  alongside general programming constructs (operators, comments, etc.).
  - It will raise lexical errors when needed.

- /src/scanner_runner.py:
  - Combines command line argument parser and allows file I/O operations
  - Works as the executable for Harmonix Scanner.

## Lexical Grammar Definition

### Keywords
- Token type: KEYWORD
- Description: These are reserved words that define the structure of the music composition or instructions in the language.
- Examples: `clef`, `timeSig`
- Regular Expression: 
```
(clef|timeSig|keySig|pattern|repeat|end|staff|duration|note|title|composer)
```

- `clef`: Specifies the clef (e.g., G, F).
- `timeSig`: Defines the time signature.
- `keySig`: Defines the key signature.
- `pattern`: Defines a musical pattern or phrase.
- `repeat`: Indicates a section to be repeated.
- `end`: Marks the end of a section or composition.
- `staff`: Defines the staff.
- `duration`: Specifies the length of the note.
- `note`: Specifies a musical note.
- `title`: Sets the title of the composition.
- `composer`: Sets the composer of the piece.

### Key Signatures
- Token type: KEYSIG
- Description: Represents a musical key signature
- Examples: `@C Major`, `@C# Minor`
- Regular Expression: 
```
@[A-G][#b]? (Major|Minor)
```

### Notes
- Token type: NOTE
- Description: Musical notes, ranging from pitch (A-G) and octave number (1-7), optionally with sharp # or flat b.
- Examples: `C6`, `D#6`
- Regular Expression: 
```
([A-G][#b]?)([1-7])
```

### Durations
- Token type: DURATION
- Description: Rhythmic durations, representing note lengths in musical notation. Though shorter note values are possible, we are limiting to 16th notes in our program.
- Examples: `whole`, `half`
- Regular Expression: 
```
(whole|half|quarter|eighth|sixteenth)
```

### Identifiers
- Token type: IDENTIFIER
- Description: Represents user-defined names for staffs, patterns, or other musical elements.
- Examples: `pattern1`, `melody1`
- Regular Expression: 
```
[a-zA-Z_][a-zA-Z0-9_]*
```

### Integer Literals
- Token type: INTLITERAL
- Description: Represents numeric values, used to repeat counts or other numerical data
- Examples: `2`, `4` (i.e. repeat 2)
- Regular Expression: 
```
[0-9]+
```

### String Literals
- Token type: STRINGLITERAL
- Description: Represents text enclosed in double quotes, used for titles, composer names, or other free-form text.
- Examples: `"Symphony No. 5"`, `"Ludwig van Beethoven"`
- Regular Expression: 
```
"[^"]*"
```


### Operators
- Token Type: OPERATOR
- Description: Reprsents assignment operators and arithmetic operators.
- Examples: `:=`, `+`, `-`
- Regular Expression: 
```
:=|\+|\-|\*
```

### Delimiters
- Token Type: DELIMITER
- Description: Characters/ punctuations to separate code elements.
- Examples: `{`, `}`
- Regular Expression: 
```
[{},;]
```

### Comments
- Token Type: COMMENT
- Description: Represents comments in source code, starting with // and countinuing until end of line.
- Examples: `//this code snippet...`
- Regular Expression: 
```
\/\/[^\n]*
```

### Whitespaces
- Token Type: WHITESPACE
- Description: Represents spaces, tabs, and newlines that separate tokens but are not part of the actual language syntax.
- Regular Expression: 
```
\s+
```

## Error Handling
We have a combination of warnings and exceptions to catch and report errors early.

### Warnings for Recoverable Errors
We used one `warning.warn()` functionality to raise warnings without halting the execution of the program for issues that do not compeltely break the lexical analysis. This is when the `@` symbol is missing in a key signature, the code would raise a `UserWarning` but continue scanning the rest of the key signature and perform the rest of the lexical analysis.
```
warnings.warn("Missing '@' symbol in key signature. Assuming '@' and continuing...", UserWarning)
```
### Exceptions for Critical Lexical Errors or Invalid Tokens
We created a function `raise_lexical_error()` to raise exception for critical issues that prevent further scanning or when a valid token cannot be formed. These errors stop the scanning process immediately and raise an exception. Specifically, our sample test 3 and 5 in sample_input contains such errors to raise an exception.

## Sample Inputs & Outputs - Lexical Analysis
### Sample Input 1
Sample input 1 is a simple programs that can be correctly tokenized by Harmonix.

### Sample Input 2
Sample input 2 is provided to showcase Harmonix's error handling ability. 
When the '@' is missing from the beginning of the key signature, Harmonix
is still able to classify it as key signature, throw a warning and 
continue to scan. It also contains most of the token classes that can be handled by Harmonix.

### Sample Input 3
Sample input 3 provides an example of key signature syntax error that cannot be
auto-corrected, where 'H Minor' is not a correct key signature token, as it has 
to start with letters 'A-G'. So, a lexical error will be raise.

### Sample Input 4
Sample input 4 provides an example program with correct lexical patterns but contain elements that will result 
in semantic errors during parsing. However, since the focus is currently on lexical analysis, our scanner should correctly tokenize the input and treat all elements as valid lexemes, even when they may not be semantically valid.
1. `keySig` should be followed by a valid `KEYSIG`; however, `H Major` is not a valid `KEYSIG`, but it could be tokenized as an `IDENTIFIER` during lexical analysis. 
2. `note` should be followed by a valid `NOTE`, but  since `H4` does not satisfy the rules for a `NOTE` (it does not start with a letter between `'A-G'`), it can be tokenized as an `IDENTIFIER` during lexical analysis.
3. `duration` should be followed by a valid `DURATION` but `hihihi` is not a valid `DURATION`. It can be tokenized as an `IDENTIFIER` during lexical analysis.

### Sample Input 5
Sample input 5 provides an common syntax error - unclosed quotation mark. So, a lexical error will be raise.

## Run Harmonix Scanner
Once Python 3.12 is installed, you can run the Harmonix Scanner locally with the following command:

```bash
# 'input.txt' needs to be replaced by the actual file name
python3 src/scanner_runner.py sample_input/input.txt runner_output/output.txt

# Running Sample Input 1
python3 src/scanner_runner.py sample_input_lexical/Sample1_input.txt runner_output_lexical/output1.txt

# Running Sample Input 2
python3 src/scanner_runner.py sample_input_lexical/Sample2_input.txt runner_output_lexical/output2.txt

# Running Sample Input 3
python3 src/scanner_runner.py sample_input_lexical/Sample3_input.txt runner_output_lexical/output3.txt

# Running Sample Input 4
python3 src/scanner_runner.py sample_input_lexical/Sample4_input.txt runner_output_lexical/output4.txt

# Running Sample Input 5
python3 src/scanner_runner.py sample_input_lexical/Sample5_input.txt runner_output_lexical/output5.txt
```

input.txt can be replaced with any file located in the $/Harmonix_PLT/sample_input directory.

### Retrieve Output
After running the command,the tokenized output will be written to runner_output/output.txt

# Part 2 - Parser

## Program Overview - Syntactical Analysis
- /src/parser.py: 
  - A syntax parser that processes token stream and constructs an Abstract Syntax Tree (AST)
  - It can recognize hierarchical structures such as program metadata, patterns, notes, durations, repeats, pattern references, nested patterns, and complex expressions involving assignments and arithmetic operations
    - The program is designed to process nested structures, such as repeated pattern references and combined patterns, enabling complex compositions to be represented accurately in the AST
  - The parser works on a recursive-descent basis, analyzing each token sequence in relation to predefined CFG rules for the language
  - It handles syntax errors by raising exceptions when unexpected tokens or structures are encountered, providing informative messages to help identify issues in the input
  - It can also parse and construct AST nodes for statements like title, composer, clef, time signature, key signature, and nested pattern blocks.
  - The parser supports arithmetic expressions in the language, allowing patterns to be combined or referenced within assignments.

- /src/parser_runner.py:
  - Combines command line argument parser and allows file I/O operations
  - Works as the executable for Harmonix Parser.

## Context Free Grammar (CFG)
```
<program> ::= <statement_list> "end"

<statement_list> ::= <statement> | <statement> <statement_list>

<statement> ::= <title_statement> 
              | <composer_statement> 
              | <staff_statement> 
              | <clef_statement> 
              | <time_sig_statement> 
              | <key_sig_statement> 
              | <pattern_definition> 
              | <repeat_statement> 
              | <assignment_statement>

<title_statement> ::= "title" STRINGLITERAL

<composer_statement> ::= "composer" STRINGLITERAL

<staff_statement> ::= "staff" IDENTIFIER

<clef_statement> ::= "clef" IDENTIFIER

<time_sig_statement> ::= "timeSig" STRINGLITERAL

<key_sig_statement> ::= "keySig" KEYSIG

<pattern_definition> ::= "pattern" IDENTIFIER "{" <pattern_body> "}"

<pattern_body> ::= <note_sequence> <pattern_body_tail>

<pattern_body_tail> ::= <note_sequence> <pattern_body_tail> | ε

<note_sequence> ::= <note_statement> 
                  | <repeat_statement> 
                  | IDENTIFIER

<note_statement> ::= "note" NOTE "duration" DURATION

<repeat_statement> ::= "repeat" INTLITERAL "{" <pattern_body> "}"

<assignment_statement> ::= IDENTIFIER ":=" <expression>

<expression> ::= <term> <expression_prime>

<expression_prime> ::= "+" <term> <expression_prime> | ε

<term> ::= IDENTIFIER | <repeat_statement>


```

## Sample Inputs & Outputs - Parser
### Sample Input 1
Sample input 1 is a simple program that can be correctly parsed by Harmonix.

### Sample Input 2
Sample input 2 tests on pattern definitions and nested structures within delimiters. It also checks for proper handling of repeat statements with integer counts and pattern references. It also ensures the parser correctly identifies the end of the program with end.

### Sample Input 3
Sample input 3 tests if parser correctly handles error when there's no end statement. In such case, the parser should raise an error and state "Missing END keyword in the end of the program ...".

### Sample Input 4
Sample input 4 tests on basic arithmetic operations including assignment operator and addition operator. 

### Sample Input 5
Sample input 5 tests on more comprehensive program with multiple pattern identifiers, each with one or multiple nested patterns. It also tests for more advanced arithmetic operations.

### Sample Input 6
Sample input 6 showcases additional error handling capabilities. Specifically, there should be a INTLITERAL after the repeat statement which should be captured by the parser. In the input, we neglected adding an INTLITERAL after the repeat statement, thus, the expected output would be something like "Syntax error: Expected INTLITERAL ... ".

## Run Harmonix Parser
Harmonix Parser can be executed locally with the following command:

```bash
# 'input.txt' needs to be replaced by the actual file name
python3 src/parser_runner.py sample_input/input.txt runner_output/output.txt

# Running Sample Input 1
python3 src/parser_runner.py sample_input_parser/Sample1_input.txt runner_output_parser/output1.txt

# Running Sample Input 2
python3 src/parser_runner.py sample_input_parser/Sample2_input.txt runner_output_parser/output2.txt

# Running Sample Input 3
python3 src/parser_runner.py sample_input_parser/Sample3_input.txt runner_output_parser/output3.txt

# Running Sample Input 4
python3 src/parser_runner.py sample_input_parser/Sample4_input.txt runner_output_parser/output4.txt

# Running Sample Input 5
python3 src/parser_runner.py sample_input_parser/Sample5_input.txt runner_output_parser/output5.txt

# Running Sample Input 6
python3 src/parser_runner.py sample_input_parser/Sample6_input.txt runner_output_parser/output6.txt
```

# Part 3 - Python Code Generator 
## Python Code Generator Introduction 
The Harmonix Python Code Generator transforms an abstract syntax tree (AST) of a Harmonix Music Notations into Python code. 

### Features
1. **AST to Python Code**: Converts AST nodes into Python functions and statements.
2. **Semantic Checking**:
   - Validates that all referenced pattern names are previously defined.
   - Throws an error for undefined pattern references.
   - Throws an error for duplicate definition of a specific pattern.
3. **Unused Pattern Detection**: Removes generated code for patterns that are defined but never used.
4. **Repetition Support**: Handles nested repeat loops by generating Python loops and recursion.

## Semantic Rules
The only semantic checks needed and performed are on **pattern names**, ensuring all referenced patterns are defined. This enforces the language's primary focus on pattern reusability and correctness. 

## Sample Inputs & Outputs - Code Generator 
### Sample Input 1
Sample input 1 is a simple program that can be correctly parsed by Harmonix Python Code generator.

### Sample Input 2
Sample input 2 defines a simple musical composition using the Harmonix language. It includes metadata, a melody pattern, and an assignment operation that manipulates the melody using repetition and addition. The program will generate the corresponding Python code.

### Sample Input 3
Sample input 3 demonstrates pattern definition, nested repetitions, pattern references, and arithmetic operations to construct complex musical structures.

### Sample Input 4
Sample input 4 is similar to sample input 2 with simple input structure that includes all operations defined in our language.

### Sample Input 5
Sample input 5 is similar to sample input 3 with complex AST as input that contains various nested functions.

### Sample Input 6
Sample input 6 showcases symantic analysis ability. Specifically, the addition expression used undefined keyword (pattern name), and it would throw "Error: Undefined pattern referenced: Main"

### Sample Input 7
Sample input 7 showcases dead code elimination. In the input,there is an unused pattern Bridge, thus, the python code generator would throw "Warning: Removing unused patterns: Bridge" and continue to generate Python code without Bridge pattern definition .

### Sample Input 8
Sample input 8 showcases duplicate definition checking. Specifically, the input contains repeated definition of pattern 'MainTheme'. And the generator would throw "Error: Duplicate pattern definition: MainTheme"

## Run Harmonix Parser
Harmonix Parser can be executed locally with the following command:

```bash
# 'input.txt' needs to be replaced by the actual file name
python3 src/_runner.py sample_input/input.txt runner_output/output.txt

# Running Sample Input 1
python3 src/python_generator_runner.py sample_input_codegen/input1.txt runner_output_codegen/output_1.py

# Running Sample Input 2
python3 src/python_generator_runner.py sample_input_codegen/input2.txt runner_output_codegen/output_2.py

# Running Sample Input 3
python3 src/python_generator_runner.py sample_input_codegen/input3.txt runner_output_codegen/output_3.py

# Running Sample Input 4
python3 src/python_generator_runner.py sample_input_codegen/input4.txt runner_output_codegen/output_4.py

# Running Sample Input 5
python3 src/python_generator_runner.py sample_input_codegen/input5.txt runner_output_codegen/output_5.py

# Running Sample Input 6
python3 src/python_generator_runner.py sample_input_codegen/input6.txt runner_output_codegen/output_6.py

# Running Sample Input 7
python3 src/python_generator_runner.py sample_input_codegen/input7.txt runner_output_codegen/output_7.py

# Running Sample Input 8
python3 src/python_generator_runner.py sample_input_codegen/input8.txt runner_output_codegen/output_8.py
```

# Shell Script to Execute Entire Compiler
The `run_harmonix.sh` script automates the process of executing the Harmonix compiler. It includes the following stages:

- Check for Python Installation

- Scanning: Converts the Harmonix source code into tokens using the scanner.
output is `scanner_output.txt`  in output_directory

- Parsing: Processes the tokens to build an Abstract Syntax Tree (AST).
output is `parser_output.txt` in output_directory

- Code Generation: Translates the AST into executable Python code.
output is `output.py` in output_directory

To execute the compiler, use the following command:

```bash
./run_harmonix.sh <input_file> [output_directory]
```

`<input_file>`: The path to the Harmonix source code file.
`[output_directory]`: The directory where all intermediate and final outputs will be stored.

A sample command & sample Harmonix source code with complex, nested structure is already provided in the run_harmonix folder. You can execute it using the following command:
```bash
./run_harmonix.sh run_harmonix_compiler/sample_code.txt run_harmonix_compiler
```

# Video Demonstrations

## Scanner & Parser

https://www.youtube.com/watch?v=rLWjSOUssLg

This video covers the following:
1. Demonstrate how the input is being parsed by the scanner.
2. Demonstrate how the scanner output is fed to the parser to generate AST

## Code Generation

https://youtu.be/__1GN2lB5Sg

This video covers the following:
1. Demonstrate the entire compiler including shell script to generate scanner, parser, and code generation.
2. Demonstration on code generation, dead code elimination, error handling capabilities of code generation portion.