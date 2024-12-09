from flask import Blueprint, request, jsonify,current_app, session

reset_password = Blueprint('_reset_password', __name__)

@reset_password.route('/api/v1/reset-password', methods=['POST'])
def index():
    try:
        mysql = current_app.extensions['mysql']
        bcrypt = current_app.extensions['bcrypt']

        raw_data = request.get_json()

        if not raw_data:
            return jsonify({"Error": "No data provided"}), 400
        
        email = raw_data.get('email')
        student_id = raw_data.get('student_id')
        new_password = raw_data.get('new_password')
        confirm_password = raw_data.get('confirm_password')

        if not (email or student_id) or not (new_password and confirm_password):
            return jsonify({'message': 'all fields are required'}), 403

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM users WHERE email = %s OR student_id = %s', (email, student_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'message':'Inavalid user'}), 404

        if confirm_password != new_password:
            return jsonify({"Error": "password mismatch!"}), 400

        if len(new_password) < 6:
            return jsonify({"message": "password must be at least 6 characters long."}), 403
       
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        cursor.execute("UPDATE users SET password = %s WHERE email = %s OR student_id = %s",
                            (hashed_password, email, student_id))
        mysql.connection.commit()

        cursor.execute('UPDATE authcheck SET set_password = %s WHERE user_id = %s', 
                        (False, user[0]))
        mysql.connection.commit()

        return jsonify({"message": f"password updated successfully."}), 200
        
    except Exception as e:
        return jsonify({"Error":f"{str(e)}"}), 400
    