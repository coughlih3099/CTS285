# CTS 285
# M1HW
# Harley Coughlin coauthored by James Reynolds
# 08/20/2024

import UI
import calcFunctions as cf


def getMainInput() -> int:
    """Gets user input for the main menu"""
    isValid = False
    while not isValid:
        try:
            mainInput = int(input("Enter a number between 1-5: "))
            if mainInput not in range(1, 6):
                raise ValueError
            isValid = True
        except ValueError:
            UI.mainMenu()
    return mainInput


def getSubMenuInput() -> bool:
    """Calls and gets input for subMenu, returns a bool"""
    isValid = False
    while not isValid:
        try:
            UI.subMenu()
            subInput = int(input("Enter 1 or 2: "))
            if subInput not in (1, 2):
                raise ValueError
            if subInput in (1, 2):
                isValid = True
        except ValueError:
            print("Please enter 1 or 2.")
            UI.subMenu()
    if subInput == 1:
        return True
    return False


def validateInput() -> int | float:
    """Checks to see if user input is int or float"""
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


def main():
    """Main calculator loop"""
    keepGoing = True
    while keepGoing:
        repeat = True
        UI.mainMenu()
        userInput = getMainInput()
        if userInput == 1:
            while repeat:
                print()
                print(f"{"Add":-^29}")
                userInput1 = validateInput()
                userInput2 = validateInput()
                summed = cf.add(userInput1, userInput2)
                UI.prettyPrint(("sum", isinstance(summed, float), userInput1, userInput2, summed))
                repeat = getSubMenuInput()
        elif userInput == 2:
            while repeat:
                print()
                print(f"{"Subtract":-^29}")
                userInput1 = validateInput()
                userInput2 = validateInput()
                difference = cf.subtract(userInput1, userInput2)
                UI.prettyPrint(("difference", isinstance(difference, float), userInput1, userInput2, difference))
                repeat = getSubMenuInput()
        elif userInput == 3:
            while repeat:
                print()
                print(f"{"Divide":-^29}")
                userInput1 = validateInput()
                userInput2 = validateInput()
                try:
                    quotient = cf.divide(userInput1, userInput2)
                    UI.prettyPrint(("quotient", isinstance(quotient, float), userInput1, userInput2, quotient))
                except ZeroDivisionError:
                    print("Can't divide by zero")
                repeat = getSubMenuInput()
        elif userInput == 4:
            while repeat:
                print()
                print(f"{"Multiply":-^29}")
                userInput1 = validateInput()
                userInput2 = validateInput()
                product = cf.multiply(userInput1, userInput2)
                UI.prettyPrint(("product", isinstance(product, float), userInput1, userInput2, product))
                repeat = getSubMenuInput()
        elif userInput == 5:
            keepGoing = False


if __name__ == "__main__":
    main()
