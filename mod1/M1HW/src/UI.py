"""UI for calculator cli app"""


def mainMenu():
    """Main Menu"""
    print()
    print(f"{"Main Menu":-^29}")
    print(f"{"":>10}1. Add")
    print(f"{"":>10}2. Subtract")
    print(f"{"":>10}3. Divide")
    print(f"{"":>10}4. Multiply")
    print(f"{"":>10}5. Exit")
    print(f"{"":-<29}")


def subMenu():
    """Sub Menu"""
    print()
    print(f"{"Menu":-^29}")
    print(f"{"":>10}1. Repeat")
    print(f"{"":>10}2. Main Menu")
    print(f"{"":-<29}")


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
