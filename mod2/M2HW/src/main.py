# CTS 285
# M2HW1
# Harley Coughlin
# 09/22/2024

from fasthtml.common import *

css = Style(":root { --pico-font-size:90%, --pico-font-family: Pacifico, cursive; }")


app = FastHTMLWithLiveReload(hdrs=(picolink, css))
rt = app.route


nav_bar = Nav(Ul(Li(Strong("Navbar"))),
              Ul(Li(Details(
                        Summary("Modes"),
                            Ul(
                                Li(A("Home", href="#")),
                                Li(A("Answer Checker", href="#")),
                                Li(A("Memory Bank", href="#")),
                                Li(A("Electro Flash", href="#"))
                              ),
                    cls="dropdown"))),
              cls="container")


@rt("/", methods=["get"])
def home():
    to_be_replaced = Body(Div(P("Here's some Text")), cls="container")
    return Titled("Dataman", nav_bar, to_be_replaced)
