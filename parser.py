# Project Name: LLM Inspired Recursive Descent Parser
# Course Name: Programming Languages & Structures (CSC 461)
# This project implements a recursive descent parser that evaluates
# arithmetic expressions while demonstrating adaptability inspired by
# large language models (LLMs). The parser handles operator precedence,
# unary operators, and includes robust error handling and recovery
# mechanisms. It also investigates edge cases to ensure comprehensive
# parsing capabilities.



# Exception class for parsing errors
class ParseError(Exception):
    """Custom exception for syntax and parsing errors"""
    pass


# COnverting input string into streams of tokens
def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        # Ignoring thr whitespace
        if char.isspace():
            i += 1
            continue

        # Handling numeric literals (integers and floats)
        if char.isdigit() or char == '.':
            num = char
            i += 1
            while i < len(expression) and (
                expression[i].isdigit() or expression[i] == '.'
            ):
                num += expression[i]
                i += 1
            tokens.append(num)
            continue

        # Handling identifiers (alphabetic tokens)
        if char.isalpha():
            name = char
            i += 1
            while i < len(expression) and expression[i].isalnum():
                name += expression[i]
                i += 1
            tokens.append(name)
            continue

        # Operators and parentheses
        tokens.append(char)
        i += 1

    return tokens


# PARSER CLASS (Recursive Descent Implementation)
#
# Grammar:
# expression → term { (+|-) term }
# term       → factor { (*|/|%) factor }
# factor     → number | (expression) | -factor | identifier

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # Current token position

    # Return current token
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # Consume expected token
    def eat(self, token):
        if self.current_token() == token:
            self.pos += 1
        else:
            raise ParseError(
                f"Expected '{token}', found '{self.current_token()}' "
                f"at position {self.pos}"
            )

   
    # EXPRESSION LEVEL (+ and -)
    def parse_expression(self):
        value = self.parse_term()

        while self.current_token() in ('+', '-'):
            op = self.current_token()
            self.eat(op)

            if op == '+':
                value += self.parse_term()
            else:
                value -= self.parse_term()

        return value

   
    # TERM LEVEL (*, /, %)

    def parse_term(self):
        value = self.parse_factor()

        while self.current_token() in ('*', '/', '%'):
            op = self.current_token()
            self.eat(op)

            if op == '*':
                value *= self.parse_factor()

            elif op == '/':
                divisor = self.parse_factor()
                if divisor == 0:
                    raise ParseError("Division by zero detected")
                value /= divisor

            elif op == '%':
                divisor = self.parse_factor()
                if divisor == 0:
                    raise ParseError("Modulo by zero detected")
                value %= divisor

        return value

   
    # FACTOR LEVEL
 
    def parse_factor(self):
        token = self.current_token()

        # Unary minus handling
        if token == '-':
            self.eat('-')
            return -self.parse_factor()

        # Unexpected end of input
        if token is None:
            raise ParseError("Unexpected end of input")

        # Numeric literal validation
        if token.count('.') <= 1 and token.replace('.', '', 1).isdigit():
            self.eat(token)
            return float(token)

        # Identifier handling (LLM-inspired prediction)
        if token.isalpha():
            predicted_value = len(token)  # Simple heuristic
            print(
                f"Warning: Unknown identifier '{token}' "
                f"predicted as {predicted_value}"
            )
            self.eat(token)
            return float(predicted_value)

        # Parenthesized expression
        if token == '(':
            self.eat('(')
            value = self.parse_expression()

            # Graceful recovery for missing ')'
            if self.current_token() == ')':
                self.eat(')')
            else:
                print("Warning: Missing ')', auto-corrected")

            return value

        # Invalid token
        raise ParseError(
            f"Invalid token '{token}' at position {self.pos}"
        )



# EVALUATION FUNCTION

def evaluate(expression):
    tokens = tokenize(expression)
    parser = Parser(tokens)
    result = parser.parse_expression()

    # Detect trailing tokens after valid expression
    if parser.current_token() is not None:
        raise ParseError(
            f"Unexpected token '{parser.current_token()}' "
            f"after complete expression"
        )

    return result



# MAIN PROGRAM (USER INPUT MODE)

if __name__ == "__main__":

    print("************************************************")
    print("------------------------------------------------")
    print(" LLM-Inspired Recursive Descent Parser (CSC 461)")
    print(" Type 'exit' to terminate the program")
    print("************************************************\n")
    prrint("-----------------------------------------------\n")

    history = []  # Store previous expressions and results

    while True:
        user_input = input("Enter expression: ")

        # Exit condition
        if user_input.lower() == "exit":
            print("\nProgram terminated.")
            break

        try:
            result = evaluate(user_input)
            history.append((user_input, result))
            print("Result:", result)

        except ParseError as error:
            print("Parsing Error:", error)
            print("Hint: Check syntax, operators, or parentheses.")

    # Display expression history
    print("\nExpression History:")
    for expr, res in history:
        print(f"{expr} = {res}")
