from flask import Blueprint, request, jsonify,current_app, session

reset_password = Blueprint('_reset_password', __name__)

@reset_password.route('/reset_password', methods=['POST'])
def index():
    try:
        new_password = request.form['password']
        confirm_password = request.form['confirm password']

        confirm_forgot_password = session.get('reset password')
        email = session.get('email')

        if confirm_forgot_password:
            if confirm_password == new_password:
                mysql = current_app.extensions['mysql']
                bcrypt = current_app.extensions['bcrypt']

                cursor = mysql.connection.cursor()

                if len(new_password) < 6:
                    return jsonify({"message": "Password must be at least 6 characters long."}), 400
                
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

                cursor.execute("UPDATE students SET password = %s WHERE email = %s",
                                    (hashed_password, email))
                mysql.connection.commit()

                return jsonify({"message": f"User ({email}) password updated successfully."}), 200
            else:
                return jsonify({"message": "password mismatch!"}), 400
        else:
            return jsonify({"message":"sorry, unable to reset password"}), 400
    except Exception as e:
        return jsonify({"message":f"{str(e)}"}), 400
    