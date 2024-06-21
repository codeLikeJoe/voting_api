from flask import Blueprint, request, jsonify,current_app, session

reset_password = Blueprint('_reset_password', __name__)

@reset_password.route('/reset_password', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']

    try:
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not email or not new_password or not confirm_password:
            return jsonify({'message': 'all fields are required'})

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM srtauthwqs WHERE email = %s', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message':'Inavalid user'}), 404
        
        new_admin = user[5]
        can_set_Password = user[6]
        if can_set_Password != 'Yes':
            return jsonify({"Error":"sorry, unable to reset password"}), 403

        if confirm_password != new_password:
            return jsonify({"Error": "password mismatch!"}), 400

        if len(new_password) < 6:
            return jsonify({"message": "Password must be at least 6 characters long."}), 400

        bcrypt = current_app.extensions['bcrypt']        
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        cursor.execute("UPDATE users SET password = %s WHERE email = %s",
                            (hashed_password, email))
        mysql.connection.commit()

        cursor.execute('UPDATE srtauthwqs SET can_set_password = %s WHERE email = %s', 
                        (None, email))
        mysql.connection.commit()

        if new_admin == 'Yes':
            cursor.execute('UPDATE srtauthwqs SET new_admin = %s WHERE email = %s', 
                        (None, email))
            mysql.connection.commit()

        return jsonify({"message": f"password updated successfully."}), 200
        
    except Exception as e:
        return jsonify({"Error":f"{str(e)}"}), 400
    