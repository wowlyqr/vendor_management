from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt,get_jwt_identity
from flask import g, jsonify, request
import jwt

from app.helpers.utils import create_response

def require_api_key(f):
    from flask import request
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get('X-API-KEY') != 'expected-key':
            return create_response(False,'Unauthorized',None,None,401)
        return f(*args, **kwargs)
    return decorated

def require_scope(required_scope):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'roles' not in claims or required_scope not in claims['roles']:
                return create_response(False,'Missing required scope',None,None,403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper 

def validate_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()

            g.current_user = get_jwt_identity()
            g.claims = get_jwt()
            return fn(*args, **kwargs)

        except Exception as e:
            raise e
           

    return wrapper