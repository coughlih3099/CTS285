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
                                Li(A("Math Master", hx_target="replacable", hx_get="math-master")),
                                Li(A("Memory Bank", hx_target="replacable", hx_get="memory-bank")),
                                Li(A("Electro Flash", hx_target="replacable", hx_get="electro-flash"))),
                    cls="dropdown"))),
              cls="container")


def get_input(**kw):
    return Input(id="user_input", name="user_input", placeholder="Enter problem here", autocomplete="off", **kw)


@rt("/", methods=["get"])
def index():
    return Redirect("/math-master")


@rt("/math-master", methods=["get"])
def math_master():
    head = "Welcome to MadMath's Math Master!"
    instructions = Fieldset(Legend("Instructions:"),
                            Div(P("1. Enter a problem, e.g. 1 + 1 = 2"),
                                P("2. Press Submit"),
                                P("3. Math Master will tell you if you got the correct answer"),
                                P("4. Try again or try a new question")))
    history = Fieldset(Legend("Problem History:"), Div(id="history"), style="padding-left: 10px; border-left: 1px solid white")
    middle = Grid(instructions, history)
    add = Form(Group(get_input(required=True), Button("Submit")))
    math_master = Card(middle, header=head, footer=add)
    return Title("MadMath"), nav_bar, Div(math_master, id="replacable", cls="container")
