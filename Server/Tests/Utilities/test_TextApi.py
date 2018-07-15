import unittest

from Controllers.database import redis
from Utilities.TextAPI import TextAPI



class TestTextApi(unittest.TestCase):

    def test_begin_auth(self):
        txt = TextAPI()
        token = txt.begin_auth(4436145125)

        self.assertEquals(redis.get(4436145125),token)




if __name__ == '__main__':
    unittest.main()