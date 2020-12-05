# pylint: disable=all
import pickle
from app.database import pop_object, flush_redis, list_len

import app.get_data
import os

from app.models import AnalysisObject

"""Run an import and save the data to a pickle file
in order that we aren't constantly making requests
whilst testing."""


def get_test_data():
    # flush the database to remove old data
    if os.path.exists('analysis_objects0.pickle'):
        os.remove('analysis_objects0.pickle')
    flush_redis()
    # call the main function of get_data to populate analysis objects
    app.get_data.get_data_main()

    # pull the analysis data from the database
    aos = []
    while list_len('analysis_objects0') != 0:
        ao = pop_object(AnalysisObject, 'analysis_objects0')
        aos.append(ao)

    # write objects to pickle file
    with open('analysis_objects0.pickle', 'wb') as fl:
        pickle.dump(aos, fl)


if __name__ == '__main__':
    get_test_data()
