"""
Test basic func functionalities
"""
from pytest import approx
import numpy as np

from examples.utils.core.ex_basic_func import ex_basic_func


def test_linear_basic_func():
    """ test linear basic func """
    y = ex_basic_func('linear', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(201.00000000000003)


def test_sigmoid_basic_func():
    """ test sigmoid basic func """
    y = ex_basic_func('sigmoid', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(-19.999999491887905)


def test_arctan_basic_func():
    """ test arctan basic func """
    y = ex_basic_func('arctan', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(-60.81668507605707)


def test_gaussian_basic_func():
    """ test gaussian basic func """
    y = ex_basic_func('gaussian', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(21.289340388624524)


def test_lorentzian_basic_func():
    """ test lorentzian basic func """
    y = ex_basic_func('lorentzian', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(29.352063785500178)


def test_pseudovoigt_basic_func():
    """ test pseudovoigt basic func """
    y = ex_basic_func('pseudovoigt', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(25.320702087062354)


def test_sho_basic_func():
    """ test sho basic func """
    y = ex_basic_func('sho', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(10970.60049463252)


def test_sho_phase_basic_func():
    """ test sho phase basic func """
    y = ex_basic_func('sho_phase', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(1569.9528184396)


def test_sho_phase_switch_basic_func():
    """ test sho phase basic func (with switch) """
    y = ex_basic_func('sho_phase_switch', make_plots=False)
    # print(np.sum(y))

    assert np.sum(y) == approx(-0.8435083552967626)
