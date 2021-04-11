import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# endpoints
# TODO
# private Email sendVerificationEmail(String username):
#   User user = findUserByUsername(username)
#   if user != null:
#     String subject = "Verification Code For Your Account"
#     String body = "Dear %user.name% %user.surname%,\n" +
#     "Your verificaiton code is: %user.verificationCode%"
#     return EmailSender.sendEmail(user.email, subject, body) // некаква фунцкија која веќе во некаков објект постои во зависност од технологијата
#   else:
#     throw UserNotFoundException
#
# Private String encrypt(String text):
#   return Encrypter.encrypt(text) // некаква фунцкија која веќе во некаков објект постои во зависност од технологијата
#
# Private String decrypt(String text):
#   return Encrypter.decrypt(text) // некаква фунцкија која веќе во некаков објект постои во зависност од технологијата

def registration(user_body):
    found_user = db.session.query(User).filter_by(username=user_body['username']).first()
    if not found_user:
        if(user_body['password'] == user_body['repeatedPassword'])
            # TODO: treba da se enkodira pasvordot
            new_user=User(username=user_body['username'],
            email=user_body['email'], name=user_body['name'],
            surname=user_body['surname'], password=user_body['password'])
            #TODO: treba da se povika sendVerificationEmail()
        else:
            return {'error': '{} passwords do not match'.format(user_body['username'])}, 400
    else:
        return {'error': '{} already exists'.format(user_body['username'])}, 409
    db.session.add(new_user)
    db.session.commit()
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
        'isAdmin': new_user.is_admin
    }

def getRole(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return {'isAdmin': found_user.is_admin}
    else:
        return {'error': '{} not found'.format(user_id)}, 404

def getUserDetails(user_id):
    found_user = findUserById(id)
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
            'isAdmin': new_user.is_admin
        }
    else:
        return {'error': '{} not found'.format(user_id)}, 404

def getUserImages(user_id):
    found_user = db.session.query(User).get(user_id)
    if found_user:
        return {'images': found_user.images}
    else:
        return {'error': '{} not found'.format(user_id)}, 404

def addImageToUser(image_body):
    image = Image(link=image_body['imageLink'], isProfile=image_body['isProfile'])
    db.session.add(image)
    db.session.commit()
    found_user = db.session.query(User).get(user_id))
    if found_user:
        found_user.images.add(image.id)
        #TODO: treba da se napraj promena ako ima nova profilna
        return {'images': found_user.images}
    else:
        return {'error': '{} not found'.format(user_id)}, 404

def changePassword(password_body):
    found_user = db.session.query(User).get(password_body['user_id']))
    if found_user != null:
        #TODO: treba da se napraj da proverva so enkripter
        if password_body['oldPassword'] == found_user.password:
            #TODO: da se enkriptira
            found_user.password = password_body['newPassword']
            db.session.commit()
        else:
            return {'error': '{} passwords do not match'.format(user_body['username'])}, 400
    else:
        return {'error': '{} not found'.format(password_body['user_id'])}, 404

def changeGender(gender_body):
    found_user = db.session.query(User).get(gender_body['user_id']))
    if found_user != null:
        found_user.gender = gender_body['gender']
        db.session.commit()
    else:
        return {'error': '{} not found'.format(gender_body['user_id'])}, 404

def changeAge(age_body):
    found_user = db.session.query(User).get(age_body['user_id']))
    if found_user != null:
        found_user.age = age_body['age']
        db.session.commit()
    else:
        return {'error': '{} not found'.format(age_body['user_id'])}, 404

def changePhone(phone_body):
    found_user = db.session.query(User).get(phone_body['user_id']))
    if found_user != null:
        found_user.phone = phone_body['gender']
        db.session.commit()
    else:
        return {'error': '{} not found'.format(phone_body['user_id'])}, 404

def changeCity(city_body):
    found_user = db.session.query(User).get(city_body['user_id']))
    if found_user != null:
        found_user.city = city_body['gender']
        db.session.commit()
    else:
        return {'error': '{} not found'.format(city_body['user_id'])}, 404

def changeCountry(country_body):
    found_user = db.session.query(User).get(country_body['user_id']))
    if found_user != null:
        found_user.country = country_body['gender']
        db.session.commit()
    else:
        return {'error': '{} not found'.format(country_body['user_id'])}, 404

def changeAddress(address_body):
    found_user = db.session.query(User).get(address_body['user_id']))
    if found_user != null:
        found_user.address = address_body['gender']
        db.session.commit()
    else:
        return {'error': '{} not found'.format(address_body['user_id'])}, 404

def changePostalCode(postal_body):
    found_user = db.session.query(User).get(postal_body['user_id']))
    if found_user != null:
        found_user.postal_code = postal_body['gender']
        db.session.commit()
    else:
        return {'error': '{} not found'.format(postal_body['user_id'])}, 404

connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

# dummy reference for migrations only
from models import User, Image

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
