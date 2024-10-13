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
                                Li(A("Math Master", hx_target="#main-card", hx_get="/math-master")),
                                Li(A("Madness's Methods", hx_target="#main-card", hx_get="/madness-methods")),
                                Li(A("Electro Flash", hx_target="#main-card", hx_get="/electro-flash"))),
                    cls="dropdown"))),
              cls="container")

@rt("/", methods=["get"])
def index():
    # TODO: Swap the hx_get back to /math-master
    return Title("MadMath"), nav_bar, Div(id="main-card", cls="container", hx_get="/madness-methods-questions", hx_trigger="load")

def get_input(**kw) -> str:
    return Input(id="user_input", name="user_input", autocomplete="off", required=True, **kw)


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
    add = Form(Group(get_input(placeholder="Enter problem here"), Button("Submit")),
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


@rt("/madness-methods", methods=["get"])
def madness_methods():
    header = "Madness's Methods"
    instructions = Div(P("Instructions:"), Ol(Li("Enter questions")))
    footer = Group(P("Press Start to begin entering questions into the memory bank"), Button("Start", hx_target="#main-card", hx_get="/madness-methods-entry"))
    return_card = Card(instructions, header=header, footer=footer, id="madness-methods-instructions")
    return return_card


def create_question(number: int):
    return Li(f"Question #{number:>2}: ", Span(id=f"question-{number}"), style="list-style-type: none")


@rt("/madness-methods-entry", name="madness-methods-entry", methods=["get"])
def madness_methods_entry():
    question_number = "1"
    header = "Madness's Methods Question Entry"
    questions = Div(Ul(*[create_question(i + 1) for i in range(10)]))
    footer = Form(Group(get_input(placeholder=f"Enter question #{question_number:>2}"), Button("Submit")),
                  Input(type="hidden", id="question-number", name="question_number", value=question_number),
                  id="trying", name="trying", post="madness-methods-entry", target_id=f"question-{question_number}")
    return_card = Card(questions, header=header, footer=footer, id="madness-methods-entry")
    return return_card


user_questions = ["1 + 1", "4 / 2", "3 * 3", "4 - 3", "5 + 10"]


@rt("/madness-methods-entry", name="madness-methods-entry-post", methods=["post"])
def madness_methods_entry_post(user_input: str, question_number: str):
    local_question_number = int(question_number)
    local_question_number += 1
    equation_parts = validate_input(user_input)
    #if equation_parts is not None:
        #user_questions.append(user_input)
    footer = Form(Group(get_input(placeholder=f"Enter question #{local_question_number:>2}"), Button("Submit")),
                  Input(type="hidden", id="question-number", name="question_number", value=local_question_number),
                  id="trying", name="trying", post="madness-methods-entry", target_id=f"question-{local_question_number}", hx_swap_oob="true")
    if local_question_number > 10:
        return (Span(user_input), Form(Button("Start"), id="trying", hx_target="#main-card", hx_get="/madness-methods-questions", hx_swap_oob="true"))
    return (Span(user_input), footer)


# @rt("/madness-methods-questions", name="madness-methods-questions", methods=["get"])
# def madness_methods_questions():
#     question_number = 0
#     header = "Madness's Methods Question Answerer"
#     return_card = Card(Div(Form(Group(P(f"Question #{question_number + 1:>2}: {user_questions[question_number]} = "),
#                                       get_input(style="display:inline-block")))), header=header)
#     return return_card


@rt("/madness-methods-questions", name="madness-methods-questions", methods=["get"])
def madness_methods_questions():
    question_number = 0
    header = "Madness's Methods Question Answerer"
    
    # Inline text with input field
    inline_question = P(
        f"Question #{question_number + 1:>2}: {user_questions[question_number]} = ", 
        get_input(style="display: inline-block; width: 4ch; font-size: inherit; height: 1.6em; line-height: inherit; vertical-align: top; border: none; border-bottom: 1px solid; padding: 3px"),
        Button("Submit", style="display: inline-block; font-size: inherit; height: auto; padding: 0 10px; line-height: inherit; vertical-align: middle;")
    )
    
    # Wrapping the form around the inline question
    form = Form(inline_question, 
                id="inline-question-form", 
                post="madness-methods-questions-post", 
                target_id="main-card")

    return_card = Card(Div(form), header=header)
    return return_card


@rt("/madness-methods-questions", name="madness-methods-questions-post", methods=["post"])
def madness_methods_questions_post(user_input: str, question: str, correct_answer: str):
    pass


@rt("/electro-flash", methods=["get"])
def electro_flash():
    return Card("Electro Flash")
