from flask import Blueprint, request, jsonify,current_app

adding_roles = Blueprint('_adding_roles', __name__)

@adding_roles.route('/api/v1/add-role', methods=['POST'])
def add_role_index():
    try:
        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()

        raw_data = request.get_json()
        
        if not raw_data:
            return jsonify({"error": "No data provided"}), 400
        
        role_title = raw_data.get("role_title")

        cursor.execute("SELECT * FROM roles WHERE title = %s", (role_title,))
        role_exists = cursor.fetchone()

        if role_exists:
            return jsonify({"message": "role already exists",}), 400
        
        cursor.execute("INSERT INTO roles (title) VALUES (%s)", (role_title,))
        cursor.connection.commit()

        cursor.execute("SELECT * FROM roles WHERE title = %s", (role_title,))
        get_role = cursor.fetchone()

        cursor.close()

        return jsonify({
            "message": 'successful',
            'role_id': get_role[0],
            'role': get_role[1]
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500