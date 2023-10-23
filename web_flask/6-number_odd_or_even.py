#!/usr/bin/python3
""" Create a Flask script that listen on 0.0.0.0:5000 """
import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['ENV'] = 'production'
app.config['DEBUG'] = False


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ Displays 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Displays 'HBNB' """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """ Displays 'C' """
    return f"C {text.replace('_', ' ')}"


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def python(text="is cool"):
    """
    Displays 'Python' if no text is passed,
    otherwise Displays what is passed'
    """
    return f"Python {text.replace('_', ' ')}"

@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """ Displays 'n is a number' """
    return f"{n} is a number"

@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """ Displays 'n is a number' """
    return render_template("5-number.html", n=n)

@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    """Displays an HTML page only if <n> is an integer.

    States whether <n> is odd or even in the body.
    """
    return render_template("6-number_odd_or_even.html", n=n)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
