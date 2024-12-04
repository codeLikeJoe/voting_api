from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime
# from random import *
# from flask_mail import Message

verify_otp = Blueprint('_verify_otp', __name__)

@verify_otp.route('/api/v1/verify-otp', methods=['POST'])
def index():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        raw_data = request.get_json()

        if not raw_data:
            return jsonify({"Error": "No data provided"}), 400

        email = raw_data.get('email')
        received_otp = raw_data.get('otp')
        student_id = raw_data.get('student_id')

        if email or student_id:
            pass
        else:
            return jsonify({'message': 'email or student id is required!'}), 403

        if not received_otp:
            return jsonify({"message": "otp required"}), 403

        cursor = mysql.connection.cursor()


        cursor.execute("SELECT * FROM users WHERE email = %s OR student_id = %s", (email, student_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"message": "invalid user"}), 404
        
        user_id = user[0]
        cursor.execute("SELECT * FROM srtauthwqs WHERE user_id = %s", (user_id,))
        srtauthwq = cursor.fetchone()

        hashed_otp_from_db = srtauthwq[2]
        otp_expiry = srtauthwq[3]

        current_time = datetime.now().timestamp() * 1000

        # Checking if the OTP has expired
        if current_time > float(otp_expiry):
            return jsonify({"message": "otp has expired"}), 403
        

        # Comparing hashes
        if bcrypt.check_password_hash(hashed_otp_from_db, received_otp):
            cursor.execute("UPDATE srtauthwqs SET verified = %s WHERE user_id = %s",
                                    ("Yes", user_id))
            mysql.connection.commit()

            return jsonify({"message": "verified successfully"}), 200
        else:
            return jsonify({"message": "invalid otp"}), 403

    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500
