from flask import Blueprint, request, jsonify,current_app

elections = Blueprint('_elections', __name__)

@elections.route('/elections', methods=['GET'])
def get_elections():

    mysql = current_app.extensions['mysql']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM election')
        elections = cursor.fetchall()

        if elections is None:
            return jsonify({'message': 'There are no elections available'}), 404
        
        response_data = []

        for election in elections:
            response_data.append({
                "election_id": election[0],
                "election_title": election[1].upper(),
                "serial_code": election[2],
                "start_date": election[3],
                "end_date": election[4],
                "created_at": election[5],
            })
        
        return jsonify({'elections': response_data}), 200

    except Exception as e:
        return jsonify({'Error': str(e)}), 500