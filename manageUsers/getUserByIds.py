from flask import Blueprint,request,jsonify,current_app
from datetime import datetime

getUserId = Blueprint('getUsersBy_id', __name__)

@getUserId.route('/user/<int:id>', methods=['GET','PUT','DELETE'])
def getUsersBy_id(id):
    bcrypt = current_app.extensions['bcrypt']
    
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
                'email': user[3],
                'dob': user[4],
                'age': user[5],
                'username': user[6],
                'verified?': user[8]
            }
            return jsonify(user_dict), 200
        else:
            return jsonify({"message":"user not found"}), 404
        

    if request.method == "PUT":
        _firstname = request.form['firstname'].capitalize()
        _lastname = request.form['lastname'].capitalize()
        _email = request.form['email']
        _dob = request.form['dob']
        _username = request.form['username']
        _password = request.form['password']

        if user:
            try:
                # Check if all fields are filled
                if not all(field.strip() for field in (_firstname, _lastname, _email, _username, _password, _dob)):
                    return jsonify({"message": "One or more fields are empty."}), 400
                else:
                    try:
                        dob = datetime.strptime(_dob, '%Y-%m-%d').date()
                    except ValueError:
                        return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400
                    if len(_password) < 6:
                        return jsonify({"message": "Password must be at least 6 characters long."}), 400
                    else:
                        hashed_password = bcrypt.generate_password_hash(_password).decode('utf-8')


                    today = datetime.now()
                    age = today.year - dob.year

                    if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
                        age -= 1

                    # Update user details
                    cursor.execute("UPDATE users SET firstname = %s, lastname = %s, email = %s, dob = %s, age = %s, username = %s, password = %s WHERE id = %s",
                                (_firstname, _lastname, _email, dob, age, _username, hashed_password, id))
                    mysql.connection.commit()
                    return jsonify({"message": f"User with id({id}) details updated successfully."}), 200
            except Exception as e:
                print("error: ", e)
                return jsonify({"message": f"Sorry, an error occurred while updating user details. {str(e)}"}), 500
        else:
            return jsonify({"message": "user not found"}), 404    

    if request.method == 'DELETE':

        if user:
            try:
                cursor.execute("DELETE FROM users WHERE id = %s", (id,))
                mysql.connection.commit()
                return jsonify({"message": f"User with id({id}) deleted successfully"}), 200
            except Exception as e:
                return jsonify({"message": f"An error occurred while deleting user"}), 500
        else:
            return jsonify({"message": "user not found"}), 404