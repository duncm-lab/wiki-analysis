#!/usr/bin/env python3
# pylint: disable=all
import unittest
from app.models import QueryObject, AnalysisObject, load_from_json


class TestQueryObject(unittest.TestCase):
    def test_constructor(self):
        """
        Test QueryObject can be instantiated
        """
        # TODO write description
        test = QueryObject(title='test', url_query='http://example.com')
        self.assertIsNotNone(test)

    def test_to_json(self):
        """
        Test QueryObject json property returns expected results
        """
        test = QueryObject(title='test', url_query='http://example.com')
        test_json = test.json
        self.assertIsInstance(test_json, str)
        self.assertEqual(test_json, '{"url_query": "http://example.com", "title": "test"}')

    def test_json_to_object(self):
        """
        Test a QueryObject can be instantiated from json
        """
        test = QueryObject(title='test', url_query='http://example.com')
        test_json = test.json
        obj = load_from_json(QueryObject, test_json)
        self.assertIsInstance(obj, QueryObject)


class TestAnalysisObject(unittest.TestCase):
    def test_constructor(self):
        """
        Test AnalysisObject class can be instantiated
        """
        test = AnalysisObject(title='test', info=['blue', 'orangutan', 'pope'])
        hasattr(test, 'info')
        hasattr(test, 'url_query')
        self.assertIsNotNone(test)

    def test_to_json(self):
        """
        Test AnalysisObject json property returns expected result
        """

        test = AnalysisObject(title='test', info=['blue', 'orangutan', 'pope'])
        test_json = test.json
        self.assertIsInstance(test_json, str)
        self.assertEqual(test_json, '{"title": "test", "info": ["blue", "orangutan", "pope"]}')

    def test_json_to_object(self):
        """
        Test an AnalysisObject can be instantiated from json
        """
        test = AnalysisObject(title='test', info=['blue', 'orangutan', 'pope'])
        test_json = test.json
        obj = load_from_json(AnalysisObject, test_json)
        self.assertIsInstance(obj, AnalysisObject)


if __name__ == '__main__':
    unittest.main()
