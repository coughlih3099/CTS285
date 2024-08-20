# CTS 285
# M1HW
# Harley Coughlin (James Reynolds)
# 08/20/2024


import calcFunctions as cf
import menus


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
            menus.mainMenu()
    return mainInput


def main():
    """Main calculator loop"""
    keepGoing = True
    while keepGoing:
        repeat = True
        menus.mainMenu()
        userInput = getMainInput()
        if userInput == 1:
            while repeat:
                repeat = cf.add()
        elif userInput == 2:
            while repeat:
                repeat = cf.subtract()
        elif userInput == 3:
            while repeat:
                repeat = cf.divide()
        elif userInput == 4:
            while repeat:
                repeat = cf.multiply()
        elif userInput == 5:
            keepGoing = False


if __name__ == "__main__":
    main()
