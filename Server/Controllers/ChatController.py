

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
    def new_msg(cls, sender_sid, recipient_id, text):

        if is_group(recipient_id):
            pass

        elif is_user(recipient_id):
            pass

