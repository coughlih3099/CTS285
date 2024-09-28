# CTS 285
# MadMath
# Harley Coughlin
# 09/27/2024


from fasthtml.common import *
from answer_checker import check_answer
import re

css = Style(":root { --pico-font-size: 100%; --pico-font-family: Pacifico, mono; }")

app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route


nav_bar = Nav(Ul(Li(Strong("MadMath"))),
              Ul(Li(Details(Summary("Modes"),
                            Ul(
                                Li(A("Answer Checker", hx_target="", hx_get="")),
                                Li(A("Memory Bank")),
                                Li(A("Electro Flash"))),
                    cls="dropdown"))),
              cls="container")


def get_input(**kw):
    return Input(id="user_input", name="user_input", placeholder="Enter problem here", **kw)


@rt("/", methods=["get"])
def answer_checker():
    head = "Welcome to MadMath's Answer Checker!"
    instructions = Fieldset(Legend("Instructions:"),
                            Div(P("1. Enter a problem, e.g. 1 + 1 = 2"),
                                P("2. Press Submit"),
                                P("3. Answer Checker will tell you if you got the correct answer"),
                                P("4. Try again or try a new question")), style="border-right: 1px solid white")
    history = Fieldset(Legend("Problem History:"), Div(id="history"))
    middle = Grid(instructions, history)
    add = Form(Group(get_input(required=True), Button("Submit")))
    answer_check = Card(middle, header=head, footer=add)
    return Title("MadMath"), nav_bar, Div(answer_check, id="replacable", cls="container")
