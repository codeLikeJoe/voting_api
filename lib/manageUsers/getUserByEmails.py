from flask import Blueprint,request,jsonify,current_app

getUserEmail = Blueprint('getUsersBy_email', __name__)

@getUserEmail.route('/user/<string:student_id>', methods=['GET','PUT','DELETE'])
def getUsersBy_id(student_id):
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
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
        _student_id = request.form['student_id'].upper()
        program_code = request.form['program_code'].lower()

        if user:
            try:
                # Check if all fields are filled
                if not all(field.strip() for field in (firstname, lastname, email, _student_id, program_code)):
                    return jsonify({"message": "One or more fields are empty."}), 400
                
                # Check if program exists
                cursor.execute("SELECT * FROM programs WHERE code = %s", (program_code,))
                _programCode = cursor.fetchone()
                if not _programCode:
                    return jsonify({"message": "The program does not exist"}), 404
        

                program = _programCode[1]


                # Update user details
                cursor.execute("UPDATE students SET firstname = %s, lastname = %s, student_id = %s, email = %s, program = %s WHERE student_id = %s",
                            (firstname, lastname, _student_id, email, program, student_id))
                mysql.connection.commit()

                return jsonify({"message": f"User details updated successfully."}), 200
            except Exception as e:
                return jsonify({"message": f"Sorry, an error occurred while updating user details. {str(e)}"}), 500
        else:
            return jsonify({"message": "user not found"}), 404    

    if request.method == 'DELETE':

        if user:
            try:
                cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
                mysql.connection.commit()
                return jsonify({"message": f"User with id({student_id}) deleted successfully"}), 200
            except Exception as e:
                return jsonify({"message": f"An error occurred while deleting user"}), 500
        else:
            return jsonify({"message": "user not found"}), 404