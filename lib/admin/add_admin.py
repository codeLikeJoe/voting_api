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
        role = request.form.get('role').lower()
        email = request.form.get('email')
        password = request.form.get('key')

        if not email or not role or not password:
            return jsonify({'Error': 'all fields are required'})

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "User already exists"}), 400
        
        cursor.execute("SELECT * FROM roles WHERE title = %s", (role,))
        _role = cursor.fetchone()
        if _role is None:
            return jsonify({"Error": f"{role} is not a role"}), 400
        
        if len(password) < 6:
            return jsonify({"message": "Password must be at least 6 characters long."}), 400
        
        # otp = randint(100000, 999999)
        # Hash the OTP
        # hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # msg = Message(subject="Verify Your Account on SmartVote", sender="ajnetworks54779@gmail.com", recipients=[email])
        # msg.body = f"""Hi,\nKindly verify your SmartVote account with the code below. Note that this code expires after 24 hours.\n\nCode\t{str(otp)}"""
        # mail.send(msg)

        current_time = datetime.now()
        cursor.execute("INSERT INTO users (email, password, date_created, role) VALUES (%s, %s, %s, %s)",
                       (email, hashed_password, current_time, role))
        mysql.connection.commit()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        new_user = cursor.fetchone()
        user_id = new_user[0]

        cursor.execute("INSERT INTO srtauthwqs (user_id, verified, new_admin) VALUES (%s, %s, %s)",
                       (user_id, 'Yes', 'Yes'))
        mysql.connection.commit()
        
        return jsonify({
            "message": f"New Administrator has been added successfully",
        }), 201
    
    except Exception as e:
        return jsonify({"Error": f"An error occurred during registration. {str(e)}"}), 500
