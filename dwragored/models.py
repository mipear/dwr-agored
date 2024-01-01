from dwragored import db


class Location(db.Model):
    # schema for the Location model
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(25), unique=True, nullable=False)
    experiences = db.relationship("Experience", backref="location", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.location_name


class Experience(db.Model):
    # schema for the experience model
    id = db.Column(db.Integer, primary_key=True)
    experience_title = db.Column(db.String(50), unique=True, nullable=False)
    experience_description = db.Column(db.Text, nullable=False)
    go_again = db.Column(db.Boolean, default=False, nullable=False)
    cleanliness_rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Experience: {1} | Go Again?: {2} | Cleanliness: {3}".format(
            self.id, self.experience_title, self.go_again, self.cleanliness_rating
        )