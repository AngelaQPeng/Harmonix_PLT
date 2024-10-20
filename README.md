# Harmonix_PLT
We are creating a language for encoding musical notations into codes, which would translate musical scores into various formats of digital sheet music. This would allow musicians and music producers to compose in a consistent, readable format.

## Team Members
Angela Peng (ap4636), Haoyuan Lu (hl3812)

## Dependency
- Docker: To run the Harmonix Scanner locally, [Docker](https://www.docker.com/) is required.

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

## Installation
### Build Docker Image
To build the Docker image, navigate to the project root directory where the `Dockerfile` is located and run the following command:
```bash
docker build -t python-scanner .
```

### Run Docker Image
Once the Docker image is built,  run the container with the following command:
```bash
# 'input.txt' needs to be replaced by actual file name 
docker run -v $(pwd)/sample_input:/Harmonix/sample_input -v $(pwd)/runner_output:/Harmonix/runner_output python-scanner /Harmonix/sample_input/input.txt /Harmonix/runner_output/output.txt
```

Similarly, all the five sample_input can be executed by running the following command:
```bash
# Running Sample Input 1
docker run -v $(pwd)/sample_input:/Harmonix/sample_input -v $(pwd)/runner_output:/Harmonix/runner_output python-scanner /Harmonix/sample_input/Sample1_input.txt /Harmonix/runner_output/output1.txt
# Running Sample Input 2
docker run -v $(pwd)/sample_input:/Harmonix/sample_input -v $(pwd)/runner_output:/Harmonix/runner_output python-scanner /Harmonix/sample_input/Sample2_input.txt /Harmonix/runner_output/output2.txt
# Running Sample Input 3
docker run -v $(pwd)/sample_input:/Harmonix/sample_input -v $(pwd)/runner_output:/Harmonix/runner_output python-scanner /Harmonix/sample_input/Sample3_input.txt /Harmonix/runner_output/output3.txt
# Running Sample Input 4
docker run -v $(pwd)/sample_input:/Harmonix/sample_input -v $(pwd)/runner_output:/Harmonix/runner_output python-scanner /Harmonix/sample_input/Sample4_input.txt /Harmonix/runner_output/output4.txt
# Running Sample Input 5
docker run -v $(pwd)/sample_input:/Harmonix/sample_input -v $(pwd)/runner_output:/Harmonix/runner_output python-scanner /Harmonix/sample_input/Sample5_input.txt /Harmonix/runner_output/output5.txt
```

input.txt can be replaced with any file located in the $/Harmonix_PLT/sample_input directory.

### Retrieve Output
After running the command,the tokenized output will be written to runner_output/output.txt

## Sample Inputs & Outputs
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

## Program Overview
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


