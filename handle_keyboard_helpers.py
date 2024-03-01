from re import sub, findall
from numexpr import evaluate
from numpy import round, array, ndarray
from constants import ALLOWED_KEYS, NUMPAD_OPERATIONS, ALL_OPERATORS


def prevent_first_operator(data: str, text: str) -> bool:
    """Checks if input is an operator and if it's the first input in the text field"""
    return text == "" and data in ("*", "/", "Numpad Multiply", "Numpad Divide")


def prevent_last_operator(text: str) -> str:
    """Checks if input is an operator and if it's the last input in the text field"""
    return text and text[-1] in ALL_OPERATORS


def is_allowed_key(data: str) -> bool:
    """Checks if the input key is allowed"""
    return data in ALLOWED_KEYS


def is_numpad_input(data: str) -> bool:
    """Checks if the input is from the numpad"""
    return isinstance(data, str) and data.startswith("Numpad")


def handle_numpad_input(data: str, text: str):
    """Handles numpad input"""
    if data in NUMPAD_OPERATIONS:
        return update_text(NUMPAD_OPERATIONS[data], text)
    else:
        return text + data[-1]


def update_text(data: str, text: str) -> str:
    """Updates the text field with input validation"""
    if data == ")":
        if text and text.count("(") > text.count(")"):
            text += data
        else:
            text += "("
    else:
        text += data

    last_char = text[-1:] if text else ""
    if (
        not data in text
        and (last_char not in ALL_OPERATORS or data not in ALL_OPERATORS)
        and not text.endswith("0")
    ):
        return text + data
    else:
        return text


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


def is_calculate_input(data: str) -> bool:
    """Checks if the input is '=' or 'Enter'"""
    return data == "=" or (isinstance(data, str) and data == "Enter")


def calculate_result(text: str) -> str:
    """Calculates the result of the expression in the text field and updates the text field"""
    result = ""
    expression = preprocess_expression(text)

    try:
        # Ensure there are 2 number and 1 operator before calculating
        # if number_count >= 2 and operator_count >= 1:
        result = evaluate(expression)
        # Ensure result is a NumPy array for element-wise rounding
        if not isinstance(result, ndarray):
            result = array([result])
        # Round each element to 10 decimal places
        rounded_result = round(result, 10)
        return str(rounded_result)
    except (SyntaxError, NameError, TypeError, ZeroDivisionError) as e:
        pass


def is_backspace_input(data: str) -> bool:
    """Checks if the input is 'e' or 'Backspace'"""
    return data == "e" or (isinstance(data, str) and data == "Backspace")


def handle_backspace(text: str, result: str) -> tuple[str, str]:
    """Handles backspace input"""
    text = text[:-1]
    result = result[:-1]
    return text, result


def is_clear_input(data: str) -> bool:
    """Checks if the input is 'c' for clear"""
    return data == "c"


def handle_clear(
    text: str, history: str, history_list: list, result: str
) -> tuple[str, str, list]:
    """Clears text field"""
    if text:
        # If text has a value, clear it regardless of history
        cleared_text = ""
        cleared_history = history
        cleared_history_list = history_list
        cleared_result = ""
    else:
        # If text is empty, check if history needs clearing
        cleared_text = text  # Keep text empty
        cleared_result = result
        if history:
            # Clear history if it has a value
            cleared_history = ""
            cleared_history_list = []
        else:
            # Nothing to clear if both text and history are empty
            cleared_history = history
            cleared_history_list = history_list
    return cleared_text, cleared_history, cleared_history_list, cleared_result


def handle_keyboard_input(event, text, result, history, history_list):
    data = event.control.data or event.key

    # Prevent "*" and "/" from being inputted first into text object
    if prevent_first_operator(data, text):
        return text

    # Append the [keyboard / pressed buttons input] to text object
    if is_allowed_key(data):
        text = update_text(data, text)
        # print(text)
        result = calculate_result(text)

    # Handle numpad input:
    elif is_numpad_input(data):
        text = handle_numpad_input(data, text)
        result = calculate_result(text)

    # Handle "=" or "Enter" to calculate the result
    elif is_calculate_input(data):
        if text == "":
            return
        elif prevent_last_operator(text):
            text = text[:-1]
        else:
            # format the history value, example (1 + 1 = 2)
            calculated_text = f"{text} = {calculate_result(text)}"

            history_list.append(calculated_text)
            history_list_len = len(history_list)
            # if length of history list if 5 or more, update its values.  Otherwise keep them the same
            if history_list_len >= 5:
                history = "\n".join(
                    history_list[history_list_len - 5 : history_list_len + 1]
                )
            else:
                history = "\n".join(history_list)

            # The current calculation (1 + 1) will be evaluated (2)
            text = calculate_result(text)
            result = calculate_result(text)

    # Handle backspace:
    elif is_backspace_input(data):
        text, result = handle_backspace(text, result)

    # Handle clear:
    elif is_clear_input(data):
        text, history, history_list, result = handle_clear(
            text, history, history_list, result
        )