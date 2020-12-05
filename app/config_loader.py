"""load settings from config file"""
import os

import yaml

path = os.path.dirname(os.path.abspath(__file__))


def load_config(config_section):
    """Read settings from config.yml
    :param config_section: config group key
    :type config_section: str

    :returns: configuration settings
    :rtype: dict or list
    """
    with open(os.path.join(path, 'config.yml'), 'r') as fl:
        cfg = yaml.safe_load(fl.read())
    return cfg[config_section]
