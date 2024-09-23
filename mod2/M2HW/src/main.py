# CTS 285
# M2HW1
# Harley Coughlin
# 09/22/2024

from fasthtml.common import *
from answer_checker import check_answer

css = Style(":root { --pico-font-size:90%, --pico-font-family: Pacifico, cursive; }")


app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route


nav_bar = Nav(Ul(Li(Strong("MadMath"))),
              Ul(Li(Details(
                        Summary("Modes"),
                            Ul(
                                Li(A("Home", hx_target="#to_replace", hx_get="/home_again")),
                                Li(A("Answer Checker", hx_target="#to_replace", hx_get="/answer_check")),
                                Li(A("Memory Bank", href="#")),
                                Li(A("Electro Flash", href="#"))
                              ),
                    cls="dropdown"))),
              cls="container")


@rt("/", methods=["get"])
def home():
    return Title("MadMath"), nav_bar, Div(P("Home"), id="to_replace", cls="container")


@rt("/home_again", methods=["get"])
def home_again():
    return Div(P("Home again"), cls="container")


def get_input(**kw):
    return Input(id="user_input", name="user_input", placeholder="Enter arithmetic here", **kw)


@rt("/answer_check", methods=["get"])
def do_it():
    add = Form(Group(get_input(required=True), Button("Submit")), post="insert_history", target_id="history", hx_swap="beforeend")
    head = "Welcome to MadMath's Answer Checker!"
    card = Card(Div(P("Hi"), id="history"), header=head, footer=add)
    return card
 

def validate_equation(user_input: str):
    equation_regex = r"^(\d+\.?\d?) *([+-\/*]) *(\d+\.?\d?) *= *(\d+\.?\d?) *$"
    regexed = re.match(equation_regex, user_input)
    if regexed is not None:
        num1 = float(regexed[1]) if "." in regexed[1] else int(regexed[1])
        operation = regexed[2]
        num2 = float(regexed[3]) if "." in regexed[3] else int(regexed[3])
        answer = float(regexed[4]) if "." in regexed[4] else int(regexed[4])
        return (num1, num2, operation, answer)
    return None


@rt("/answer_check", name="insert_history", methods=["post"])
def maybe(user_input: str):

    equation_parts = validate_equation(user_input)
    return_string = "You need to enter an arithmetic equation"
    if equation_parts is not None:
        num1, num2, operation, answer = equation_parts
        try:
            if check_answer(num1, num2, operation, answer):
                return_string = f"{num1} {operation} {num2} = {answer} is correct"
            else:
                return_string = f"{num1} {operation} {num2} does not equal {answer}"
        except ZeroDivisionError:
            return_string = "You can't divide by zero."
    return P(return_string), get_input(hx_swap_oob="true", required=True)
