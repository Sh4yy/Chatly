from mongoengine import connect
from Utilities.Config import Config
from redis import Redis


def init_mongo():
    host = "mongodb://{}:{}@{}/{}".format(Config.default().db_user,
                                          Config.default().db_pass,
                                          Config.default().db_uri,
                                          Config.default().db_name)
    connect(Config.default().db_name, host=host)


redis = None


def init_redis():

    global redis
    redis = Redis(Config.default().redis_uri)
    return redis

init_redis()
