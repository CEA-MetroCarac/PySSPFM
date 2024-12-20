"""
Test gen_data methods
"""
from pytest import approx
import numpy as np

from examples.utils.datacube_to_nanoloop.ex_gen_data import ex_gen_segments


# class TestGenDatas(unittest.TestCase):


def test_gen_segments_fit():
    """ Test ex_gen_segments 'fit' mode """

    dict_meas = ex_gen_segments('fit')

    key_dict_meas = list(dict_meas.keys())
    true_keys = ['sspfm bias', 'times', 'tip_bias', 'amp', 'pha',
                 'deflection', 'height']

    assert np.sum(dict_meas['times']) == approx(9605978.999999806)
    assert np.sum(dict_meas['tip_bias']) == approx(1.4551915228366852e-11)
    assert np.sum(dict_meas['amp']) == approx(14298019.68521869)
    assert np.sum(dict_meas['pha']) == approx(34957828.199933924)
    assert key_dict_meas == true_keys


def test_gen_segments_dfrt():
    """ Test ex_gen_segments 'dfrt' mode """

    dict_meas = ex_gen_segments('dfrt')

    key_dict_meas = list(dict_meas.keys())
    true_keys = ['sspfm bias', 'times', 'tip_bias', 'amp', 'pha',
                 'deflection', 'height']

    assert np.sum(dict_meas['times']) == approx(9605978.999999806)
    assert np.sum(dict_meas['tip_bias']) == approx(1.4551915228366852e-11)
    assert np.sum(dict_meas['amp']) == approx(4906599.144687748)
    assert np.sum(dict_meas['pha']) == approx(17219838.632536672)
    assert key_dict_meas == true_keys
