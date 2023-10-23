#!/usr/bin/python3
"""
create a flask script that listen on 0.0.0.0:5000
and it should route to:
	/: Displays "Hello HBNB!"
"""

from flask import Flask
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbnb():
	""" Display 'Hello HBNB!' """
	return "Hello HBNB!"

if __name__== "__main__":
	app.run(host="0.0.0.0")
