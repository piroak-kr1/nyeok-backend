from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/echo")
def echo():
    message = request.args.get(key="message")
    if message is None:
        return f"Test echo with /echo?message={escape("<message>")}"
    else:
        return f"echo: {escape(message)}"
