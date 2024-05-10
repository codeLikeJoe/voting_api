from flask import Blueprint, request, jsonify,current_app
import jwt

signInUser = Blueprint("sign_In_User", __name__)

@signInUser.route('/login', methods=['POST'])
def login():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        _username = request.form['username']
        _password = request.form['password']

        if not _username or not _password:
            return jsonify({"message": "Please provide username and password."})

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (_username,))
        user = cursor.fetchone()

        if user:
            if user[8] == 'Yes':
                
                if bcrypt.check_password_hash(user[7], _password):
                    token = jwt.encode({
                        'username': request.form['username'],
                        'email': user[3],
                        'firstname': user[1],
                        'lastname': user[2],
                        'date of birth': user[4].strftime('%Y-%m-%d'),
                        'age': user[5],
                    }, current_app.config['SECRET_KEY'], algorithm="HS256")

                    user_info = {
                        'id': user[0],
                        'firstname': user[1],
                        'lastname': user[2],
                        'email': user[3],
                        'date of birth': user[4],
                        'age': user[5],
                        'username': user[6],
                    }
                    return jsonify({
                        'token': token,
                        'message': 'successful', 
                        "user info": user_info
                        }), 200
                else:
                    return jsonify({'message':'Invalid username or password'}), 401
            else:
                return jsonify({"message": "Please verify your email address"}), 401
        else:
            return jsonify({"message": "Invalid username or password"}), 400
        
    except Exception as e:
        print('Error: ', e)
        return jsonify({"message":f'An error occurred while trying to login. {str(e)}'}), 500
