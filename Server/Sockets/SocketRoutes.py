from app import socketio
from flask import request
from flask_socketio import send
import Controllers.ChatController as Chat
from schema import Schema


@socketio.on('message')
def handle_message(json):

    schema = Schema({'to': str, 'text': str})
    if not schema.is_valid(json):
        return send('invalid query')
    user_id = Chat.ChatController.get_sid_id(request.sid)
    Chat.ChatController.new_msg(user_id, json['to'], json['text'])


@socketio.on('connect')
def handle_connect():
    token = request.args.get('token')
    return Chat.ChatController.user_joined(request.sid, token)


@socketio.on('disconnect')
def handle_disconnect():
    Chat.ChatController.user_left(request.sid)