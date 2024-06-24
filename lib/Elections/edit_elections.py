from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import re
import jwt
from lib.Authentications.token.token_requirement import TokenRequirement

# DATE_FORMAT = '%Y-%m-%d'

edit_elections = Blueprint('_edit_elections', __name__)
token_requirement = TokenRequirement(edit_elections)

@edit_elections.route('/edit_elections/<int:election_id>', methods=['PUT', 'GET', 'DELETE'])
@token_requirement.token_required
def edit_index(election_id):
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

    if request.method == 'PUT':

        try:
            title = request.form.get('title').lower()
            start_datetime_str = request.form.get('start_datetime')
            end_datetime_str = request.form.get('end_datetime')

            datetime_format = "%Y-%m-%d %H:%M"

            # Regular expression pattern for validation
            datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

            # Checking if the datetime strings are in the correct format
            if not datetime_pattern.match(start_datetime_str) or not datetime_pattern.match(end_datetime_str):
                return jsonify({'message': 'Invalid datetime format. Expected format: YYYY-MM-DD HH:MM'}), 400

            # Converting string datetimes to datetime objects
            start_datetime = datetime.strptime(start_datetime_str, datetime_format)
            end_datetime = datetime.strptime(end_datetime_str, datetime_format)

            cursor = mysql.connection.cursor()
            
            # Fetch the existing election details
            cursor.execute("SELECT * FROM election WHERE election_id = %s", (election_id,))
            election = cursor.fetchone()

            if not election:
                return jsonify({"message": "Election not found"}), 404
            
            # Fetch the existing election details
            cursor.execute("SELECT * FROM election WHERE election_title = %s", (title,))
            election_title = cursor.fetchone()

            if election_title:
                return jsonify({"message": "title already exist"}), 404

            # Update the election
            cursor.execute("""
                UPDATE election 
                SET election_title = %s, 
                    start_datetime = %s, 
                    end_datetime = %s
                WHERE election_id = %s
            """, (title, start_datetime, end_datetime, election_id))
            mysql.connection.commit()

            cursor.execute("SELECT * FROM election WHERE election_id = %s", (election_id,))
            get_election = cursor.fetchone()

            response_data = {
                "election_id": get_election[0],
                "election_title": get_election[1],
                "serial_code": get_election[2],
                "start_date": get_election[3].strftime("%a, %d %b %Y %H:%M"),
                "end_date": get_election[4].strftime("%a, %d %b %Y %H:%M"),
                "date_created": get_election[5],
            }
            return jsonify({'message': 'successful', 'response_data': response_data}), 200
            # return jsonify({"message": f"Election with ID {election_id} has been updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    if request.method == 'GET':

        try:
            # Fetch the election details
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM election WHERE election_id = %s", (election_id,))
            election = cursor.fetchone()

            if not election:
                return jsonify({"message": "Election not found"}), 404

            # Prepare the response
            response_data = {
                "election_id": election[0],
                "election_title": election[1],
                "serial_code": election[2],
                "start_date": election[3].strftime("%a, %d %b %Y %H:%M"),
                "end_date": election[4].strftime("%a, %d %b %Y %H:%M"),
                "date_created": election[5],
            }

            return jsonify(response_data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
        

    if request.method == 'DELETE':

        try:
            cursor = mysql.connection.cursor()
            
            # Delete the election
            cursor.execute("DELETE FROM election WHERE election_id = %s", (election_id,))
            mysql.connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({"message": f"Election with ID {election_id} has been deleted successfully"}), 200
            else:
                return jsonify({"message": f"No election found with ID {election_id}"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 400