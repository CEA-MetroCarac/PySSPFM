"""
Test hyst_to_map_s2 methods
"""

import pytest
from examples.data_processing.ex_hyst_to_map_s2 import ex_multi_script


# class TestMain(unittest.TestCase):


@pytest.mark.slow
def test_multi_script():
    """ Test ex_multi_script """

    ex_multi_script()
