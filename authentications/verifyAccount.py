from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime, timedelta
from random import *
from flask_mail import Message

verify_user = Blueprint('verify_user_account', __name__)

@verify_user.route('/verify', methods=['POST'])
def verify():
    mail = current_app.extensions['mail']
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()

    try:
        otp = randint(100000, 999999)

        email = request.form['email']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            msg = Message(subject="OTP", sender="ajnetworks54779@gmail.com", recipients= [email])
            msg.body=str(otp)
            mail.send(msg)

            # current_time = datetime.now().replace(tzinfo=None)
            # expiry = current_time + timedelta(minutes=1)

            # session['otp_expiry'] = expiry
            session['otp'] = otp
            session['email'] = email

            return jsonify({"message": "OTP sent successfully", "otp":otp})
        else:
            return jsonify({"message":"user not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 400
    

@verify_user.route('/validate', methods=['POST'])
def validate():

    try:
        user_otp = request.form['otp']

        stored_otp = session.get('otp')
        stored_email = session.get('email')
        # otp_expiry = session.get('otp_expiry')
        # current_time = datetime.now().replace(tzinfo=None)

        if stored_email:
            if stored_otp == int(user_otp):
                # if current_time < otp_expiry:
                    mysql = current_app.extensions['mysql']
                    cursor = mysql.connection.cursor()

                    # Update user details
                    cursor.execute("UPDATE users SET verified = %s WHERE email = %s",
                                ('Yes', stored_email))
                    mysql.connection.commit()

                    return jsonify({"message": "Verification successful"})
                # else:
                #     return jsonify({"message": "OTP has expired!"})
            return jsonify({"message": "Invalid OTP. Please try again."})
        else:
            return jsonify({"message": "Verification failed"})
    
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"})
