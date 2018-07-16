from flask import Blueprint, request, abort
from Routes.RouteMethods import response, error_response, authorized
from Models import User, Group, Message
from schema import Schema, SchemaError, Optional
from Controllers.ChatController import ChatController


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


@mod.route('/group', methods=['POST'])
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

    users = User.find_username(username)
    groups = Group.find_username(username)
    if users or groups:
        return error_response('username has been already taken')

    group = Group.new(user.id, title, username)
    return response({'group': group.make_json()})


@mod.route('/group/<username>', methods=['GET'])
@authorized
def find_group(username, user, session):

    group = Group.find(username=username)
    if not group:
        abort(404)

    return response({'group': group.make_json()})


@mod.route('/user/<username>', methods=['GET'])
@authorized
def find_user(username, user, session):

    user = User.find(username=username)
    if not user:
        abort(404)
    return response({'user': user.make_json()})


@mod.route('/user/<username>/friend', methods=['POST'])
@authorized
def friend_user(username, user, session):

    friend = User.find(username=username)
    if not user:
        abort(404)

    if friend.is_blocked(user):
        return error_response('you have been blocked by user')

    user.friend(friend)
    return response({'added': True,
                     'friend': friend.make_json()})


@mod.route('/user/<username>/unfriend', methods=['POST'])
@authorized
def unfriend_user(username, user, session):

    friend = User.find(username=username)
    if not user:
        abort(404)

    if not user.is_friends(friend):
        return error_response('user is not a friend')

    user.unfriend(friend)
    return response({'unfriended': True})


@mod.route('/user/<username>/block', methods=['POST'])
@authorized
def block_user(username, user, session):

    target = User.find(username=username)
    if not user:
        abort(404)

    user.block(target)
    return response({'blocked': True})


@mod.route('/user/<username>/unblock', methods=['POST'])
@authorized
def unblock_user(username, user, session):

    target = User.find(username=username)
    if not user:
        abort(404)

    if not user.is_blocked(target):
        return error_response('user is not blocked')

    user.unblock(target)
    return response({'unblocked': True})


@mod.route('/group/<username>/join', methods=['POST'])
@authorized
def join_group(username, user, session):

    group = Group.find(username=username)
    if not group:
        abort(404)

    group.add_user(user)
    ChatController.user_joined_group(group, user)
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
    ChatController.user_left_group(group, user)
    return response({'joined': True,
                     'group': group.make_json()})


@mod.route('/my/groups', methods=['GET'])
@authorized
def get_my_groups(user, session):

    groups = Group.objects.filter(members=user.id)
    return response({'groups': [group.make_json() for group in groups]})


@mod.route('/my/updates', methods=['GET'])
@authorized
def get_my_updates(user, session):

    messages = Message.objects.filter(recipient_id=user.id)
    messages_data = [message.make_json() for message in messages]
    [message.delete() for message in messages]
    return response({'messages': messages_data})


@mod.route('/my/account', methods=['GET'])
@authorized
def get_my_account(user, session):
    return response({'user': user.make_json(True, True)})


@mod.route('/my/friends', methods=['GET'])
@authorized
def get_my_friends(user, session):

    users = User.objects.filter(id__in=user.friends)
    return response({'friends': [user.make_json() for user in users]})


@mod.route('/my/blocked', methods=['GET'])
@authorized
def get_my_blocked(user, session):

    users = User.objects.filter(id__in=user.blocked)
    return response({'blocked': [user.make_json() for user in users]})


@mod.route('/send/message', methods=['POST'])
@authorized
def send_message(user, session):

    json = request.json
    schema = Schema({'to': str, 'text': str})
    try:
        schema.validate(json)
    except SchemaError as err:
        return response(err.code)

    to = json['to']
    text = json['text']

    try:
        ChatController.new_msg(user.id, to, text)
    except Exception as err:
        return error_response(str(err))

    return response({'sent': True})
