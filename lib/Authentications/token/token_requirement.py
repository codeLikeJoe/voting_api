from flask import request, jsonify, current_app
import jwt
from functools import wraps

class TokenRequirement:
    def __init__(self, blueprint):
        self.blueprint = blueprint

    def token_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.args.get('token')

            if not token:
                return jsonify({'message':'Authentication required'}), 401
            
            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 400
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 403
            
            return f(*args, **kwargs)
        return decorated