from flask import Blueprint, request, jsonify,current_app, session
from lib.core.token_requirement import TokenRequirement

apply_position = Blueprint('_apply_position', __name__)
token_requirement = TokenRequirement(apply_position)

@apply_position.route('/apply_for_position', methods=['POST'])
@token_requirement.token_required
def index():
    return jsonify({"message":"Apply for a position"})