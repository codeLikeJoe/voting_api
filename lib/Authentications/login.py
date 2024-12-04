from flask import Blueprint, request, jsonify,current_app
from datetime import datetime, timedelta
import jwt

signInUser = Blueprint("sign_In_User", __name__)

@signInUser.route('/api/v1/login', methods=['POST'])
def login():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        raw_data = request.get_json()
        
        if not raw_data:
            return jsonify({"Error": "No data provided"}), 400

        # retrieving data from input fields
        student_id = raw_data.get("student_id")
        password = raw_data.get("password")
        email = raw_data.get("email")

        # showing error for empty inputs
        if not (password and email) and not (password and student_id):
            return jsonify({"Error": "Please provide your credentials."}), 403

        cursor = mysql.connection.cursor() # register database connection

        if email:
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,)) # lookup email address
        elif student_id:
            cursor.execute("SELECT * FROM users WHERE student_id=%s", (student_id,)) # lookup student id's

        user = cursor.fetchone() # fetching user data from database

        # showing error for non-users
        if not user:
            return jsonify({"Error": f"Invalid user {student_id}"}), 404

        user_id = user[0]
        first_name = user[1]
        last_name = user[2]
        _student_id = user[3]
        _email = user[4]
        program_id = user[5]
        p_title = user[6]
        database_password = user[7]
        created_at = user[8]
        role_id = user[9]
        year_of_admission = user[10]
        year_of_completion = user[11]

        cursor.execute("SELECT * FROM roles WHERE id = %s", (role_id,)) # look through roles
        role = cursor.fetchone() # fetching roles from database
        role_title = role[1]

        cursor.execute("SELECT * FROM srtauthwqs WHERE user_id=%s", (user_id,)) # user authentication lookup
        auth = cursor.fetchone()
        verified = auth[4]
        set_password = auth[5]

        if bcrypt.check_password_hash(database_password, password): # authenticat password
            current_time = datetime.now()
            expiry = current_time + timedelta(hours=2)
            # expiry = current_time + timedelta(minutes = 1)
            expire_ms = expiry.timestamp() * 1000

            token = jwt.encode({
                'user_id': user_id,
                'expiry': str(expire_ms),
            }, current_app.config['SECRET_KEY'], algorithm="HS256")

            return jsonify({
                    'id': user_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'program_id': program_id,
                    'program_title':p_title,
                    'email': _email,
                    'student_id': _student_id,
                    'verified': verified,
                    'token': token,
                    'current_time': current_time,
                    'expiry': expiry,
                    'expiry_ms': expire_ms,
                    'created_at': created_at,
                    'set_password': set_password,
                    'message': 'successful',
                    'role_id': role_id, 
                    'role_title': role_title, 
                    'year_of_admission': year_of_admission,
                    'year_of_completion': year_of_completion,
                    }), 200
        else:
            return jsonify({'Error':'Invalid credentials'}), 400

    except Exception as e:
        return jsonify({"Error":f'An error occurred while trying to login. {str(e)}'}), 500

