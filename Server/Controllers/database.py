from mongoengine import connect
from Utilities.Config import Config


def init():
    host = "mongodb://{}:{}@{}/{}".format(Config.default().db_user,
                                          Config.default().db_pass,
                                          Config.default().db_uri,
                                          Config.default().db_name)
    connect(Config.default().db_name, host=host)
