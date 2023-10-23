#!/usr/bin/python3
""" Lists all State objects from the database hbtn_0e_6_usa """
from flask import Flask, render_template
from models import storage

app = Flask(__name__)

@app.route("/states_list", strict_slashes=False)
def states_list():
    """ Lists all State objects from the database hbtn_0e_6_usa """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)

@app.teardown_appcontext
def teardown_db(exc):
    """ Remove the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
