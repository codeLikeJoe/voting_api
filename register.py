from flask import Blueprint, request, jsonify,current_app
from datetime import datetime
import jwt

register = Blueprint('register',__name__)


@register.route('/register', methods=['POST'])
def registerNow():
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    try:
        _firstname = request.form['firstname']
        _lastname = request.form['lastname']
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

        if len(password) < 6:
            return jsonify({"message": "Password must be at least 6 characters long."}), 400

        try:
            dob = datetime.strptime(_dob, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert new user
        cursor.execute("INSERT INTO users (firstname, lastname, email, dob, username, password, verified) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (_firstname, _lastname, _email, dob, _username, hashed_password, 'No'))
        mysql.connection.commit()

        return jsonify({"message": "User registered successfully"}), 201
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": f"An error occurred during registration. {str(e)}"}), 500
    

# if __name__ == '__main__':
#     register.run(debug=True)

