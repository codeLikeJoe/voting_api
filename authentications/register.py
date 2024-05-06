from flask import Blueprint, request, jsonify,current_app
from datetime import datetime

# Create a Blueprint named 'register' for handling user registration routes
register = Blueprint('register', __name__)


@register.route('/register', methods=['POST'])
def registerNow():
    # Retrieve the bcrypt library and MySQL database connection from the Flask application's extensions
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']

    try:
        _firstname = request.form['firstname'].capitalize()
        _lastname = request.form['lastname'].capitalize()
        _email = request.form['email']
        _dob = request.form['dob']
        _username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (_username, _email))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Username or Email already exists"}), 400
        
        # Check if password is strong enough
        if len(password) < 6:
            return jsonify({"message": "Password must be at least 6 characters long."}), 400
        
        # Attempt to parse the date of birth (_dob) from a string to a datetime object.
        # If the format is incorrect (not YYYY-MM-DD), catch the ValueError and return a 400 error with a message indicating the correct format.
        try:
            dob = datetime.strptime(_dob, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400


        # Generate a hashed version of the password using bcrypt for secure storage.
        # The hashed password is then decoded from bytes to a string.
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Record the current date and time as the date the user account was created.
        today = datetime.now()

        # calculate the age of the user
        age = today.year - dob.year # Calculate the difference in years

        # Check if the birthday has occurred this year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1 # Subtract one year if the birthday hasn't occurred yet



        # Insert new user
        cursor.execute("INSERT INTO users (id, firstname, lastname, email, dob, age, username, password, verified, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (None, _firstname, _lastname, _email, dob, age, _username, hashed_password, 'No', today))
        mysql.connection.commit()

        return jsonify({"message": f"User with email: {_email}, has been registered successfully"}), 201
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": f"An error occurred during registration. {str(e)}"}), 500
    

