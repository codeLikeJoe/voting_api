from flask import Blueprint, request, jsonify,current_app
import jwt

signInUser = Blueprint("sign_In_User", __name__)

@signInUser.route('/login', methods=['POST'])
def login():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        student_id = request.form['student id']
        password = request.form['password']

        if not student_id or not password:
            return jsonify({"message": "Please provide id and password."})

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM srtauthwq WHERE student_id=%s", (student_id,))
        auth = cursor.fetchone()

        if auth:
            if auth[5] == 'Yes':
                cursor.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
                user = cursor.fetchone()

                if user[6] == "":
                    return jsonify({"message":"Please set a password"}), 400
                               
                if bcrypt.check_password_hash(user[6], password):
                    token = jwt.encode({
                        'firstname': user[1],
                        'lastname': user[2],
                        'student id': user[3],
                        'email': user[4],
                        'program': user[5],
                    }, current_app.config['SECRET_KEY'], algorithm="HS256")

                    user_info = {
                        'id': user[0],
                        'firstname': user[1],
                        'lastname': user[2],
                        'student id': user[3],
                        'email': user[4],
                        'program': user[5],
                    }
                    return jsonify({
                        'token': token,
                        'message': 'Welcome to SmartVote', 
                        "user info": user_info
                        }), 200
                else:
                    return jsonify({'message':'Invalid username or password'}), 401
            else:
                return jsonify({"message": "Please verify your email address"}), 401
        else:
            return jsonify({"message": "Invalid id or password"}), 400
        
    except Exception as e:
        print('Error: ', e)
        return jsonify({"message":f'An error occurred while trying to login. {str(e)}'}), 500
