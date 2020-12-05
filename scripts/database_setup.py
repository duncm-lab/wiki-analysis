#! /usr/bin/env python3
"""
Import data into the words.db sqlite database


"""
from nltk.corpus import stopwords, names

from app.data_processing import get_objects
from app.models import AnalysisObject
from app.database import word_db
from app.config_loader import path
import os

stp_words = stopwords.words('english')
names = [i.lower() for i in names.words()]
word_filter = [i.lower() for i in stp_words]
lang_titles = [i.title.lower() for i in get_objects('analysis_objects0', AnalysisObject)]

if __name__ == '__main__':

    with open(os.path.join(path, '../app/words.txt'), 'r') as fl:
        valid = fl.read()
        valid = {i.lower() for i in valid.split(' ')} - set(word_filter)

    with open(os.path.join(path, '../app/schema.sql'), 'r') as fl:
        schema = fl.read()

    with word_db:
        cur = word_db.cursor()
        cur.executescript(schema)

    with word_db:
        cur = word_db.cursor()

        for i in valid:
            cur.execute('insert into valid_words (word) values (?)', (i,))

        for i in lang_titles:
            cur.execute('insert into language_titles (word) values (?)', (i,))

        for i in names:
            cur.execute('insert into first_names (word) values (?)', (i,))
