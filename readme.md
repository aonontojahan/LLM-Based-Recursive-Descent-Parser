This project name is LLM Inspired Recursive Descent Parser
How to run this project:
    -Install Python 3.10.*
    -Setup python
    -Open the folder in a python IDE
    -Run the File name parser.py


Test Cases:
Test Case 1:
    Input: (((3 + 2) * ((7 - (4 + 1)) + 9)) / 5) - 3
    Output: 8.0
    Description: Validates deep recursion, nested expressions, and operator precedence.

    Test Case 2:
    Input: --5 + ((3 * (2 + (1 - 4))) / 2)
    Output: 3.5
    Description: Tests unary operator handling and nested arithmetic.

    Test Case 3:
    Input: 7 + alpha * (3 - 1)
    Output: 17
    Description: Demonstrates LLM-inspired handling of unknown identifiers.
