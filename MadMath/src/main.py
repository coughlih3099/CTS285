# CTS285
# MadMath
# Harley Coughlin

from fasthtml.common import *
from answer_checker import check_answer
import re


css = Style(":root { --pico-font-size: 100%; --pico-font-family: Pacifico, mono; }")

app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route


nav_bar = Nav(Ul(Li(Strong("MadMath"))),
              Ul(Li(Details(Summary("Modes"),
                            Ul(
                                Li(A("Math Master", hx_target="#replacable", hx_get="/math-master")),
                                Li(A("Madness's Methods", hx_target="#replacable", hx_get="/memory-bank")),
                                Li(A("Electro Flash", hx_target="#replacable", hx_get="/electro-flash"))),
                    cls="dropdown"))),
              cls="container")

@rt("/", methods=["get"])
def index():
    return Title("MadMath"), nav_bar, Div(id="replacable", cls="container", hx_get="/math-master", hx_trigger="load")

def get_input(**kw) -> str:
    return Input(id="user_input", name="user_input", placeholder="Enter problem here", autocomplete="off", required=True, **kw)


@rt("/math-master", methods=["get"])
def math_master_ui():
    problems_solved = "0"
    number_correct = "0"
    number_of_tries = "0"
    head = "Welcome to MadMath's Math Master!"
    instructions = Div(P("1. Enter a problem, e.g. 1 + 1 = 2"),
                        P("2. Press Submit"),
                        P("3. Math Master will tell you if you got the correct answer"),
                        P("4. Try again or try a new question"),
                        P("Tip: the biggest numbers possible are 99 for operands and 999 for answers"))
    history = Div(id="history")
    add = Form(Group(get_input(), Button("Submit")),
               Input(type="hidden", id="problems-solved", name="problems_solved", value=problems_solved),
               Input(type="hidden", id="number-of-tries", name="number_of_tries", value=number_of_tries),
               Input(type="hidden", id="number-correct", name="number_correct", value=number_correct),
               post="math-master-history", target_id="history", hx_swap="beforeend",
               id="submit", name="submit")
    
    middle = Grid(Card(instructions, header="Instructions:"), Card(history, header="Problem History:"))
    math_master = Card(middle, header=head, footer=add)
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
def math_master_logic(user_input: str, problems_solved: str, number_of_tries: str, number_correct: str):
    local_problems_solved = int(problems_solved)
    local_number_of_tries = int(number_of_tries)
    local_number_correct = int(number_correct)
    problem_number = local_problems_solved + 1
    return_input = ""

    equation_parts = validate_input(user_input)
    return_string = "You need to enter an arithmetic equation"
    is_correct = False
    if equation_parts is not None:
        num1, num2, operation, answer = equation_parts
        try:
            if check_answer(num1, num2, operation, answer):
                return_string = f"Problem #{problem_number:>2}: {num1} {operation} {num2} = {answer} is correct"
                is_correct = True
                local_number_correct += 1
            else:
                return_string = f"Problem #{problem_number:>2}: {num1} {operation} {num2} does not equal {answer}"
                local_number_of_tries += 1
                return_input = f"{num1} {operation} {num2} = "
        except ValueError:
            return_string = "You can't subtract a bigger number from a smaller number."
            return_input = f"{num1} - "
        except ZeroDivisionError:
            return_string = "You can't divide by zero."
            return_input = f"{num1} / "
    
    if local_number_of_tries == 2 or is_correct:
        local_problems_solved += 1
        local_number_of_tries = 0
        return_string += " (moving to next problem)."
        return_input = ""

    restart = (P(return_string),
                Form(Group(P(f"""You've completed {local_problems_solved} questions
                    and your final score is: {local_number_correct}/{local_problems_solved}"""),
                            Button("Start Again")), id="submit", name="submit", hx_swap_oob="true"))

    # TODO: find a better way to structure this return statement
    if local_problems_solved >= 10:
        return restart
    else:
        return (
            P(return_string),
            get_input(hx_swap_oob="true") if return_string == "" else get_input(value=return_input, hx_swap_oob="true"),
            Input(type="hidden", id="problems-solved", name="problems_solved", value=str(local_problems_solved), hx_swap_oob="true"),
            Input(type="hidden", id="number-of-tries", name="number_of_tries", value=str(local_number_of_tries), hx_swap_oob="true"),
            Input(type="hidden", id="number-correct", name="number_correct", value=str(local_number_correct), hx_swap_oob="true")
        )


@rt("/memory-bank", methods=["get"])
def memory_bank():
    return Card("Madness's Methods")


@rt("/electro-flash", methods=["get"])
def electro_flash():
    return Card("Electro Flash")
