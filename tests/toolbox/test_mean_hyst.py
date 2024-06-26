"""
Test mean_hyst methods
"""
from pytest import approx
import numpy as np

from examples.toolbox.ex_mean_hyst import example_mean_hyst


# class TestMeanLoop(unittest.TestCase):


def test_mean_hyst_1_on():
    """ Test mean_hyst function: select phase 1, on field """

    mean_best_loop, best_hysts = example_mean_hyst(phase='1', mode='on')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -0.00977709797788614, rel=1e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        9593.581692857146, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.09190636352673492, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(4.0131025519600705, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        31.742030053892524, rel=1e-2)


def test_mean_hyst_1_off():
    """ Test mean_hyst function: select phase 1, off field """

    mean_best_loop, best_hysts = example_mean_hyst(phase='1', mode='off')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -0.014858995909200489, rel=1e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        10878.788703231292, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.02943137767175129, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(0.8495199624994088, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        23.31603162632309, rel=1e-2)


def test_mean_hyst_1_coupled():
    """ Test mean_hyst function: select phase 1, coupled """

    mean_diff_piezorep, fit_res = example_mean_hyst(phase='1', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(0.00030457459140239223, rel=1e-2)
    assert fit_res[1] == approx(-0.0052612852065401835, rel=1e-2)
    assert fit_res[2] == approx(17.274209192286747, rel=1e-2)
    assert fit_res[3] == approx(0.9986500848186182, rel=1e-2)
    assert np.sum(mean_diff_piezorep) == approx(-0.2662060707108222, rel=1e-2)


def test_mean_hyst_2_on():
    """ Test mean_hyst function: select phase 2, on field """

    mean_best_loop, best_hysts = example_mean_hyst(phase='2', mode='on')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -0.023796092386975352, rel=1e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        10119.649, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.09662851394441734, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(4.537629967759128, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        30.754763280935652, rel=1e-2)


def test_mean_hyst_2_off():
    """ Test mean_hyst function: select phase 2, off field """

    mean_best_loop, best_hysts = example_mean_hyst(phase='2', mode='off')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -0.014167267180081992, rel=1e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        10065.232700680273, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.051398923765410595, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(0.6475140254636365, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        12.600744006996758, rel=1e-2)


def test_mean_hyst_2_coupled():
    """ Test mean_hyst function: select phase 2, coupled """

    mean_diff_piezorep, fit_res = example_mean_hyst(phase='2', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(0.00023159545049958598, rel=1e-2)
    assert fit_res[1] == approx(-0.00606389134788622, rel=1e-2)
    assert fit_res[2] == approx(26.18311946459009, rel=1e-2)
    assert fit_res[3] == approx(0.9993101829453005, rel=1e-2)
    assert np.sum(mean_diff_piezorep) == approx(
        -0.30708313103702317, rel=1e-2)
