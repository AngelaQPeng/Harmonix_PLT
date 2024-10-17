# Harmonix_PLT
We are creating a language for encoding musical notations into codes, which would translate musical scores into various formats of digital sheet music. This would allow musicians and music producers to compose in a consistent, readable format.

## Team Members
Angela Peng (ap4636), Haoyuan Lu (hl3812)

# Lexical Grammar Definition

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
- Description: Rhythmic durations, representing note lengths in musical notation. Though shorter note values are possible, we are limiting to 64th notes in our program.
- Examples: `whole`, `half`
- Regular Expression: 
```
(whole|half|quarter|eighth|sixteenth|32nd|64th)
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
:=|\+|\-|\*|/
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