from flask import Blueprint,request,jsonify,current_app

get_programs = Blueprint('_programs', __name__)

@get_programs.route('/api/v1/programs', methods=['GET'])
def index():    
    try:
        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()
        
        cursor.execute("SELECT * FROM programs")
        programs = cursor.fetchall()

        program_list = []

        for program in programs:
            program_data = {
                'program_id': program[0],
                'program_title': program[1],
                'program_code': program[2],
            }
            program_list.append(program_data)
        
        if not program_list:
            return jsonify({'message': 'No programs found'}), 404
        else:
            return jsonify(program_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500