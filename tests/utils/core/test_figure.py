"""
Test figure methods
"""

from examples.utils.core.ex_figure import \
    ex_plot_graph, ex_plot_hist, ex_plot_map


def test_plot_graph():
    """ Test ex_plot_graph """

    fig = ex_plot_graph()
    assert len(list(fig)) == 1


def test_plot_hist():
    """ Test ex_plot_hist """

    fig = ex_plot_hist()
    assert len(list(fig)) == 1


def test_plot_map():
    """ Test ex_plot_map """

    fig = ex_plot_map()
    assert len(list(fig)) == 1
