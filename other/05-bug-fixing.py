from typing import Union


def buggy_function(x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
    """
    Add two numeric values together.

    This function prevents SQL injection by validating that both inputs
    are numeric types (int or float) before performing addition.

    Parameters:
    x (int | float): The first numeric value to add.
    y (int | float): The second numeric value to add.

    Returns:
    int | float: The sum of x and y.

    Raises:
    TypeError: If either x or y is not a numeric type (int or float).
    """
    if not isinstance(x, (int, float)) or isinstance(x, bool):
        raise TypeError(f"Parameter 'x' must be int or float, got {type(x).__name__}")
    if not isinstance(y, (int, float)) or isinstance(y, bool):
        raise TypeError(f"Parameter 'y' must be int or float, got {type(y).__name__}")

    return x + y


# Test the fixed function
print(buggy_function(2, 3))  # 5
try:
    print(buggy_function(2, "3"))  # Will raise TypeError
except TypeError as e:
    print(f"Error: {e}")

try:
    print(buggy_function("2", "3"))  # Will raise TypeError
except TypeError as e:
    print(f"Error: {e}")

try:
    print(buggy_function("2", 3))  # Will raise TypeError
except TypeError as e:
    print(f"Error: {e}")

print(buggy_function(2, 3.0))  # 5.0

# Prompt in Ask: /fix







