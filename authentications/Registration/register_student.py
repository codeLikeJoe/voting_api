from flask import Blueprint, request, jsonify,current_app
from datetime import datetime, timedelta
from random import *
from flask_mail import Message

# Create a Blueprint named 'register' for handling user registration routes
register_student = Blueprint('_register_student', __name__)


@register_student.route('/register_student', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    mail = current_app.extensions['mail']

    try:
        firstname = request.form['firstname'].capitalize()
        lastname = request.form['lastname'].capitalize()
        email = request.form['email']
        student_id = request.form['student_id'].capitalize()

        cursor = mysql.connection.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT * FROM students WHERE student_id = %s OR email = %s", (student_id, email))
        user = cursor.fetchone()
        
        if user:
            return jsonify({"message": "ID or Email already exists"}), 400
        
        
        otp = randint(100000, 999999)

        # Hash the OTP
        hashed_otp = bcrypt.generate_password_hash(str(otp)).decode('utf-8')

        msg = Message(subject="Verify Your Account on SmartVote", sender="ajnetworks54779@gmail.com", recipients= [email])
        msg.body = f"""Hi {firstname},\nKindly verify your SmartVote account with the code below. Note that this code expires after 24 hours.\n\nCode\t{str(otp)}"""
        mail.send(msg)

        current_time = datetime.now()
        expiry = current_time + timedelta(minutes=1)

        # Convert expiry to milliseconds
        expire_ms = expiry.timestamp() * 1000

        # Insert new user
        cursor.execute("INSERT INTO students (id, firstname, lastname, email, student_id, otp, otp_expiry, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (None, firstname, lastname, email, student_id, hashed_otp, str(expire_ms), current_time))
        mysql.connection.commit()

        return jsonify({
            "message": f"Student with ID: {student_id}, has been added successfully",
            "otp": otp,
            }), 201
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": f"An error occurred during registration. {str(e)}"}), 500
    

