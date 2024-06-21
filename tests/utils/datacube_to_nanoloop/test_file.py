"""
Test file methods
"""
import numpy as np
from pytest import approx

from examples.utils.datacube_to_nanoloop.ex_file import example_file


# class TestFile(unittest.TestCase):


def test_file():
    """ Test example_file """

    phase_tab = example_file()

    assert np.sum(phase_tab) == approx(2253.0115110174156)
