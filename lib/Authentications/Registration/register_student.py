from flask import Blueprint, request, jsonify,current_app
from datetime import datetime, timedelta
from random import *
from flask_mail import Message


register_student = Blueprint('_register_student', __name__)


@register_student.route('/register_student', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    mail = current_app.extensions['mail']

    try:
        firstname = request.form['firstname'].capitalize()
        lastname = request.form['lastname'].capitalize()
        email = request.form['email'].lower()
        student_id = request.form['student_id'].upper()
        program_code = request.form['program code'].lower()

        cursor = mysql.connection.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT * FROM students WHERE student_id = %s OR email = %s", (student_id, email))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "ID or Email already exists"}), 400
        

        # Check if program exists
        cursor.execute("SELECT * FROM programs WHERE code = %s", (program_code,))
        _programCode = cursor.fetchone()
        if not _programCode:
            return jsonify({"message": "The program does not exist"}), 404
        

        program = _programCode[1]
        
        otp = randint(100000, 999999)
        # Hash the OTP
        hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')

        msg = Message(subject="Verify Your Account on SmartVote", sender="ajnetworks54779@gmail.com", recipients= [email])
        msg.body = f"""Hi {firstname},\nKindly verify your SmartVote account with the code below. Note that this code expires after 24 hours.\n\nCode\t{str(otp)}"""
        mail.send(msg)

        current_time = datetime.now()
        expiry = current_time + timedelta(minutes=5)
        # Convert expiry to milliseconds
        expire_ms = expiry.timestamp() * 1000


        # Insert new user
        cursor.execute("INSERT INTO students (id, firstname, lastname, student_id, email, program, password, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (None, firstname, lastname, student_id, email, program, "", current_time))
        mysql.connection.commit()


        # Insert otp data
        cursor.execute("INSERT INTO srtauthwq (id, student_id, email, otp, expiry, verified) VALUES (%s, %s, %s, %s, %s, %s)",
                    (None, student_id, email, hashed_otp, str(expire_ms), "No"))
        mysql.connection.commit()

        
        return jsonify({
            "message": f"Student with ID: {student_id}, has been added successfully",
            "otp": otp,
            }), 201
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": f"An error occurred during registration. {str(e)}"}), 500
    

