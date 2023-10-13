"""
Test list_map_reader methods
"""

from examples.toolbox.ex_list_map_reader import ex_list_map_reader


# class TestReaderListMaps(unittest.TestCase):


def test_list_map_reader():
    """ Test ex_list_map_reader """

    figures = ex_list_map_reader()

    assert len(list(figures)) == 3
