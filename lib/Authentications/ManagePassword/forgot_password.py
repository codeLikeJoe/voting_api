from flask import Blueprint, request, jsonify,current_app, session
from random import *
from flask_mail import Message
from datetime import datetime, timedelta

forgot_password = Blueprint('_forgot_password', __name__)

@forgot_password.route('/forgot_password', methods=['POST'])
def forgotpassword():

    mail = current_app.extensions['mail']
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    cursor = mysql.connection.cursor()

    try:
        email = request.form['email']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"message":"user not found"}), 404


        otp = randint(100000, 999999)
        # Hashing the OTP
        hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')

        current_time = datetime.now()
        expiry = current_time + timedelta(minutes=5)

        # Converting expiry to milliseconds
        expire_ms = expiry.timestamp() * 1000

        # student_id = user[3]

        cursor.execute("UPDATE srtauthwqs SET otp = %s, expiry = %s WHERE email = %s",
                            (hashed_otp, str(expire_ms), email))
        mysql.connection.commit()

        return jsonify({"message": "OTP sent successfully", "otp":otp}), 200
        
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 500
