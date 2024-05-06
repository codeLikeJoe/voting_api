from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from authentications.register import register
from manageUsers.getAllUsers import getUsers
from manageUsers.getUserByIds import getUserId
from manageUsers.getUserByEmails import getUserEmail
import os

app = Flask(__name__)

load_dotenv()
secretKey = os.getenv("API_SECRET")

# Configure your application
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

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'message': 'Method not allowed'}), 405


@app.errorhandler(404)
def method_not_allowed(error):
    return jsonify({'message': 'This endpoint does not exist', 'error': f'{str(error)}'}), 404


if __name__ == '__main__':
    app.run(debug=True)
