from app import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    phone = db.Column(db.String)
    is_admin = db.Column(db.Boolean)
    verification_code = db.Column(db.String)
    is_verified = db.Column(db.Boolean)
    city = db.Column(db.String,)
    country = db.Column(db.String)
    address = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    date_of_birth = db.Column(db.String)


class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    is_profile = db.Column(db.Boolean, nullable=False)

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    id = auto_field()
    username = auto_field()
    email = auto_field()
    name = auto_field()
    surname = auto_field()
    gender = auto_field()
    age = auto_field()
    phone = auto_field()
    city = auto_field()
    countr = auto_field()
    address = auto_field()
    postal_code = auto_field()
    is_admin = auto_field()
    date_of_birth = auto_field()

class ImageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Image
        load_instance = True
