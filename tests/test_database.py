# pylint: disable=all
import unittest
import redis
from app.models import AnalysisObject, QueryObject
from app.database import RedisContext, push_object, pop_object, get_index, flush_redis, list_len
import tests.setup_data


def data_setup():
    if list_len('analysis_objects0') in [None, 0]:
        tests.setup_data.main()


class TestDatabase(unittest.TestCase):

    def test_db_connection(self):
        """
        Test a connection can be made to redis
        """
        with RedisContext() as r:
            self.assertEqual(type(r), redis.Redis)

    def test_push_query_object(self):
        """
        Test QueryObjects can be pushed to a redis list
        """
        flush_redis()
        qo = QueryObject(title='test', url_query='https://www.example.com')
        push_object(qo, 'query_objects')
        with RedisContext() as r:
            self.assertEqual(r.llen('query_objects'), 1)

    def test_push_analysis_object(self):
        """
        Test AnalysisObjects can be pushed to a redis list
        """
        flush_redis()
        ao = AnalysisObject(title='test', info=['foo', 'bar', 'baz'])
        push_object(ao, 'analysis_objects0')
        with RedisContext() as r:
            self.assertEqual(r.llen('analysis_objects0'), 1)

    def test_pop_query_object(self):
        """
        Test a json object can be popped from the list and instantiated
        as a QueryObject
        """
        qo = QueryObject(title='test', url_query='https://www.example.com')
        push_object(qo, 'query_objects')
        pop_qo = pop_object(QueryObject, 'query_objects')
        self.assertIsInstance(pop_qo, QueryObject)
        self.assertEqual(pop_qo.url_query, 'https://www.example.com')

    def test_pop_analysis_object(self):
        """
        Test a json object can be popped from the list and instantiated
        as an AnalysisObject
        """
        ao = AnalysisObject(title='test', info=['foo', 'bar', 'baz'])
        push_object(ao, 'analysis_objects0')
        pop_ao = pop_object(AnalysisObject, 'analysis_objects0')
        self.assertIsInstance(pop_ao, AnalysisObject)
        self.assertEqual(pop_ao.info, ['foo', 'bar', 'baz'])


if __name__ == '__main__':
    unittest.main()
