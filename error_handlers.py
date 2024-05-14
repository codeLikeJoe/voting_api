from flask import jsonify

def method_not_allowed(error):
    return jsonify({'Error': 'Method not allowed'}), 405

def not_found(error):
    return jsonify({'message': 'This endpoint does not exist', 'error': f'{str(error)}'}), 404
