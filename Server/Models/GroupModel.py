from mongoengine import *
from Utilities.Generator import id_generator
from Models import User


class Group(Document):

    meta = {'indexes': [
        {{'fields': ['$username'],
          'default_language': 'english',
          'weights': {'title': 10}}
         }
    ]}

    id = StringField(primary_key=True)
    admin_id = StringField()
    title = StringField()
    username = StringField()
    members = ListField(StringField())

    def __init__(self, admin_id, title, username, *args, **kwargs):
        """
        initialize a new group chat
        :param admin_id: group's creator
        :param title: group's title
        :param username: group's username
        """
        super(Document).__init__(*args, **kwargs)
        self.id = "G{}".format(id_generator(9))
        self.admin_id = admin_id
        self.username = username.lower()
        self.members = list()
        self.title = title
        self.save()

    def make_json(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "username": self.username,
            "title": self.title,
            "members": [user.make_json() for user in self.get_users()]
        }

    def get_users(self):
        """
        get a list of member instances
        for this group
        :return: [User]
        """
        return User.objects.filter(id__in=self.members)

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

    @classmethod
    def find_username(cls, username):
        return cls.objects.search_text(username)

    def add_user(self, user):
        """
        append a new user to this group
        if user is already a member returns false
        :param user: user instance
        :return: true if successful
        """
        if self.has_user(user):
            return False
        self.members.append(user.id)
        return True

    def has_user(self, user):
        """
        checks to see if user is a member
        of this chat
        group chat
        :param user: user instance
        :return: true if user is a member of this
        """
        return user.id in self.members

    def remove_user(self, user):
        """
        removes the user from this group
        if user is a member
        :param user: user instance
        :return: true if successful
        """
        if not self.has_user(user):
            return False
        self.members.remove(user.id)
        return True

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id