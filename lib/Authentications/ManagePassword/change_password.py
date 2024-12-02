from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime, timedelta
from lib.authentications.token_requirement import TokenRequirement
import jwt

change_password = Blueprint('_change_password', __name__)
token_requirement = TokenRequirement(change_password)

@change_password.route('/change_password', methods=['POST'])
@token_requirement.token_required
def index():
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    
    try:
        token = request.args.get('token')

        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        expiry = data.get('expiry')
        user_id = data.get('user_id')

        current_time = datetime.now().timestamp() * 1000
        
        if current_time > float(expiry):
            return jsonify({"message": "token has expired"}), 403

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()

        database_password = user[6]

        # checking if old password matches
        if not bcrypt.check_password_hash(database_password, old_password):
            return jsonify({'message': 'Invalid old password'}), 400
        
        if new_password != confirm_password:
            return jsonify({'message': 'Password mismatch'}), 400
        
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        cursor.execute("UPDATE users SET password = %s WHERE id = %s",
                                    (hashed_password, user_id))
        mysql.connection.commit()

        return jsonify({'message': 'Password changed successfully'}), 200

    except Exception as e:
        return jsonify({"Error": f"Error {str(e)}"}), 400