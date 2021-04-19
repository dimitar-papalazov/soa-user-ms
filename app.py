import connexion
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

# INVOICE_APIKEY = '123abc'
# SHIPPING_APIKEY = 'abc321'


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


# @has_role(['invoice', 'shipping'])
# def get_test1(test1_id):
#     data = request.data
#     headers = request.headers
#     # token = headers['HTTP_AUTHORIZATION']
#     return {'id': 1, 'name': 'name', 'entered_id': test1_id}


def auth(auth_body):
    timestamp = int(time.time())
    found_user = db.session.query(User).filter_by(username=auth_body['username']).first()
    user_id = found_user.id
    roles = []
    if found_user.is_admin:
        roles.append("admin")
    payload = {
        "iss": 'User Microservice',
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": user_id,
        "roles": roles,
        "user-details": user_to_json(found_user)
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return encoded


# def auth_microservice(auth_body_microservice):
#     apikey = auth_body_microservice['apikey']

#     if apikey == INVOICE_APIKEY:
#         roles = ['invoice']
#         sub = 'invoice'
#     elif apikey == SHIPPING_APIKEY:
#         roles = ['shipping', 'editing']
#         sub = 'shipping'

#     timestamp = int(time.time())
#     payload = {
#         "iss": 'my app',
#         "iat": int(timestamp),
#         "exp": int(timestamp + JWT_LIFETIME_SECONDS),
#         "sub": sub,
#         "roles": roles
#     }
#     encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
#     return encoded


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])


def user_to_json(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'name': user.name,
        'surname': user.surname,
        'gender': user.gender,
        'age': user.age,
        'phone': user.phone,
        'city': user.city,
        'country': user.country,
        'address': user.address,
        'postalCode': user.postal_code,
        'isAdmin': user.is_admin,
        'dateOfBirth': user.date_of_birth
    }


#endpoints
def sendVerificationEmail(user_id):
  found_user = db.session.query(User).get(user_id)
  if found_user:
      msg = Message('Hello', sender = 'soauserms@gmail.com', recipients = [found_user.email])
      msg.subject='Verification Code For Your Account'
      msg.body = "Dear "+str(found_user.name)+" "+str(found_user.surname)+",\n" + "Your verificaiton code is: " + str(found_user.verification_code)
      mail.send(msg)
      return {'message': "Successfully sent!"}
  else:
      return {'error': '{} not found'.format(user_id)}, 404

# TODO: da se dodaj gender i date of birth
def registration(user_body):
    found_user = db.session.query(User).filter_by(username=user_body['username']).first()
    if not found_user:
        if user_body['password'] == user_body['repeatedPassword']:
            date_of_birth = datetime.strptime(user_body['dateOfBirth'], '%m-%d-%Y')
            today = date.today()
            age = relativedelta(today, date_of_birth).years
            letter_and_digits = string.ascii_letters + string.digits
            code = ''.join(secrets.choice(letter_and_digits) for i in range(6))
            new_user = User(username=user_body['username'],
            email=user_body['email'], name=user_body['name'],
            surname=user_body['surname'], password=bcrypt.generate_password_hash(user_body['password']),
            is_admin=False, is_verified=False, date_of_birth=user_body['dateOfBirth'],
             gender=user_body['gender'], age=age, verification_code=code)
        else:
            return {'error': '{} passwords do not match'.format(user_body['username'])}, 400
    else:
        return {'error': '{} already exists'.format(user_body['username'])}, 409
    db.session.add(new_user)
    db.session.commit()
    sendVerificationEmail(new_user.id)
    #TODO: send notification to Statistics MS
    return user_to_json(new_user)


def getRole(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return {'isAdmin': found_user.is_admin}
    else:
        return {'error': '{} not found'.format(user_id)}, 404


def getUserDetails(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return user_to_json(found_user)
    else:
        return {'error': '{} not found'.format(user_id)}, 404


def getUserImages(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        images = db.session.query(Image).filter_by(user_id=user_id).all()
        json_images = []
        for i in images:
            json_images.append({'id': i.id, 'link': i.link, 'is_profile': i.is_profile})
        print(json_images)
        return {'images': json_images}
    else:
        return {'error': '{} not found'.format(user_id)}, 404


def addImageToUser(image_body):
    found_user = db.session.query(User).get(image_body['user_id'])
    if found_user:
        image = Image(link=image_body['imageLink'], is_profile=image_body['isProfile'], user_id=image_body['user_id'])
        db.session.add(image)
        db.session.commit()
        images = db.session.query(Image).filter_by(user_id=image_body['user_id']).all()
        if image.is_profile:
            for i in images:
                if i.id != image.id:
                    i.is_profile = False
                    db.session.commit()
        json_images = []
        for i in images:
            json_images.append({'id': i.id, 'link': i.link, 'is_profile': i.is_profile})
        print(json_images)
        return {'images': json_images}
    else:
        return {'error': '{} not found'.format(user_id)}, 404


def changePassword(password_body):
    found_user = db.session.query(User).get(password_body['user_id'])
    if found_user:
        if bcrypt.check_password_hash(found_user.password, password_body['oldPassword']):
            found_user.password = bcrypt.generate_password_hash(password_body['newPassword'])
            db.session.commit()
            return user_to_json(found_user)
        else:
            return {'error': '{} passwords do not match'.format(user_body['username'])}, 400
    else:
        return {'error': '{} not found'.format(password_body['user_id'])}, 404

def changePhone(phone_body):
    found_user = db.session.query(User).get(phone_body['user_id'])
    if found_user:
        found_user.phone = phone_body['phone']
        db.session.commit()
        return user_to_json(found_user)
    else:
        return {'error': '{} not found'.format(phone_body['user_id'])}, 404


def changeCity(city_body):
    found_user = db.session.query(User).get(city_body['user_id'])
    if found_user:
        found_user.city = city_body['city']
        db.session.commit()
        return user_to_json(found_user)
    else:
        return {'error': '{} not found'.format(city_body['user_id'])}, 404


def changeCountry(country_body):
    found_user = db.session.query(User).get(country_body['user_id'])
    if found_user:
        found_user.country = country_body['country']
        db.session.commit()
        return user_to_json(found_user)
    else:
        return {'error': '{} not found'.format(country_body['user_id'])}, 404


def changeAddress(address_body):
    found_user = db.session.query(User).get(address_body['user_id'])
    if found_user:
        found_user.address = address_body['address']
        db.session.commit()
        return user_to_json(found_user)
    else:
        return {'error': '{} not found'.format(address_body['user_id'])}, 404


def changePostalCode(postal_body):
    found_user = db.session.query(User).get(postal_body['user_id'])
    if found_user:
        found_user.postal_code = postal_body['postalCode']
        db.session.commit()
        return user_to_json(found_user)
    else:
        return {'error': '{} not found'.format(postal_body['user_id'])}, 404


def verifyUser(verification_body):
    found_user = db.session.query(User).get(verification_body['user_id'])
    if found_user:
        if found_user.verification_code == verification_body['code']:
            found_user.is_verified = True
            db.session.commit()
            return {'message': "Successfully verified!"}
        else:
            return {'error': '{} codes do not match'.format(found_user.username)}, 400
    else:
        return {'error': '{} not found'.format(verification_body['user_id'])}, 404


def getAllUsers():
    users = db.session.query(User).all()
    users_json = []
    for user in users:
        users_json.append(user_to_json(user))
    return users_json


def deleteUser(user_id):
    db.session.query(User).filter_by(id=user_id).delete()
    return {'message': 'User successfully deleted'}, 200


def deleteImage(image_id):
    db.session.query(Image).filter_by(id=image_id).delete()
    return {'message': 'Image successfully deleted'}, 200


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
from models import User, Image


if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
