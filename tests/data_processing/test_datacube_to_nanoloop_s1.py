"""
Test datacube_to_nanoloop_s1 methods
"""

from pytest import approx

from examples.data_processing.ex_datacube_to_nanoloop_s1 import ex_single_script


# class TestMain(unittest.TestCase):


def test_single_script():
    """ Test ex_single_script """

    phase_offset_val = ex_single_script()
    assert phase_offset_val['On field'] == approx(89, rel=3e-2)
    assert phase_offset_val['Off field'] == approx(89, rel=3e-2)
