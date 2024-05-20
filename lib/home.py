from flask import Blueprint, jsonify
from lib.Authentications.token.token_requirement import TokenRequirement

home = Blueprint('_home', __name__)
token_requirement = TokenRequirement(home)

@home.route('/', methods=['GET'])
@token_requirement.token_required
def index():
    return jsonify({'message': 'Welcome home'}), 200
