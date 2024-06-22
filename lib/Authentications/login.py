from flask import Blueprint, request, jsonify,current_app
from datetime import datetime, timedelta
import jwt

signInUser = Blueprint("sign_In_User", __name__)

@signInUser.route('/login', methods=['POST'])
def login():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        student_id = request.form.get('student_id')
        password = request.form.get('password')
        email = request.form.get('email')

        if not (password and email) and not (password and student_id):
            return jsonify({"Error": "Please provide your credentials."}), 400

        cursor = mysql.connection.cursor()

        if email:
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        elif student_id:
            cursor.execute("SELECT * FROM users WHERE student_id=%s", (student_id,))

        user = cursor.fetchone()
        if not user:
            return jsonify({"Error": "Invalid user"}), 400
        
        student_id = user[3]
        email = user[4]
        database_password = user[6]
        role = user[8]
        
        cursor.execute("SELECT * FROM srtauthwqs WHERE email=%s", (email,))
        auth = cursor.fetchone()
        verified = auth[4]
        new_admin = auth[5]

        if verified == 'Yes':

            if database_password is None:
                return jsonify({"Error":"no password"}), 400
            
            # return jsonify({"message":"logged in"}), 200
                            
            if bcrypt.check_password_hash(database_password, password):

                if new_admin == 'Yes':
                    cursor.execute('UPDATE srtauthwqs SET can_set_password = %s WHERE email = %s', 
                                ('Yes', email))
                    mysql.connection.commit()
                    return jsonify({'message': 'new admin'})

                cursor.execute('UPDATE srtauthwqs SET can_set_password = %s WHERE email = %s', 
                                (None, email))
                mysql.connection.commit()

                current_time = datetime.now()
                expiry = current_time + timedelta(hours=2)
                expire_ms = expiry.timestamp() * 1000

                token = jwt.encode({
                    'first_name': user[1],
                    'last_name': user[2],
                    'student_id': user[3],
                    'email': user[4],
                    'program': user[5],
                    'expiry': str(expire_ms),
                }, current_app.config['SECRET_KEY'], algorithm="HS256")
                
                return jsonify({
                    'token': token,
                    'message': 'login successful',
                    'role': role 
                    }), 200
            else:
                return jsonify({'Error':'Invalid credentials'}), 401
        else:
            return jsonify({"Error": "user not verified"}), 401
        
    except Exception as e:
        print('Error: ', e)
        return jsonify({"Error":f'An error occurred while trying to login. {str(e)}'}), 500
