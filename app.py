from functools import wraps
import connexion
from flask import request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
from flask_bcrypt import Bcrypt
from random import randint
from flask_mail import Mail, Message
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import secrets
import string
import jwt
import time


JWT_SECRET = 'USER MS SECRET'
JWT_LIFETIME_SECONDS = 600000

INVENTORY_APIKEY = "INVENTORY MS SECRET"
PAYMENTS_APIKEY = "PAYMENTS MS SECRET"
INVOICES_APIKEY = "INVOICES MS SECRET"
SHIPPING_APIKEY = "SHIPPING MS SECRET"
SHOPPING_CART_APIKEY = "SHOPPING CART MS SECRET"
DISCOUNTS_APIKEY = "DISCOUNTS MS SECRET"
STATISTICS_APIKEY = "STATISTICS MS SECRET"
LOCATIONS_APIKEY = "LOCATIONS MS SECRET"
RESERVE_APIKEY = "RESERVE MS SECRET"
SOCIAL_APIKEY = "SOCIAL MS SECRET"


def has_role(arg):
    def has_role_inner(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                headers = request.headers
                if 'AUTHORIZATION' in headers:
                    token = headers['AUTHORIZATION'].split(' ')[1]
                    decoded_token = decode_token(token)
                    if 'admin' in decoded_token['roles']:
                        return fn(*args, **kwargs)
                    for role in arg:
                        if role in decoded_token['roles']:
                            return fn(*args, **kwargs)
                    abort(401)
                return fn(*args, **kwargs)
            except Exception as e:
                abort(401)
        return decorated_view
    return has_role_inner


def auth(auth_body):
    timestamp = int(time.time())
    found_user = db.session.query(User).filter_by(username=auth_body['username']).first()
    user_id = found_user.id
    roles = []
    if found_user.is_admin:
        roles.append("admin")
    else:
        roles.append("basic_user")
    payload = {
        "iss": 'User Microservice',
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": user_id,
        "roles": roles,
        "user-details": user_schema.dump(found_user)
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return encoded


def auth_microservice(auth_body_microservice):
    apikey = auth_body_microservice['apikey']
    roles = []        
    if apikey == INVENTORY_APIKEY:
        roles.append("inventory")
        sub = 'inventory'
    elif apikey == PAYMENTS_APIKEY:
        roles.append("payments")
        sub = 'payments'
    elif apikey == INVOICES_APIKEY:
        roles.append("invoices")
        sub = 'invoices'
    elif apikey == SHIPPING_APIKEY:
        roles.append("shipping")
        sub = 'shipping'
    elif apikey == SHOPPING_CART_APIKEY:
        roles.append("shopping_cart")
        sub = 'shopping_cart'
    elif apikey == DISCOUNTS_APIKEY:
        roles.append("discounts")
        sub = 'discounts'
    elif apikey == STATISTICS_APIKEY:
        roles.append("statistics")
        sub = 'statistics'
    elif apikey == LOCATIONS_APIKEY:
        roles.append("locations")
        sub = 'locations'
    elif apikey == RESERVE_APIKEY:
        roles.append("reserve")
        sub = 'reserve'
    elif apikey == SOCIAL_APIKEY:
        roles.append("social")
        sub = 'social'

    timestamp = int(time.time())
    payload = {
        "iss": 'my app',
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": sub,
        "roles": roles
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return encoded


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])


#endpoints
@has_role(["admin"])
def send_verification_email(user_id):
  found_user = db.session.query(User).get(user_id)
  if found_user:
      msg = Message('Hello', sender = 'soauserms@gmail.com', recipients = [found_user.email])
      msg.subject='Verification Code For Your Account'
      msg.body = "Dear "+str(found_user.name)+" "+str(found_user.surname)+",\n" + "Your verificaiton code is: " + str(found_user.verification_code)
      mail.send(msg)
      return 200
  else:
      return 404

# TODO: da se dodaj gender i date of birth
def registration(user_body):
    found_user = db.session.query(User).filter_by(username=user_body['username']).first()
    if not found_user:
        if user_body['password'] == user_body['repeated_password']:
            date_of_birth = datetime.strptime(user_body['date_of_birth'], '%m-%d-%Y')
            today = date.today()
            age = relativedelta(today, date_of_birth).years
            letter_and_digits = string.ascii_letters + string.digits
            code = ''.join(secrets.choice(letter_and_digits) for i in range(6))
            new_user = User(username=user_body['username'],
            email=user_body['email'], name=user_body['name'],
            surname=user_body['surname'], password=bcrypt.generate_password_hash(user_body['password']),
            is_admin=False, is_verified=False, date_of_birth=user_body['date_of_birth'],
             gender=user_body['gender'], age=age, verification_code=code)
        else:
            return 400
    else:
        return 409
    db.session.add(new_user)
    db.session.commit()
    send_verification_email(new_user.id)
    #TODO: send notification to Statistics MS
    return user_schema.dump(new_user)


def get_role(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return {'is_admin': found_user.is_admin}
    else:
        return 404


def get_user_details(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return user_schema.dump(found_user)
    else:
        return 404


@has_role(["admin", "social"])
def get_user_images(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        images = db.session.query(Image).filter_by(user_id=user_id).all()
        return image_schema.dump(images, many=True)
    else:
        return 404


@has_role(["admin", "social"])
def add_image_to_user(image_body):
    found_user = db.session.query(User).get(image_body['user_id'])
    if found_user:
        image = Image(link=image_body['image_link'], is_profile=image_body['is_profile'], user_id=image_body['user_id'])
        db.session.add(image)
        db.session.commit()
        images = db.session.query(Image).filter_by(user_id=image_body['user_id']).all()
        if image.is_profile:
            for i in images:
                if i.id != image.id:
                    i.is_profile = False
                    db.session.commit()
        return image_schema.dump(images, many=True)
    else:
        return 404


@has_role(["admin", "basic_user"])
def change_password(password_body):
    found_user = db.session.query(User).get(password_body['user_id'])
    if found_user:
        if bcrypt.check_password_hash(found_user.password, password_body['old_password']):
            found_user.password = bcrypt.generate_password_hash(password_body['new_password'])
            db.session.commit()
            return user_schema.dump(found_user)
        else:
            return 400
    else:
        return 404


@has_role(["admin", "basic_user"])
def change_phone(phone_body):
    found_user = db.session.query(User).get(phone_body['user_id'])
    if found_user:
        found_user.phone = phone_body['phone']
        db.session.commit()
        return user_schema.dump(found_user)
    else:
        return 404


@has_role(["admin", "basic_user"])
def change_city(city_body):
    found_user = db.session.query(User).get(city_body['user_id'])
    if found_user:
        found_user.city = city_body['city']
        db.session.commit()
        return user_schema.dump(found_user)
    else:
        return 404


@has_role(["admin", "basic_user"])
def change_country(country_body):
    found_user = db.session.query(User).get(country_body['user_id'])
    if found_user:
        found_user.country = country_body['country']
        db.session.commit()
        return user_schema.dump(found_user)
    else:
        return 404


@has_role(["admin", "basic_user"])
def change_address(address_body):
    found_user = db.session.query(User).get(address_body['user_id'])
    if found_user:
        found_user.address = address_body['address']
        db.session.commit()
        return user_schema.dump(found_user)
    else:
        return 404


@has_role(["admin", "basic_user"])
def change_postal_code(postal_body):
    found_user = db.session.query(User).get(postal_body['user_id'])
    if found_user:
        found_user.postal_code = postal_body['postal_code']
        db.session.commit()
        return user_schema.dump(found_user)
    else:
        return 404


@has_role(["admin", "basic_user"])
def verify_user(verification_body):
    found_user = db.session.query(User).get(verification_body['user_id'])
    if found_user:
        if found_user.verification_code == verification_body['code']:
            found_user.is_verified = True
            db.session.commit()
            return 200
        else:
            return 400
    else:
        return 404


def get_all_users():
    users = db.session.query(User).all()
    return user_schema.dump(users,many=True)


@has_role(["admin"])
def delete_user(user_id):
    user_images = db.session.query(Image).filter_by(user_id=user_id).all()
    for i in user_images:
        delete_image(i.id)
    db.session.query(User).filter_by(id=user_id).delete()
    db.session.commit()


@has_role(["admin"])
def delete_image(image_id):
    db.session.query(Image).filter_by(id=image_id).delete()
    db.session.commit()


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")


# Setup for mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'soauserms@gmail.com'
app.config['MAIL_PASSWORD'] = 'soauserms123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# dummy reference for migrations only
from models import User, Image, UserSchema, ImageSchema


image_schema = ImageSchema()
user_schema = UserSchema(exclude=['is_verified', 'password', 'verification_code'])


if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
