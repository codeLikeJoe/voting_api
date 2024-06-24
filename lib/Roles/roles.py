from flask import Blueprint, request, jsonify,current_app

roles = Blueprint('_roles', __name__)

@roles.route('/roles', methods=['GET'])
def get_roles_index():

    try:
        mysql = current_app.extensions['mysql']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM roles')
        roles = cursor.fetchall()

        if roles is None:
            return jsonify({"message": 'sorry, there are no roles available at the moment'})

        response_data = []

        for role in roles:
            response_data.append({
                "role_id": role[0],
                "role_title": role[1],
            })
        
        return jsonify({'roles': response_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500