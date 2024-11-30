"""
Test mean_hyst methods
"""
import os
from pytest import approx, skip
import numpy as np

from examples.toolbox.ex_mean_hyst import example_mean_hyst


# class TestMeanLoop(unittest.TestCase):


def test_mean_hyst_1_on():
    """ Test mean_hyst function: select phase 1, on field """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    mean_best_loop, best_hysts = example_mean_hyst(phase='1', mode='on')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -0.4275656279881551, rel=5e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        9593.581692857146, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        4.0191887333333325, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(3.965749310674802, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        32.095511972280626, rel=1e-2)


def test_mean_hyst_1_off():
    """ Test mean_hyst function: select phase 1, off field """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    mean_best_loop, best_hysts = example_mean_hyst(phase='1', mode='off')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -0.6498038509545887, rel=1e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        10878.788703231292, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        1.287073680272109, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(0.7874513742123793, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        23.680332131993126, rel=1e-2)


def test_mean_hyst_1_coupled():
    """ Test mean_hyst function: select phase 1, coupled """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    mean_diff_piezorep, fit_res = example_mean_hyst(phase='1', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(0.013319456012074763, rel=1e-2)
    assert fit_res[1] == approx(-0.004041589030114636, rel=1e-2)
    assert fit_res[2] == approx(0.30343499212360703, rel=1e-2)
    assert fit_res[3] == approx(0.9986500848186182, rel=1e-2)
    assert np.sum(mean_diff_piezorep) == approx(-0.11343355948225486, rel=1e-2)


def test_mean_hyst_2_on():
    """ Test mean_hyst function: select phase 2, on field """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    mean_best_loop, best_hysts = example_mean_hyst(phase='2', mode='on')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -1.0406350849826533, rel=1e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        10119.649, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        4.225694714285714, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(4.49331664877594, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        31.057832976428845, rel=1e-2)


def test_mean_hyst_2_off():
    """ Test mean_hyst function: select phase 2, off field """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    mean_best_loop, best_hysts = example_mean_hyst(phase='2', mode='off')

    # print(np.sum(mean_best_loop.piezorep.y_meas))
    # print(np.sum(mean_best_loop.treated_pha.y_meas))
    # print(np.sum(mean_best_loop.amp.y_meas))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep.y_meas) == approx(
        -0.6195536244423917, rel=5e-2)
    assert np.sum(mean_best_loop.treated_pha.y_meas) == approx(
        10065.232700680273, rel=1e-2)
    assert np.sum(mean_best_loop.amp.y_meas) == approx(
        2.247743979591837, rel=1e-2)
    assert np.sum(best_hysts.params) == approx(0.5214184435556072, rel=1e-2)
    assert np.sum(list(best_hysts.props.values())) == approx(
        13.051725967473164, rel=1e-2)


def test_mean_hyst_2_coupled():
    """ Test mean_hyst function: select phase 2, coupled """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    mean_diff_piezorep, fit_res = example_mean_hyst(phase='2', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(0.010127980148713238, rel=1e-2)
    assert fit_res[1] == approx(-0.006336912648294382, rel=1e-2)
    assert fit_res[2] == approx(0.6256837548303733, rel=1e-2)
    assert fit_res[3] == approx(0.9993101829453003, rel=1e-2)
    assert np.sum(mean_diff_piezorep) == approx(
        -0.22805254243375853, rel=1e-2)
