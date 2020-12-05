# pylint: disable=all
import os
import pickle

from app.project_logging import logger
from app.database import push_object, flush_redis


"""
Import test data into redis
"""

file = os.path.join(os.path.dirname(__file__), 'analysis_objects0.pickle')
logger.info('Reading from %s', file)

with open(file, 'rb') as fl:
    data_in = pickle.loads(fl.read())


def main():
    start_count = len(data_in)
    end_count = 0
    while len(data_in) != 0:
        data = data_in.pop(0)
        push_object(data, 'analysis_objects0')
        end_count = end_count + 1
    logger.info('Imported %d out of %d', end_count, start_count)


if __name__ == '__main__':
    flush_redis()
    main()
