from flask_socketio import SocketIO
from flask import Flask
from Routes import AuthRoutes
from Routes import ChatRoutes

socketio = SocketIO()


def create_app(debug=False):

    app = Flask(__name__)
    app.debug = debug
    app.register_blueprint(AuthRoutes.mod)
    app.register_blueprint(ChatRoutes.mod)

    socketio.init_app(app)
    return app
