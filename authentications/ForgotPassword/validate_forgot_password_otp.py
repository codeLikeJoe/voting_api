from flask import Blueprint, request, jsonify,current_app, session

validate_reset_password_otp = Blueprint('_reset_password_otp', __name__)

@validate_reset_password_otp.route('/reset_password_otp', methods=['POST'])
def index():
    try:
        user_otp = request.form['otp']

        otp = session.get('forgot_password_otp')
        email = session.get('forgot_password_email')

        if email:
            if otp == int(user_otp):
                # if current_time < otp_expiry:
                    session['reset password'] = True
                    session['email'] = email
                    return jsonify({"message": "verified successfully"}), 200
                # else:
                #     return jsonify({"message": "OTP has expired!"})
            return jsonify({"message": "Invalid OTP. Please try again."}), 400
        else:
            return jsonify({"message": "Verification failed"}), 400
    
    except Exception as e:
        return jsonify({"message": f"Error {str(e)}"}), 400