# CTS285
# MadMath
# Harley Coughlin

from fasthtml.common import *
from answer_checker import check_answer
import re


css = Style(":root { --pico-font-size: 100%; --pico-font-family: Pacifico, mono; }")

app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route

# Server-side storage for game state
math_master_state = {}

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
    math_master_state['problem_number'] = 0
    math_master_state['number_of_tries'] = 0
    math_master_state['number_correct'] = 0
    math_master_state['history'] = []
