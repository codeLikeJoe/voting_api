# from dotenv import load_dotenv
from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail
# from random import *
from authentications.Registration.register import register
from manageUsers.getAllUsers import getUsers
from manageUsers.getUserByIds import getUserId
from manageUsers.getUserByEmails import getUserEmail
from authentications.verifyAccount import verify_user
from authentications.login import signInUser
from authentications.Registration.validate_otp import validate_otp
from authentications.ForgotPassword.forgot_password import forgot_password
from authentications.ForgotPassword.validate_forgot_password_otp import validate_reset_password_otp
from authentications.ForgotPassword.reset_password import reset_password
from home import home
# import os
from datetime import datetime, timedelta

app = Flask(__name__)

# load_dotenv()
# secretKey = os.getenv("API_SECRET")

# Mail Configration
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "ajnetworks54779@gmail.com"
app.config['MAIL_PASSWORD'] = "pvwn wvdw lvmk txbn"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Database Configuration
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "smartvote"
app.config['SECRET_KEY'] = 'secretKey007'


# Initialize MySQL and Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)
mail = Mail(app)


# Initialize the MySQL extension for the Flask application
app.extensions['mysql'] = mysql

# Initialize the bcrypt extension for password hashing in the Flask application
app.extensions['bcrypt'] = bcrypt

# Initialize the mail extension for the Flask application
app.extensions['mail'] = mail


# Register the blueprint
app.register_blueprint(register)
app.register_blueprint(getUsers)
app.register_blueprint(getUserId)
app.register_blueprint(getUserEmail)
app.register_blueprint(verify_user)
app.register_blueprint(signInUser)
app.register_blueprint(home)
app.register_blueprint(validate_otp)
app.register_blueprint(forgot_password)
app.register_blueprint(validate_reset_password_otp)
app.register_blueprint(reset_password)

# current_time = datetime.now()
# expire = current_time + timedelta(minutes=5)
# print(current_time)
# print(expire)

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'message': 'Method not allowed'}), 405


@app.errorhandler(404)
def method_not_allowed(error):
    return jsonify({'message': 'This endpoint does not exist', 'error': f'{str(error)}'}), 404


if __name__ == '__main__':
    app.run(debug=True)
