#!/bin/bash

# Run Harmonix Compiler: Scanning -> Parsing -> Code Generation
# Script should stop on the first error
set -e

# Colors for terminal output
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

# Check for Python Installation
echo -e "${GREEN}Checking Python3 installation...${NC}"
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}Error: Python3 is not installed.${NC}"
  echo "Please install Python3 from https://www.python.org/downloads/"
  exit 1
fi
echo -e "${GREEN}Python3 is installed.${NC}"

# Input file validation
if [ "$#" -lt 1 ]; then
  echo -e "${RED}Error: No input file provided.${NC}"
  exit 1
fi

INPUT_FILE=$1
OUTPUT_DIR=$2

# Prepare output directory
echo -e "${GREEN}Preparing output directory: $OUTPUT_DIR${NC}"
mkdir -p "$OUTPUT_DIR"

# Run Scanner
echo -e "${GREEN}Running Scanner...${NC}"
python3 src/scanner_runner.py "$INPUT_FILE" "$OUTPUT_DIR/scanner_output.txt"

# Run Parser
echo -e "${GREEN}Running Parser...${NC}"
python3 src/parser_runner.py "$OUTPUT_DIR/scanner_output.txt" "$OUTPUT_DIR/parser_output.txt"

# Run Code Generator
echo -e "${GREEN}Running Code Generator...${NC}"
python3 src/python_generator_runner.py "$OUTPUT_DIR/parser_output.txt" "$OUTPUT_DIR/output.py"

# Run Code Generator
echo -e "${GREEN}Running Code Optimizer...${NC}"
python3 src/optimizer_runner.py "$OUTPUT_DIR/output.py" "$OUTPUT_DIR/optimized_output.py"

# Completion
echo -e "${GREEN}Compilation completed successfully.${NC}"
echo "Generated Python code is available at: $OUTPUT_DIR/output.py"
