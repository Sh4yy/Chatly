import gevent.monkey; gevent.monkey.patch_all()
from flask import Flask
from flask_socketio import SocketIO
from Routes import AuthRoutes
from Routes.ChatRoutes import mod as ChatRouteMod
from Controllers import database


app = Flask(__name__)
app.register_blueprint(AuthRoutes.mod)
app.register_blueprint(ChatRouteMod)
database.socketio = SocketIO(app)

if __name__ == '__main__':
    database.init_mongo()
    database.socketio.run(app, debug=True, port=8080)
