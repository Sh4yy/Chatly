import gevent.monkey;  gevent.monkey.patch_all()
from app import socketio, create_app
from Controllers import database
import Sockets

app = create_app(debug=True)


if __name__ == '__main__':
    database.init_mongo()
    socketio.run(app, port=8080, debug=True)
