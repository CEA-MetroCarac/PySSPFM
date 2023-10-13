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

    # print(np.nansum(coef_arr['on']))
    # print(np.nansum(coef_arr['off']))
    # print(np.nansum(coef_arr['off on']))

    assert np.nansum(coef_arr['on']) == approx(157.33132034451688)
    assert np.nansum(coef_arr['off']) == approx(92.95253375859342)
    assert np.nansum(coef_arr['off on']) == approx(2.8008741872277128)