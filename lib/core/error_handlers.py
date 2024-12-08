from flask import jsonify

def method_not_allowed(error):
    return jsonify({'error': f"Method not allowed, {str(error)}"}), 405

def not_found(error):
    return jsonify({'error': f"This endpoint does not exist error, {str(error)}"}), 404
