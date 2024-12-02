from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import re
import jwt
from lib.authentications.token_requirement import TokenRequirement

create_positions = Blueprint('_create_positions', __name__)
token_requirement = TokenRequirement(create_positions)

@create_positions.route('/create_positions', methods=['POST'])
@token_requirement.token_required
def create_positions_index():
    mysql = current_app.extensions['mysql']
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

    try:
        position_title = request.form['position_title'].lower()
        cgpa_criteria = request.form['cgpa_criteria']
        fee = request.form['fee']
        number_of_slots = request.form['number_of_slots']
        program_id = request.form['program_id']
        election_id = request.form['election_id']
        start_datetime_str = request.form['start_datetime']
        end_datetime_str = request.form['end_datetime']

        if not position_title or not cgpa_criteria or not fee or not election_id or not start_datetime_str or not end_datetime_str:
            return jsonify({'message': 'Missing required data'}), 400

        cursor = mysql.connection.cursor()


        cursor.execute('SELECT * FROM election WHERE election_id = %s', (election_id,))
        _election = cursor.fetchone()

        if _election is None:
            return jsonify({'message': 'Election is not available'}), 404
        
        election = _election[1]

        expired = _election[4].strftime("%Y-%m-%d %H:%M")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        # print(expired)
        # print(now)
        # Check if the election has ended
        if now >= expired:
            return jsonify({'message': f'Sorry, {str(election).capitalize()} has already ended'}), 400


        if program_id:
            cursor.execute('SELECT * FROM program WHERE program_id = %s', (program_id,))
            _program = cursor.fetchone()

            if _program is None:
                return jsonify({'message': 'Program does not exist'}), 404
            
            cursor.execute('SELECT * FROM positions WHERE position_title = %s AND program_id = %s AND election_id = %s', 
                           (position_title, program_id, election_id))
        else:
            cursor.execute('SELECT * FROM positions WHERE position_title = %s AND program_id IS NULL AND election_id = %s', 
                           (position_title, election_id))


        _position = cursor.fetchone()
        if _position:
            return jsonify({'message': 'This position already exists'}), 400

        datetime_format = "%Y-%m-%d %H:%M"

        # Regular expression pattern for validation
        datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

        # Checking if the datetime strings are in the correct format
        if not datetime_pattern.match(start_datetime_str) or not datetime_pattern.match(end_datetime_str):
            return jsonify({'message': 'Invalid datetime format. Expected format: YYYY-MM-DD HH:MM'}), 400


        # Converting string datetimes to datetime objects
        start_datetime = datetime.strptime(start_datetime_str, datetime_format)
        end_datetime = datetime.strptime(end_datetime_str, datetime_format)
        date = datetime.now()


        # Inserting the data into the database
        if program_id:
            cursor.execute("""INSERT INTO positions 
                           (position_title, cgpa_criteria, application_fee, program_id, election_id, 
                              application_start_date, application_end_date, date_created, 
                           number_of_slots, slots_available) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (position_title, cgpa_criteria, fee, program_id, election_id, 
                            start_datetime, end_datetime, date, number_of_slots, number_of_slots))
        else:
            cursor.execute("""INSERT INTO positions 
                           (position_title, cgpa_criteria, application_fee, program_id, election_id, 
                              application_start_date, application_end_date, date_created, 
                           number_of_slots, slots_available) 
                              VALUES (%s, %s, %s, NULL, %s, %s, %s, %s, %s, %s)""", 
                           (position_title, cgpa_criteria, fee, election_id, start_datetime, 
                            end_datetime, date, number_of_slots, number_of_slots))
        mysql.connection.commit()


        if program_id:
            cursor.execute('SELECT * FROM positions WHERE position_title = %s AND program_id = %s AND election_id = %s', 
                        (position_title, program_id, election_id))
        else:
            cursor.execute('SELECT * FROM positions WHERE position_title = %s AND program_id IS NULL AND election_id = %s', 
                        (position_title, election_id))


        get_positions = cursor.fetchone()
        response_data = {
            'positionid': get_positions[0],
            'position_title': get_positions[1],
            'cgpa_criteria': get_positions[2],
            'application_fee': get_positions[3],
            'program_id': get_positions[4] if get_positions[4] is not None else None,
            'election_id': get_positions[5],
            'start_datetime': get_positions[7].strftime("%a, %d %b %Y %H:%M"),
            'end_datetime': get_positions[8].strftime("%a, %d %b %Y %H:%M"),
            'date_created': get_positions[9],
            'number_of_slots': get_positions[10],
        }

        cursor.close()
        return jsonify({'message': 'successful', 'recorded_data': response_data}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'Error': str(e)}), 400
