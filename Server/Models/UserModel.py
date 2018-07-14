from mongoengine import *
from Utilities.Generator import id_generator
from time import time


class Session(Document):
    token = StringField(primary_key=True)
    user_id = StringField()
    created_date = FloatField()
    ip = StringField()

    def __init__(self, user_id, ip=None, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.token = "{}:{}".format(user_id, id_generator(10))
        self.user_id = user_id
        self.created_date = time()
        self.ip = ip
        self.save()

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()


class User(Document):

    meta = {'indexes': [
        {{'fields': ['$username'],
          'default_language': 'english',
          'weights': {'title': 10}}
         }
    ]}

    id = StringField(primary_key=True)
    first_name = StringField()
    last_name = StringField()
    username = StringField()
    phone_num = StringField()

    def __init__(self, first_name, last_name, username, phone_num, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.id = "U{}".format(id_generator(9))
        self.first_name = first_name
        self.last_name = last_name
        self.username = username.lower()
        self.phone_num = phone_num
        self.save()

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

    @classmethod
    def find_username(cls, username):
        return cls.objects.search_text(username)

