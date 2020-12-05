# pylint: disable=all
import unittest

import pickle
import tests.setup_data
from app.data_processing import valid_word, tag_words, filter_words
from app.database import list_len, get_index
from app.models import AnalysisObject, DbList

with open('ao.pickle', 'rb') as fl:
    test_ao = pickle.load(fl)


def data_setup():
    if list_len('analysis_objects0') in [None, 0]:
        tests.setup_data.main()


class TestDataProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        data_setup()

    def test_valid_word(self):
        """valid_word returns True for valid words and False for invalid"""
        x = valid_word(('functional', 'iterative', 'the', 'fortran', 'paul', 'safdasdas'))
        x.sort()
        self.assertEqual(['fortran', 'functional', 'iterative'], x)

    def test_tag_words(self):
        """tag_words takes an AnalysisObject and returns a new
        AnalysisObject with the words in the info attribute tagged"""
        tao = tag_words(test_ao)
        self.assertIsInstance(tao, AnalysisObject)

    def test_filter_words(self):
        """
        filter_words removes any non valid words from a tagged AnalysisObject
        """
        fao = filter_words(test_ao)
        words = [i[1] for i in fao.info]
        self.assertNotIn('ticketsingle', words)
        self.assertNotIn('and', words)


if __name__ == '__main__':
    unittest.main()
