# CTS285
# MadMath
# Harley Coughlin

from fasthtml.common import *
from answer_checker import check_answer
from answer_checker import get_answer
import re
import random


css = Style(":root { --pico-font-size: 100%; --pico-font-family: Pacifico, mono; }")

app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route


nav_bar = Nav(Ul(Li(Strong("MadMath"))),
              Ul(Li(Details(Summary("Modes"),
                            Ul(
                                Li(A("Math Master", hx_target="#main-card", hx_get="/math-master")),
                                Li(A("Madness's Methods", hx_target="#main-card", hx_get="/madness-methods")),
                                Li(A("Box Numbers", hx_target="#main-card", hx_get="/box-numbers"))),
                    cls="dropdown"))),
              cls="container")

@rt("/", methods=["get"])
def index():
    # TODO: change back to math-master
    return Title("MadMath"), nav_bar, Div(id="main-card", cls="container", hx_get="/math-master", hx_trigger="load")

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
                        P("Tip: All division is remainder division, enter the whole number and I'll return the remainder"),
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
    pattern_raw = r"^(\d{1,2}) *([+*-/]) *(\d{1,2}) *= *(\d{1,3}) *$"
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
    remainder = ""
    is_correct = False
    if equation_parts is not None:
        num1, num2, operation, answer = equation_parts
        if operation == "/" and num1 % num2 != 0:
            remainder = f", the remainder is {num1 % num2}, "
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
        return_string += remainder
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
    instructions = Div(P("Instructions:"), Ul(Li("Enter 10 questions (e.g. 1 + 1)"),
                                              Li("Each question must be unique"),
                                              Li("Once 10 questions have been answered, try to solve them"),
                                              Li("All division is remainder division, enter the whole number to solve division problems"),
                                              Li("Tip: the biggest number for operands is 99 and 999 for answers")))
    footer = Group(P("Press Start to begin entering questions"), Button("Start", hx_target="#main-card", hx_get="/madness-methods-entry"))
    return_card = Card(instructions, header=header, footer=footer, id="madness-methods-instructions")
    return return_card


def create_question(number: int):
    return Li(f"Question #{number:>2}: ", Span(id=f"question-{number}"), style="list-style-type: none")


@rt("/madness-methods-entry", name="madness-methods-entry", methods=["get"])
def madness_methods_entry():
    # clear the user_questions list
    user_questions.clear()
    user_questions_list.clear()
    question_number = "1"
    header = "Madness's Methods Question Entry"
    questions = Div(Ul(*[create_question(i + 1) for i in range(10)]))
    footer = Form(Group(get_input(placeholder=f"Enter question #{question_number:>2}"), Button("Submit")),
                  Input(type="hidden", id="question-number", name="question_number", value=question_number),
                  id="madness-start-button", name="madness-start-button", post="madness-methods-entry", target_id=f"question-{question_number}")
    return_card = Card(questions, header=header, footer=footer, id="madness-methods-entry")
    return return_card


user_questions = {}
user_questions_list = []

def validate_question(user_input:str) -> tuple[int, int, str] | None:
    pattern_raw = r"^(\d{1,2}) *([+*-/]) *(\d{1,2}) *$"
    equation_parts = re.match(pattern_raw, user_input)
    if equation_parts is not None:
        num1 = int(equation_parts[1])
        operation = equation_parts[2]
        num2 = int(equation_parts[3])
        return (num1, num2, operation)
    return None

@rt("/madness-methods-entry", name="madness-methods-entry-post", methods=["post"])
def madness_methods_entry_post(user_input: str, question_number: str):
    equation_parts = validate_question(user_input)
    if equation_parts is not None and user_input not in user_questions:
        user_questions[user_input] = False
        user_questions_list.append(user_input)
        local_question_number = int(question_number)
        local_question_number += 1
        footer = Form(Group(get_input(placeholder=f"Enter question #{local_question_number:>2}"), Button("Submit")),
                    Input(type="hidden", id="question-number", name="question_number", value=local_question_number),
                    id="madness-start-button", name="madness-start-button", post="madness-methods-entry", target_id=f"question-{local_question_number}", hx_swap_oob="true")
        if local_question_number > 10:
            return (Span(user_input), Group(P("Press Start to begin answering the questions"),
                                            Button("Start"), id="madness-start-button", hx_target="#main-card", hx_get="/madness-methods-questions", hx_swap_oob="true"))
        return (Span(user_input), footer)


@rt("/madness-methods-questions", name="madness-methods-questions", methods=["get"])
def madness_methods_questions():
    question_number = 0
    header = "Madness's Methods Question Answerer"
    
    # Inline text with input field
    inline_question = P(
        f"Question #{question_number + 1:>2}: {user_questions_list[question_number]} = ", 
        get_input(style="display: inline-block; width: 4ch; font-size: inherit; height: 1.6em; line-height: inherit; vertical-align: top; border: none; border-bottom: 1px solid; padding: 3px"),
        Button("Submit", style="display: inline-block; font-size: inherit; height: auto; padding: 0 10px; line-height: inherit; vertical-align: middle;")
    )
    
    # Wrapping the form around the inline question
    form = Form(inline_question, 
                Input(type="hidden", id="question_number", name="question_number", value=str(question_number)),
                id="inline-question-form", 
                post="madness-methods-questions-post", 
                hx_target="#inline-question-div")

    return_card = Card(Div(form, id="inline-question-div"), header=header)
    return return_card


@rt("/madness-methods-questions", name="madness-methods-questions-post", methods=["post"])
def madness_methods_questions_post(user_input: str, question_number: str):
    local_question_number = int(question_number)
    # This is the byproduct of my design decisions
    full_equation = user_questions_list[local_question_number] + " = " + user_input
    equation_parts = validate_input(full_equation)
    if equation_parts is not None:
        num1, num2, operation, answer = equation_parts
        # This just feels gross lol
        user_questions[user_questions_list[local_question_number]] = check_answer(num1, num2, operation, answer)
    if local_question_number < len(user_questions_list) - 1:
        local_question_number += 1
        question = f"Question #{local_question_number + 1:>2}: {user_questions_list[local_question_number]} = "
        inline_question = P(question,
                            get_input(style="display: inline-block; width: 4ch; font-size: inherit; height: 1.6em; line-height: inherit; vertical-align: top; border: none; border-bottom: 1px solid; padding: 3px"),
                            Button("Submit", style="display: inline-block; font-size: inherit; height: auto; padding: 0 10px; line-height: inherit; vertical-align: middle;")
                            )
        form = Form(inline_question,
                    Input(type="hidden", id="question_number", name="question_number", value=str(local_question_number)),
                    id="inline-question-form", 
                    post="madness-methods-questions-post", 
                    hx_target="#inline-question-div")
        return Div(form)
    else:
        return Div(hx_target="#main-card", hx_trigger="load", hx_get="/madness-methods-results", hx_swap_oop="true")


def create_list_item(key: str):
    return Li(Span(f"You got {key} {'correct' if user_questions[key] else 'incorrect'}"))


def get_num_correct():
    num_correct = 0
    for val in user_questions.values():
        if val is True:
            num_correct += 1
    return num_correct


@rt("/madness-methods-results", methods=["get"])
def madness_methods_results():
    header = f"Madness's Methods Results - Number Correct: {get_num_correct()}/10"
    if len(user_questions_list) != 0:
        return Card(Div(Ol(*[create_list_item(key) for key in user_questions.keys()])), header=header)


def generate_problem(difficulty: str = "easy") -> tuple[int, int, str, int]:
    # True if difficulty == hard
    difficult = difficulty == "hard"
    ANSWER_MAX = 999
    RAND_MAX =  99 if difficult else 12
    RAND_MIN = 3 if difficult else 1
    operations = ["+", "-", "*", "/"]
    num1 = random.randint(RAND_MIN, RAND_MAX)
    operation = random.choice(operations)
    match operation:
        case ("-"|"/"):
            num2 = random.randint(RAND_MIN, num1)
        case "*":
            num2 = ANSWER_MAX // num1 if difficult else random.randint(RAND_MIN, RAND_MAX)
        case "+":
            num2 = random.randint(RAND_MIN, RAND_MAX)
    answer = get_answer(num1, num2, operation)
    return (num1, num2, operation, answer)


@rt("/box-numbers", methods=["get"])
def box_numbers():
    header = "Box Numbers"
    instructions = Ol(Li("Select a difficulty"),
                      Li("Choose which box to solve for"),
                      Li("???"),
                      Li("Profit"))
    difficulty_options = Fieldset(Legend("Difficulty:"),
                                  Label(Input(type="radio", name="difficulty", value="easy", checked=True), "Easy"),
                                  Label(Input(type="radio", name="difficulty", value="hard"), "Hard")
                                  )
    box_options = Fieldset(Legend("Solve for:"),
                           Label(Input(type="radio", name="box", value="left", checked=True), "Left Box"),
                           Label(Input(type="radio", name="box", value="right"), "Right Box"),
                           Label(Input(type="radio", name="box", value="answer"), "Answer Box"),
                           )
    options = Div(difficulty_options, box_options)
    middle = Group(Div(instructions), options)
    form = Form(
        middle,
        Button("Start", type="submit"),
        hx_post="/box-numbers-questions",
        hx_target="#main-card"
    )
    card = Card(form, header=header)
    return card


@rt("/box-numbers-check", methods=["post"])
def box_numbers_check(user_input: str, difficulty: str, box: str, correct_answer: str, number_correct: str, question_number: str):
    local_input = int(user_input)
    local_correct_answer = int(correct_answer)
    local_number_correct = int(number_correct)
    local_question_number = int(question_number)
    if local_input == local_correct_answer:
        local_number_correct += 1
    local_question_number += 1
    return box_numbers_questions(difficulty, box, str(local_number_correct), str(local_question_number))


@rt("/box-numbers-questions", methods=["post"])
def box_numbers_questions(difficulty: str, box: str, number_correct: str = "0", question_number: str = "0"):
    num1, num2, operation, answer = generate_problem(difficulty=difficulty)
    match box:
        case "left":
            question = f"[?] {operation} {num2} = {answer}"
            correct_answer = num1
        case "right":
            question = f"{num1} {operation} [?] = {answer}"
            correct_answer = num2
        case "answer":
            question = f"{num1} {operation} {num2} = [?]"
            correct_answer = answer
    question_form = Form(
            P(f"Solve the equation {question}"),
            get_input(placeholder="Enter your answer", autofocus=True),
            Input(type="hidden", name="difficulty", value=difficulty),
            Input(type="hidden", name="box", value=box),
            Input(type="hidden", name="correct_answer", value=str(correct_answer)),
            Input(type="hidden", name="number_correct", value=number_correct),
            Input(type="hidden", name="question_number", value=question_number),
            Button("Submit", type="submit"),
            hx_post="/box-numbers-check",
            hx_target="#main-card"
    )
    if int(question_number) < 10:
        return Card(question_form, header=f"Box Numbers - Question #{int(question_number) + 1:>2}")
    else:
        return box_numbers_results(str(number_correct))


@rt("/box-numbers-results", methods=["get"])
def box_numbers_results(number_correct):
    footer = Button("Restart", hx_get="/box-numbers", hx_target="#main-card")
    return Card(f"{number_correct} correct out of 10", header="Box Numbers Results", footer=footer)
