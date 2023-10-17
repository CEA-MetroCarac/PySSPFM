"""
Test mean_loop methods
"""
from pytest import approx
import numpy as np

from examples.toolbox.ex_mean_loop import example_mean_loop


# class TestMeanLoop(unittest.TestCase):


def test_mean_loop_1_on():
    """ Test mean_loop function: select phase 1, on field """

    mean_best_loop, best_hysts = example_mean_loop(phase='1', mode='on')

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep) == approx(0.013894300140924453)
    assert np.sum(mean_best_loop.pha) == approx(8162.9121683673475)
    assert np.sum(mean_best_loop.amp) == approx(0.07878820642891968)
    assert np.sum(best_hysts.params) == approx(2.7083908411461195)
    assert np.sum(list(best_hysts.props.values())) == approx(12.554442526538555,
                                                             abs=1e-6)


def test_mean_loop_1_off():
    """ Test mean_loop function: select phase 1, off field """

    mean_best_loop, best_hysts = example_mean_loop(phase='1', mode='off')

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep) == approx(0.010593325340580346)
    assert np.sum(mean_best_loop.pha) == approx(7872.582328571429)
    assert np.sum(mean_best_loop.amp) == approx(0.05025387861725987)
    assert np.sum(best_hysts.params) == approx(0.9034962392174538)
    assert np.sum(list(best_hysts.props.values())) == approx(14.569503871304713)


def test_mean_loop_1_coupled():
    """ Test mean_loop function: select phase 1, coupled """

    mean_diff_piezorep, fit_res = example_mean_loop(phase='1', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(-0.00022698554219434226, abs=1e-8)
    assert fit_res[1] == approx(0.00014247330929064136)
    assert fit_res[2] == approx(0.6276757008984186)
    assert fit_res[3] == approx(0.999334257370327)
    assert np.sum(mean_diff_piezorep) == approx(0.005286339592318832)


def test_mean_loop_2_on():
    """ Test mean_loop function: select phase 2, on field """

    mean_best_loop, best_hysts = example_mean_loop(phase='2', mode='on')

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep) == approx(0.008748704931341604)
    assert np.sum(mean_best_loop.pha) == approx(8432.661070699709)
    assert np.sum(mean_best_loop.amp) == approx(0.09628777682066487)
    assert np.sum(best_hysts.params) == approx(2.3476624929724266)
    assert np.sum(list(best_hysts.props.values())) == approx(12.145800505900846)


def test_mean_loop_2_off():
    """ Test mean_loop function: select phase 2, off field """

    mean_best_loop, best_hysts = example_mean_loop(phase='2', mode='off')

    # print(np.sum(mean_best_loop.piezorep))
    # print(np.sum(mean_best_loop.pha))
    # print(np.sum(mean_best_loop.amp))
    # print(np.sum(best_hysts.params))
    # print(np.sum(list(best_hysts.props.values())))

    assert np.sum(mean_best_loop.piezorep) == approx(0.011137901732232256)
    assert np.sum(mean_best_loop.pha) == approx(6975.453306122449, abs=1e-2)
    assert np.sum(mean_best_loop.amp) == approx(0.02825795313366302)
    assert np.sum(best_hysts.params) == approx(0.5378600460241104)
    assert np.sum(list(best_hysts.props.values())) == approx(23.03784757853354)


def test_mean_loop_2_coupled():
    """ Test mean_loop function: select phase 2, coupled """

    mean_diff_piezorep, fit_res = example_mean_loop(phase='2', mode='coupled')

    # print(fit_res[0])
    # print(fit_res[1])
    # print(fit_res[2])
    # print(fit_res[3])
    # print(np.sum(mean_diff_piezorep))

    assert fit_res[0] == approx(-0.0002861700476343689, abs=1e-8)
    assert fit_res[1] == approx(0.00013029822120773734, abs=1e-8)
    assert fit_res[2] == approx(0.4553174669566242)
    assert fit_res[3] == approx(0.9988143410969148)
    assert np.sum(mean_diff_piezorep) == approx(0.004077805282110943)
