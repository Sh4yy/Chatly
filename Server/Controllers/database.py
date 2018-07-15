from mongoengine import connect
from Utilities.Config import Config
from redis import Redis
from flask_socketio import SocketIO

socketio = SocketIO()


def init_mongo():
    host = "mongodb://{}:{}@{}/{}".format(Config.default().db_user,
                                          Config.default().db_pass,
                                          Config.default().db_uri,
                                          Config.default().db_name)
    connect(Config.default().db_name, host=host)


redis = None


def init_redis():

    global redis
    redis = Redis(Config.default().redis_uri, 13010, password=Config.default().redis_password)
    return redis


init_redis()
