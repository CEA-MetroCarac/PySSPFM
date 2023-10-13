"""
Test analysis methods
"""
from pytest import approx
import numpy as np

from examples.utils.nanoloop.ex_analysis import example_analysis


# class TestAnalysis(unittest.TestCase):


def test_analysis_on():
    """ Test example_analysis mode 'on' field """

    loop_tab, mean_loop, init_meas, ckpfm_loop_dict = example_analysis('on')

    prs_l = np.sum([loop.piezorep_left for loop in loop_tab])
    prs_r = np.sum([loop.piezorep_right for loop in loop_tab])
    phase = np.sum([loop.treat_pha for loop in loop_tab])
    amps_mark = np.sum([loop.amp_marker for loop in loop_tab])
    pr_l = np.sum(mean_loop.piezorep_left)
    pr_r = np.sum(mean_loop.piezorep_right)
    amp_mark = np.sum(mean_loop.amp_marker)

    assert ckpfm_loop_dict == {}
    assert init_meas['amp'] == approx(1.1114887643999471)
    assert init_meas['pha'] == approx(184.23485476198212)
    assert prs_l == approx(2080.2335233259655)
    assert prs_r == approx(709.5950689068047)
    assert amps_mark == approx(144.83436060090833)
    assert phase == approx(131445.90458320786)
    assert pr_l == approx(520.0583808314913)
    assert pr_r == approx(177.39876722670124)
    assert amp_mark == approx(36.20859015022709)


def test_analysis_off():
    """ Test example_analysis mode 'off' field """

    out = example_analysis('off')
    (loop_tab, mean_loop, init_meas, ckpfm_loop_dict) = out
    piezorep = np.array(ckpfm_loop_dict['piezorep'])
    prs_l = np.sum([loop.piezorep_left for loop in loop_tab])
    prs_r = np.sum([loop.piezorep_right for loop in loop_tab])
    phase = np.sum([loop.treat_pha for loop in loop_tab])
    amps_mark = np.sum([loop.amp_marker for loop in loop_tab])
    pr_l = np.sum(mean_loop.piezorep_left)
    pr_r = np.sum(mean_loop.piezorep_right)
    amp_mark = np.sum(mean_loop.amp_marker)

    assert init_meas['amp'] == approx(1.4189108225846916)
    assert init_meas['pha'] == approx(0.0)
    assert np.sum(ckpfm_loop_dict['write volt']) == approx(
        2.2737367544323206e-13)

    assert piezorep.shape[0] == 400
    assert piezorep.shape[1] == 4
    assert np.sum(piezorep) == approx(2753.8277139862294)
    assert ckpfm_loop_dict['read volt'][0] == approx(-1.0)
    assert ckpfm_loop_dict['read volt'][1] == approx(-0.33333333333333337)

    assert ckpfm_loop_dict['read volt'][2] == approx(0.33333333333333326)

    assert ckpfm_loop_dict['read volt'][3] == approx(1.0)
    assert prs_l == approx(2080.1814251520286)
    assert prs_r == approx(686.1010077516336)
    assert amps_mark == approx(32.85924605451086)
    assert phase == approx(90051.47828723147)
    assert pr_l == approx(520.0453562880072)
    assert pr_r == approx(171.52525193790837)
    assert amp_mark == approx(8.214811513627716)
