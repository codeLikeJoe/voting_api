from flask import Blueprint, request, jsonify,current_app
from datetime import datetime, timedelta
import jwt

signInUser = Blueprint("sign_In_User", __name__)

@signInUser.route('/login', methods=['POST'])
def login():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        # retrieving data from input fields
        student_id = request.form.get('student_id')
        password = request.form.get('password')
        email = request.form.get('email')

        # showing error for empty inputs
        if not (password and email) and not (password and student_id):
            return jsonify({"Error": "Please provide your credentials."}), 400

        cursor = mysql.connection.cursor() # register database connection

        if email:
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,)) # lookup email address
        elif student_id:
            cursor.execute("SELECT * FROM users WHERE student_id=%s", (student_id,)) # lookup student id's

        user = cursor.fetchone() # fetching user data from database
        user_id = user[0]
        first_name = user[1]
        last_name = user[2]
        student_id = user[3]
        email = user[4]
        program_id = user[5]
        database_password = user[6]
        role_id = user[8]
        year_of_admission = user[9]
        year_of_completion = user[10]

        # showing error for non-users
        if user is None:
            return jsonify({"Error": "Invalid user"}), 404
        
        cursor.execute("SELECT * FROM roles WHERE id = %s", (role_id,)) # look through roles
        role = cursor.fetchone() # fetching roles from database
        role_title = role[1]

        cursor.execute("SELECT * FROM program WHERE program_id = %s", (program_id,)) # look through programs
        program = cursor.fetchone() # fetching programs from database
        program_title = program[1]
        
        cursor.execute("SELECT * FROM srtauthwqs WHERE user_id=%s", (user_id,)) # user authentication lookup
        auth = cursor.fetchone()
        verified = auth[4]
        new_admin = auth[5]

        if verified == 'Yes':

            if database_password is None:
                return jsonify({"Error":"no password"}), 401
                            
            if bcrypt.check_password_hash(database_password, password):

                if new_admin == 'Yes':
                    cursor.execute('UPDATE srtauthwqs SET can_set_password = %s WHERE user_id = %s', 
                                ('Yes', user_id))
                    mysql.connection.commit()
                    # return jsonify({'message': 'new admin'})

                cursor.execute('UPDATE srtauthwqs SET can_set_password = %s WHERE user_id = %s', 
                                (None, user_id))
                mysql.connection.commit()

                current_time = datetime.now()
                expiry = current_time + timedelta(hours=2)
                expire_ms = expiry.timestamp() * 1000

                token = jwt.encode({
                    'user_id': user[0],
                    'expiry': str(expire_ms),
                }, current_app.config['SECRET_KEY'], algorithm="HS256")
                
                return jsonify({
                    'user_id': user_id,
                    'first_name': first_name if first_name else 'N/A',
                    'last_name': last_name if last_name else 'N/A',
                    'program_id': program_id if program_id else 'N/A',
                    'program_title':program_title if program_title else 'N/A',
                    'email': email,
                    'student_id': student_id if student_id else 'N/A',
                    'verified': verified if verified else 'No',
                    'token': token,
                    'message': 'login successful',
                    'role_id': role_id if role_id else 'N/A', 
                    'role_title': role_title if role_title else 'N/A', 
                    'year_of_admission': year_of_admission,
                    'year_of_completion': year_of_completion,
                    }), 200
            else:
                return jsonify({'Error':'Invalid credentials'}), 400
        else:
            return jsonify({"Error": "user not verified"}), 401
        
    except Exception as e:
        print('Error: ', e)
        return jsonify({"Error":f'An error occurred while trying to login. {str(e)}'}), 500
