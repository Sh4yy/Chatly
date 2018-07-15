from time import time
from flask import jsonify, request, abort
from functools import wraps
from Models import User, Session


def response(data, code=200):
    return jsonify({
        "ok": True,
        "code": code,
        "timestamp": time(),
        "response": data
    })


def error_response(msg, code=400):
    return jsonify({
        "ok": False,
        "code": code,
        "timestamp": time(),
        "message": msg
    })


def check_json(data, keys):
    for key in keys:
        if key not in data:
            return key
    return None


def authorized(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            abort(401)
        method, token = auth.split()
        if method != 'bearer' or not token:
            abort(401)

        session = Session.find(token=token)
        if not session:
            abort(401)

        user = User.find(id=session.user_id)
        return func(user=user, session=session, *args, **kwargs)

    return wrapper

