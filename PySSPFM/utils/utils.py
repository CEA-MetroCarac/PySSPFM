"""
Utils functions
"""
import sys
import os

from PySSPFM.settings import SETTINGS_DICT
from PySSPFM.default_settings import DEF_SETTINGS_DICT


def get_setting(key):
    """
    Get a setting value based on the specified key. This function allows you
    to check whether the initial code launch is a test or an example.
    In such cases, default settings are used to align with example data and
    achieve the correct target values for tests. Otherwise, user-adjustable
    settings are extracted.

    Parameters
    ----------
    key : str
        The key to look up in the settings dictionaries.

    Returns
    -------
    setting : object
        The value associated with the provided key in the settings dictionaries.
    """
    origin_path = sys.argv[0]
    sep_origin_path = origin_path.split(os.path.sep)

    # Use the default settings if 'examples' or 'test' is in the script path
    settings_to_use = \
        DEF_SETTINGS_DICT if 'examples' in sep_origin_path or \
                             'tests' in sep_origin_path else SETTINGS_DICT
    setting = settings_to_use.get(key)

    return setting
