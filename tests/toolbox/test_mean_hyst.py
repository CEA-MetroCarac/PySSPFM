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

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        0.023817347654832385, abs=1e-8)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        7739.825023809523, abs=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.09687934526247358, abs=1e-8)
    assert np.sum(best_hysts.params) == approx(4.877862257641804, abs=1e-6)
    assert np.sum(list(best_hysts.props.values())) == approx(
        33.45777995370079, abs=1e-6)


def test_mean_hyst_1_off():
    """ Test mean_hyst function: select phase 1, off field """

    mean_best_loop, best_hysts = example_mean_hyst(phase='1', mode='off')

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        0.014257965966354052, abs=1e-8)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        7899.7688520408165, abs=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.05151371961876901, abs=1e-8)
    assert np.sum(best_hysts.params) == approx(0.6466366857553892, abs=1e-6)
    assert np.sum(list(best_hysts.props.values())) == approx(
        12.53729157192051, abs=1e-6)


def test_mean_hyst_1_coupled():
    """ Test mean_hyst function: select phase 1, coupled """

    mean_diff_piezorep, fit_res = example_mean_hyst(phase='1', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(-0.00023134389912081156, abs=1e-8)
    assert fit_res[1] == approx(0.005712523654603662, abs=1e-7)
    assert fit_res[2] == approx(24.692778483950807, abs=1e-3)
    assert fit_res[3] == approx(0.9992722531698784, abs=1e-5)
    assert np.sum(mean_diff_piezorep) == approx(0.28917574443307176, abs=1e-5)


def test_mean_hyst_2_on():
    """ Test mean_hyst function: select phase 2, on field """

    mean_best_loop, best_hysts = example_mean_hyst(phase='2', mode='on')

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        0.009777369584858076, abs=1e-8)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        8404.361462500001, abs=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.09217496530716723, abs=1e-8)
    assert np.sum(best_hysts.params) == approx(4.022167481420474, abs=1e-6)
    assert np.sum(list(best_hysts.props.values())) == approx(
        31.764081898315638, abs=1e-6)


def test_mean_hyst_2_off():
    """ Test mean_hyst function: select phase 2, off field """

    mean_best_loop, best_hysts = example_mean_hyst(phase='2', mode='off')

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        0.013260336560458203, abs=1e-8)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        7224.888276360544)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        0.029393670007661767, abs=1e-8)
    assert np.sum(best_hysts.params) == approx(0.8354624824790046, abs=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        23.463940770122115, abs=1e-3)


def test_mean_hyst_2_coupled():
    """ Test mean_hyst function: select phase 2, coupled """

    mean_diff_piezorep, fit_res = example_mean_hyst(phase='2', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(-0.00030392628011313634, abs=1e-8)
    assert fit_res[1] == approx(0.005263717240490688, abs=1e-7)
    assert fit_res[2] == approx(17.31905920913214, abs=1e-3)
    assert fit_res[3] == approx(0.9986761322985575, abs=1e-5)
    assert np.sum(mean_diff_piezorep) == approx(
        0.266055632453863, abs=1e-5)
