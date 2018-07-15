from time import time
from flask import jsonify
import json


def response(data, code=200):
    return jsonify({
        "ok": True,
        "code": code,
        "timestamp": time(),
        "response": json.dumps(data)
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
