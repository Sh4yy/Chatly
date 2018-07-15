from flask import Blueprint, request, abort, jsonify
from Utilities.TextApi import TextAPI
from Routes.RouteMethods import response, error_response, authorized
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
    user = User.find(phone_num=phone)

    return jsonify({'ok': True, 'signed_up': user is not None})


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

    if User.find(username=username):
        return error_response("username already exists")

    if not TextAPI.verify_auth(phone, token):
        return error_response('invalid phone authentication')

    user = User.new(first_name, last_name, username, phone)
    session = Session.new(user.id)
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

    session = Session.new(user.id)
    return response({'user': user.make_json(),
                     'session': session.make_json()})


@mod.route('/auth/logout', methods=['POST'])
@authorized
def logout(user, session):
    """
    logout and delete a previous session token
    """

    session.delete()
    return response({'logged_out': True})
