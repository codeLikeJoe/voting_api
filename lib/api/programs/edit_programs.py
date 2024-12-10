from flask import Blueprint, request, jsonify,current_app
import jwt
from datetime import datetime
from lib.core.token_requirement import TokenRequirement


program = Blueprint('_program', __name__)
token_requirement = TokenRequirement(program)


@program.route('/api/v1/program/<int:id>', methods=['PUT', 'GET', 'DELETE'])
@token_requirement.token_required
def index(id):
    try:
        mysql = current_app.extensions['mysql']
        token = request.args.get('token')
        cursor = mysql.connection.cursor()

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        expiry = data.get('expiry')
        user_id = data.get('user_id')

        current_time = datetime.now().timestamp() * 1000
        
        if current_time > float(expiry):
            return jsonify({"message": "token has expired"}), 403

        cursor.execute("SELECT * FROM programs WHERE id = %s", (id,))
        program = cursor.fetchone()

        if not program:
            return jsonify({"message": "program not found"}), 404

        if request.method == 'GET':
            try:
                return jsonify({
                    'program_id': program[0],
                    'program_title': program[1],
                    'program_code': program[2],
                }), 200
            except Exception as e:
                return jsonify({"error": f"cannot fetch data because {str(e)}"}), 500
            
            
        if request.method == 'PUT':
            try:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                role_id = user[6]
                
                if role_id != 1:
                    return jsonify({"message": "you are not authorized to edit programs"}), 401
                
                raw_data = request.get_json()
                
                if not raw_data:
                    return jsonify({"error": "No data provided"}), 400

                program_title = raw_data.get('program_title').lower()
                program_code = raw_data.get('program_code').lower()

                if not program_title or not program_code:
                    return jsonify({"error": "Program title or code is missing"}), 400
                
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()

                if not user[8]:
                    return jsonify({"message": "user not verified"}), 401
                
                cursor.execute("UPDATE programs SET program_title = %s, program_code = %s WHERE id = %s",
                                        (program_title, program_code, id))
                mysql.connection.commit()

                cursor.execute("SELECT * FROM programs WHERE id = %s", (id,))
                get_program = cursor.fetchone()

                cursor.close()
                return jsonify({
                    'program_id': get_program[0],
                    'program_title': get_program[1],
                    'program_code': get_program[2],
                    'message': "successful",
                }), 200

            except Exception as e:
                return jsonify({"error": f"cannot edit because {str(e)}"}), 500
            

        if request.method == 'DELETE':
            try:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                role_id = user[6]
                
                if role_id != 1:
                    return jsonify({"message": "you are not authorized to delete programs"}), 401
                
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()

                if not user[8]:
                    return jsonify({"message": "user not verified"}), 401
                
                cursor.execute("DELETE FROM programs WHERE id = %s", (id,))
                mysql.connection.commit()

                if cursor.rowcount > 0:
                    return jsonify({"message": f"program with id ({id}) has been deleted successfully"}), 200
                else:
                    return jsonify({"message": f"no program found with id ({id})"}), 404
            except Exception as e:
                return jsonify({"error": {str(e)}}), 500
            
    except Exception as e:
        return jsonify({"error": {str(e)}}), 500         