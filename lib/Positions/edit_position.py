from flask import Blueprint, request, jsonify,current_app
from datetime import datetime
import re

edit_positions = Blueprint('_edit_positions', __name__)

@edit_positions.route('/edit_positions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def create_positions_index(id):
    mysql = current_app.extensions['mysql']

    if request.method == 'GET':

        try:
            cursor = mysql.connection.cursor()


            cursor.execute('SELECT * FROM positions WHERE position_id = %s', (id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": f"Sorry, position with the id ({str(id)}) does not exist"})
            
            response_data = {
                'position_id': result[0],
                'position': result[1].capitalize(),
                'cgpa_criteria': result[2],
                'application_fee': result[3],
                'program': result[4].upper() if result[4] is not None else None,
                'election_source': result[5].upper(),
                'application_form': result[6] if result[6] is not None else None,
                'application_start_datetime': result[7].strftime("%a, %d %b %Y %H:%M"),
                'application_end_datetime': result[8].strftime("%a, %d %b %Y %H:%M"),
                'date_created': result[9],
            }
            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({'Error': str(e)}), 400
        

    if request.method == 'PUT':

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

            if not _election:
                return jsonify({'message': 'Election is not available'}), 404
            
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
            

            datetime_format = "%Y-%m-%d %H:%M"

            # Regular expression pattern for validation
            datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

            # Checking if the datetime strings are in the correct format
            if not datetime_pattern.match(start_datetime_str) or not datetime_pattern.match(end_datetime_str):
                return jsonify({'message': 'Invalid datetime format. Expected format: YYYY-MM-DD HH:MM'}), 400


            # Converting string datetimes to datetime objects
            start_datetime = datetime.strptime(start_datetime_str, datetime_format)
            end_datetime = datetime.strptime(end_datetime_str, datetime_format)


            if program:
                cursor.execute('SELECT * FROM programs WHERE code = %s', (program,))
                _program = cursor.fetchone()

                if not _program:
                    return jsonify({'message': 'Program does not exist'}), 404
                
                cursor.execute("""SELECT * FROM positions WHERE position = %s AND program = %s AND 
                               election_source = %s AND cgpa_criteria = %s AND application_fee = %s 
                               AND application_start_date = %s AND application_end_date = %s""", 
                            (position, program, election, cgpa_criteria, fee, start_datetime, end_datetime))
            else:
                cursor.execute("""SELECT * FROM positions WHERE position = %s AND program IS NULL AND 
                               election_source = %s AND cgpa_criteria = %s AND application_fee = %s 
                               AND application_start_date = %s AND application_end_date = %s""", 
                            (position, election, cgpa_criteria, fee, start_datetime, end_datetime))


            _position = cursor.fetchone()
            if _position:
                return jsonify({'message': 'This position already exists'}), 400
            
            # if not position:
            #     return jsonify({'message': 'Position does not exists'}), 400



            # Inserting the data into the database
            if program:
                cursor.execute("""UPDATE positions SET position = %s, cgpa_criteria = %s, application_fee = %s, program = %s, 
                                election_source = %s, application_start_date = %s, application_end_date = %s 
                                WHERE position_id = %s""", 
                            (position, cgpa_criteria, fee, program, election, start_datetime, end_datetime, id))
            else:
                cursor.execute("""UPDATE positions SET position = %s, cgpa_criteria = %s, application_fee = %s, program = NULL, 
                                election_source = %s, application_start_date = %s, application_end_date = %s 
                                WHERE position_id = %s""", 
                            (position, cgpa_criteria, fee, election, start_datetime, end_datetime, id))

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
            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({'Error': str(e)}), 400


    if request.method == 'DELETE':

        try:
            cursor = mysql.connection.cursor()


            cursor.execute("DELETE FROM positions WHERE position_id = %s", (id,))
            mysql.connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"message": f"Position with ID - ({str(id)}) has been deleted successfully"}), 200
            else:
                return jsonify({"message": f"No position found with ID - ({str(id)})"}), 404

        except Exception as e:
            return jsonify({'Error': str(e)}), 400
