from flask import Blueprint, request, jsonify,current_app

adding_roles = Blueprint('_adding_roles', __name__)

@adding_roles.route('/adding_roles', methods=['POST'])
def add_role_index():

    role = request.form.get('role_title')

    if not role:
        return jsonify({"message": "role field is required"}), 400

    try:
        role_title = role.lower()

        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM roles WHERE title = %s", (role_title,))
        role_exists = cursor.fetchone()

        if role_exists:
            return jsonify({"message": "role already exists",}), 400
        
        cursor.execute("INSERT INTO roles (title) VALUES (%s)", (role_title,))
        cursor.connection.commit()

        cursor.execute("SELECT * FROM roles WHERE title = %s", (role_title,))
        get_role = cursor.fetchone()

        response_data = {
            'role_id': get_role[0],
            'role': get_role[1],
        }
        cursor.close()

        return jsonify({"message": 'successful', 'response_data': response_data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500