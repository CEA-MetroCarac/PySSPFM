"""
Test noise methods
"""
from pytest import approx
import numpy as np

from examples.utils.core.ex_noise import \
    ex_gen_noise, ex_filter_mean, ex_butter_filter


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


def test_ex_butter_filter_low():
    """ Test ex_butter_filter low pass """

    y_filt_low = ex_butter_filter(filter_type='low')

    assert np.sum(y_filt_low) == approx(21.049807430587258)


def test_ex_butter_filter_high():
    """ Test ex_butter_filter high pass """

    y_filt_high = ex_butter_filter(filter_type='high')

    assert np.sum(y_filt_high) == approx(0.07489646793298177)


def test_ex_butter_filter_bandpass():
    """ Test ex_butter_filter band pass """

    y_filt_bandpass = ex_butter_filter(filter_type='bandpass')

    assert np.sum(y_filt_bandpass) == approx(-24.70597466183571, abs=1e-5)


def test_ex_butter_filter_bandstop():
    """ Test ex_butter_filter band stop """

    y_filt_bandstop = ex_butter_filter(filter_type='bandstop')

    assert np.sum(y_filt_bandstop) == approx(33.83620308961862, abs=1e-5)
