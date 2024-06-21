from flask import Blueprint, request, jsonify,current_app


add_program = Blueprint('_add_program', __name__)


@add_program.route('/add_program', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']

    try:
        title = request.form['title'].lower()
        code = request.form['code'].lower()

        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM programs WHERE title = %s OR code = %s", (title, code))
        program = cursor.fetchone()

        if program:
            return jsonify({"message":"program already exists"}), 400
        
        cursor.execute("INSERT INTO programs (id, title, code) VALUES (%s, %s, %s)",
                    (None, title, code))
        mysql.connection.commit()

        cursor.execute("SELECT * FROM programs WHERE title = %s OR code = %s", (title, code))
        _program = cursor.fetchone()

        response_data = {
            'program_id': _program[0],
            'program_name': _program[1],
            'program_code': _program[2],
        }

        return jsonify({"message":"successfully", 'response_data': response_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400