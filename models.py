from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    gender = db.Column(db.Integer)
    age = db.Column(db.Integer)
    phone = db.Column(db.String)
    is_admin = db.Column(db.Boolean)
    verification_code = db.Column(db.Integer,)
    is_verified = db.Column(db.Boolean,)
    city = db.Column(db.String,)
    country = db.Column(db.String)
    address = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    date_of_birth = db.Column(db.Integer)
    images = db.Column(db.ARRAY(db.Integer))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=False)
    is_profile = db.Column(db.Boolean, nullable=False)
