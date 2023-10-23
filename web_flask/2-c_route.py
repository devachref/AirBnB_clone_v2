#!/usr/bin/python3
""" Create a Flask script that listen on 0.0.0.0:5000 """
from flask import Flask
app = Flask(__name__)


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
    return "C {}".format(text.replace("_", " "))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
