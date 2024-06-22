from flask import Blueprint, request, jsonify,current_app


program = Blueprint('_program', __name__)


@program.route('/program/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def index(id):
    mysql = current_app.extensions['mysql']

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM program WHERE program_id = %s", (id,))
        program = cursor.fetchone()

        if not program:
            return jsonify({"message": "program not found"}), 404

        if request.method == 'GET':

            try:          
                user_dict = {
                    'program_id': program[0],
                    'program_title': program[1],
                    'program_code': program[2],
                }
                return jsonify(user_dict), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
            
        if request.method == 'PUT':

            program_title = request.form.get('program_title')
            program_code = request.form.get('program_code')

            if not program_title or not program_code:
                return jsonify({"error": "Program title or code is missing"}), 400

            try:
                program_title = program_title.lower()
                program_code = program_code.lower()
                
                cursor.execute("UPDATE program SET program_title = %s, program_code = %s WHERE program_id = %s",
                                        (program_title, program_code, id))
                mysql.connection.commit()

                cursor.execute("SELECT * FROM program WHERE program_id = %s", (id,))
                get_program = cursor.fetchone()

                response_data = {
                    'program_id': get_program[0],
                    'program_title': get_program[1],
                    'program_code': get_program[2],
                }
                cursor.close()
                return jsonify({'message': 'successful', 'response_data': response_data}), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500
            


        if request.method == 'DELETE':

            try:
            
                cursor.execute("DELETE FROM program WHERE program_id = %s", (id,))
                mysql.connection.commit()

                if cursor.rowcount > 0:
                    return jsonify({"message": f"Election with ID {id} has been deleted successfully"}), 200
                else:
                    return jsonify({"message": f"No election found with ID {id}"}), 404

                # return jsonify({"message": f"program with program_id ({id}) deleted successfully"}), 200
            except Exception as e:
                return jsonify({"error": {str(e)}}), 500
            
    except Exception as e:
        return jsonify({"error": {str(e)}}), 500         