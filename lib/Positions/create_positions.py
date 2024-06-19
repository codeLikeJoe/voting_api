from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import re

create_positions = Blueprint('_create_positions', __name__)

@create_positions.route('/create_positions', methods=['POST'])
def create_positions_index():
    mysql = current_app.extensions['mysql']

    try:
        position = request.form['position'].lower()
        cgpa_criteria = request.form['cgpa_criteria']
        fee = request.form['fee']
        program = request.form['program_code'].lower()
        election_id = request.form['election_id']
        start_datetime_str = request.form['start_datetime']
        end_datetime_str = request.form['end_datetime']

        if not position or not cgpa_criteria or not fee or not election_id or not start_datetime_str or not end_datetime_str:
            return jsonify({'message': 'Missing required data'}), 400

        cursor = mysql.connection.cursor()


        cursor.execute('SELECT * FROM elections WHERE election_id = %s', (election_id,))
        _election = cursor.fetchone()

        election = _election[1]
        if not _election:
            return jsonify({'message': 'Election is not available'}), 404

        expired = _election[4].strftime("%Y-%m-%d %H:%M")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        # print(expired)
        # print(now)
        # Check if the election has ended
        if now >= expired:
            return jsonify({'message': f'Sorry, {str(election).capitalize()} has already ended'}), 400


        if program:
            cursor.execute('SELECT * FROM programs WHERE code = %s', (program,))
            _program = cursor.fetchone()

            if not _program:
                return jsonify({'message': 'Program does not exist'}), 404
            
            cursor.execute('SELECT * FROM positions WHERE position = %s AND program = %s AND election_source = %s', 
                           (position, program, election))
        else:
            cursor.execute('SELECT * FROM positions WHERE position = %s AND program IS NULL AND election_source = %s', 
                           (position, election))


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
        if program:
            cursor.execute("""INSERT INTO positions (position, cgpa_criteria, application_fee, program, election_source, 
                              application_start_date, application_end_date, date_created) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (position, cgpa_criteria, fee, program, election, start_datetime, end_datetime, date))
        else:
            cursor.execute("""INSERT INTO positions (position, cgpa_criteria, application_fee, program, election_source, 
                              application_start_date, application_end_date, date_created) 
                              VALUES (%s, %s, %s, NULL, %s, %s, %s, %s)""", 
                           (position, cgpa_criteria, fee, election, start_datetime, end_datetime, date))
        mysql.connection.commit()


        if program:
            cursor.execute('SELECT * FROM positions WHERE position = %s AND program = %s AND election_source = %s', 
                        (position, program, election))
        else:
            cursor.execute('SELECT * FROM positions WHERE position = %s AND program IS NULL AND election_source = %s', 
                        (position, election))


        get_positions = cursor.fetchone()
        response_data = {
            'id': get_positions[0],
            'position': get_positions[1].capitalize(),
            'cgpa_criteria': get_positions[2],
            'application_fee': get_positions[3],
            'program': get_positions[4].upper() if get_positions[4] is not None else None,
            'election_source': get_positions[5].capitalize(),
            'start_datetime': get_positions[7].strftime("%a, %d %b %Y %H:%M"),
            'end_datetime': get_positions[8].strftime("%a, %d %b %Y %H:%M"),
            'date_created': get_positions[9]
        }

        cursor.close()
        return jsonify({'recorded_data': response_data}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'Error': str(e)}), 400
