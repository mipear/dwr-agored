from flask import render_template, request, redirect, url_for, flash, session
from dwragored import app, db, login_manager
from dwragored.models import Location, MySwim, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
    LoginManager,
)

# UserMixin
class Users(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/allswims")
def allswims():
    myswim = list(MySwim.query.order_by(MySwim.id).all())
    return render_template("myswim.html", myswim=myswim)

# Home Page
@app.route("/")
def homepage():
    print(current_user)
    return render_template("homepage.html")

@app.route("/user_login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                
                flash("Logged in Successfully!", category="success")
                login_user(user, remember=False)
                session["user"] = user.username
                session["user"] = user.username
                return redirect(url_for("profile", username=current_user.username))
            else:
                flash("Incorrect Password, Try again.", category="error")
        else:
            flash("User does not exist", category="error")
    return render_template("login.html", user=current_user)




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

# Register account
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
        return redirect(url_for("profile", username=username))

    return render_template("register.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

# Location
@app.route("/location")
def location():
    location = list(Location.query.order_by(Location.location_name).all())
    return render_template("location.html", location=location)

# Add location
@app.route("/add_location", methods=["GET", "POST"])
@login_required
def add_location():
    if request.method == "POST":
        location = Location(location_name=request.form.get("location_name"),user_id=current_user.id)
        db.session.add(location)
        db.session.commit()
        return redirect(url_for("location"))
    return render_template("add_location.html")

# Edit location
@app.route("/edit_location/<int:location_id>", methods=["GET", "POST"])
@login_required
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    if request.method == "POST":
        location.location_name = request.form.get("location_name")
        db.session.commit()
        return redirect(url_for("location"))
    return render_template("edit_location.html", location=location)

# Delete location
@app.route("/delete_location/<int:location_id>")
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    return redirect(url_for("location"))

# Add swim
@app.route("/add_swim", methods=["GET", "POST"])
@login_required
def add_swim():
    print(current_user)
    location = list(Location.query.order_by(Location.location_name).all())
    if request.method == "POST":
        print(request.form)
        myswim = MySwim(
            myswim_title=request.form.get("myswim_title"),
            myswim_description=request.form.get("myswim_description"),
            go_again=bool(True if request.form.get("go_again") else False),
            cleanliness_rating=request.form.get("cleanliness_rating"),
            date=request.form.get("date"),
            location_id=request.form.get("location_id"),
            user_id=current_user.id
        )

        db.session.add(myswim)
        db.session.commit()
        return redirect(url_for("allswims"))
    return render_template("add_swim.html", location=location)

# Edit swim
@app.route("/edit_swim/<int:myswim_id>", methods=["GET", "POST"])
@login_required
def edit_swim(myswim_id):
    myswim = MySwim.query.get_or_404(myswim_id)
    location = list(Location.query.order_by(Location.location_name).all())
    print(f'swim user id: {myswim.user_id}')
    print(f'current user id: {current_user.id}')
    if myswim.user_id == current_user.id:
        if request.method == "POST":
            myswim.myswim_title = request.form.get("myswim_title")
            myswim.myswim_description = request.form.get("myswim_description")
            myswim.go_again = bool(True if request.form.get("go_again") else False)
            myswim.cleanliness_rating = request.form.get("cleanliness_rating")
            myswim.date = request.form.get("date")
            myswim.location_id = request.form.get("location_id")
        
            db.session.commit()
        return render_template("edit_swim.html", myswim=myswim, location=location)
    
    else:
        flash("You cannot edit other users' swims!")
        return redirect(url_for("allswims"))
    

# Delete swim
@app.route("/delete_swim/<int:myswim_id>")
@login_required
def delete_swim(myswim_id):
    myswim = MySwim.query.get_or_404(myswim_id)
    db.session.delete(myswim)
    db.session.commit()
    return redirect(url_for("allswims"))

# Profile
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    
    user = User.query.filter_by(username=username)
    if user:
        return render_template("profile.html", username=username)
    else:
        return render_template("user_not_found.html")


    logout_user(user, remember=False)

@app.route("/user_logout")
def logout():
    logout_user(user, remember=False)
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

    



