"""
Define some data structures for various objects.

The BaseObject is inherited by all model classes and contains
"""

import json
import os
from abc import abstractmethod, ABC

path = os.path.dirname(os.path.abspath(__file__))


class ModelMeta(ABC):

    @property
    @abstractmethod
    def json(self):
        pass


class QueryObject(ModelMeta):
    """
    A model containing a title specifying the language and a url to query

    :param title: The name of the language
    :type title: str
    :param url_query: The url associated with the language
    :type url_query: str
    """
    def __init__(self, title='', url_query=''):
        self.url_query: str = url_query
        self.title: str = title

    def __repr__(self):
        """

        :return:
        :rtype: str
        """
        repr_str = f'QueryObject(title=\'{self.title}\', url_query=\'{self.url_query}\')'
        return repr_str

    @property
    def json(self):
        """
        Return the model as a json object
        :return:
        :rtype: str
        """
        return json.dumps({'url_query': self.url_query, 'title': self.title})


class AnalysisObject(ModelMeta):
    """
    A model of the language title and a list of words from in the associated web
    page.

    :param title: The name of the language
    :type title: str
    :param info:
    :type info: str or list
    """
    def __init__(self, title='', info=None):
        self.title = title
        self.info = info

    def __repr__(self):
        """

        :return:
        :rtype: list
        """
        repr_str = f'AnalysisObject(title=\'{self.title}\', info=\'{self.info}\')'
        return repr_str

    @property
    def json(self):
        """
        Return the model as a json object
        :return:
        :rtype: list
        """
        return json.dumps({'title': self.title, 'info': self.info})


class DbList:
    """
    Lookup of list names for validation purposes
    """
    query_objects = 'query_objects'
    analysis_objects0 = 'analysis_objects0'  # get_data
    tagged_analysis_objects = 'tagged_analysis_objects'
    analysis_objects1 = 'analysis_objects1'  # data_processing
    filtered_objects = 'filtered_objects'


def load_from_json(class_name, jsn):
    """
    Take a json object and instantiate the corresponding model class
    :param class_name: name of class to map the json object to
    :type class_name:
    :param jsn: jsn object to map
    :type jsn: str
    :return:
    :rtype: object
    """
    json_to_dict = json.loads(jsn)
    dict_to_object = class_name(**json_to_dict)
    return dict_to_object
