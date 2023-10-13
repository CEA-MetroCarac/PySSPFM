"""
Test peak methods
"""
from pytest import approx
import numpy as np

from examples.utils.core.ex_peak import \
    (ex_find_main_peaks, ex_detect_peak, ex_width_peak, ex_guess_affine,
     ex_guess_bckgnd)


def test_ex_find_main_peaks():
    """ Test ex_find_main_peaks """

    res_peaks, res_main, res_lim = ex_find_main_peaks()

    assert np.sum(res_peaks) == 1552
    assert res_main[0] == 1
    assert res_main[1] == 2
    assert res_main[2] == 0
    assert np.sum(res_lim) == 3018


def test_ex_detect_peak():
    """ Test ex_detect_peak """

    test_peak, test_bckgnd = ex_detect_peak(verbose=False)

    assert test_peak is True
    assert test_bckgnd is False


def test_ex_width_peak():
    """ Test ex_width_peak """

    width = ex_width_peak(make_plots=False)

    assert width['width'] == 2.2
    assert width['ind left'] == 39
    assert width['ind right'] == 61


def test_ex_guess_affine():
    """ Test ex_guess_affine """

    slope, bckgnd = ex_guess_affine(make_plots=False)

    assert slope == approx(0.1998774462703993)
    assert bckgnd == approx(2.0255260178836707)


def test_ex_guess_bckgnd():
    """ Test ex_guess_bckgnd """

    bckgnd = ex_guess_bckgnd(make_plots=False)

    assert bckgnd == approx(2.024913249235667)
