"""
Test plot methods
"""

from examples.utils.seg_to_loop.ex_plot import \
    ex_plt_bias, ex_plt_amp, ex_plt_signals, ex_amp_pha_map, ex_segments


# class TestPlot(unittest.TestCase):


def test_plt_bias():
    """ Test ex_plt_bias """
    ex_plt_bias()


def test_plt_amp():
    """ Test ex_plt_amp """
    ex_plt_amp()


def test_plt_signals():
    """ Test ex_plt_signals """
    ex_plt_signals()


def test_amp_pha_map_max():
    """ Test ex_amp_pha_map """

    ex_amp_pha_map('max', 'off f')


def test_amp_pha_map_dfrt():
    """ Test ex_amp_pha_map """

    ex_amp_pha_map('dfrt', 'off f')


def test_segments_max():
    """ Test ex_segments 'max' mode """
    ex_segments('max', 'off f', make_plots=True)


def test_segments_fit():
    """ Test ex_segments 'fit' mode """
    ex_segments('fit', 'off f', make_plots=True)


def test_segments_dfrt():
    """ Test ex_segments 'dfrt' mode """
    ex_segments('dfrt', 'off f', make_plots=True)
