from flask import Blueprint, request, jsonify,current_app


program = Blueprint('_program', __name__)


@program.route('/program/<string:code>', methods=['PUT', 'GET', 'DELETE'])
def index(code):
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM programs WHERE code = %s", (code,))
    program = cursor.fetchone()

    if request.method == 'GET':
        try:
            if not program:
                return jsonify({"message":"No record found"}), 404
            

            user_dict = {
                'id': program[0],
                'title': program[1].capitalize(),
                'code': program[2].upper(),
            }
            return jsonify(user_dict), 200
        except Exception as e:
            return jsonify({"error": str(e)})
        
        

    if request.method == 'PUT':
        try:
            if not program:
                return jsonify({"message": "program not found"}), 404
            
            title = request.form['title'].lower()
            _code = request.form['code'].lower()
            
            cursor.execute("UPDATE programs SET title = %s, code = %s WHERE code = %s",
                                    (title, _code, code))
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