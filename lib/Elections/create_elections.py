from flask import Blueprint, request, jsonify,current_app
from random import *
from datetime import datetime, timedelta
import re
import jwt
from lib.Authentications.token.token_requirement import TokenRequirement

# DATE_FORMAT = '%Y-%m-%d'


create_elections = Blueprint('_create_elections', __name__)
token_requirement = TokenRequirement(create_elections)


@create_elections.route('/create_elections', methods=['POST'])
@token_requirement.token_required
def index():
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
        
        title = request.form.get('title').lower()
        start_datetime_str = request.form.get('start_datetime')
        end_datetime_str = request.form.get('end_datetime')

        if not title or not start_datetime_str or not end_datetime_str:
            return jsonify({'message': 'all fields are required'}), 400

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
        
        cursor.execute("SELECT * FROM election WHERE election_title = %s", (title,))
        election = cursor.fetchone()

        if election:
            return jsonify({"message":"Election title already exists"}), 400
        
        code = randint(10000, 99999)
        while True:
            cursor.execute("SELECT * FROM election WHERE serial_code = %s", (code,))
            existing_code = cursor.fetchone()
            if not existing_code:
                break  # Exit the loop if no existing code found
            else:
                print(f"{code} already exists")
                code = randint(10000, 99999)  # Generate a new code if the current one exists
                print(f"new coed: {code}")

        date_created = datetime.now()
        
        cursor.execute("""INSERT INTO election (election_id, election_title, serial_code, 
                       start_datetime, end_datetime, date_created) VALUES (%s, %s, %s, %s, %s, %s)""",
                    (None, title, code, start_datetime, end_datetime, date_created))
        mysql.connection.commit()


        cursor.execute("SELECT * FROM election WHERE serial_code = %s", (code,))
        election = cursor.fetchone()


        if not election:
            return jsonify({"message": "Election not found"}), 404

        response_data = {
            "election_id": election[0],
            "election_title": election[1],
            "serial_code": election[2],
            "start_date": election[3].strftime("%a, %d %b %Y %H:%M"),
            "end_date": election[4].strftime("%a, %d %b %Y %H:%M"),
            "date_created": election[5],
        }
        return jsonify({"message":"successful", 'record': response_data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400