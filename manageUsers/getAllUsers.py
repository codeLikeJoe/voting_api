from flask import Blueprint,jsonify,current_app

getUsers = Blueprint('getUsers', __name__)

@getUsers.route('/users', methods=['GET'])
def get_all_users():
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    users = cursor.fetchall()

    # Execute a query to count the total number of users
    cursor.execute("SELECT COUNT(*) FROM students")
    total_users = cursor.fetchone()[0] # Fetch the count from the first (and only) row

    user_list = []

    for user in users:
        user_data = {
            'id': user[0],
            'firstname': user[1],
            'lastname': user[2],
            'student_id': user[3],
            'email': user[4],
            'program': user[5],
            'date_created': user[7],
        }
        user_list.append(user_data)

     # Include the total number of users in the response
    response_data = {
        'users': user_list,
        'total_users': total_users
    }
    
    if not user_list:
        return jsonify({'message': 'No users found'}), 404
    else:
        return jsonify(response_data), 200
