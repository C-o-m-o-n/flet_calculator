import flet as ft


# Allowed key for input
ALLOWED_KEYS = set("1234567890+-*/().%")

# Numpad operations mapping
NUMPAD_OPERATIONS = {
    "Numpad Add": "+",
    "Numpad Subtract": "-",
    "Numpad Multiply": "*",
    "Numpad Divide": "/",
    "Numpad Decimal": ".",
}

# Create a list of all valid operators, including those from the numpad.
all_values_set = set(NUMPAD_OPERATIONS.values())
all_values_set.discard(".")
ALL_OPERATORS = ["+", "-", "*", "/", "%"] + list(all_values_set)



COLORS = {
    "background": "#191F26",  # Matches dark background (adjust slightly for more contrast)
    "listview_bg": "#1E2630",  # Darker than background for visual separation
    "text": "#FFFFFF",  # White text for optimal contrast
    "hint_text": "#C0C0C0",  # White text for hint text
    "button_bg": "#2C3742",  # Slightly darker than widget background for distinction
    "operator_bg": "#009688",  # Similar to widget background for consistency
    "border": "#7d3c98",
    "operator_text": "#FFFFFF",  # White text for operators
}

LIGHT_COLORS = {
    "background": "#FFFFFF",  # White background
    "textfield_bg": "#F2F2F2",  # Light gray for text field background
    "text": "#222222",  # Black text for good contrast
    "button_bg": "#E6E6E6",  # Lighter gray for button background
    "operator_bg": "#F2F2F2",  # Light gray for operator background
    "operator_text": "#222222",  # Black text for operators
}

# Defines how the button layout will look like
BUTTON_LAYOUT = [
    [
        ["⌫", "e"],
        ["(", "("],
        [")", ")"],
        ["÷", "/"],
    ],
    [
        ["7", "7"],
        ["8", "8"],
        ["9", "9"],
        ["x", "*"],
    ],
    [
        ["4", "4"],
        ["5", "5"],
        ["6", "6"],
        ["-", "-"],
    ],
    [
        ["1", "1"],
        ["2", "2"],
        ["3", "3"],
        ["+", "+"],
    ],
    [
        ["C", "c"],
        ["0", "0"],
        [".", "."],
        ["=", "="],
    ],
]
