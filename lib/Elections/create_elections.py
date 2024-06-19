from flask import Blueprint, request, jsonify,current_app
from random import *
from datetime import datetime, timedelta
import re

# DATE_FORMAT = '%Y-%m-%d'


create_elections = Blueprint('_create_elections', __name__)


@create_elections.route('/create_elections', methods=['POST'])
def index():
    mysql = current_app.extensions['mysql']

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
        
        cursor.execute("SELECT * FROM elections WHERE election_title = %s", (title,))
        election = cursor.fetchone()

        if election:
            return jsonify({"message":"Election title already exists"}), 400
        
        code = randint(10000, 99999)
        while True:
            cursor.execute("SELECT * FROM elections WHERE serial_code = %s", (code,))
            existing_code = cursor.fetchone()
            if not existing_code:
                break  # Exit the loop if no existing code found
            else:
                print(f"{code} already exists")
                code = randint(10000, 99999)  # Generate a new code if the current one exists
                print(f"new coed: {code}")

        date_created = datetime.now()
        
        cursor.execute("""INSERT INTO elections (election_id, election_title, serial_code, 
                       start_date, end_date, date_created) VALUES (%s, %s, %s, %s, %s, %s)""",
                    (None, title, code, start_datetime, end_datetime, date_created))
        mysql.connection.commit()


        cursor.execute("SELECT * FROM elections WHERE serial_code = %s", (code,))
        election = cursor.fetchone()


        if not election:
            return jsonify({"message": "Election not found"}), 404

        response_data = {
            "election_id": election[0],
            "election_title": election[1].upper(),
            "serial_code": election[2],
            "start_date": election[3].strftime("%a, %d %b %Y %H:%M"),
            "end_date": election[4].strftime("%a, %d %b %Y %H:%M"),
            "date_created": election[5],
        }
        return jsonify({"message":f"{str(title)} has been added successfully", 'record': response_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400