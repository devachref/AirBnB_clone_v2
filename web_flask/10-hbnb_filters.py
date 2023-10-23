#!/usr/bin/python3
"""
Create a flask script that listen on 0.0.0.0:5000
and it should route to:
Routes:
    /hbnb_filters: HTML page with a list of all states and related cities.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """
    Route decorator for the "/hbnb_filters" endpoint.
    
    Retrieves all states and amenities from the storage.
    
    :return: The rendered template "10-hbnb_filters.html" with the states and amenities as parameters.
    :rtype: str
    """
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html", states=states, amenities=amenities)

@app.teardown_appcontext
def teardown(exc):
    """
    A function decorator that is used to register a function
    to be called when the application context is closed.
    This function is automatically called by Flask when the
    application context is destroyed. The `exc` parameter 
    is an exception or error that caused the teardown, if any.
    The function does not have any return value.
    """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
