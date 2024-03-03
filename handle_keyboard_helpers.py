from re import sub
from numexpr import evaluate
from numpy import round, array, ndarray
from constants import ALLOWED_KEYS, NUMPAD_OPERATIONS, ALL_OPERATORS


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
        return update_calculator_display(NUMPAD_OPERATIONS[input_key], current_expression)
    else:
        return current_expression + input_key[-1]


def update_calculator_display(input_key: str, current_expression: str) -> str:
    """Updates the current_expression with input validation"""
    # Check if ")" is inputted first, and replace it with "("
    if input_key == ")":
        if current_expression and current_expression.count("(") > current_expression.count(")"):
            current_expression += input_key
        else:
            current_expression += "("
    else:
        current_expression += input_key


    last_char = current_expression[-1:] if current_expression else ""
    if (
        not input_key in current_expression
        and (last_char not in ALL_OPERATORS or input_key not in ALL_OPERATORS)
        and not current_expression.endswith("0")
    ):
        return current_expression + input_key
    else:
        return current_expression
    
    


def preprocess_expression(expression: str) -> str:
    # Check for empty expressions
    if not expression.strip():
        return ""

    # Remove leading zeros from all numbers
    expression = sub(r"\b0+(?=\d)", "", expression)

    # Replace "(" with "*("
    expression = sub(r"(\d)\(", r"\1*(", expression)

    # Ensure balanced parentheses and handle order of operations
    open_count = expression.count("(")
    close_count = expression.count(")")
    if open_count != close_count:
        return ""

    # Recursive function to handle nested operations and parentheses
    def process_innermost(expr):
        start_index = expr.rfind("(")
        while start_index != -1:  # Handle multiple nested operations
            end_index = expr.find(")", start_index)
            if end_index == -1:
                return ""  # Missing closing parenthesis
            inner_expr = process_innermost(expr[start_index + 1 : end_index])
            if not inner_expr.strip():
                inner_expr = "0"
            expr = expr[:start_index] + str(evaluate(inner_expr)) + expr[end_index + 1 :]
            start_index = expr.rfind("(", end_index)  # Check for more nested ops
        return expr

    # Process the expression, handling nested operations and parentheses
    processed_expression = process_innermost(expression)
    if processed_expression == "":
        return ""

    return processed_expression


def is_calculate_key_pressed(input_key: str) -> bool:
    """Checks if the input is '=' or 'Enter'."""
    return input_key == "=" or (isinstance(input_key, str) and input_key == "Enter")


def calculate_result(current_expression: str) -> str:
    """Calculates the result of the expression in the current_expression object and updates it"""
    result = ""
    expression = preprocess_expression(current_expression)

    try:
        result = evaluate(expression)
        # Ensure result is a NumPy array for element-wise rounding
        if not isinstance(result, ndarray):
            result = array([result])
        # Round each element to 10 decimal places
        rounded_result = round(result, 10)
        return str(rounded_result)
    except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
        pass


def is_backspace_key_pressed(input_key: str) -> bool:
    """Checks if the input is 'e' or 'Backspace'"""
    return input_key == "e" or (isinstance(input_key, str) and input_key == "Backspace")


def handle_backspace(current_expression: str, result: str) -> tuple[str, str]:
    """Handles backspace input"""
    current_expression = current_expression[:-1]
    result = result[:-1]
    return current_expression, result


def is_clear_key_pressed(input_key: str) -> bool:
    """Checks if the input is 'c' for clear"""
    return input_key == "c"


def clear_calculator_state(
    current_expression: str, history: str, history_list: list, result: str
) -> tuple[str, str, list]:
    """Clears current_expression, history, and result"""
    if current_expression:
        # If current_expression has a value, clear it regardless of history
        cleared_history = history
        cleared_history_list = history_list
        cleared_current_expression = ""
        cleared_result = ""
    else:
        # If current_expression is empty, check if history needs clearing
        cleared_current_expression = current_expression  # Keep current_expression empty
        cleared_result = result
        if history:
            # Clear history if it has a value
            cleared_history = ""
            cleared_history_list = []
        else:
            # Nothing to clear if both current_expression and history are empty
            cleared_history = history
            cleared_history_list = history_list
            
    return cleared_current_expression, cleared_history, cleared_history_list, cleared_result


def handle_keyboard_input(event, current_expression, result, history, history_list):
    input_key = event.control.data or event.key

    # Prevent "*" and "/" from being inputted first into current_expression object
    if prevent_initial_operator_input(input_key, current_expression):
        return current_expression

    # Append the [keyboard / pressed buttons input] to current_expression object
    if is_valid_input_key(input_key):
        current_expression = update_calculator_display(input_key, current_expression)
        # print(current_expression)
        result = calculate_result(current_expression)

    # Handle numpad input:
    elif is_input_from_numpad(input_key):
        current_expression = process_numpad_input(input_key, current_expression)
        result = calculate_result(current_expression)

    # Handle "=" or "Enter" to calculate the result
    elif is_calculate_key_pressed(input_key):
        if current_expression == "":
            return
        elif prevent_last_operator_input(current_expression):
            current_expression = current_expression[:-1]
        else:
            # format the history value, example (1 + 1 = 2)
            calculated_current_expression = f"{current_expression} = {calculate_result(current_expression)}"

            history_list.append(calculated_current_expression)
            history_list_len = len(history_list)
            # if length of history list if 5 or more, update its values.  Otherwise keep them the same
            if history_list_len >= 5:
                history = "\n".join(history_list[history_list_len - 5 : history_list_len + 1])
            else:
                history = "\n".join(history_list)

            # The current calculation (1 + 1) will be evaluated (2)
            current_expression = calculate_result(current_expression)
            result = calculate_result(current_expression)

    # Handle backspace:
    elif is_backspace_key_pressed(input_key):
        current_expression, result = handle_backspace(current_expression, result)

    # Handle clear:
    elif is_clear_key_pressed(input_key):
        current_expression, result, history, history_list = clear_calculator_state(
            current_expression, result, history, history_list
        )
        
    return current_expression, result, history, history_list