from flask import Blueprint, request, jsonify,current_app, session
from datetime import datetime, timedelta

validate_otp = Blueprint('_validate_otp', __name__)

@validate_otp.route('/validate', methods=['POST'])
def validate():

    try:
        user_otp = request.form['otp']

        stored_otp = session.get('otp')
        stored_email = session.get('email')
        otp_expiry = session.get('otp_expiry')
        current_time = datetime.now().timestamp() * 1000

        if stored_email:
            if stored_otp == int(user_otp):
                if current_time < otp_expiry:
                    mysql = current_app.extensions['mysql']
                    cursor = mysql.connection.cursor()

                    # Update user details
                    cursor.execute("UPDATE users SET verified = %s WHERE email = %s",
                                ('Yes', stored_email))
                    mysql.connection.commit()

                    return jsonify({"status": "successful", 
                                    "message":f"{stored_email} has been verified"}), 200
                else:
                    return jsonify({"message": "sorry, the OTP code has expired!"}), 400
            return jsonify({"message": "Invalid OTP. Please try again."}), 400
        else:
            return jsonify({"message": "Verification failed"}), 400
    
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"})
