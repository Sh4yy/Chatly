from Models import User, Group
from .database import redis


def is_group(id):
    """
    check to see whether
    an id is for a group
    :param id: id
    :return: true if is a group
    """
    return id.startswith('G')


def is_user(id):
    """
    check to see whether
    an id is for a user
    :param id: id
    :return: true if is a user
    """
    return id.startswith('U')


class ChatController:

    @classmethod
    def user_joined(cls, sid, token):
        """
        a new session has been created
        add user's sid to cache with their
        related chat id
        :param sid: socket's sid
        :param token: handshake's token
        """
        pass

    @classmethod
    def user_left(cls, sid):
        """
        a user has been disconnected
        from the server. delete its sid
        :param sid: socket's sid
        """
        pass

    @classmethod
    def get_user_sid(cls, user_id):
        """
        search for a user's socket id
        :param user_id: user's id
        :return: sid if exists, else None
        """
        pass

    @classmethod
    def get_sid_id(cls, sid):
        """
        get a user id using its sid
        user has to be joined
        :param sid: socket session id
        :return: user id if exists, else None
        """
        pass

    @classmethod
    def new_msg(cls, sender_id, recipient_id, text):

        sender = User.find(id=sender_id)
        sender_sid = cls.get_user_sid(sender.id)

        if is_group(recipient_id):
            recipient_group = Group.find(id=recipient_id)
            cls._broadcast_group(sender, sender_sid,
                                 recipient_group, text)

        elif is_user(recipient_id):
            recipient = User.find(id=recipient_id)
            cls._broadcast_user(sender, sender_sid, recipient,
                                text)

    @classmethod
    def _broadcast_group(cls, sender, sender_sid, group, text):
        """
        broadcast a new message to a group chat
        :param sender: sender's instance
        :param sender_sid: sender's socket id
        :param group: targeted group instance
        :param text: message text
        :return:
        """
        pass

    @classmethod
    def _broadcast_user(cls, sender, sender_sid, recipient, text, chat_id=None):
        """
        broadcast a new message to a user
        :param sender: sender's instance
        :param sender_sid: sender's socket session id
        :param recipient: recipient instance
        :param text: message's text
        :param chat_id: optional chat id if is in group
        :return:
        """
        pass
