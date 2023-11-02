"""
Test gen_data methods
"""
from pytest import approx
import numpy as np

from examples.utils.nanoloop_to_hyst.ex_gen_data import example_gen_data


# class TestGenDatas(unittest.TestCase):


def test_gen_data_multi_off():
    """ Test gen_data: off field: multi loop """

    datas_dict, dict_str = example_gen_data(analysis='multi_off')

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    # print(sum_datas_dict)

    assert sum_datas_dict == approx(98097.62513626559)
    assert dict_str == {'unit': 'nm', 'label': 'Off field', 'col': 'w'}


def test_gen_data_mean_off():
    """ Test gen_data: off field: mean loop """

    datas_dict, dict_str = example_gen_data(analysis='mean_off')

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    # print(sum_datas_dict)

    assert sum_datas_dict == approx(97734.6636422566)
    assert dict_str == {'unit': 'nm', 'label': 'Off field', 'col': 'w'}


def test_gen_data_mean_on():
    """ Test gen_data: on field: mean loop """

    datas_dict, dict_str = example_gen_data(analysis='mean_on')

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    # print(sum_datas_dict)

    assert sum_datas_dict == approx(96630.14113616597)
    assert dict_str == {'unit': 'nm', 'label': 'On field', 'col': 'y'}
