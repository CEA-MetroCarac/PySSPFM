"""
Test list_map_reader methods
"""

from examples.toolbox.ex_list_map_reader import \
    (ex_list_map_reader_properties, ex_list_map_reader_phase_inversion,
     ex_list_map_reader_phase_offset)


# class TestReaderListMaps(unittest.TestCase):


def test_list_map_reader_properties():
    """ Test ex_list_map_reader_properties """

    figures = ex_list_map_reader_properties()

    assert len(list(figures)) == 5


def test_list_map_reader_phase_inversion():
    """ Test ex_list_map_reader_phase_inversion """

    figures = ex_list_map_reader_phase_inversion()

    assert len(list(figures)) == 4


def test_list_map_reader_phase_offset():
    """ Test ex_list_map_reader_phase_offset """

    figures = ex_list_map_reader_phase_offset()

    assert len(list(figures)) == 4
