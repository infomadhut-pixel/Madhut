from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required,get_jwt

def check_role(*role_required):
    def decorator(role):
        @wraps(role)
        @jwt_required(locations=['headers'])
        def decorated_functions(*args,**kwargs):
            authorize=get_jwt()
            if authorize['role'] not in role_required:
                return jsonify({'message':'access denied'})
            return role(*args,**kwargs)
        return decorated_functions
    return decorator




