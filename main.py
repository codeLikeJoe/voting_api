from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from random import *
from authentications.register import register
from manageUsers.getAllUsers import getUsers
from manageUsers.getUserByIds import getUserId
from manageUsers.getUserByEmails import getUserEmail
import os

app = Flask(__name__)
# mail = Mail(app)

load_dotenv()
secretKey = os.getenv("API_SECRET")

# Mail Configration
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "ajnetworks54779@gmail.com"
app.config['MAIL_PASSWORD'] = "pvwn wvdw lvmk txbn"
# app.config['MAIL_PASSWORD'] = "*******"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
otp = randint(000000, 999999)

# Database Configuration
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "smartvote"
app.config['SECRET_KEY'] = secretKey


# Initialize MySQL and Bcrypt
mysql = MySQL(app)
bcrypt = Bcrypt(app)


# Initialize the MySQL extension for the Flask application
app.extensions['mysql'] = mysql

# Initialize the bcrypt extension for password hashing in the Flask application
app.extensions['bcrypt'] = bcrypt


# Register the blueprint
app.register_blueprint(register)
app.register_blueprint(getUsers)
app.register_blueprint(getUserId)
app.register_blueprint(getUserEmail)

# print(secretKey)

@app.route('/verify', methods=['POST'])
def verify():
    try:
        email = request.form['email']
        msg = Message(subject="OTP", sender="ajnetworks54779@gmail.com", recipients= [email])
        msg.body=str(otp)
        mail.send(msg)
        return jsonify({"message": "OTP sent successfully"})
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"})
    

@app.route('/validate', methods=['POST'])
def validate():
    try:
        user_otp = request.form['otp']
        if otp == int(user_otp):
            me =otp
        return jsonify({"message": "OTP sent successfully"})
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"})

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'message': 'Method not allowed'}), 405


@app.errorhandler(404)
def method_not_allowed(error):
    return jsonify({'message': 'This endpoint does not exist', 'error': f'{str(error)}'}), 404


if __name__ == '__main__':
    app.run(debug=True)
