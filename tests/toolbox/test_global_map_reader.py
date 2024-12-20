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

    off_mask_target = [1, 20]
    on_mask_target = [1, 5]
    coupled_mask_target = [1, 5, 11]
    other_mask_target = [0, 1, 2, 3, 4, 6]

    # print(np.nansum(coef_arr['off']))
    # print(np.nansum(coef_arr['on']))
    # print(np.nansum(coef_arr['off on']))

    assert list(mask['off']) == off_mask_target
    assert list(mask['on']) == on_mask_target
    assert list(mask['coupled']) == coupled_mask_target
    assert list(mask['other']) == other_mask_target

    assert np.nansum(coef_arr['off']) == approx(21.598076551114232)
    assert np.nansum(coef_arr['on']) == approx(231.4654733521148)
    assert np.nansum(coef_arr['off on']) == approx(16.772036861532527)
