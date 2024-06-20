from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime, timedelta
from random import *
from flask_mail import Message

verify_user = Blueprint('verify_user_account', __name__)

@verify_user.route('/verify', methods=['POST'])
def verify():
    mail = current_app.extensions['mail']
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    cursor = mysql.connection.cursor()

    try:
        otp = randint(100000, 999999)
        # Hash the OTP
        hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')

        email = request.form['email']

        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"message":"Sorry, user not found"}), 404

        # msg = Message(subject="OTP", sender="ajnetworks54779@gmail.com", recipients= [email])
        # msg.body=str(otp)
        # mail.send(msg)

        current_time = datetime.now()
        expiry = current_time + timedelta(minutes=5)
        # Convert expiry to milliseconds
        expire_ms = expiry.timestamp() * 1000

        student_id = user[3]

        cursor.execute("UPDATE srtauthwqs SET otp = %s, expiry = %s WHERE student_id = %s",
                                (hashed_otp, str(expire_ms), student_id))
        mysql.connection.commit()

        return jsonify({"message": "OTP sent successfully", "otp":otp}), 200
        
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 400
    
