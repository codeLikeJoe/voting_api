from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime, timedelta
from lib.Authentications.token.token_requirement import TokenRequirement

change_password = Blueprint('_change_password', __name__)
token_requirement = TokenRequirement(change_password)

@change_password.route('/change_password', methods=['POST'])
@token_requirement.token_required
def index():
    mysql = current_app.extensions['mysql']
    bcrypt = current_app.extensions['bcrypt']
    
    try:
        received_otp = request.form['otp']

        email = session.get('forgot_password_email')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM srtauthwq WHERE email=%s", (email,))
        user = cursor.fetchone()

        # otp = session.get('forgot_password_otp')
        # otp_expiry = session.get('otp_expiry')

        hashed_otp_from_db = user[3]
        otp_expiry = user[4]
        current_time = datetime.now().timestamp() * 1000

        # if email:
        #     if bcrypt.check_password_hash(hashed_otp_from_db, received_otp):
        #         if current_time < float(otp_expiry):
        #             session['reset password'] = True
        #             session['email'] = email
        #             return jsonify({"message": "verified successfully"}), 200
        #         else:
        #             return jsonify({"message": "sorry, the OTP code has expired!"}), 400
        #     return jsonify({"message": "Invalid OTP. Please try again."}), 400
        # else:
        #     return jsonify({"message": "Verification failed"}), 400
    
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 400