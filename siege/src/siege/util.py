from flask import request, jsonify
from functools import wraps

def require_json(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
          return jsonify('Content Type is not json'), 400
        return func(*args, **kwargs)
    return decorated_function

