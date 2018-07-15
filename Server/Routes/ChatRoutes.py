from flask import Blueprint, request, abort, jsonify
from Utilities.TextApi import TextAPI
from Routes.RouteMethods import response, error_response, authorized
from Models import User, Session, Group
from schema import Schema, Optional, SchemaError


mod = Blueprint('chat_routes', __name__)


@mod.route('/search/username/<username>', methods=['GET'])
@authorized
def search_username(username, user, session):

    users = User.find_username(username)
    groups = Group.find_username(username)

    return response({'groups': [group.make_json(include_members=False) for group in groups],
                     'users': [user.make_json() for user in users]})


@mod.route('/search/username/<username>/available', methods=['GET'])
@authorized
def username_available(username, user, session):

    users = User.find_username(username)
    groups = Group.find_username(username)

    available = not users and not groups
    return response({'username': username, 'available': available})


@mod.route('/group', methods=['CREATE'])
@authorized
def create_group(user, session):

    json = request.json
    schema = Schema({'title': str, 'username': str})
    try:
        schema.validate(json)
    except SchemaError as err:
        return response(err.code)

    title = json['title']
    username = json['username']

    group = Group.new(user.id, title, username)
    return response({'group': group.make_json()})


@mod.route('/group/<username>', methods=['GET'])
@authorized
def find_group(username, user, session):

    group = Group.find(username=username)
    if not group:
        abort(404)

    return response({'group': group.make_json()})


@mod.route('/group/<username>/join', methods=['POST'])
@authorized
def join_group(username, user, session):

    group = Group.find(username=username)
    if not group:
        abort(404)

    group.add_user(user)
    return response({'joined': True,
                     'group': group.make_json()})


@mod.route('/group/<username>/leave', methods=['POST'])
@authorized
def leave_group(username, user, session):

    group = Group.find(username=username)
    if not group:
        abort(404)

    if not group.has_user(user):
        return error_response('you are not a member of this group')

    group.remove_user(user)
    return response({'joined': True,
                     'group': group.make_json()})

