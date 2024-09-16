# minimal Flask app

from flask import Flask, render_template

app = Flask(__name__)

app.config["DEBUG"] = True # always run in debug


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/action")
def action():
    return "Hello from the action route!"