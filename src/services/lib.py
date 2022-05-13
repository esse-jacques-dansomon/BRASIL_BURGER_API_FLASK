from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from src.models.User import User


def getUser():
    user_id = get_jwt_identity()
    return User.query.filter_by(id=user_id).first()


# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator
def is_granted(role='Admin'):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = getUser()
            if claims.role == role:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg=f"{role} only!"), 403

        return decorator

    return wrapper


def make_slug(name):
    return name.lower().replace(' ', '-')



