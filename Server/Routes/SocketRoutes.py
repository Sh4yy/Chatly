from Controllers.database import socketio
from flask import request
from flask_socketio import send, emit
from time import sleep


@socketio.on('connect', namespace='/chat')
def test_connect():
    print(request.sid)
    print('new user')


@socketio.on('connect')
def test_connect():
    print(request.sid)
    print('new user1')