from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import re

# DATE_FORMAT = '%Y-%m-%d'

edit_elections = Blueprint('_edit_elections', __name__)

@edit_elections.route('/edit_elections/<int:election_id>', methods=['PUT', 'GET', 'DELETE'])
def edit_index(election_id):
    mysql = current_app.extensions['mysql']

    if request.method == 'PUT':

        try:
            title = request.form['title'].lower()
            start_datetime_str = request.form['start_datetime']
            end_datetime_str = request.form['end_datetime']

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
            cursor.execute("SELECT * FROM elections WHERE election_id = %s", (election_id,))
            election = cursor.fetchone()

            if not election:
                return jsonify({"message": "Election not found"}), 404

            # Update the election
            cursor.execute("""
                UPDATE elections 
                SET election_title = %s, 
                    start_date = %s, 
                    end_date = %s
                WHERE election_id = %s
            """, (title, start_datetime, end_datetime, election_id))

            mysql.connection.commit()

            # cursor.execute("SELECT * FROM elections WHERE election_id = %s", (election_id,))
            # election = cursor.fetchone()

            # Prepare the response
            response_data = {
                "election_id": election[0],
                "election_title": election[1].upper(),
                "serial_code": election[2],
                "start_date": election[3].strftime("%a, %d %b %Y %H:%M"),
                "end_date": election[4].strftime("%a, %d %b %Y %H:%M"),
                "date_created": election[5],
            }
            return jsonify(response_data), 200
            # return jsonify({"message": f"Election with ID {election_id} has been updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    if request.method == 'GET':

        try:
            # Fetch the election details
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM elections WHERE election_id = %s", (election_id,))
            election = cursor.fetchone()

            if not election:
                return jsonify({"message": "Election not found"}), 404

            # Prepare the response
            response_data = {
                "election_id": election[0],
                "election_title": election[1].upper(),
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
            cursor.execute("DELETE FROM elections WHERE election_id = %s", (election_id,))
            mysql.connection.commit()
            
            if cursor.rowcount > 0:
                return jsonify({"message": f"Election with ID {election_id} has been deleted successfully"}), 200
            else:
                return jsonify({"message": f"No election found with ID {election_id}"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 400