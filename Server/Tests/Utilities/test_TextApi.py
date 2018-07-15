import unittest
from Server.Utilities.TextApi import TextAPI



class TestTextApi(unittest.TestCase):

    def test_begin_auth(self):
        txt = TextAPI()
        token = txt.begin_auth(4436145125)

        self.assertEquals(txt.db.get(4436145125),token)



if __name__ == '__main__':
    unittest.main()