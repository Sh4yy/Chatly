from app import socketio
from flask import request
from flask_socketio import send, emit
from time import sleep
import Controllers.ChatController as Chat
from schema import Schema


@socketio.on('message')
def handle_message(json):

    print("Received {}".format(json))
    emit("echo", str(json))

    schema = Schema({'to': str, 'text': str})
    if not schema.is_valid(json):
        return send('invalid query')
    user_id = Chat.ChatController.get_sid_id(request.sid)
    Chat.ChatController.new_msg(user_id, json['to'], json['text'])


@socketio.on('connect')
def handle_connect():
    print('user joined')
    token = request.args.get('token')
    return Chat.ChatController.user_joined(request.sid, token)


@socketio.on('disconnect')
def handle_disconnect():
    print('user left')
    Chat.ChatController.user_left(request.sid)