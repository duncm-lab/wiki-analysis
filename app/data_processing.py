"""
Various functions for cleaning and sorting data
"""
import os
from multiprocessing import Process

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from app.database import list_len, get_index, push_object, word_db, pop_object, TempTable
from app.models import AnalysisObject, DbList
from app.project_logging import logger


def lang_search(temp_name):
    """
    Query the temp table for rows matching language_titles
    :param temp_name: temporary table name
    :type temp_name: str
    :return: list of strings in temporary table matching language titles
    :rtype: list
    """
    query = f'select a.word from {temp_name} a \
             join language_titles b \
             on a.word = b.word  \
             where b.word is not null'
    with word_db:
        cur = word_db.cursor()
        x = cur.execute(query)
        e = x.fetchall()
        if e:
            return [i[0] for i in e]
        else:
            return []


def valid_search(temp_name):
    """
    Query the temp table for rows matching valid words
    :param temp_name: temporary table name
    :type temp_name: str
    :return: list of strings in temporary table matching valid words
    :rtype: list
    """
    query = f'select a.word from {temp_name} a \
            left join valid_words b\
            on a.word = b.word\
            left join first_names c on\
            a.word = c.word\
            where b.word is not null and c.word is null'
    with word_db:
        cur = word_db.cursor()
        x = cur.execute(query)
        e = x.fetchall()
    if e:
        return [i[0] for i in e]
    else:
        return []


def get_objects(list_name, model):
    """
    Return a list of objects from redis table
    :param list_name: name of redis list to search
    :type list_name: str
    :param model: model class to convert results to
    :type model: object
    :return: iter of current objects in redis list
    :rtype: iter
    """
    objs = []
    for i in range(list_len(list_name)):
        objs.append(get_index(model, list_name, i))
    return iter(objs)


def valid_word(words):
    """
    Take the input list of words and return a list of words
    which are valid

    :param words: a list of words to check
    :type words: list
    :returns: a list of valid words
    :rtype: list
    """
    with TempTable(words) as tmp:
        langs = lang_search(tmp)
        valid = valid_search(tmp)

    return list(set(langs + valid))


def indexer(list_name):
    """
    Loop through the list of AnalysisObjects and then through each info property
    create a Dict of:
        {'word': N}

    - 'N': Number of occurrences of the word in all info lists
    :param list_name: name of redis list
    :type list_name: str
    :return: Dictionary of words and occurrence count
    :rtype: dict
    """

    word_lookup = {}

    for i in range(list_len(list_name)):
        ao_info = get_index(AnalysisObject, list_name, i, 'info')
        for j in ao_info:
            if j[0] not in word_lookup.keys():
                word_lookup[j[0]] = 1
            else:
                word_lookup[j[0]] += 1
    return word_lookup


def get_edge_cases(list_name, min_count, max_count):
    """
    Return the x, y positions of all words with a total count < min_count or > max_count
    :param list_name: name of list
    :type list_name: str
    :param min_count: minimum count of word occurrence
    :type min_count: int
    :param max_count: maximum count of word occurrence
    :type max_count: int
    :return:
    :rtype: set
    """
    ecs = []
    wl = indexer(list_name)
    for k, v in wl.items():
        if v not in range(min_count, max_count):
            ecs.append(k)

    return set(ecs)


def tag_words(ao):
    """
    Do a first pass and tag the words in the AnalysisObject info attribute list.
    :param ao:
    :type ao: AnalysisObject
    :return: tagged analysis object
    :rtype: AnalysisObject
    """
    tokens = word_tokenize(ao.info)
    logger.debug('%d - tagging %s', os.getpid(), ao.title)
    tags = set(pos_tag([i for i in tokens if i.isalpha()]))
    # see nltk.help.upenn_tagset()
    tags = [i for i in tags if i[1] not in
            ['DT', 'IN', 'CD', 'TO', 'PRP', 'PRP$', 'WP', 'WP$', 'MD', 'CC']]
    logger.debug('%d - tagged %s', os.getpid(), ao.title)
    tao = AnalysisObject(ao.title, tags)
    return tao


def filter_words(ao):
    """
    Take an AnalysisObject tag the info words with tag_words then
    remove any unwanted words from the list. Tagging is done before
    filtering so as to give nltk the correct context for specific words.
    :param ao:
    :type ao: AnalysisObject
    :return: filtered analysis object
    :rtype: AnalysisObject
    :raises ValueError: Non tagged object received
    """
    tao = tag_words(ao)
    if not isinstance(tao.info[0], tuple):
        raise ValueError('Expected Analysis object is '
                         'not a list of tuples, has it been tagged?')

    words = [i[0] for i in tao.info]
    valid = valid_word(words)
    rebuild = [i for i in tao.info if i[0] in valid]

    fao = AnalysisObject(tao.title, rebuild)
    logger.debug('%d - filtered %s', os.getpid(), tao.title)
    return fao


def filter_words_list():
    """
    Apply filter words to the list, this is done post tagging in order
    that the tagged objects have the correct lexical context
    """
    while list_len(DbList.analysis_objects0) != 0:
        ao = pop_object(AnalysisObject, DbList.analysis_objects0)
        fao = filter_words(ao)
        push_object(fao, DbList.filtered_objects)


def filter_main():
    processes = [Process(target=filter_words_list, args=())
                 for _ in range(int(os.cpu_count()))]  # pylint disable=unused-variable
    for i in processes:
        i.start()

    for i in processes:
        i.join()


if __name__ == '__main__':
    filter_main()
