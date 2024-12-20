# CTS285
# M2HW1
# Harley Coughlin
# 09/22/2024

def add(num1: int, num2: int) -> int:
    return num1 + num2


def subtract(num1: int, num2: int) -> int:
    return num1 - num2


def divide(num1: int, num2: int) -> int:
    return num1 // num2


def multiply(num1: int, num2: int) -> int:
    return num1 * num2


def get_answer(num1: int, num2: int, operation: str) -> int:
    match operation:
        case "+":
            answer = add(num1, num2)
        case "-":
            # there should never be a time where num2 is greater than num1
            if num2 > num1:
                raise ValueError
            answer = subtract(num1, num2)
        case "/":
            # there should never be a time where num2 is 0
            if num2 == 0:
                raise ZeroDivisionError
            answer = divide(num1, num2)
        case "*":
            answer = multiply(num1, num2)
    return answer


def check_answer(num1: int, num2: int, operation: str, answer: int) -> bool:
    result = None
    match operation:
        case "+":
            result = add(num1, num2)
        case "-":
            if num2 > num1:
                raise ValueError
            result = subtract(num1, num2)
        case "/":
            if num2 == 0:
                raise ZeroDivisionError
            result = divide(num1, num2)
        case "*":
            result = multiply(num1, num2)
    if result == answer:
        return True
    return False
