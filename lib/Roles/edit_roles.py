from flask import Blueprint, request, jsonify,current_app

edit_roles = Blueprint('_edit_roles', __name__)

@edit_roles.route('/edit_roles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def edit_roles_index(id):

    try:
        mysql = current_app.extensions['mysql']
        cursor = mysql.connection.cursor()

        if request.method == 'GET':
            cursor.execute('select * from roles where id = %s', (id,))
            role = cursor.fetchone()

            if role is None:
                return jsonify({'message':'role not found'}), 404
            
            response_data = {
                'role_id': role[0],
                'role_title': role[1],
            }

            cursor.close()
            return jsonify(response_data), 200
        

        if request.method == 'PUT':
            role = request.form.get('role_title')

            if not role:
                return jsonify({"message": "role field is required"}), 400
            
            cursor.execute('select * from roles where id = %s', (id,))
            row = cursor.fetchone()

            if row is None:
                return jsonify({'message':'role not found'}), 404
            
            try:
                role_title = role.lower()
                cursor.execute('select * from roles where title =%s', (role_title,))
                role_exists = cursor.fetchone()

                if role_exists:
                    role_id = role_exists[0]
                    title = role_exists[1]

                    if role_id == id:
                        response_data = {
                            'role_id': role_id,
                            'role_title': title,
                        }
                        return jsonify({"message": 'no changes', 'response_data': response_data}), 200
                    
                    return jsonify({"message": 'role with same title already exists',}), 400
                
                cursor.execute('update roles set title=%s where id=%s', (role_title, id,))
                cursor.connection.commit()

                cursor.execute('select * from roles where title=%s', (role_title,))
                get_role = cursor.fetchone()

                response_data = {
                    'role_id': get_role[0],
                    'role_title': get_role[1],
                }
                return jsonify({"message": 'successful', 'response_data': response_data}), 200

            except Exception as e:
                return jsonify({'error': str(e)}),500
            

        if request.method == 'DELETE':
            cursor.execute('select * from roles where id = %s', (id,))
            role = cursor.fetchone()

            if role is None:
                return jsonify({'message':'role not found'}), 404
            
            cursor.execute('delete from roles where id = %s', (id,))
            cursor.connection.commit()

            cursor.execute('select * from roles where id = %s', (id,))
            get_deleted_role = cursor.fetchone()

            if get_deleted_role is None:
                return jsonify({'message':'role deleted successfully'}), 200
            else:
                return jsonify({'message':"sorry, couldn't delete role. Try again..." }), 400


    except Exception as e:
        return jsonify({'error': str(e)}), 500