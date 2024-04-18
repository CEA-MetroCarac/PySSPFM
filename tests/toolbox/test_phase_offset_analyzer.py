"""
Test phase_offset_analyzer methods
"""
from pytest import approx, skip
import numpy as np

from examples.toolbox.ex_phase_offset_analyzer import \
    example_phase_offset_analyzer
from PySSPFM.utils.raw_extraction import NanoscopeError


# class TestCorrelation(unittest.TestCase):


def test_phase_offset_analyzer():
    """ Test phase_offset_analyzer """
    try:
        phase_offset_tab, map_dim = example_phase_offset_analyzer()
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    # print(np.nansum(phase_offset_tab['On field']))
    # print(np.nansum(phase_offset_tab['Off field']))
    # print(np.nansum(phase_offset_tab['Mean']))

    assert np.nansum(phase_offset_tab['On field']) == approx(1644.3122963182652)
    assert np.nansum(phase_offset_tab['Off field']) == \
           approx(1677.1248775829279)
    assert np.nansum(phase_offset_tab['Mean']) == approx(1750.3109771168647)
    assert map_dim == {'x mic': 50, 'x pix': 50, 'y mic': 3, 'y pix': 3}
