"""
Test map_correlation methods
"""
from pytest import approx
import numpy as np

from examples.toolbox.ex_map_correlation import ex_map_correlation


# class TestCorrelation(unittest.TestCase):


def test_map_correlation():
    """ Test ex_map_correlation """

    coef_arr = ex_map_correlation()

    # print(np.nansum(coef_arr['off']))
    # print(np.nansum(coef_arr['on']))
    # print(np.nansum(coef_arr['off on']))

    assert np.nansum(coef_arr['off']) == approx(21.598076551114232)
    assert np.nansum(coef_arr['on']) == approx(231.4654733521148)
    assert np.nansum(coef_arr['off on']) == approx(16.772036861532527)
