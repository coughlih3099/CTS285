"""Functions for calculator.py"""


def multiply(num1: int | float, num2: int | float) -> int | float:
    """Multiplies to numbers and returns the product"""
    return num1 * num2


def divide(num1: int | float, num2: int | float) -> int | float | None:
    """Divides two numbers and returns the quotient"""
    return num1 / num2


def add(num1: int | float, num2: int | float) -> int | float:
    """Adds to numbers and returns the sum"""
    return num1 + num2


def subtract(num1: int | float, num2: int | float) -> int | float:
    """Subtracts two numbers and returns the difference"""
    return num1 - num2


# def add() -> bool:
#     """Adds two numbers, calls getSubMenuInput, returns bool"""
#     print()
#     print(f"{"Add":-^29}")
#     userInput1 = validateInput()
#     userInput2 = validateInput()
#     sum = userInput1 + userInput2
#     prettyPrint(("sum", isinstance(sum, float), userInput1, userInput2, sum))
#     return getSubMenuInput()
#
#
# def subtract():
#     print()
#     print(f"{"Subtract":-^29}")
#     userInput1 = validateInput()
#     userInput2 = validateInput()
#     difference = userInput1 - userInput2
#     prettyPrint(("difference", isinstance(difference, float), userInput1, userInput2, difference))
#     return getSubMenuInput()
#
#
# def divide():
#     """Divides two numbers, calls getSubMenuInput, returns bool"""
#     print()
#     print(f"{"Divide":-^29}")
#     userInput1 = validateInput()
#     userInput2 = validateInput()
#     try:
#         quotient = userInput1 / userInput2
#     except ZeroDivisionError:
#         print("Can't divide by zero\n")
#         getSubMenuInput()
#     prettyPrint(("quotient", isinstance(quotient, float), userInput1, userInput2, quotient))
#     return getSubMenuInput()
#
#
# def multiply():
#     """Mutliplies two numbers, calls getSubMenuInput, returns bool"""
#     print()
#     print(f"{"Multiply":-^29}")
#     userInput1 = validateInput()
#     userInput2 = validateInput()
#     product = userInput1 * userInput2
#     prettyPrint(("product", isinstance(product, float), userInput1, userInput2, product))
#     return getSubMenuInput()
