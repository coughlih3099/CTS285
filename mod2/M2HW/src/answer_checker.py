# CTS285
# M2HW1
# Harley Coughlin
# 09/22/2024

def add(num1: int | float, num2: int | float) -> int | float:
    return num1 + num2


def subtract(num1: int | float, num2: int | float) -> int | float:
    return num1 - num2


def divide(num1: int | float, num2: int | float) -> int | float:
    return num1 / num2


def multiply(num1: int | float, num2: int | float) -> int | float:
    return num1 * num2


def check_answer(num1: int | float, num2: int | float, operation: str, answer: int | float) -> bool:
    result = None
    match(operation):
        case "+":
            result = add(num1, num2)
        case "-":
            result = subtract(num1, num2)
        case "/":
            result = divide(num1, num2)
        case "*":
            result = multiply(num1, num2)
    if result == answer:
        return True
    return False