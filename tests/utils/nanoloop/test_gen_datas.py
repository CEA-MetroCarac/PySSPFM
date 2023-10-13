"""
Test gen_datas methods
"""
from pytest import approx
import numpy as np

from examples.utils.nanoloop.ex_gen_datas import ex_gen_loops


# class TestGenDatas(unittest.TestCase):


def test_gen_loops_on():
    """ Test ex_gen_loops 'on' field """

    write_voltage, read_voltage, amp, pha = ex_gen_loops('on')

    sum_1 = sum(np.sum(tab) for tab in amp)
    sum_2 = sum(np.sum(tab) for tab in pha)
    sum_3 = sum(np.sum(tab) for tab in write_voltage)

    assert sum_1 == approx(13755.71032023054)
    assert sum_2 == approx(131445.90458320786)
    assert sum_3 == approx(9.094947017729282e-13)
    assert sum(read_voltage) == approx(-2.220446049250313e-16)


def test_gen_loops_off():
    """ Test ex_gen_loops 'off' field """

    write_voltage, read_voltage, amp, pha = ex_gen_loops('off')

    sum_1 = sum(np.sum(tab) for tab in amp)
    sum_2 = sum(np.sum(tab) for tab in pha)
    sum_3 = sum(np.sum(tab) for tab in write_voltage)

    assert sum_1 == approx(4248.967320529875)
    assert sum_2 == approx(90051.47828723147)
    assert sum_3 == approx(9.094947017729282e-13)
    assert sum(read_voltage) == approx(-2.220446049250313e-16)
