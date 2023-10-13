"""
Test correct iterable examples execution
"""
import numpy as np

from examples.utils.core.ex_iterable import ex_iterable


def test_ex_iterable():
    """ Test ex_iterable """

    out = ex_iterable(verbose=False)
    (ind_cond_1, ind_cond_2, sort_tab_l0, sort_tab_c2) = out

    assert np.sum(ind_cond_1) == 24
    assert np.sum(ind_cond_2) == 13
    assert np.sum(sort_tab_l0[0]) == 18
    assert np.sum(np.array(sort_tab_l0)[:, 0]) == 3
    assert np.sum(sort_tab_c2[0]) == 27
    assert np.sum(np.array(sort_tab_c2)[:, 0]) == 3
