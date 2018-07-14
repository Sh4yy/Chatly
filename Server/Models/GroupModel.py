from mongoengine import *
from Utilities.Generator import id_generator


class Group(Document):
    id = StringField(primary_key=True)
    admin_id = StringField()
    username = StringField()
    members = ListField(StringField())

    def __init__(self, admin_id, username, *args, **kwargs):
        super(Document).__init__(*args, **kwargs)
        self.id = "G{}".format(id_generator(9))
        self.admin_id = admin_id
        self.username = username.lower()
        self.members = list()
        self.save()

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

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
