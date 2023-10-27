"""
Test electrostatic methods
"""
from pytest import approx
import numpy as np

from examples.utils.hyst_to_map.ex_electrostatic import \
    (ex_btfly_analysis, ex_offset_analysis, ex_plot_on_off_field,
     ex_differential_analysis, ex_sat_analysis)


# class TestElectrostatic(unittest.TestCase):


def test_btfly_analysis():
    """ Test ex_btfly_analysis """

    imprint = ex_btfly_analysis()

    assert imprint == approx(0.2500000000000009)


def test_sat_analysis():
    """ Test ex_sat_analysis """

    sat_res = ex_sat_analysis()

    assert np.sum(list(sat_res.values())) == approx(-2.2475045978511963)


def test_offset_analysis():
    """ Test ex_offset_analysis """

    offset_res = ex_offset_analysis()

    assert np.sum(list(offset_res.values())) == approx(-0.8153937580539776)


def test_differential_analysis():
    """ Test ex_differential_analysis """

    diff_res = ex_differential_analysis()

    assert np.sum(list(diff_res.values())) == approx(-4.011985086147616)


def test_plot_on_off_field():
    """ Test ex_plot_on_off_field """

    fig = ex_plot_on_off_field()

    assert len(list(fig)) == 1
