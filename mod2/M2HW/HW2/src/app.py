from flask import Flask, render_template


app = Flask(__name__)
app.config["DEBUG"] = True # run app in debug

@app.route("/")
def index():
    return render_template("index.html")
