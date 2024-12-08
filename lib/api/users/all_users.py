from flask import Blueprint,jsonify,current_app
from lib.core.token_requirement import TokenRequirement

getUsers = Blueprint('getUsers', __name__)
token_requirement = TokenRequirement(getUsers)

@getUsers.route('/api/v1/users', methods=['GET'])
@token_requirement.token_required
def get_all_users():
    try:
        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        # Execute a query to count the total number of users
        # cursor.execute("SELECT COUNT(*) FROM users")
        # total_users = cursor.fetchone()[0] # Fetch the count from the first (and only) row

        user_list = []

        for user in users:
            user_data = {
                'id': user[0],
                'firstname': user[1],
                'lastname': user[2],
                'student_id': user[3],
                'email': user[4],
                'program_id': user[5],
                'program_title': user[6],
                'role_id': user[9],
                'created_at': user[8],
                'admission_date': user[10],
                'completion_date': user[11],
            }
            user_list.append(user_data)

            # Include the total number of users in the response
            # response_data = {
            #     'users': user_list,
            #     'total_users': total_users
            # }
        
        if not user_list:
            return jsonify({'error': 'no users found'}), 404
        else:
            return jsonify(user_list), 200

    except Exception as e:
        return jsonify({"error":f'an error occurred. {str(e)}'}), 500
