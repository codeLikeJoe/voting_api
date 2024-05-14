from flask import Blueprint, request, jsonify,current_app, session
from random import *
from flask_mail import Message

forgot_password = Blueprint('_forgot_password', __name__)

@forgot_password.route('/forgot_password', methods=['POST'])
def forgotpassword():

    mail = current_app.extensions['mail']
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()

    try:
        otp = randint(100000, 999999)

        email = request.form['email']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            msg = Message(subject="OTP To Reset Password", sender="ajnetworks54779@gmail.com", recipients= [email])
            msg.body= f"""Hi {user[1]},\n\n You requested to reset your password.\nUse this code to verify your account in order to set a new password.\n\n\nCode\t {str(otp)}"""
            mail.send(msg)

            # current_time = datetime.now().replace(tzinfo=None)
            # expiry = current_time + timedelta(minutes=1)

            # session['otp_expiry'] = expiry
            session['forgot_password_otp'] = otp
            session['forgot_password_email'] = email

            return jsonify({"message": "OTP sent successfully", "otp":otp}), 200
        else:
            return jsonify({"message":"user not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 400
