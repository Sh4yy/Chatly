from mongoengine import *
from Utilities.Generator import id_generator
from time import time
import re


class Session(Document):
    token = StringField(primary_key=True)
    user_id = StringField()
    created_date = FloatField()
    ip = StringField()

    @classmethod
    def new(cls, user_id, ip=None):
        """
        initialize a new authentication
        session for a user
        :param user_id: user's id
        :param ip: user's ip (optional)
        """
        temp = cls()
        temp.token = "{}:{}".format(user_id, id_generator(10))
        temp.user_id = user_id
        temp.created_date = time()
        temp.ip = ip
        temp.save()
        return temp

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
    id = StringField(primary_key=True)
    first_name = StringField()
    last_name = StringField()
    username = StringField(unique=True)
    phone_num = StringField(unique=True)
    friends = ListField(StringField())
    blocked = ListField(StringField())

    @classmethod
    def new(cls, first_name, last_name, username,
            phone_num):
        """
        initialize a new user
        :param first_name: user's first name
        :param last_name: user's last name (optional)
        :param username: user's username
        :param phone_num: user's phone number
        """
        temp = cls()
        temp.id = "U{}".format(id_generator(9))
        temp.first_name = first_name
        temp.last_name = last_name
        temp.username = username.lower()
        temp.phone_num = phone_num
        temp.friends = []
        temp.save()
        return temp

    def make_json(self, include_friends=False, include_blocked=False):
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username
        }

        if include_friends:
            users = User.objects.filter(id__in=self.friends)
            data['friends'] = [user.make_json() for user in users]

        if include_blocked:
            users = User.objects.filter(id__in=self.blocked)
            data['blocked'] = [user.make_json() for user in users]

        return data

    def friend(self, user):
        """
        add a new friend to user's friends
        :param user: user instance
        :return: True on success
        """
        if self.is_friends(user):
            return True

        if self.is_blocked(user):
            self.unblock(user)

        self.friends.append(user.id)
        self.save()
        return True

    def unfriend(self, user):
        """
        unfriend a user
        :param user: user's instance
        :return: True on success
        """
        if not self.is_friends(user):
            return False

        self.friends.remove(user.id)
        self.save()
        return True

    def is_friends(self, user):
        """
        check to see whether a user
        is already in this user's friends
        :param user: user's instance
        :return: True if friends
        """
        return user.id in self.friends

    def block(self, user):
        """
        block a user
        :param user: user's instance
        :return: True on success
        """
        if self.is_blocked(user):
            return True

        if self.is_friends(user):
            self.unfriend(user)

        self.blocked.append(user.id)
        self.save()
        return True

    def unblock(self, user):
        """
        unblock a user
        :param user: user's instance
        :return: True if user was unblocked
        """
        if not self.is_blocked(user):
            return False

        self.blocked.remove(user.id)
        self.save()
        return True

    def is_blocked(self, user):
        """
        check to see if user has blocked
        another user
        :param user: user instance
        :return: True if blocked
        """
        return user.id in self.blocked

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

    @classmethod
    def find_username(cls, username):
        username_re = re.compile('.*{}.*'.format(username))
        return cls.objects.filter(username=username_re)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

