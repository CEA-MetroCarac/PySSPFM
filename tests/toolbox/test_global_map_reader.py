"""
Test global_map_reader methods
"""
from pytest import approx
import numpy as np

from examples.toolbox.ex_global_map_reader import ex_global_map_reader


# class TestReaderAllMaps(unittest.TestCase):


def test_global_map_reader():
    """ Test ex_global_map_reader """

    mask, coef_arr = ex_global_map_reader()

    off_mask_target = [1, 6, 20]
    on_mask_target = [1, 6, 11]
    coupled_mask_target = [1, 5, 11]

    # print(np.nansum(coef_arr['off']))
    # print(np.nansum(coef_arr['on']))
    # print(np.nansum(coef_arr['off on']))

    assert list(mask['off']) == off_mask_target
    assert list(mask['on']) == on_mask_target
    assert list(mask['coupled']) == coupled_mask_target

    assert np.nansum(coef_arr['off']) == approx(92.8133823858753)
    assert np.nansum(coef_arr['on']) == approx(157.33132034451688)
    assert np.nansum(coef_arr['off on']) == approx(2.8008741872277128)
