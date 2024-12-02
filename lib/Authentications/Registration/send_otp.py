from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime, timedelta
from random import *
from flask_mail import Message

verify_user = Blueprint('verify_user_account', __name__)

@verify_user.route('/verify', methods=['POST'])
def verify():
    # mail = current_app.extensions['mail']
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    

    try:
        email = request.form.get('email')
        student_id = request.form.get('student_id')

        if email or student_id:
            pass
        else:
            return jsonify({'message': 'email or student id is required!'}), 400   
        
        cursor = mysql.connection.cursor() # establish connection

        if email:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        elif student_id:
            cursor.execute("SELECT * FROM users WHERE student_id = %s", (student_id,))

        user = cursor.fetchone() #fetch user data

        if not user:
            return jsonify({"message":"Invalid user"}), 404
        
        user_id = user[0]
        # has_password = user[6]
        email = user[4]
        
        # if has_password is not None:             
        #     return jsonify({'message': 'has password'})
        
        otp = randint(100000, 999999)
        hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')

        # msg = Message(subject="OTP", sender="ajnetworks54779@gmail.com", recipients= [email])
        # msg.body=str(otp)
        # mail.send(msg)

        current_time = datetime.now()
        expiry = current_time + timedelta(minutes=60)
        expire_ms = expiry.timestamp() * 1000

        # cursor.execute('SELECT * FROM srtauthwqs WHERE email = %s', (email,))
        # auth = cursor.fetchone()
        # verified = auth[4]
        
        cursor.execute("UPDATE srtauthwqs SET otp = %s, expiry = %s WHERE user_id = %s",
                                (hashed_otp, str(expire_ms), user_id))
        mysql.connection.commit()

        return jsonify({"message": "OTP sent successfully", "otp":otp}), 200
        
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 500
    
