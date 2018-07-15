from Models import User, Group, Session, Message
from .database import redis
from time import time
from main import socketio


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
        session = Session.find(token=token)
        redis.hset('sid-id', sid, session.user_id)
        redis.hset('id-sid', session.user_id, sid)
        return session.user_id

    @classmethod
    def user_left(cls, sid):
        """
        a user has been disconnected
        from the server. delete its sid
        :param sid: socket's sid
        """
        id = redis.hget('sid-id', sid)
        redis.hdel('sid-id', sid)
        redis.hdel('id-sid', id)
        return id

    @classmethod
    def get_user_sid(cls, user_id):
        """
        search for a user's socket id
        :param user_id: user's id
        :return: sid if exists, else None
        """
        return redis.hget('id-sid', user_id)

    @classmethod
    def get_sid_id(cls, sid):
        """
        get a user id using its sid
        user has to be joined
        :param sid: socket session id
        :return: user id if exists, else None
        """
        return redis.hget('sid-id', sid)

    @classmethod
    def new_msg(cls, sender_id, recipient_id, text):
        """
        when a user sends a new message to the server
        :param sender_id: sender's id
        :param recipient_id: recipient (group/user) id
        :param text: message's text
        :return:
        """

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
        # todo make this method async
        """
        broadcast a new message to a group chat
        :param sender: sender's instance
        :param sender_sid: sender's socket id
        :param group: targeted group instance
        :param text: message text
        :return:
        """
        for recipient in group.get_users():
            cls._broadcast_user(sender, sender_sid, recipient, text, chat_id=group.id)

    @classmethod
    def _broadcast_user(cls, sender, sender_sid, recipient, text, chat_id=None):
        # todo make this method async
        """
        broadcast a new message to a user
        :param sender: sender's instance
        :param sender_sid: sender's socket session id
        :param recipient: recipient instance
        :param text: message's text
        :param chat_id: optional chat id if is in group
        :return:
        """
        recipient_sid = cls.get_user_sid(recipient.id)
        if not recipient_sid:
            cls._cache_msg(sender.id, recipient.id, text, chat_id)
            return
        data = {'sender_id': sender.id, 'recipient_id': recipient.id,
                'text': text, 'chat_id': chat_id or 'private', 'time': time()}
        socketio.send(data=data, json=True, namespace='/chat', room=recipient_sid)

    @classmethod
    def _cache_msg(cls, sender_id, recipient_id, text, chat_id=None):
        # todo make this method async
        """
        cache a message that failed to be delivered
        :param sender_id: sender's object id
        :param recipient_id: recipient's object id
        :param text: message's text
        :param chat_id: chat id if in group
        :return:
        """
        message = Message(sender_id, recipient_id, text, chat_id)
        return message