import unittest
<<<<<<< HEAD

from Controllers.database import redis
from Utilities.TextAPI import TextAPI
=======
from Utilities.TextApi import TextAPI
>>>>>>> 6bdc1c2487f375e2b61a6a7a55ff22169b744dcc



class TestTextApi(unittest.TestCase):

    def test_begin_auth(self):
        txt = TextAPI()
        token = txt.begin_auth(4436145125)

        self.assertEquals(redis.get(4436145125),token)




if __name__ == '__main__':
    unittest.main()