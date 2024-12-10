from flask import Blueprint, request, jsonify,current_app

roles = Blueprint('_roles', __name__)

@roles.route('/api/v1/roles', methods=['GET'])
def get_roles_index():

    try:
        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM roles')
        roles = cursor.fetchall()

        if not roles:
            return jsonify({"message": 'sorry, there are no roles available at the moment'})

        response_list = []

        for role in roles:
            response_data = {
                "role_id": role[0],
                "role_title": role[1],
            }
            response_list.append(response_data)

        if not response_list:
            return jsonify({'message': 'sorry, there are no roles available at the moment'}), 404
        else:
            return jsonify(response_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500