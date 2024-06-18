from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

edit_elections = Blueprint('_edit_elections', __name__)

@edit_elections.route('/edit_elections/<int:election_id>', methods=['PUT', 'GET', 'DELETE'])
def edit_index(election_id):
    mysql = current_app.extensions['mysql']

    if request.method == 'PUT':

        try:
            title = request.form.get('title').lower()
            start_date_str = request.form.get('start date')
            end_date_str = request.form.get('end date')

            # Validate date format
            try:
                start_date = datetime.strptime(start_date_str, DATE_FORMAT)
                end_date = datetime.strptime(end_date_str, DATE_FORMAT)
            except ValueError:
                return jsonify({"error": "Invalid date format. Expected format: YYYY-MM-DD"}), 400

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
            """, (title, start_date, end_date, election_id))

            mysql.connection.commit()
            return jsonify({"message": f"Election with ID {election_id} has been updated successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
        

    if request.method == 'GET':

        try:
            # Fetch the election details
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM elections WHERE election_id = %s", (election_id,))
            election = cursor.fetchone()
            print(election)

            if not election:
                return jsonify({"message": "Election not found"}), 404

            # Prepare the response
            response_data = {
                "election_id": election[0],
                "election_title": election[1].upper(),
                "serial_code": election[2],
                "start_date": election[3],
                "end_date": election[4],
                "created_at": election[5],
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