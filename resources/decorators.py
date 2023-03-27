from functools import wraps
from flask import abort, request
import jwt, hashlib
from models import UserModel
from passlib.hash import pbkdf2_sha256

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        auth = request.authorization
        if not auth:
                abort(401)
        user_id = auth.get("username")
        print("user id", user_id)
        password = pbkdf2_sha256.hash(str(auth.get("password")))
        user = None
        try:
            user = UserModel.find_by_id(user_id)
            print(user.password)
            print(password)
            if not pbkdf2_sha256.verify(auth.get("password"), user.password):
                print("ko match")
                abort(401)
            else:
                print(user.email)
        except:
            abort(401)
        return f(*args, **kws)
    return decorated_function

