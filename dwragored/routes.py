from flask import render_template
from dwragored import app, db
from dwragored.models import Location, Experience


@app.route("/")
def home():
    return render_template("base.html")
