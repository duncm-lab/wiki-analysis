# pylint: disable=all
from setuptools import setup, find_packages


with open('app/readme.md', 'r') as fl:
    long_description = fl.read()

setup(
    name='wiki_analysis',
    version='0.0.1.dev1',
    packages=find_packages(exclude=['tests']),
    package_data={'': ['readme.md', 'schema.sql', 'words.txt', 'config.yml']},
    include_package_date=True,
    url='',
    license='GNU GPLv3',
    author='duncanmaginn',
    author_email='',
    description='Create graphs from data obtained from Wikipedia',
    long_description=long_description,
    classifiers=['Programming Language :: Python :: 3.9',
                 'Licence :: OSI Approved :: GNU GPLv3',
                 'Operating System :: Linux/MacOS'],
    scripts=['./scripts/database_setup.py', './scripts/server.py'],
    install_requires=['beautifulsoup4', 'bs4', 'pylint', 'redis',
                      'requests', 'nltk', 'PyYAML'])
