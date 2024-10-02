# CTS285
# MadMath
# Harley Coughlin

from fasthtml.common import *
from answer_checker import check_answer
import re


css = Style(":root { --pico-font-size: 100%; --pico-font-family: Pacifico, mono; }")

app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route


problems_solved = 0
number_of_tries = 0
number_correct = 0


nav_bar = Nav(Ul(Li(Strong("MadMath"))),
              Ul(Li(Details(Summary("Modes"),
                            Ul(
                                Li(A("Math Master", hx_target="#replacable", hx_get="/math-master")),
                                Li(A("Memory Bank", hx_target="#replacable", hx_get="/memory-bank")),
                                Li(A("Electro Flash", hx_target="#replacable", hx_get="/electro-flash"))),
                    cls="dropdown"))),
              cls="container")

@rt("/", methods=["get"])
def index():
    return Title("MadMath"), nav_bar, Div(id="replacable", cls="container", hx_get="/math-master", hx_trigger="load")

def get_input(**kw) -> str:
    return Input(id="user_input", name="user_input", placeholder="Enter problem here", autocomplete="off", **kw)


@rt("/math-master", methods=["get"])
def math_master_ui():
    global problems_solved, number_of_tries, number_correct
    head = "Welcome to MadMath's Math Master!"
    instructions = Div(P("1. Enter a problem, e.g. 1 + 1 = 2"),
                        P("2. Press Submit"),
                        P("3. Math Master will tell you if you got the correct answer"),
                        P("4. Try again or try a new question"))
    history = Div(id="history")
    add = Form(Group(get_input(required=True), Button("Submit")),
               post="math-master-history", target_id="history", hx_swap="beforeend")
    progress = Group(P("Problems Solved: ", Span(problems_solved)),
                   P("Number of Tries: ", Span(number_of_tries)),
                   P("Number Correct: ", Span(str(number_correct) + "/10")), id="progress")
    middle = Grid(Card(instructions, header="Instructions:"), Card(history, header="Problem History:"))
    math_master = Card(progress,middle, header=head, footer=add)
    return math_master


def validate_input(user_input: str) -> tuple[int, int, str, int] | None:
    # input must be (at most 2 digit number) (operator) (at most 2 digit number) = (at most 3 digit number)
    pattern_raw = r"^(\d{,2}) *([+*-/]) *(\d{,2}) *= *(\d{,3}) *$"
    equation_parts = re.match(pattern_raw, user_input)
    if equation_parts is not None:
        num1 = int(equation_parts[1])
        operation = equation_parts[2]
        num2 = int(equation_parts[3])
        answer = int(equation_parts[4])
        return (num1, num2, operation, answer)
    return None


@rt("/math-master", name="math-master-history", methods=["post"])
def math_master_logic(user_input: str):
    global problems_solved, number_of_tries, number_correct
    equation_parts = validate_input(user_input)
    return_string = "You need to enter an arithmetic equation"
    is_correct = False
    if equation_parts is not None:
        num1, num2, operation, answer = equation_parts
        try:
            if check_answer(num1, num2, operation, answer):
                return_string = f"{num1} {operation} {num2} = {answer} is correct"
                is_correct = True
                number_correct += 1
            else:
                return_string = f"{num1} {operation} {num2} does not equal {answer}"
                number_of_tries += 1
        except ValueError:
            return_string = "You can't subtract a bigger number from a smaller number."
        except ZeroDivisionError:
            return_string = "You can't divide by zero."
    progress = Group(P("Problems Solved: ", Span(problems_solved)),
                   P("Number of Tries: ", Span(number_of_tries)),
                   P("Number Correct: ", Span(str(number_correct) + "/10")), id="progress", hx_swap_oob="True")
    if number_of_tries == 3 or is_correct:
        problems_solved += 1
        number_of_tries = 0
    else:
        return (P(return_string),
                get_input(hx_swap_oob="true", required=True),
                progress)


@rt("/memory-bank", methods=["get"])
def memory_bank():
    return Card("Memory Bank")


@rt("/electro-flash", methods=["get"])
def electro_flash():
    return Card("Electro Flash")
