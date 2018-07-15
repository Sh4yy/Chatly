from mongoengine import *
from Utilities.Generator import id_generator
from time import time


class Session(Document):
    token = StringField(primary_key=True)
    user_id = StringField()
    created_date = FloatField()
    ip = StringField()

    def __init__(self, user_id, ip=None, *args, **kwargs):
        """
        initialize a new authentication
        session for a user
        :param user_id: user's id
        :param ip: user's ip (optional)
        """
        super(Document, self).__init__(*args, **kwargs)
        self.token = "{}:{}".format(user_id, id_generator(10))
        self.user_id = user_id
        self.created_date = time()
        self.ip = ip
        self.save()

    def make_json(self):
        return {
            "token": self.token,
            "user_id": self.user_id,
            "created_date": self.created_date
        }

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

    def __eq__(self, other):
        return self.token == other.token

    def __ne__(self, other):
        return self.token != other.token


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
    username = StringField(unique=True)
    phone_num = StringField(unique=True)

    def __init__(self, first_name, last_name, username,
                 phone_num, *args, **kwargs):
        """
        initialize a new user
        :param first_name: user's first name
        :param last_name: user's last name (optional)
        :param username: user's username
        :param phone_num: user's phone number
        """
        super(Document, self).__init__(*args, **kwargs)
        self.id = "U{}".format(id_generator(9))
        self.first_name = first_name
        self.last_name = last_name
        self.username = username.lower()
        self.phone_num = phone_num
        self.save()

    def make_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username
        }

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

    @classmethod
    def find_username(cls, username):
        return cls.objects.search_text(username)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

