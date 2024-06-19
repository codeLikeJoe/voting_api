from flask import Blueprint, request, jsonify,current_app

positions = Blueprint('_positions', __name__)

@positions.route('/positions', methods = ['GET'])
def get_positions():
    mysql = current_app.extensions['mysql']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM positions')
        positions = cursor.fetchall()

        if not positions:
            return jsonify({'message': 'There are no positions available'})
        
        response_data = []
        
        for position in positions:
            response_data.append({
                'id': position[0],
                'position': position[1].capitalize(),
                'cgpa_criteria': position[2],
                'application_fee': position[3],
                'program': position[4].upper() if position[4] is not None else None,
                'election_source': position[5].capitalize(),
                'start_datetime': position[7].strftime("%a, %d %b %Y %H:%M"),
                'end_datetime': position[8].strftime("%a, %d %b %Y %H:%M"),
                'date_created': position[9]
            })

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 400