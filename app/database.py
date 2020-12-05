"""
Connections and context managers for Redis and SQLITE DB
"""
import json
import os
import sqlite3
from random import randint
from string import ascii_lowercase
from typing import Any

import redis

from app.config_loader import load_config, path
from app.models import DbList
from app.project_logging import logger


redis_config = load_config('databases')['redis']

word_db = sqlite3.connect(os.path.join(path, load_config('databases')['word_lookup']),
                          check_same_thread=False)


class RedisContext:
    """
    Create a connection to redis then close when finished
    """
    def __init__(self):
        pass

    def __enter__(self):
        """

        :return: redis connection
        :rtype: redis.Redis
        :raises ConnectionError:
        """
        try:
            self.r = redis.Redis(host=redis_config['host'],
                                 port=redis_config['port'],
                                 decode_responses=True)
        except ConnectionError as e:
            logger.error(e)
            raise e
        return self.r

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.r.close()


class TempTable:
    """
    A context manager for temporary lookup tables.

    On enter a unique table is created containing the words provided in the constructor
    word_list argument. On exit, the temporary table is deleted. This is intended for
    use with multiprocessing whereby multiple processes could be doing validation at
    the same time and we want to isolate them.

    :param word_list: A list of words to be validated.
    :type word_list: list
    """

    def __init__(self, word_list):
        suffix = ''.join([ascii_lowercase[randint(0, len(ascii_lowercase) - 1)]
                          for _ in range(5)])
        self.word_list = word_list
        self.table_name = 'temp_words' + suffix

    def __enter__(self):
        """
        :return: name of temp table
        :rtype: str
        """
        query = f'create table {self.table_name} (word text);'
        with word_db:
            cur = word_db.cursor()
            cur.execute(query)
            for i in self.word_list:
                cur.execute('insert into ' + self.table_name + ' values (?)', (i,))
        return self.table_name

    def __exit__(self, exc_type, exc_value, exc_traceback):
        query = f'drop table if exists {self.table_name}'
        with word_db:
            cur = word_db.cursor()
            cur.execute(query)


def flush_redis() -> None:
    """
    clear all data from redis
    """
    with RedisContext() as r:
        r.flushall()


def check_list(list_name: str) -> bool:
    """
    Check the specified list name is valid.

    :param list_name: name of list to check
    :return:
    """
    if getattr(DbList, list_name):
        return True


def list_len(list_name: str) -> int:
    """
    Return the count of items in a list
    :param list_name: Name of list to check
    :return:
    """
    if check_list(list_name):
        with RedisContext() as r:
            return r.llen(list_name)


def push_object(model: Any, list_name: str) -> None:
    """
    Insert object into redis list.
    :param model: Instance of model class
    :param list_name: Name of list
    """
    if check_list(list_name):
        with RedisContext() as r:
            r.lpush(list_name, model.json)


def pop_object(model: Any,
               list_name: str) -> Any:
    """
    Pop an object from the redis list and return it as an instance of the
    specified model

    :param model: The model to map the result to
    :param list_name: the name of the list to pop from
    :return:
    """
    if check_list(list_name):
        with RedisContext() as r:
            json_data = r.lpop(list_name)
            if json_data is None:
                return None
            else:
                json_to_dict = json.loads(json_data)
            return model(**json_to_dict)


def get_index(model: Any, list_name: str, idx: int, key: str = '') -> Any:
    """
    Return the item at index
    :param key: The attribute of the returned model to return
    :param list_name: the name of list to search
    :param model: The model to map the result to
    :param idx: The list index
    :return:
    """

    if check_list(list_name):
        with RedisContext() as r:
            json_data = r.lindex(list_name, idx)
            if json_data is None:
                return None
            else:
                json_to_dict = json.loads(json_data)
                mdl = model(**json_to_dict)
            if mdl and key != '':
                return getattr(mdl, key)
            else:
                return mdl
