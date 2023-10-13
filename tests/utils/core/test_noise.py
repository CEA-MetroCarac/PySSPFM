"""
Test noise methods
"""
from pytest import approx
import numpy as np

from examples.utils.core.ex_noise import ex_gen_noise, ex_filter_mean


def test_ex_gen_noise():
    """ Test ex_gen_noise """

    out = ex_gen_noise()
    (y_noise_lin, y_noise_normal, y_noise_laplace,
     pure_noise_lin, pure_noise_normal, pure_noise_laplace) = out

    assert np.sum(y_noise_lin) == approx(-40.784656282172094)
    assert np.sum(y_noise_normal) == approx(62.42441893840551)
    assert np.sum(y_noise_laplace) == approx(46.30080405125386)
    assert np.sum(pure_noise_lin) == approx(-40.78465628217209)
    assert np.sum(pure_noise_normal) == approx(62.42441893840544)
    assert np.sum(pure_noise_laplace) == approx(46.300804051253806)


def test_ex_filter_mean():
    """ Test ex_filter_mean """

    y_filt = ex_filter_mean()

    assert np.sum(y_filt) == approx(52.48731220242615)
