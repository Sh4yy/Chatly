from twilio.rest import Client
from .Generator import id_generator
from .Config import Config
from Server.Controllers.database import init_redis






class TextAPI:
    def __init__(self):
        self.client = Client(Config.default().twilio_account,Config.default().twilio_token)
        self.db = init_redis()


    def begin_auth(self,phone_num):
        """
        initiate user authentication by generating token
        :return:
        """
        token = id_generator(6)
        self.client.messages.create(to=str(phone_num),
                               from_="3232-232",
                               body="Thank you for signing up for Chatly. Your access token: {}".format(token))
        self.db.set(phone_num, token,ex=900)
        return token



    def verify_auth(self,phone_num, token):
        """
        verifies auth token from user
        :param phone_num
        :param token:
        """

        if self.db.get(phone_num) == token:
            return True
        return False


