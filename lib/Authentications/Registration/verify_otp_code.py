from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime
# from random import *
# from flask_mail import Message

verify_otp = Blueprint('_verify_otp', __name__)

@verify_otp.route('/verify_otp', methods=['POST'])
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
        
        student_id = user[3]
        
        cursor.execute("SELECT * FROM srtauthwqs WHERE student_id = %s", (student_id,))
        student = cursor.fetchone()

        hashed_otp_from_db = student[2]
        otp_expiry = student[3]

        current_time = datetime.now().timestamp() * 1000

        # Checking if the OTP has expired
        if current_time > float(otp_expiry):
            return jsonify({"message": "OTP has expired"}), 400
        

        # Comparing hashes
        if bcrypt.check_password_hash(hashed_otp_from_db, received_otp):
            cursor.execute("UPDATE srtauthwqs SET verified = %s, reset_password = %s WHERE student_id = %s",
                                    ("Yes", "Yes", student_id))
            mysql.connection.commit()

            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "Invalid OTP"}), 401

    except Exception as e:
        return jsonify({"error": f"{str(e)}"})
