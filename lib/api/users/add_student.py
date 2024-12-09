from flask import Blueprint, request, jsonify,current_app
from datetime import datetime, timedelta
from random import *
from flask_mail import Message
from lib.api.auth.password_generator import generate_password


register_student = Blueprint('_register_student', __name__)


@register_student.route('/api/v1/add-student', methods=['POST'])
def index():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']
        # mail = current_app.extensions['mail']

        raw_data = request.get_json()

        if not raw_data:
            return jsonify({"Error": "No data provided"}), 400
        
        firstname = raw_data.get('firstname').lower()
        lastname = raw_data.get('lastname').lower()
        email = raw_data.get('email')
        student_id = raw_data.get('student_id').lower()
        program_code = raw_data.get('program_code').lower()
        year_of_admission = raw_data.get('admission_date')
        year_of_completion = raw_data.get('completion_date')

        cursor = mysql.connection.cursor() # establish connection

        # fetch user data
        cursor.execute("SELECT * FROM users WHERE student_id = %s OR email = %s", (student_id, email))
        user = cursor.fetchone()

        if user:
            return jsonify({"message": "student id or email already exists"}), 302

        # fetch available programs
        cursor.execute("SELECT * FROM programs WHERE program_code = %s", (program_code,))
        _program = cursor.fetchone()

        if _program is None:
            return jsonify({"message": "The program does not exist"}), 404
        
        program_id = _program[0]
        p_title = _program[1]
        p_code = _program[2]
        
        # Generate random password
        password = generate_password()

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # otp = randint(100000, 999999)
        # hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')

        # msg = Message(subject="Verify Your Account on SmartVote", sender="ajnetworks54779@gmail.com", recipients= [email])
        # msg.body = f"""Hi {firstname},\nKindly verify your SmartVote account with the code below. Note that this code expires after 24 hours.\n\nCode\t{str(otp)}"""
        # mail.send(msg)

        current_time = datetime.now()

        cursor.execute("SELECT * FROM roles WHERE title = %s", ('student',))
        role = cursor.fetchone()
        role_id = role[0]
        role_title = role[1]

        cursor.execute("""INSERT INTO users (first_name, last_name, student_id, email, program_id, 
                       password, created_at, role_id, admission_date, completion_date) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (firstname, lastname, student_id, email, program_id, hashed_password, current_time, 
                     role_id, year_of_admission, year_of_completion))
        mysql.connection.commit()

        # fetch new user data
        cursor.execute("SELECT * FROM users WHERE student_id = %s OR email = %s", (student_id, email))
        new_user = cursor.fetchone()
        user_id = new_user[0] # get user id from database

        # create auth row with user_id
        cursor.execute("INSERT INTO authcheck (user_id, set_password) VALUES (%s, %s)",
                    (user_id, True,),)
        mysql.connection.commit()
        
        return jsonify({
            'user_id': user_id,
            'first_name': new_user[1],
            'last_name': new_user[2],
            'email': new_user[3],
            'student_id': new_user[4],
            'program_id': program_id,
            'program_title': p_title,
            'program_code': p_code,
            'role_id': role_id,
            'role_title': role_title,
            'password': password,
            'message': 'successful',
            'verified': new_user[8],
            'admission_date': new_user[9],
            'completion_date': new_user[10],
            'created_at': new_user[11]
        }), 201
    
    except Exception as e:
        return jsonify({"Error": f"An error occurred during registration. {str(e)}"}), 500
    
