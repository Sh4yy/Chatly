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

    def __init__(self, sender_id, recipient_id, text,
                 chat_id=None, *args, **kwargs):
        """
        initialize a new cached message
        :param sender_id: sender's user id
        :param recipient_id: recipient's id
        :param text: message's text
        :param chat_id: optional chat id if in group
        """
        super(Document).__init__(*args, **kwargs)
        self.id = "M{}".format(id_generator(9))
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.text = text
        self.created_date = time()
        self.chat_id = chat_id
        self.save()

    def make_json(self):
        return {
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "created_date": self.created_date,
            "chat_id": self.chat_id or 'private'
        }

    @classmethod
    def find(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs).first()

    @classmethod
    def find_recipient(cls, user):
        return cls.objects.filter(recipient_id=user.id)
