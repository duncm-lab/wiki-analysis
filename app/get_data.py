"""
- Take each link listed in https://en.wikipedia.org/wiki/List_of_programming_languages.
- Read page data from each linked page and scrub it of unwanted values
- Push to database
"""

import os
import re
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError  # pylint: disable=redefined-builtin

from app.cpu_share import share
from app.database import push_object
from app.models import QueryObject, AnalysisObject
from app.project_logging import logger

lang_titles = []


def get_info(url_query):
    """
    Perform a GET request on the url passed into the function, parse the data
    and sanitise it of any unwanted data then return the parsed data as a list
    of strings

    :param url_query: page to be queried
    :type url_query: str
    :returns: list of filtered strings from webpage
    :rtype: list
    """
    try:
        req = requests.get(url_query, timeout=30)
    except (ConnectionError, requests.exceptions.ReadTimeout) as e:
        logger.error(e)
        req = None

    if req is None or req.status_code != 200:
        logger.info('%s returned no information or invalid status', url_query)
        info = ''
    else:
        remove_tags = ['pre', 'script', 'nav', 'footer', 'form', 'input', 'meta']
        soup = BeautifulSoup(req.text, features='html.parser')
        soup = soup.find('div', attrs={'class': 'mw-parser-output'})
        #  soup = soup.find('p')

        for f in remove_tags:  # remove this stuff from the soup object
            for j in soup.find_all(f):
                j.decompose()

        info = soup.text.replace('\n', '').replace('"', '').replace("'", '').lower()

    return info


def create_query_object(query_result):
    """
    :param query_result:
    :type query_result: bs4.element.Tag
    :return: QueryObject
    :rtype: QueryObject


    Args:
        query_result (bs4.element.Tag): bs4 result

    Returns:
        QueryObject

    >>> example_data = get_languages()
    >>> elem = next(example_data)
    >>> create_query_object(elem)
    QueryObject(url_query='https://en.wikipedia.org/wiki/A_Sharp_(.NET)',
        title='A Sharp (.NET)')
    >>> elem = next(example_data)
    >>> create_query_object(elem)
    QueryObject(url_query='https://en.wikipedia.org/wiki/A-0_System',
        title='A-0 System')

    """
    url = 'https://en.wikipedia.org'
    url_query = url + query_result.attrs['href']
    title = query_result.attrs['title']
    title = re.sub(r'\W[Pp]rogramming [Ll]anguage\W', '', title).strip()
    lang_titles.append(title)
    return QueryObject(title=title, url_query=url_query)


def get_languages():
    """
    Parse the master 'https://en.wikipedia.org/wiki/List_of_programming_languages'
    for links.

    >>> example_data = get_languages()
    >>> type(example_data)
    <class 'generator'>
    >>> elem = next(example_data)
    >>> type(elem)
    <class 'bs4.element.Tag'>
    :return:
    :rtype: list
    """
    url = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features='html.parser')
    divs = soup.find_all('div', attrs={'class': 'div-col columns column-width'})
    links = []
    for d in divs:
        for j in d.find_all('a'):
            links.append(create_query_object(j))
    return share(iter(links))


def create_analysis_object(qo):
    """
    Take a QueryObject and GET data from the page specified in
    the url_query attribute.

    :param qo: A list of QueryObjects
    :type qo: list[QueryObject]
    """
    try:
        for qu in qo:
            logger.info('pid: %d - processing: %s', os.getpid(), qu.title)
            ao = AnalysisObject(title=qu.title, info=get_info(qu.url_query))
            push_object(ao, 'analysis_objects0')

    except AttributeError as e:
        logger.error(e)


def get_data_main():
    langs = get_languages()
    p = Pool(processes=os.cpu_count())
    p.map(create_analysis_object, langs)


if __name__ == '__main__':
    get_data_main()
