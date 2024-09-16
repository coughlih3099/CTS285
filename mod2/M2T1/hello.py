# minimal Flask app

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config["DEBUG"] = True # always run in debug

# TODO: Make this a database
comments = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)

    comments.append(request.form["contents"])
    return redirect(url_for('index'))


@app.route("/action")
def action():
    return "Hello from the action route!"