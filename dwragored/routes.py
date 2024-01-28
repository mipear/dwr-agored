from flask import render_template, request, redirect, url_for, flash, session
from dwragored import app, db
from dwragored.models import Location, MySwim, User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/home")
def home():
    myswim = list(MySwim.query.order_by(MySwim.id).all())
    return render_template("myswim.html", myswim=myswim)


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/loginaccount", methods=["GET", "POST"])
def loginaccount():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username
            flash("Welcome, {}".format(username))
            return redirect(url_for(
                "profile", username=session["user"]))
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("loginaccount"))

    return render_template("loginaccount.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        existing_user = User.query.filter_by(username=username.lower()).first()

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        new_user = User(username=username.lower(), password=password)
        db.session.add(new_user)
        session["user"] = username
        print( "user in session -register route = ",session["user"])
        db.session.commit()

        flash("Registration Successful!")
        # return redirect(url_for("profile", username=session["user"]))
        return redirect(url_for("profile", username=username))

    return render_template("register.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

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


@app.route("/edit_swim/<int:myswim_id>", methods=["GET", "POST"])
def edit_swim(myswim_id):
    myswim = MySwim.query.get_or_404(myswim_id)
    location = list(Location.query.order_by(Location.location_name).all())
    if request.method == "POST":
        myswim.myswim_title = request.form.get("myswim_title")
        myswim.myswim_description = request.form.get("myswim_description")
        myswim.go_again = bool(True if request.form.get("go_again") else False)
        myswim.cleanliness_rating = request.form.get("cleanliness_rating")
        myswim.date = request.form.get("date")
        myswim.location_id = request.form.get("location_id")
        db.session.commit()
    return render_template("edit_swim.html", myswim=myswim, location=location)


@app.route("/delete_swim/<int:myswim_id>")
def delete_swim(myswim_id):
    myswim = MySwim.query.get_or_404(myswim_id)
    db.session.delete(myswim)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    
    # user = User.query.filter_by(username=session["user"]).first()
    user = User.query.filter_by(username=username)
    if user:
        # username = user.username
        return render_template("profile.html", username=username)
    else:
        return render_template("user_not_found.html")

@app.route("/logoutaccount")
def logoutaccount():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("loginaccount"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
