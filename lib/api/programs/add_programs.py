from flask import Blueprint, request, jsonify,current_app
from datetime import datetime
import jwt
from lib.core.token_requirement import TokenRequirement


add_program = Blueprint('_add_program', __name__)
token_requirement = TokenRequirement(add_program)


@add_program.route('/api/v1/add-program', methods=['POST'])
@token_requirement.token_required
def index():
    try:
        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()

        raw_data = request.get_json()
            
        if not raw_data:
            return jsonify({"error": "No data provided"}), 400

        program_title = raw_data.get('program_title').lower()
        program_code = raw_data.get('program_code').lower()

        if not program_title or not program_code:
            return jsonify({"error": "Programs title or code is missing"}), 400
        
        token = request.args.get('token')

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        expiry = data.get('expiry')
        user_id = data.get('user_id')

        current_time = datetime.now().timestamp() * 1000
        
        if current_time > float(expiry):
            return jsonify({"message": "token has expired"}), 403
        
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        role_id = user[6]
        
        if role_id != 1:
            return jsonify({"message": "you are not authorized to create programs"}), 401
        
        cursor.execute("SELECT * FROM programs WHERE program_title = %s OR program_code = %s", 
                       (program_title, program_code))
        program = cursor.fetchone()

        if program:
            return jsonify({"message":"program title or code already exists"}), 400
        
        cursor.execute("INSERT INTO programs (program_title, program_code) VALUES (%s, %s)",
                    (program_title, program_code))
        mysql.connection.commit()

        cursor.execute("SELECT * FROM programs WHERE program_title = %s OR program_code = %s", 
                       (program_title, program_code))
        _program = cursor.fetchone()

        return jsonify({
            'id': _program[0],
            'program_title': _program[1],
            'program_code': _program[2],
            'message': 'successful',
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500