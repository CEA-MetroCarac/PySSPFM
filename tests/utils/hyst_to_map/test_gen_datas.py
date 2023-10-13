"""
Test gen_datas methods
"""
from pytest import approx
import numpy as np

from examples.utils.hyst_to_map.ex_gen_datas import example_gen_datas


# class TestGenDatas(unittest.TestCase):


def test_gen_datas_multi_off():
    """ Test gen_datas: off field: multi loop """

    datas_dict, dict_str = example_gen_datas(analysis='multi_off')

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    # print(sum_datas_dict)

    assert sum_datas_dict == approx(98097.62513626559)
    assert dict_str == {'unit': 'nm', 'label': 'Off field', 'col': 'w'}


def test_gen_datas_mean_off():
    """ Test gen_datas: off field: mean loop """

    datas_dict, dict_str = example_gen_datas(analysis='mean_off')

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    # print(sum_datas_dict)

    assert sum_datas_dict == approx(97734.6636422566)
    assert dict_str == {'unit': 'nm', 'label': 'Off field', 'col': 'w'}


def test_gen_datas_mean_on():
    """ Test gen_datas: on field: mean loop """

    datas_dict, dict_str = example_gen_datas(analysis='mean_on')

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    # print(sum_datas_dict)

    assert sum_datas_dict == approx(96630.14113616597)
    assert dict_str == {'unit': 'nm', 'label': 'On field', 'col': 'y'}
