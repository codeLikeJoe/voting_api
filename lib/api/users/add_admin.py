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
        role_id = request.form.get('role_id').lower()
        email = request.form.get('email')
        password = request.form.get('key')

        if not email or not role_id or not password:
            return jsonify({'Error': 'all fields are required'})
        
        if role_id == '1':
            return jsonify({'error': 'this role can not be assigned to an administrator'}), 400

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "User already exists"}), 400
        
        cursor.execute("SELECT * FROM roles WHERE id = %s", (role_id,))
        _role = cursor.fetchone()
        if _role is None:
            return jsonify({"Error": "this role does not exist"}), 400
        
        cursor.execute('select * from users where role_id = %s', (role_id,))
        if cursor.rowcount > 0:
            return jsonify({'error': 'sorry, the accepted number of persons for this role is up'}), 400
        
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
        cursor.execute("INSERT INTO users (email, password, date_created, role_id) VALUES (%s, %s, %s, %s)",
                       (email, hashed_password, current_time, role_id))
        mysql.connection.commit()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        new_user = cursor.fetchone()
        user_id = new_user[0]

        cursor.execute("INSERT INTO srtauthwqs (user_id, verified, new_admin) VALUES (%s, %s, %s)",
                       (user_id, 'Yes', 'Yes'))
        mysql.connection.commit()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        get_user = cursor.fetchone()
        
        cursor.execute("SELECT * FROM roles WHERE id = %s", (role_id,))
        get_role = cursor.fetchone()

        response_data = {
            'user_id':get_user[0],
            'email':get_user[4],
            'role':get_role[1],
        }
        
        return jsonify({
            "message": "successful",
            'response_data': response_data
        }), 201
    
    except Exception as e:
        return jsonify({"Error": f"An error occurred during registration. {str(e)}"}), 500
