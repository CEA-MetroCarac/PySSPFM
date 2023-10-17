"""
Test analysis methods
"""
from pytest import approx
import numpy as np

from examples.utils.seg_to_loop.ex_analysis import \
    ex_calib, ex_init_parameters, ex_segments


# class TestAnalysis(unittest.TestCase):


def test_calib():
    """ Test ex_calib """

    amp_zi_dfrt, pha_zi_dfrt, amp_cal_dfrt = ex_calib()

    assert np.sum(amp_zi_dfrt) == approx(48085791.44687746)
    assert np.sum(pha_zi_dfrt) == approx(17219838.632536672)
    assert np.sum(amp_cal_dfrt) == approx(24042895.72343873)


def test_init_parameters():
    """ Test ex_init_parameters """

    cut_dict, read_mode = ex_init_parameters()
    assert cut_dict['index hold']['start'][0] == 0
    assert cut_dict['index hold']['start'][1] == 19
    assert cut_dict['index hold']['end'][0] == 196021
    assert cut_dict['index hold']['end'][1] == 196040
    assert np.sum(cut_dict['start hold seg']) == approx(9.499999999999998)

    assert np.sum(cut_dict['end hold seg']) == approx(1890.4999999999338)

    assert np.sum(cut_dict['index on field']) == approx(95961600)
    assert np.sum(cut_dict['index off field']) == approx(96059600)
    assert cut_dict['nb seg'] == 1960
    assert cut_dict['experimental time'] == approx(99.94999999999652)
    assert cut_dict['start hold time exp'] == 1.0
    assert cut_dict['end hold time exp'] == approx(0.9500000000000028)

    assert cut_dict['theoretical time'] == 99.95
    assert read_mode == 'Single Read Step'


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
    assert seg.cut_seg == {'start': 10, 'end': 10}
    assert seg.end_ind == 910
    assert seg.end_ind_init == 920
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.inc_amp is None
    assert seg.inc_pha is None
    assert seg.len == 80
    assert seg.len_init == 100
    assert seg.pha == approx(125.71207649637046)
    assert seg.pha_best_fit == []
    assert np.sum(seg.pha_tab) == approx(11973.066691195469)
    assert np.sum(seg.pha_tab_init) == approx(15566.80339447678)
    assert seg.q_fact == approx(163.0)
    assert seg.res_freq == 326.0
    assert seg.start_ind == 830
    assert seg.start_ind_init == 820
    assert np.sum(seg.time_tab) == approx(114.00000000000003)
    assert np.sum(seg.time_tab_init) == approx(142.50000000000003)


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
    assert seg.cut_seg == {'start': 10, 'end': 10}
    assert seg.end_ind == 1010
    assert seg.end_ind_init == 1020
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.inc_amp is None
    assert seg.inc_pha is None
    assert seg.len == 80
    assert seg.len_init == 100
    assert seg.pha == approx(226.59664881153964)
    assert seg.pha_best_fit == []
    assert np.sum(seg.pha_tab) == approx(13323.539465541126)
    assert np.sum(seg.pha_tab_init) == approx(16557.26211717034)
    assert seg.q_fact == approx(74.0)
    assert seg.res_freq == 296.0
    assert seg.start_ind == 930
    assert seg.start_ind_init == 920
    assert np.sum(seg.time_tab) == approx(118.00000000000003)
    assert np.sum(seg.time_tab_init) == approx(147.50000000000003)


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

    assert seg.amp == approx(3774.8297802368393, abs=1e-5)
    assert np.sum(seg.amp_tab) == approx(10881.912337393867)
    assert np.sum(seg.amp_tab_init) == approx(11438.773117664969)
    assert seg.bckgnd == approx(12.518852685044568)
    assert np.sum(seg.best_fit) == approx(10881.9123373826)
    assert seg.cut_seg == {'start': 10, 'end': 10}
    assert seg.end_ind == 910
    assert seg.end_ind_init == 920
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.inc_amp is None
    assert seg.inc_pha is None
    assert seg.len == 80
    assert seg.len_init == 100
    assert seg.pha == approx(179.37831666015322)
    assert np.sum(seg.pha_best_fit) == approx(12037.411509536036)
    assert np.sum(seg.pha_tab) == approx(11973.066691195469)
    assert np.sum(seg.pha_tab_init) == approx(15566.80339447678)
    assert seg.q_fact == approx(343.3272390563352)
    assert seg.res_freq == approx(326.76409251747384)
    assert seg.start_ind == 830
    assert seg.start_ind_init == 820
    assert np.sum(seg.time_tab) == approx(114.00000000000003)
    assert np.sum(seg.time_tab_init) == approx(142.50000000000003)


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

    assert seg.amp == approx(4095.160211311271, abs=1e-5)
    assert np.sum(seg.amp_tab) == approx(9383.733235635878)
    assert np.sum(seg.amp_tab_init) == approx(9971.142229811065)
    assert seg.bckgnd == approx(1.8890050339911803e-13)
    assert np.sum(seg.best_fit) == approx(9697.147279262597)
    assert seg.cut_seg == {'start': 10, 'end': 10}
    assert seg.end_ind == 1010
    assert seg.end_ind_init == 1020
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.inc_amp is None
    assert seg.inc_pha is None
    assert seg.len == 80
    assert seg.len_init == 100
    assert seg.pha == approx(183.25126624314055)
    assert np.sum(seg.pha_best_fit) == approx(13205.780336868818)
    assert np.sum(seg.pha_tab) == approx(13323.539465541126)
    assert np.sum(seg.pha_tab_init) == approx(16557.26211717034)
    assert seg.q_fact == approx(341.7160661770409, abs=1e-6)
    assert seg.res_freq == approx(295.0595059372857)
    assert seg.start_ind == 930
    assert seg.start_ind_init == 920
    assert np.sum(seg.time_tab) == approx(118.00000000000003)
    assert np.sum(seg.time_tab_init) == approx(147.50000000000003)


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
    assert seg.bckgnd is None
    assert seg.best_fit == []
    assert seg.cut_seg == {'start': 10, 'end': 10}
    assert seg.end_ind == 910
    assert seg.end_ind_init == 920
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.inc_amp == approx(0.6291232603935817)
    assert seg.inc_pha == approx(2.0731919158003196)
    assert seg.len == 80
    assert seg.len_init == 100
    assert seg.pha == approx(90.9675711197639)
    assert seg.pha_best_fit == []
    assert np.sum(seg.pha_tab) == approx(7277.405689581113)
    assert np.sum(seg.pha_tab_init) == approx(8996.054642657837)
    assert seg.q_fact is None
    assert seg.res_freq is None
    assert seg.start_ind == 830
    assert seg.start_ind_init == 820
    assert np.sum(seg.time_tab) == approx(114.00000000000003)
    assert np.sum(seg.time_tab_init) == approx(142.50000000000003)


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
    assert seg.bckgnd is None
    assert seg.best_fit == []
    assert seg.cut_seg == {'start': 10, 'end': 10}
    assert seg.end_ind == 1010
    assert seg.end_ind_init == 1020
    assert seg.error == ''
    assert np.sum(seg.freq_tab) == approx(23920.0)
    assert np.sum(seg.freq_tab_init) == approx(29900.0)
    assert seg.inc_amp == approx(0.6835243969792533)
    assert seg.inc_pha == approx(1.5333272675407086)
    assert seg.len == 80
    assert seg.len_init == 100
    assert seg.pha == approx(72.0800326320837)
    assert seg.pha_best_fit == []
    assert np.sum(seg.pha_tab) == approx(5766.402610566696)
    assert np.sum(seg.pha_tab_init) == approx(7132.943058414065)
    assert seg.q_fact is None
    assert seg.res_freq is None
    assert seg.start_ind == 930
    assert seg.start_ind_init == 920
    assert np.sum(seg.time_tab) == approx(118.00000000000003)
    assert np.sum(seg.time_tab_init) == approx(147.50000000000003)
