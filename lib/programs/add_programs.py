from flask import Blueprint, request, jsonify,current_app


add_program = Blueprint('_add_program', __name__)


@add_program.route('/add_program', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']

    if not request.form:
        return jsonify({"error": "No form data provided"}), 400

    program_title = request.form.get('program_title')
    program_code = request.form.get('program_code')

    if not program_title or not program_code:
        return jsonify({"error": "Program title or code is missing"}), 400

    try:
        program_title = program_title.lower()
        program_code = program_code.lower()

        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM program WHERE program_title = %s OR program_code = %s", 
                       (program_title, program_code))
        program = cursor.fetchone()

        if program:
            return jsonify({"message":"program already exists"}), 400
        
        cursor.execute("INSERT INTO program (program_title, program_code) VALUES (%s, %s)",
                    (program_title, program_code))
        mysql.connection.commit()

        cursor.execute("SELECT * FROM program WHERE program_title = %s OR program_code = %s", 
                       (program_title, program_code))
        _program = cursor.fetchone()

        response_data = {
            'program_id': _program[0],
            'program_title': _program[1],
            'program_code': _program[2],
        }

        return jsonify({"message":"successfully", 'response_data': response_data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500