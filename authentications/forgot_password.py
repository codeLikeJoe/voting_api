from flask import Blueprint, request, jsonify,current_app, session

forgot_password = Blueprint('_forgot_password', __name__)

@forgot_password.route('/forgot_password', methods=['POST'])
def forgot_password():
    return jsonify({"message": "forgot password"}), 200