from flask import Blueprint, request, jsonify,current_app


program = Blueprint('_program', __name__)


@program.route('/program/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def index(id):
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        try:
            cursor.execute("SELECT * FROM programs WHERE id = %s", (id,))
            program = cursor.fetchone()

            if not program:
                return jsonify({"message":"No record found"}), 404
            

            user_dict = {
                'id': program[0],
                'title': program[1],
                'code': program[2],
            }
            return jsonify(user_dict), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        
    if request.method == 'PUT':
        try:
            cursor.execute("SELECT * FROM programs WHERE id = %s", (id,))
            program = cursor.fetchone()

            if not program:
                return jsonify({"message": "program not found"}), 404
            
            title = request.form.get('title').lower()
            _code = request.form.get('code').lower()

            cursor.execute("SELECT * FROM programs WHERE title = %s AND code = %s", (title, _code))
            program = cursor.fetchone()

            if program:
                return jsonify({"message":"program already exists"}), 400
            
            cursor.execute("UPDATE programs SET title = %s, code = %s WHERE id = %s",
                                    (title, _code, id))
            mysql.connection.commit()
            return jsonify({"message": f"program details updated successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)})
        


    if request.method == 'DELETE':
        try:

            if not program:
                return jsonify({"message": "program not found"}), 404
        
            cursor.execute("DELETE FROM programs WHERE code = %s", (code,))
            mysql.connection.commit()
            return jsonify({"message": f"program with code({code}) deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message": {str(e)}})