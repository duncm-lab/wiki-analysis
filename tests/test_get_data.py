# pylint: disable=all
import unittest

from app.database import flush_redis
from app.get_data import (get_info, get_languages)
from app.models import QueryObject


class TestGetData(unittest.TestCase):

    def setUp(self) -> None:
        flush_redis()

    def test_get_languages(self):
        """
        A list of evenly (as possible) lists should be produced
        """
        test = get_languages()
        self.assertEqual(len(test[0]), 87)
        self.assertEqual(len(test[4]), 87)

    def test_get_languages_elem(self):
        test = get_languages()
        x = test[3][0]
        self.assertIsInstance(x, QueryObject)

    def test_get_info(self):
        """
        get_info should take a url and return the text data
        from the page
        """
        test = get_info('https://en.wikipedia.org/wiki/A_Sharp_(.NET)')
        self.assertIsInstance(test, str)

    def test_get_info_non_200_resp(self):
        """
        Test non 200 responses return 'invalid_response'
        """

        test = get_info('https://en.wedia.org/wiki/XA_Sharp_(.NET)')
        self.assertEqual(test, '')

    def tearDown(self) -> None:
        flush_redis()


if __name__ == '__main__':
    unittest.main()
