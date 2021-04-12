import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
from flask_bcrypt import Bcrypt
from random import randint
from flask_mail import Mail, Message

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

def registration(user_body):
    found_user = db.session.query(User).filter_by(username=user_body['username']).first()
    if not found_user:
        if user_body['password'] == user_body['repeatedPassword']:
            new_user=User(username=user_body['username'],
            email=user_body['email'], name=user_body['name'],
            surname=user_body['surname'], password=bcrypt.generate_password_hash(user_body['password']),
            is_admin=False, is_verified=False, verification_code=randint(1000, 9999))
        else:
            return {'error': '{} passwords do not match'.format(user_body['username'])}, 400
    else:
        return {'error': '{} already exists'.format(user_body['username'])}, 409
    db.session.add(new_user)
    db.session.commit()
    sendVerificationEmail(new_user.id)
    #TODO: send notification to Statistics MS
    return {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'name': new_user.name,
        'surname': new_user.surname,
        'gender': new_user.gender,
        'age': new_user.age,
        'phone': new_user.phone,
        'city': new_user.city,
        'country': new_user.country,
        'address': new_user.address,
        'postalCode': new_user.postal_code,
        'isAdmin': new_user.is_admin,
        'dateOfBirth': new_user.date_of_birth
    }

def getRole(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return {'isAdmin': found_user.is_admin}
    else:
        return {'error': '{} not found'.format(user_id)}, 404

def getUserDetails(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
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
            return {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'name': new_user.name,
                'surname': new_user.surname,
                'gender': new_user.gender,
                'age': new_user.age,
                'phone': new_user.phone,
                'city': new_user.city,
                'country': new_user.country,
                'address': new_user.address,
                'postalCode': new_user.postal_code,
                'isAdmin': new_user.is_admin,
                'dateOfBirth': new_user.date_of_birth
            }
        else:
            return {'error': '{} passwords do not match'.format(user_body['username'])}, 400
    else:
        return {'error': '{} not found'.format(password_body['user_id'])}, 404

def changeGender(gender_body):
    found_user = db.session.query(User).get(gender_body['user_id'])
    if found_user:
        found_user.gender = gender_body['gender']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(gender_body['user_id'])}, 404

def changeAge(age_body):
    found_user = db.session.query(User).get(age_body['user_id'])
    if found_user:
        found_user.age = age_body['age']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(age_body['user_id'])}, 404

def changePhone(phone_body):
    found_user = db.session.query(User).get(phone_body['user_id'])
    if found_user:
        found_user.phone = phone_body['phone']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(phone_body['user_id'])}, 404

def changeCity(city_body):
    found_user = db.session.query(User).get(city_body['user_id'])
    if found_user:
        found_user.city = city_body['city']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(city_body['user_id'])}, 404

def changeCountry(country_body):
    found_user = db.session.query(User).get(country_body['user_id'])
    if found_user:
        found_user.country = country_body['country']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(country_body['user_id'])}, 404

def changeAddress(address_body):
    found_user = db.session.query(User).get(address_body['user_id'])
    if found_user:
        found_user.address = address_body['address']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(address_body['user_id'])}, 404

def changePostalCode(postal_body):
    found_user = db.session.query(User).get(postal_body['user_id'])
    if found_user:
        found_user.postal_code = postal_body['postalCode']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(postal_body['user_id'])}, 404

def changeDateOfBirth(birth_body):
    found_user = db.session.query(User).get(birth_body['user_id'])
    if found_user:
        found_user.date_of_birth = birth_body['birth']
        db.session.commit()
        return {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'name': new_user.name,
            'surname': new_user.surname,
            'gender': new_user.gender,
            'age': new_user.age,
            'phone': new_user.phone,
            'city': new_user.city,
            'country': new_user.country,
            'address': new_user.address,
            'postalCode': new_user.postal_code,
            'isAdmin': new_user.is_admin,
            'dateOfBirth': new_user.date_of_birth
        }
    else:
        return {'error': '{} not found'.format(birth_body['user_id'])}, 404

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
