from flask import render_template, request, redirect, url_for
from dwragored import app, db
from dwragored.models import Location, MySwim


@app.route("/")
def home():
    myswim = list(MySwim.query.order_by(MySwim.id).all())
    return render_template("myswim.html", myswim=myswim)


@app.route("/location")
def location():
    location = list(Location.query.order_by(Location.location_name).all())
    return render_template("location.html", location=location)


@app.route("/add_location", methods=["GET", "POST"])
def add_location():
    if request.method == "POST":
        location = Location(location_name=request.form.get("location_name"))
        db.session.add(location)
        db.session.commit()
        return redirect(url_for("location"))
    return render_template("add_location.html")

@app.route("/edit_location/<int:location_id>", methods=["GET", "POST"])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    if request.method == "POST":
        location.location_name = request.form.get("location_name")
        db.session.commit()
        return redirect(url_for("location"))
    return render_template("edit_location.html", location=location)

@app.route("/delete_location/<int:location_id>")
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for("location"))

@app.route("/add_swim", methods=["GET", "POST"])
def add_swim():
    location = list(Location.query.order_by(Location.location_name).all())
    if request.method == "POST":
        print(request.form)
        myswim = MySwim(
            myswim_title=request.form.get("myswim_title"),
            myswim_description=request.form.get("myswim_description"),
            go_again=bool(True if request.form.get("go_again") else False),
            cleanliness_rating=request.form.get("cleanliness_rating"),
            date=request.form.get("date"),
            location_id=request.form.get("location_id")
        )
        
        db.session.add(myswim)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_swim.html", location=location)
