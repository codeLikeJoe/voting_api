from flask import Blueprint,request,jsonify,current_app

getUserId = Blueprint('getUsersBy_id', __name__)

@getUserId.route('/user/<int:id>', methods=['GET','PUT','DELETE'])
def getUsersBy_id(id):    
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    user = cursor.fetchone()

    if request.method == "GET":

        if user:
            user_dict = {
                'id': user[0],
                'firstname': user[1],
                'lastname': user[2],
                'student_id': user[3].upper(),
                'email': user[4],
                'program': user[5].capitalize(),
                'date_created': user[7],
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"message":"user not found"}), 404
        

    if request.method == "PUT":
        firstname = request.form['firstname'].capitalize()
        lastname = request.form['lastname'].capitalize()
        email = request.form['email'].lower()
        student_id = request.form['student_id'].upper()
        program_code = request.form['program_code'].lower()

        if user:
            try:
                # Check if all fields are filled
                if not all(field.strip() for field in (firstname, lastname, email, student_id, program_code)):
                    return jsonify({"message": "One or more fields are empty."}), 400
                
                # Check if program exists
                cursor.execute("SELECT * FROM programs WHERE code = %s", (program_code,))
                _programCode = cursor.fetchone()
                if not _programCode:
                    return jsonify({"message": "The program does not exist"}), 404
        

                program = _programCode[1]


                # Update user details
                cursor.execute("UPDATE students SET firstname = %s, lastname = %s, student_id = %s, email = %s, program = %s WHERE id = %s",
                            (firstname, lastname, student_id, email, program, id))
                mysql.connection.commit()

                return jsonify({"message": f"User with id({id}) details updated successfully."}), 200
            except Exception as e:
                return jsonify({"message": f"Sorry, an error occurred while updating user details. {str(e)}"}), 500
        else:
            return jsonify({"message": "user not found"}), 404    

    if request.method == 'DELETE':

        if user:
            try:
                cursor.execute("DELETE FROM students WHERE id = %s", (id,))
                mysql.connection.commit()
                return jsonify({"message": f"User with id({id}) deleted successfully"}), 200
            except Exception as e:
                return jsonify({"message": f"An error occurred while deleting user"}), 500
        else:
            return jsonify({"message": "user not found"}), 404