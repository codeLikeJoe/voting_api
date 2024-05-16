from flask import Blueprint,request,jsonify,current_app

get_programs = Blueprint('_programs', __name__)

@get_programs.route('/programs', methods=['GET'])
def index():    
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM programs")
    programs = cursor.fetchall()

    # Execute a query to count the total number of programs
    cursor.execute("SELECT COUNT(*) FROM programs")
    total_programs = cursor.fetchone()[0] # Fetch the count from the first (and only) row

    program_list = []

    for program in programs:
        program_data = {
            'id': program[0],
            'firstname': program[1],
            'lastname': program[2],
        }
        program_list.append(program_data)

     # Include the total number of users in the response
    response_data = {
        'programs': program_list,
        'program_total': total_programs
    }
    
    if not program_list:
        return jsonify({'message': 'No users found'}), 404
    else:
        return jsonify(response_data), 200