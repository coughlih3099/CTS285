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
            subMenu()
    if subInput == 1:
        return True
    return False


def add() -> bool:
    """Adds two numbers, calls getSubMenuInput, returns bool"""
    print()
    print(f"{"Add":-^29}")
    userInput1 = int(input("Enter number 1: "))
    userInput2 = int(input("Enter number 2: "))
    product = userInput1 + userInput2
    print(f"{userInput1} + {userInput2} = {product}")
    return getSubMenuInput()


def subtract():
    print("This is the subtract function")
    return getSubMenuInput()


def divide():
    print("This is the divide function")
    return getSubMenuInput()

def multiply():
    print("This is the multiply function")
    return getSubMenuInput()
