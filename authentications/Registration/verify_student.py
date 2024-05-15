from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime, timedelta
# from random import *
# from flask_mail import Message

verify_student = Blueprint('_verify_student', __name__)

@verify_student.route('/verify_student', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']

    try:
        email = request.form['email']
        received_otp = request.form['otp']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM students WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"message": "user not found"}), 404

        hashed_otp_from_db = user[5]
        otp_expiry = user[6]

        # Check if the OTP has expired
        current_time = datetime.now().timestamp() * 1000
        if current_time > float(otp_expiry):
            return jsonify({"message": "OTP has expired"}), 400
        

        # Compare hashes
        if bcrypt.check_password_hash(hashed_otp_from_db, received_otp):
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "Invalid OTP"}), 401

    except Exception as e:
        return jsonify({"error": f"{str(e)}"})
