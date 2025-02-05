"""
Test analysis methods
"""
import os
from pytest import approx, skip
import numpy as np

from examples.utils.datacube_to_nanoloop.ex_analysis import \
    ex_calib, ex_cut_function, ex_segments, ex_extract_other_properties


# class TestAnalysis(unittest.TestCase):


def test_calib():
    """ Test ex_calib """

    amp_external, pha_external, amp_cal_external = ex_calib()

    assert np.sum(amp_external) == approx(48085791.44687746)
    assert np.sum(pha_external) == approx(17219838.632536672)
    assert np.sum(amp_cal_external) == approx(24042895.72343873)


def test_cut_function():
    """ Test ex_cut_function """

    cut_dict, nb_seg_tot = ex_cut_function()
    assert cut_dict['off f'][0] == 120
    assert cut_dict['off f'][-1] == 195920
    assert cut_dict['on f'][0] == 20
    assert cut_dict['on f'][-1] == 195820
    assert np.sum(cut_dict['off f']) == 96059600
    assert np.sum(cut_dict['on f']) == 95961600
    assert nb_seg_tot == 1960


def test_segments_max_on():
    """ Test ex_segments on field, with 'max' analysis """

    seg = ex_segments('max', 'on f')

    # print(seg.amp)
    # print(np.sum(seg.amp_tab))
    # print(np.sum(seg.amp_tab_init))
    # print(np.sum(seg.freq_tab))
    # print(np.sum(seg.freq_tab_init))
    # print(seg.pha)
    # print(np.sum(seg.pha_tab))
    # print(np.sum(seg.pha_tab_init))
    # print(seg.q_fact)
    # print(seg.res_freq)
    # print(np.sum(seg.time_tab))
    # print(np.sum(seg.time_tab_init))

    assert seg.amp == approx(2012.7048661231383)
    assert np.sum(seg.amp_tab) == approx(10881.912337393867)
    assert np.sum(seg.amp_tab_init) == approx(11438.773117664969)
    assert seg.bckgnd is None
    assert seg.best_fit == []
    assert seg.end_ind == 910
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.len == 80
    assert seg.pha == approx(125.71207649637046)
    assert seg.pha_best_fit == []
    assert np.sum(seg.pha_tab) == approx(11973.066691195469)
    assert np.sum(seg.pha_tab_init) == approx(15566.80339447678)
    assert seg.q_fact == approx(163.0)
    assert seg.res_freq == 326.0
    assert seg.start_ind == 830
    assert np.sum(seg.time_tab) == approx(34.0)
    assert np.sum(seg.time_tab_init) == approx(42.5)


def test_segments_max_off():
    """ Test ex_segments off field, with 'max' analysis """

    seg = ex_segments('max', 'off f')

    # print(seg.amp)
    # print(np.sum(seg.amp_tab))
    # print(np.sum(seg.amp_tab_init))
    # print(np.sum(seg.freq_tab))
    # print(np.sum(seg.freq_tab_init))
    # print(seg.pha)
    # print(np.sum(seg.pha_tab))
    # print(np.sum(seg.pha_tab_init))
    # print(seg.q_fact)
    # print(seg.res_freq)
    # print(np.sum(seg.time_tab))
    # print(np.sum(seg.time_tab_init))

    assert seg.amp == approx(1701.4644734367341)
    assert np.sum(seg.amp_tab) == approx(9383.733235635878)
    assert np.sum(seg.amp_tab_init) == approx(9971.142229811065)
    assert seg.bckgnd is None
    assert seg.best_fit == []
    assert seg.end_ind == 1010
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.len == 80
    assert seg.pha == approx(226.59664881153964)
    assert seg.pha_best_fit == []
    assert np.sum(seg.pha_tab) == approx(13323.539465541126)
    assert np.sum(seg.pha_tab_init) == approx(16557.26211717034)
    assert seg.q_fact == approx(74.0)
    assert seg.res_freq == 296.0
    assert seg.start_ind == 930
    assert np.sum(seg.time_tab) == approx(38.0)
    assert np.sum(seg.time_tab_init) == approx(47.5)


def test_segments_fit_on():
    """ Test ex_segments on field, with 'fit' analysis """

    seg = ex_segments('fit', 'on f')

    # print(seg.amp)
    # print(np.sum(seg.amp_tab))
    # print(np.sum(seg.amp_tab_init))
    # print(seg.bckgnd)
    # print(np.sum(seg.best_fit))
    # print(np.sum(seg.freq_tab))
    # print(np.sum(seg.freq_tab_init))
    # print(seg.pha)
    # print(np.sum(seg.pha_best_fit))
    # print(np.sum(seg.pha_tab))
    # print(np.sum(seg.pha_tab_init))
    # print(seg.q_fact)
    # print(seg.res_freq)
    # print(np.sum(seg.time_tab))
    # print(np.sum(seg.time_tab_init))

    assert seg.amp == approx(3774.8297802368393, abs=1e-3)
    assert np.sum(seg.amp_tab) == approx(10881.912337393867)
    assert np.sum(seg.amp_tab_init) == approx(11438.773117664969)
    assert seg.bckgnd == approx(12.518852685044568)
    assert np.sum(seg.best_fit) == approx(10881.9123373826)
    assert seg.end_ind == 910
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.len == 80
    assert seg.pha == approx(179.37831666015322)
    assert np.sum(seg.pha_best_fit) == approx(12037.411509536036)
    assert np.sum(seg.pha_tab) == approx(11973.066691195469)
    assert np.sum(seg.pha_tab_init) == approx(15566.80339447678)
    assert seg.q_fact == approx(343.3272390563352, abs=1e-4)
    assert seg.res_freq == approx(326.76409251747384)
    assert seg.start_ind == 830
    assert np.sum(seg.time_tab) == approx(34.0)
    assert np.sum(seg.time_tab_init) == approx(42.5)


def test_segments_fit_off():
    """ Test ex_segments off field, with 'fit' analysis """

    seg = ex_segments('fit', 'off f')

    # print(seg.amp)
    # print(np.sum(seg.amp_tab))
    # print(np.sum(seg.amp_tab_init))
    # print(seg.bckgnd)
    # print(np.sum(seg.best_fit))
    # print(np.sum(seg.freq_tab))
    # print(np.sum(seg.freq_tab_init))
    # print(seg.pha)
    # print(np.sum(seg.pha_best_fit))
    # print(np.sum(seg.pha_tab))
    # print(np.sum(seg.pha_tab_init))
    # print(seg.q_fact)
    # print(seg.res_freq)
    # print(np.sum(seg.time_tab))
    # print(np.sum(seg.time_tab_init))

    assert seg.amp == approx(4095.160211311271, abs=1e-3)
    assert np.sum(seg.amp_tab) == approx(9383.733235635878)
    assert np.sum(seg.amp_tab_init) == approx(9971.142229811065)
    assert seg.bckgnd == approx(1.8890050339911803e-13)
    assert np.sum(seg.best_fit) == approx(9697.147279262597)
    assert seg.end_ind == 1010
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.len == 80
    assert seg.pha == approx(183.25126624314055)
    assert np.sum(seg.pha_best_fit) == approx(13205.780336868818)
    assert np.sum(seg.pha_tab) == approx(13323.539465541126)
    assert np.sum(seg.pha_tab_init) == approx(16557.26211717034)
    assert seg.q_fact == approx(341.7160661770409, abs=1e-4)
    assert seg.res_freq == approx(295.0595059372857)
    assert seg.start_ind == 930
    assert np.sum(seg.time_tab) == approx(38.0)
    assert np.sum(seg.time_tab_init) == approx(47.5)


def test_segments_dfrt_on():
    """ Test ex_segments on field, with 'dfrt' analysis """

    seg = ex_segments('dfrt', 'on f')

    # print(seg.amp)
    # print(np.sum(seg.amp_tab))
    # print(np.sum(seg.amp_tab_init))
    # print(np.sum(seg.freq_tab))
    # print(np.sum(seg.freq_tab_init))
    # print(seg.pha)
    # print(np.sum(seg.pha_tab))
    # print(np.sum(seg.pha_tab_init))
    # print(seg.q_fact)
    # print(seg.res_freq)
    # print(np.sum(seg.time_tab))
    # print(np.sum(seg.time_tab_init))

    assert seg.amp == approx(30.05119398728839)
    assert np.sum(seg.amp_tab) == approx(2404.095518983071)
    assert np.sum(seg.amp_tab_init) == approx(2974.1984182330775)
    assert seg.end_ind == 910
    assert np.sum(seg.freq_tab) is None
    assert np.sum(seg.freq_tab_init) is None
    assert seg.inc_amp == approx(0.6291232603935817)
    assert seg.inc_pha == approx(2.0731919158003196)
    assert seg.len == 80
    assert seg.pha == approx(90.9675711197639)
    assert np.sum(seg.pha_tab) == approx(7277.405689581113)
    assert np.sum(seg.pha_tab_init) == approx(8996.054642657837)
    assert seg.start_ind == 830
    assert np.sum(seg.time_tab) == approx(34.0)
    assert np.sum(seg.time_tab_init) == approx(42.5)


def test_segments_dfrt_off():
    """ Test ex_segments off field, with 'dfrt' analysis """

    seg = ex_segments('dfrt', 'off f')

    # print(seg.amp)
    # print(np.sum(seg.amp_tab))
    # print(np.sum(seg.amp_tab_init))
    # print(np.sum(seg.freq_tab))
    # print(np.sum(seg.freq_tab_init))
    # print(seg.pha)
    # print(np.sum(seg.pha_tab))
    # print(np.sum(seg.pha_tab_init))
    # print(seg.q_fact)
    # print(seg.res_freq)
    # print(np.sum(seg.time_tab))
    # print(np.sum(seg.time_tab_init))

    assert seg.amp == approx(36.87806856414231)
    assert np.sum(seg.amp_tab) == approx(2950.245485131385)
    assert np.sum(seg.amp_tab_init) == approx(3655.151450529881)
    assert seg.end_ind == 1010
    assert np.sum(seg.freq_tab) is None
    assert np.sum(seg.freq_tab_init) is None
    assert seg.inc_amp == approx(0.6835243969792533)
    assert seg.inc_pha == approx(1.5333272675407086)
    assert seg.len == 80
    assert seg.pha == approx(72.0800326320837)
    assert np.sum(seg.pha_tab) == approx(5766.402610566696)
    assert np.sum(seg.pha_tab_init) == approx(7132.943058414065)
    assert seg.start_ind == 930
    assert np.sum(seg.time_tab) == approx(38.0)
    assert np.sum(seg.time_tab_init) == approx(47.5)


def test_extract_other_properties():
    """ Test ex_extract_other_properties """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    other_properties, height_tab, deflection_tab = ex_extract_other_properties()

    # print(other_properties['height'])
    # print(other_properties['deflection'])
    # print(other_properties['deflection error'])
    # print(other_properties['adhesion approach'])
    # print(other_properties['adhesion retract'])
    # print(np.sum(height_tab))
    # print(np.sum(deflection_tab))

    assert other_properties['height'] == approx(521.1579825588465)
    assert other_properties['deflection'] == approx(19.673814725026293)
    assert other_properties['deflection error'] == approx(0.27821102040834866)
    assert other_properties['adhesion approach'] == approx(12.350508256155033)
    assert other_properties['adhesion retract'] == approx(59.93650761460044)
    assert np.sum(height_tab) == approx(103293189.1668825)
    assert np.sum(deflection_tab) == approx(3850966.2500644387)
