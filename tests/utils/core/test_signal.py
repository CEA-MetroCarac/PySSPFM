"""
Test signal methods
"""
from pytest import approx
import numpy as np

from examples.utils.core.ex_signal import ex_line_reg, ex_interpolate


def test_ex_line_reg():
    """ Test ex_line_reg """

    results = ex_line_reg()

    assert results['coefs'][0] == approx(4.919704346171228)
    assert results['coefs'][1] == approx(2.70629292705652)
    assert results['unc a'] == approx(0.21179516137035528)
    assert results['r**2'] == approx(0.9137743107055035)
    assert np.sum(results['x fit']) == approx(250.0)
    assert np.sum(results['y fit']) == approx(1365.240732895633)


def test_ex_interpolate():
    """ Test test_ex_interpolate """

    x_interp, y_interp = ex_interpolate()

    assert np.sum(x_interp) == 0.0
    assert np.sum(y_interp) == approx(1336.759322016279)
