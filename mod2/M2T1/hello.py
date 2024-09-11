# minimal Flask app

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <h3>Hello, CTS285!!!</h3>
    <p>This is a paragraph</p>
    <a href="action">Click here</a>
    """

@app.route("/action")
def action():
    return "Hello from the action route!"