"""Functions for calculator.py"""

from menus import subMenu

def getSubMenuInput() -> bool:
    """Calls and gets input for subMenu, returns a bool"""
    isValid = False
    while not isValid:
        try:
            subMenu()
            subInput = int(input("Enter 1 or 2: "))
            if subInput not in (1, 2):
                raise ValueError
            if subInput in (1, 2):
                isValid = True
        except ValueError:
            print("Please enter 1 or 2.")
            subMenu()
    if subInput == 1:
        return True
    return False


def prettyPrint(sdqp: tuple[str, bool, int | float, int | float, int | float]) -> None:
    if sdqp[0] == "sum":
        operation = "+"
    elif sdqp[0] == "difference":
        operation = "-"
    elif sdqp[0] == "quotient":
        operation = "/"
    elif sdqp[0] == "product":
        operation = "*"

    if sdqp[1]:
        print(f"{sdqp[2]} {operation} {sdqp[3]} = {sdqp[4]:.5}")
    else:
        print(f"{sdqp[2]} {operation} {sdqp[3]} = {sdqp[4]:}")



def validateInput() -> int | float:
    isValid = False
    while not isValid:
        userInput = input("Enter a number: ")
        try:
            if "." in userInput:
                userInput = float(userInput)
                isValid = True
            else:
                userInput = int(userInput)
                isValid = True
        except ValueError:
            print("Enter a valid integer or float\n")
    return userInput

def add() -> bool:
    """Adds two numbers, calls getSubMenuInput, returns bool"""
    print()
    print(f"{"Add":-^29}")
    userInput1 = validateInput()
    userInput2 = validateInput()
    sum = userInput1 + userInput2
    prettyPrint(("sum", isinstance(sum, float), userInput1, userInput2, sum))
    return getSubMenuInput()


def subtract():
    print()
    print(f"{"Subtract":-^29}")
    userInput1 = validateInput()
    userInput2 = validateInput()
    difference = userInput1 - userInput2
    prettyPrint(("difference", isinstance(difference, float), userInput1, userInput2, difference))
    return getSubMenuInput()


def divide():
    """Divides two numbers, calls getSubMenuInput, returns bool"""
    print()
    print(f"{"Divide":-^29}")
    userInput1 = validateInput()
    userInput2 = validateInput()
    try:
        quotient = userInput1 / userInput2
    except ZeroDivisionError:
        print("Can't divide by zero\n")
        getSubMenuInput()
    prettyPrint(("quotient", isinstance(quotient, float), userInput1, userInput2, quotient))
    return getSubMenuInput()


def multiply():
    """Mutliplies two numbers, calls getSubMenuInput, returns bool"""
    print()
    print(f"{"Multiply":-^29}")
    userInput1 = validateInput()
    userInput2 = validateInput()
    product = userInput1 * userInput2
    prettyPrint(("product", isinstance(product, float), userInput1, userInput2, product))
    return getSubMenuInput()