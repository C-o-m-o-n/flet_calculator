from sympy import sympify, simplify, SympifyError, Number
from constants import ALLOWED_KEYS, NUMPAD_OPERATIONS, ALL_OPERATORS, SHIFT_KEY_MAPPINGS
from re import search, sub
from flet import KeyboardEvent
import timeit
# ------------------------------------------------------------------------------


def prevent_initial_operator_input(input_key: str, current_expression: str) -> bool:
    """Checks if the first input is empty and is either '*' or '/' in the current_expression object"""
    return current_expression == "" and input_key in ("*", "/", "Numpad Multiply", "Numpad Divide")

def prevent_last_operator_input(current_expression: str) -> str:
    """Checks if the current_expression object has a value and the last input is an operator in the current_expression object"""
    return current_expression and current_expression[-1] in ALL_OPERATORS


def is_valid_input_key(input_key: str) -> bool:
    """Checks if the input key is allowed"""
    return input_key in ALLOWED_KEYS


def is_input_from_numpad(input_key: str) -> bool:
    """Checks if the input is from the numpad"""
    return isinstance(input_key, str) and input_key.startswith("Numpad")


def process_numpad_input(input_key: str, current_expression: str):
    """Handles numpad input"""
    if input_key in NUMPAD_OPERATIONS:
        return update_expression(NUMPAD_OPERATIONS[input_key], current_expression)
    else:
        return current_expression + input_key[-1]

def calculate(current_expression: str) -> str:
    """Validates the user's input, calculates the result using sympy, and returns it or the original expression on failure."""
    
    # Strips whitespace and avoids processing if empty
    current_expression = current_expression.strip()
    if not current_expression:
        return current_expression

    # parentheses and invalid character validation
    if current_expression.count("(") != current_expression.count(")") or search(r"[^\d\(\)+\-*/.%^]", current_expression):
        return current_expression

    # Handle multiple outer parentheses and replace applicable opening parentheses with *(, if needed
    # processed_expression = current_expression[0] + current_expression[1:].replace("(", "*(")
    # Handle implied multiplication: 
    # - after a closing parenthesis ")"
    # - before an opening parenthesis "(" excluding at the start
    processed_expression = ''
    i = 0
    while i < len(current_expression):
        char = current_expression[i]
        if char == '(' and i > 0 and (current_expression[i-1].isdigit() or current_expression[i-1] in '.)'):
            processed_expression += '*('
        elif char == ')' and i < len(current_expression) - 1 and current_expression[i+1].isdigit():
            processed_expression += ')*'
        else:
            processed_expression += char
        i += 1

        # Special handling to prevent multiplication between **) sequences from exponentiation and adjacent parentheses
        if processed_expression.endswith("**("):
            processed_expression = processed_expression[:-2] + "("
    
    try:
        # parsing safety checks
        parsed_expression = sympify(processed_expression)
        # Calculate the result
        simplified_expression = simplify(parsed_expression)

        # Conditionally convert to float only when necessary
        if isinstance(simplified_expression, Number):
            if simplified_expression.is_integer:
                result = int(simplified_expression)
            else:
                result = simplified_expression.evalf(5)
        else:
            result = simplified_expression

        return str(result)

    except SympifyError:
        return current_expression


def update_expression(input_key: str, current_expression: str) -> str:
    if input_key not in ("=", "Enter"):
        if input_key.isdigit():
            current_expression = sub(r"\b0+(?=\d)", "", current_expression)
        current_expression += input_key
    return current_expression

# Benchmarking logic moved outside the function (optional)
def benchmark_calculate(input_key: str, current_expression: str):
    if is_calculate_key_pressed(input_key):
        benchmark_calculate_result = calculate(current_expression)  # Avoid modifying original expression
    
        time_taken = timeit.timeit(lambda: benchmark_calculate_result, number=1000)
        return print(f"Total execution time for calculate: {time_taken:.6f} seconds")
            
def is_calculate_key_pressed(input_key: str) -> bool:
    """Checks if the input is '=' or 'Enter'."""
    return input_key == "=" or (isinstance(input_key, str) and input_key == "Enter")

def handle_calculate_key_pressed(input_key: str, current_expression: str, result: str, history: str, history_list: list[str]) -> tuple[str, str, str, list[str]]:
    if current_expression == "":
        return
    elif prevent_last_operator_input(current_expression):
        current_expression = current_expression[:-1]
    else:
        # format the history value, example (1 + 1 = 2)
        calculated_current_expression = f"{current_expression} = {calculate(current_expression)}"

        history_list.append(calculated_current_expression)
        history_list_len = len(history_list)
        # if length of history list if 5 or more, update its values.  Otherwise keep them the same
        if history_list_len >= 5:
            history = "\n".join(history_list[history_list_len - 5 : history_list_len + 1])
        else:
            history = "\n".join(history_list)
        # The current calculation (1 + 1) will be evaluated (2)
        current_expression = calculate(update_expression(input_key, current_expression))
        result = calculate(current_expression)
        result = ""
        
        # Benchmark calculating the result
        # benchmark_calculate(input_key, current_expression)

    return current_expression, result, history, history_list


def is_backspace_key_pressed(input_key: str) -> bool:
    """Checks if the input is 'e' or 'Backspace'"""
    return input_key == "e" or (isinstance(input_key, str) and input_key == "Backspace")


def handle_backspace(current_expression: str, result: str) -> tuple[str, str]:
    """Handles backspace input"""
    if current_expression:
        current_expression = current_expression[:-1]
    if isinstance(result, str):
        result = result[:-1]
    else:
        result = str(result)[:-1]
    return current_expression, result


def is_clear_key_pressed(input_key: str) -> bool:
    """Checks if the input is 'c' for clear"""
    return input_key == "C" or (isinstance(input_key, str) and input_key == "C")


def clear_calculator_state(
    current_expression: str, result: str, history: str, history_list: list[str]
) -> tuple[str, str, str, list[str]]:
    """Clears current_expression, history, and result"""
    if current_expression or result:
        # Clear current expression and result on first press of "C"
        current_expression = ""
        result = ""
    else:
        # Clear history on second press of "C"
        history = ""
        history_list = []
        
    return current_expression, result, history, history_list


# ------------------------------------------------------------------------------
# Main handle keyboard function
# ------------------------------------------------------------------------------

def handle_keyboard_input(event: KeyboardEvent, current_expression: str, result: str, history: str, history_list: list[str]) -> tuple[str, str, str, list]:
    # Accept input from control/UI buttons or keyboard
    input_key = event.control.data or event.key

    # Apply Shift + key combinations (if any)
    if isinstance(event, KeyboardEvent) and event.shift and event.key in SHIFT_KEY_MAPPINGS:
        input_key = SHIFT_KEY_MAPPINGS[event.key]

    # Prevent "*" and "/" from being inputted first into current_expression object
    if prevent_initial_operator_input(input_key, current_expression):
        return current_expression

    # Append the [keyboard / pressed buttons input] to current_expression object
    if is_valid_input_key(input_key) and len(current_expression) <= 15:
        current_expression = update_expression(input_key, current_expression)

    # Handle numpad input:
    elif is_input_from_numpad(input_key) and len(current_expression) <= 15:
        current_expression = process_numpad_input(input_key, current_expression)

    # Handle "=" or "Enter" to calculate the result
    elif is_calculate_key_pressed(input_key):
        current_expression, result, history, history_list = handle_calculate_key_pressed(
            input_key, current_expression, result, history, history_list
        )

    # Handle backspace:
    elif is_backspace_key_pressed(input_key):
        current_expression, result = handle_backspace(current_expression, result)

    # Handle clear:
    elif is_clear_key_pressed(input_key):
        current_expression, result, history, history_list = clear_calculator_state(
            current_expression, result, history, history_list
        )
    if input_key not in {"=", "Enter", "Clear", "C", "Backspace", "e"}:
        result = calculate(current_expression)

    return current_expression, result, history, history_list


# from sympy import sympify, simplify, SympifyError, symbols
# import re

# # Example of expanding recognized symbols and functions if necessary
# x, y, z = symbols('x y z')
# recognized_functions = ['sin', 'cos', 'tan', 'log', 'exp']

# def is_recognized_function(s):
#     for func in recognized_functions:
#         if s.startswith(func):
#             return True
#     return False

# def calculate(current_expression: str) -> str:
#     current_expression = current_expression.strip()
#     if not current_expression:
#         return current_expression

#     if current_expression.count("(") != current_expression.count(")") or re.search(r"[^\d\(\)+\-*/.%^]", current_expression):
#         return current_expression
    
#     processed_expression = ''
#     i = 0
#     while i < len(current_expression):
#         char = current_expression[i]
#         if char == '(' and i > 0 and (current_expression[i-1].isdigit() or current_expression[i-1] in '.)'):
#             processed_expression += '*('
#         elif char == ')' and i < len(current_expression) - 1 and current_expression[i+1].isdigit():
#             processed_expression += ')*'
#         else:
#             processed_expression += char
#         i += 1

#         # Special handling to prevent multiplication between **) sequences from exponentiation and adjacent parentheses
#         if processed_expression.endswith("**("):
#             processed_expression = processed_expression[:-2] + "("

#         # Looking ahead for recognized functions to prevent improper multiplication insertion
#         if i < len(current_expression)-1 and current_expression[i].isalpha():
#             lookahead = current_expression[i:]
#             if any(lookahead.startswith(func) for func in recognized_functions):
#                 while i < len(current_expression) and current_expression[i].isalpha():
#                     processed_expression += current_expression[i]
#                     i += 1
#                 continue

#     try:
#         result = simplify(sympify(processed_expression, rational=True))
#         return str(result)
#     except SympifyError:
#         return current_expression

