from flask import Flask, Blueprint, request, abort, jsonify
from Utilities.TextApi import TextAPI
from Routes.RouteMethods import response, error_response, check_json
from Models import User, Session
from schema import Schema, Optional, SchemaError

mod = Blueprint('auth_routes', __name__)


@mod.route('/auth/verify/phone', methods=['POST'])
def verify_phone():
    """
    initialize a new phone verification
    """

    json = request.json
    if 'phone' not in json:
        abort(400)

    phone = json['phone']
    TextAPI.begin_auth(phone)
    return jsonify({'ok': True})


@mod.route('/auth/register', methods=['POST'])
def register():
    """
    verify user's phone number and
    authenticate with a new token
    :return:
    """

    json = request.json
    schema = Schema({"first_name": str, "username": str,
                     "token": str, "phone": str, Optional('last_name'): str},
                    ignore_extra_keys=True)
    try:
        schema.validate(request.json)
    except SchemaError as err:
        return response(err.code)

    last_name = None
    if 'last_name' in json:
        last_name = json['last_name']

    first_name = json['first_name']
    username = json['username']
    token = json['token']
    phone = json['phone']

    if not TextAPI.verify_auth(phone, token):
        return error_response('invalid phone authentication')

    user = User(first_name, last_name, username, phone)
    session = Session(user.id)
    return response({'user': user.make_json(),
                     'session': session.make_json()})


@mod.route('/auth/login', methods=['POST'])
def login():
    """
    verify user's phone number and login
    the user
    """
    json = request.json
    schema = Schema({"token": str, "phone": str},
                    ignore_extra_keys=True)
    try:
        schema.validate(request.json)
    except SchemaError as err:
        return response(err.code)

    token = json['token']
    phone = json['phone']

    if not TextAPI.verify_auth(phone, token):
        return error_response('invalid phone authentication')

    user = User.find(phone_num=phone)
    if not user:
        return error_response('user is not registered')

    session = Session(user.id)
    return response({'user': user.make_json(),
                     'session': session.make_json()})


@mod.route('/auth/logout', methods=['POST'])
def logout():
    """
    logout and delete a previous session token
    """

    auth = request.authorization
    if not auth:
        return error_response("missing authorization header")
    method, auth_token = auth.split()
    if method != 'bearer':
        return error_response('bad authorization method')

    session = Session.find(token=auth_token)
    if not session:
        return error_response('invalid auth token')

    session.delete()
    return response({'logged_out': True})
