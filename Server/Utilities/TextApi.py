from twilio.rest import Client
from .Generator import id_generator
from .Config import Config
<<<<<<< HEAD
from Controllers.database import redis
=======
from Controllers.database import init_redis
>>>>>>> 6bdc1c2487f375e2b61a6a7a55ff22169b744dcc






class TextAPI:
    def __init__(self):
        self.client = Client(Config.default().twilio_account,Config.default().twilio_token)



    def begin_auth(self,phone_num):
        """
        initiate user authentication by generating token
        :return: token for user
        """
        token = id_generator(6)
        self.client.messages.create(to=str(phone_num),
                               from_="4433414409",
                               body="Thank you for signing up for Chatly. Your access token: {}".format(token))
        redis.set(phone_num, token,ex=900)
        return token



    def verify_auth(self,phone_num, token):
        """
        verifies auth token from user
        :param phone_num user number needs auth verified
        :param token token that user entered
        """

        if redis.get(phone_num) == token:
            return True
        return False


textApi = TextAPI()
