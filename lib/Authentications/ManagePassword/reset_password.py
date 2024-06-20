from flask import Blueprint, request, jsonify,current_app, session

reset_password = Blueprint('_reset_password', __name__)

@reset_password.route('/reset_password', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']

    try:
        email = request.form['email']
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']

        # confirm_forgot_password = session.get('reset password')
        # email = session.get('email')

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM students WHERE email = %s', (email,))
        user = cursor.fetchone()

        student_id = user[3]
        print(student_id)

        cursor.execute('SELECT * FROM srtauthwqs WHERE student_id = %s', (student_id,))
        student = cursor.fetchone()

        canResetPassword = student[5]
        print(canResetPassword)

        if canResetPassword == 'Yes':
            if confirm_password == new_password:
                bcrypt = current_app.extensions['bcrypt']


                if len(new_password) < 6:
                    return jsonify({"message": "Password must be at least 6 characters long."}), 400
                
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

                cursor.execute("UPDATE students SET password = %s WHERE email = %s",
                                    (hashed_password, email))
                mysql.connection.commit()

                cursor.execute('UPDATE srtauthwqs SET reset_password = %s WHERE student_id = %s', 
                               ('No', student_id))
                mysql.connection.commit()

                return jsonify({"message": f"User ({email}) password updated successfully."}), 200
            else:
                return jsonify({"message": "password mismatch!"}), 400
        else:
            return jsonify({"message":"sorry, unable to reset password"}), 400
    except Exception as e:
        return jsonify({"Error":f"{str(e)}"}), 400
    