# CTS 285
# M2HW1
# Harley Coughlin
# 09/22/2024

from fasthtml.common import *

css = Style(":root { --pico-font-size:90%, --pico-font-family: Pacifico, cursive; }")


app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route


nav_bar = Nav(Ul(Li(Strong("Dataman"))),
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
    return Title("Dataman"), nav_bar, Div(P("Home"), id="to_replace", cls="container")


@rt("/home_again", methods=["get"])
def home_again():
    return Div(P("Home again"), cls="container")


def get_input(**kw):
    return Input(id="user_input", name="user_input", placeholder="Enter text here", **kw)


@rt("/answer_check", methods=["get"])
def do_it():
    add = Form(Group(get_input(required=True), Button("Submit")), post="insert_history", target_id="history", hx_swap="beforeend")
    card = Card(Div(P("Enter some text and submit"), id="history"), header="Answer Checker", footer=add)
    return card
                

@rt("/answer_check", name="insert_history", methods=["post"])
def maybe(user_input: str):
    return P(f"You entered: {user_input}"), get_input(hx_swap_oob="true")
