from flask import render_template, request, redirect, url_for
from dwragored import app, db
from dwragored.models import Location, MySwim


@app.route("/")
def home():
    return render_template("myswim.html")


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    if request.method == "POST":
        location = Location(location_name=request.form.get("location_name"))
        db.session.add(location)
        db.session.commit()
        return redirect(url_for("location"))
    return render_template("add_location.html")