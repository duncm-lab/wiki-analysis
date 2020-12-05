"""Defines a shared log file and level"""
import json
from logging import Formatter, getLogger, Handler

import requests

from app.client import is_open
from app.config_loader import load_config

es_host = load_config('elastic_search')['host']
es_port = load_config('elastic_search')['port']
es_index = load_config('elastic_search')['index']
es_scheme = load_config('elastic_search')['scheme']

es_index_url = f'{es_scheme}://{es_host}:{es_port}/{es_index}'

# Check server and port are accessible
if not is_open((es_host, es_port)):
    raise ConnectionError('Cannot connect to logging server')

# check if elasticsearch index exists
index_check = requests.get(es_index_url)
if index_check.status_code != 200:
    requests.put(es_index_url)

log_level = load_config('elastic_search')['log_level']

log_format = '{"level": "%(levelname)s",' \
             '"timestamp": "%(asctime)s",' \
             '"process_id": "%(process)s",' \
             '"module": "%(module)s",' \
             '"function": "%(funcName)",' \
             '"message": "%(message)s"}'

formatter = Formatter(log_format)
logger = getLogger('wiki_analysis')
logger.setLevel(log_level)


class ElasticLogHandler(Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        req = f'{es_index_url}/_doc'
        data = json.dumps(record.__dict__)
        response = requests.post(url=req,
                                 data=data,
                                 headers={'content-type': 'application/json'})
        if response.status_code not in range(200, 300):
            raise requests.HTTPError(f'Response was {response.status_code} not 200')


handler = ElasticLogHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
