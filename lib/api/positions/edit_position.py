from flask import Blueprint, request, jsonify,current_app
from datetime import datetime
import re
import jwt
from lib.core.token_requirement import TokenRequirement

edit_positions = Blueprint('_edit_positions', __name__)
token_requirement = TokenRequirement(edit_positions)

@edit_positions.route('/edit_positions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_requirement.token_required
def create_positions_index(id):
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
    

    if request.method == 'GET':

        try:
            cursor = mysql.connection.cursor()


            cursor.execute('SELECT * FROM positions WHERE position_id = %s', (id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": f"Sorry, position with the id ({str(id)}) does not exist"})
            
            response_data = {
                'position_id': result[0],
                'position': result[1],
                'cgpa_criteria': result[2],
                'application_fee': result[3],
                'program_id': result[4] if result[4] is not None else None,
                'election_source': result[5],
                'application_form': result[6] if result[6] is not None else None,
                'application_start_datetime': result[7].strftime("%a, %d %b %Y %H:%M"),
                'application_end_datetime': result[8].strftime("%a, %d %b %Y %H:%M"),
                'date_created': result[9],
                'number_of_slots': result[10],
                'slots_available': result[11],
            }
            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({'Error': str(e)}), 400
        

    if request.method == 'PUT':

        try:
            position_title = request.form['position_title'].lower()
            cgpa_criteria = request.form['cgpa_criteria']
            fee = request.form['fee']
            program_id = request.form['program_id'].lower()
            election_id = request.form['election_id']
            new_slot = request.form['number_of_slots']
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
                return jsonify({'message': f'Sorry, {str(election)} has already ended'}), 400
            

            datetime_format = "%Y-%m-%d %H:%M"

            # Regular expression pattern for validation
            datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

            # Checking if the datetime strings are in the correct format
            if not datetime_pattern.match(start_datetime_str) or not datetime_pattern.match(end_datetime_str):
                return jsonify({'message': 'Invalid datetime format. Expected format: YYYY-MM-DD HH:MM'}), 400


            # Converting string datetimes to datetime objects
            start_datetime = datetime.strptime(start_datetime_str, datetime_format)
            end_datetime = datetime.strptime(end_datetime_str, datetime_format)


            if program_id:
                cursor.execute('SELECT * FROM program WHERE program_id = %s', (program_id,))
                _program = cursor.fetchone()

                if _program is None:
                    return jsonify({'message': 'Program does not exist'}), 404
                
                cursor.execute("""SELECT * FROM positions WHERE position_title = %s AND program_id = %s AND 
                               election_id = %s AND cgpa_criteria = %s AND application_fee = %s 
                               AND application_start_date = %s AND application_end_date = %s""", 
                            (position_title, program_id, election_id, cgpa_criteria, fee, start_datetime, end_datetime))
            else:
                cursor.execute("""SELECT * FROM positions WHERE position_title = %s AND program_id IS NULL AND 
                               election_id = %s AND cgpa_criteria = %s AND application_fee = %s 
                               AND application_start_date = %s AND application_end_date = %s""", 
                            (position_title, election_id, cgpa_criteria, fee, start_datetime, end_datetime))


            _position = cursor.fetchone()
            if _position:
                return jsonify({'message': 'This position already exists'}), 400
            
            # old_slot = _position[10]
            # slot_available = _position[11]

            # if new_slot < old_slot:
            #     if old_slot != slot_available:
            #         return jsonify({'error': 'sorry, cannot edit slot'}), 400
            #     elif old_slot == slot_available:
            #         number_of_slots = new_slot
            #         new_slot_available = new_slot
            # elif new_slot > old_slot:
            #     number_of_slots = new_slot
            #     new_slot_available = slot_available



            # Inserting the data into the database
            if program_id:
                cursor.execute("""UPDATE positions SET position_title = %s, cgpa_criteria = %s, 
                               application_fee = %s, program_id = %s, election_id = %s, 
                               application_start_date = %s, application_end_date = %s, 
                             WHERE position_id = %s""", 
                            (position_title, cgpa_criteria, fee, program_id, election_id, start_datetime, 
                             end_datetime, id))
            else:
                cursor.execute("""UPDATE positions SET position_title = %s, cgpa_criteria = %s, 
                               application_fee = %s, program_id = NULL, election_id = %s, 
                               application_start_date = %s, application_end_date = %s,
                               WHERE position_id = %s""", 
                            (position_title, cgpa_criteria, fee, election_id, start_datetime, 
                             end_datetime, id))

            mysql.connection.commit()


            if program_id:
                cursor.execute('SELECT * FROM positions WHERE position_title = %s AND program_id = %s AND election_id = %s', 
                            (position_title, program_id, election_id))
            else:
                cursor.execute('SELECT * FROM positions WHERE position_title = %s AND program_id IS NULL AND election_id = %s', 
                            (position_title, election_id))


            get_positions = cursor.fetchone()
            response_data = {
                'id': get_positions[0],
                'position_title': get_positions[1],
                'cgpa_criteria': get_positions[2],
                'application_fee': get_positions[3],
                'program_id': get_positions[4] if get_positions[4] is not None else None,
                'election_id': get_positions[5],
                'start_datetime': get_positions[7].strftime("%a, %d %b %Y %H:%M"),
                'end_datetime': get_positions[8].strftime("%a, %d %b %Y %H:%M"),
                'date_created': get_positions[9],
                'number_of_slots': get_positions[10],
                'slots_available': get_positions[11],
            }

            cursor.close()
            return jsonify({'message': 'successful', 'response_data': response_data}), 200

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
