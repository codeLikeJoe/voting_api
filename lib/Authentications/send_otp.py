from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime, timedelta
from random import *
from flask_mail import Message

verify_user = Blueprint('verify_user_account', __name__)

@verify_user.route('/api/v1/send-otp', methods=['POST'])
def verify(): 
    try:
        # mail = current_app.extensions['mail']
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        raw_data = request.get_json()

        if not raw_data:
            return jsonify({"Error": "No data provided"}), 400

        email = raw_data.get('email')
        student_id = raw_data.get('student_id')

        if email or student_id:
            pass
        else:
            return jsonify({'message': 'email or student id is required!'}), 403   
        
        cursor = mysql.connection.cursor() # establish connection

        if email:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        elif student_id:
            cursor.execute("SELECT * FROM users WHERE student_id = %s", (student_id,))

        user = cursor.fetchone() #fetch user data

        if not user:
            return jsonify({"message":"invalid user"}), 404
        
        user_id = user[0]
        # has_password = user[6]
        email = user[4]
        
        otp = randint(100000, 999999)
        hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')

        # msg = Message(subject="OTP", sender="ajnetworks54779@gmail.com", recipients= [email])
        # msg.body=str(otp)
        # mail.send(msg)

        current_time = datetime.now()
        expiry = current_time + timedelta(minutes=60)
        expire_ms = expiry.timestamp() * 1000
        
        cursor.execute("UPDATE srtauthwqs SET otp = %s, expiry = %s WHERE user_id = %s",
                                (hashed_otp, str(expire_ms), user_id))
        mysql.connection.commit()

        return jsonify({"message": "otp sent successfully", "otp":otp}), 200
        
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 500
    
