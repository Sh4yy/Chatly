from mongoengine import *
from time import time
from Utilities.Generator import id_generator


class Message(Document):
    id = StringField(primary_key=True)
    sender_id = StringField()
    text = StringField()
    recipient_id = StringField()
    chat_id = StringField()
    created_date = FloatField()

    @classmethod
    def new(cls, sender_id, recipient_id, text,
            chat_id=None):
        """
        initialize a new cached message
        :param sender_id: sender's user id
        :param recipient_id: recipient's id
        :param text: message's text
        :param chat_id: optional chat id if in group
        """
        temp = cls()
        temp.id = "M{}".format(id_generator(9))
        temp.sender_id = sender_id
        temp.recipient_id = recipient_id
        temp.text = text
        temp.created_date = time()
        temp.chat_id = chat_id
        temp.save()
        return temp

    def make_json(self):
        return {
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "created_date": self.created_date,
            "text": self.text,
            "chat_id": self.chat_id or 'private'
        }

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

    @classmethod
    def find_recipient(cls, user):
        return cls.objects.filter(recipient_id=user.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id