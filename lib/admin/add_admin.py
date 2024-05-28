from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from random import *
from flask_mail import Message

add_admin = Blueprint('_admin_admin', __name__)

@add_admin.route('/add_admin', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    mail = current_app.extensions['mail']

    try:
        firstname = request.form['firstname'].capitalize()
        lastname = request.form['lastname'].capitalize()
        email = request.form['email'].lower()
        password = request.form['key']

        cursor = mysql.connection.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Email already exists"}), 400
        
        otp = randint(100000, 999999)
        # Hash the OTP
        hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        msg = Message(subject="Verify Your Account on SmartVote", sender="ajnetworks54779@gmail.com", recipients=[email])
        msg.body = f"""Hi {firstname},\nKindly verify your SmartVote account with the code below. Note that this code expires after 24 hours.\n\nCode\t{str(otp)}"""
        mail.send(msg)

        current_time = datetime.now()
        expiry = current_time + timedelta(minutes=5)
        # Convert expiry to milliseconds
        expire_ms = str(expiry.timestamp() * 1000)

        # Insert new user
        cursor.execute("INSERT INTO admins (id, firstname, lastname, email, password, maskot, exp, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (None, firstname, lastname, email, hashed_password, hashed_otp, expire_ms, current_time))
        mysql.connection.commit()
        
        return jsonify({
            "message": f"New Admin has been added successfully",
            "otp": otp,
        }), 201
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": f"An error occurred during registration. {str(e)}"}), 500
