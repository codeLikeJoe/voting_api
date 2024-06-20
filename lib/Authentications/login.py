from flask import Blueprint, request, jsonify,current_app
import jwt

signInUser = Blueprint("sign_In_User", __name__)

@signInUser.route('/login', methods=['POST'])
def login():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        student_id = request.form['student_id']
        password = request.form['password']

        if not student_id or not password:
            return jsonify({"message": "Please provide id and password."})

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM srtauthwqs WHERE student_id=%s", (student_id,))
        auth = cursor.fetchone()

        if auth:
            if auth[4] == 'Yes':
                cursor.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
                user = cursor.fetchone()

                if user[6] is None:
                    return jsonify({"message":"Please set a password"}), 400
                               
                if bcrypt.check_password_hash(user[6], password):

                    cursor.execute('UPDATE srtauthwqs SET reset_password = %s WHERE student_id = %s', 
                                   ('No', student_id))
                    mysql.connection.commit()

                    token = jwt.encode({
                        'first_name': user[1],
                        'last_name': user[2],
                        'student_id': user[3],
                        'email': user[4],
                        'program': user[5],
                    }, current_app.config['SECRET_KEY'], algorithm="HS256")

                    user_info = {
                        'id': user[0],
                        'first_name': user[1].capitalize(),
                        'last_name': user[2].capitalize(),
                        'student id': user[3].upper(),
                        'email': user[4],
                        'program': user[5].upper(),
                    }
                    
                    return jsonify({
                        'token': token,
                        'message': 'Welcome to SmartVote', 
                        "user_info": user_info
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
