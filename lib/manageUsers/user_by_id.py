from flask import Blueprint,request,jsonify,current_app

getUserId = Blueprint('getUsersBy_id', __name__)

@getUserId.route('/api/v1/user/<int:id>', methods=['GET','PUT','DELETE'])
def getUsersBy_id(id):    
    mysql = current_app.extensions['mysql']
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()

    if request.method == "GET":

        if user:
            user_dict = {
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
            return jsonify(user_dict), 200
        else:
            return jsonify({"message":"user not found"}), 404
        

    if request.method == "PUT":

        raw_data = request.get_json()

        if not raw_data:
            return jsonify({"Error": "No data provided"}), 400

        firstname = raw_data.get('firstname').lower()
        lastname = raw_data.get('lastname').lower()
        email = raw_data.get('email')
        student_id = raw_data.get('student_id').lower()
        program_code = raw_data.get('program_code').lower()
        year_of_admission = raw_data.get('year_of_admission')
        year_of_completion = raw_data.get('year_of_completion')

        if user:
            try:
                # Check if all fields are filled
                if not all(field.strip() for field in 
                           (firstname, lastname, email, student_id, program_code, 
                            year_of_admission, year_of_completion)):
                    return jsonify({"error": "all fields are required"}), 403
                
                # Check if program exists
                cursor.execute("SELECT * FROM program WHERE program_code = %s", (program_code,))
                _programCode = cursor.fetchone()

                if not _programCode:
                    return jsonify({"message": "the program does not exist"}), 404
        
                program_id = _programCode[0]
                program_title = _programCode[1]

                # Check if program exists
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                _user = cursor.fetchone()

                _email = _user[4]
                _user_id = _user[0]

                if not _email:
                    pass

                if _user_id != id:
                    return jsonify({"message": "email already exist"}), 403


                # Update user details
                cursor.execute("""UPDATE users SET first_name = %s, last_name = %s, student_id = %s, email = %s, 
                               program_id = %s, program_title = %s, year_of_admission = %s, year_of_completion = %s 
                               WHERE id = %s""",
                            (firstname, lastname, student_id, email, program_id, program_title, 
                             year_of_admission, year_of_completion, id))
                mysql.connection.commit()

                return jsonify({"message": f"user with id({id}) details updated successfully."}), 200
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