"""
Test phase_inversion_analyzer methods
"""
from pytest import skip

from examples.toolbox.ex_phase_inversion_analyzer import \
    example_phase_inversion_analyzer
from PySSPFM.utils.raw_extraction import NanoscopeError


# class TestCorrelation(unittest.TestCase):


def test_phase_inversion_analyzer():
    """ Test phase_inversion_analyzer """
    try:
        phase_grad_tab, map_dim = example_phase_inversion_analyzer()
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    # print(phase_grad_tab['Grad On field'])
    # print(phase_grad_tab['Grad Off field'])
    # print(phase_grad_tab['Revert On Off'])

    target_on_field = [False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False]
    target_off_field = [True, True, True, True, True, True, True, True, True,
                        True, True, True, True, True, True, True, True, True,
                        True, True, True]
    target_revert_on_off = [True, True, True, True, True, True, True, True,
                            True, True, True, True, True, True, True, True,
                            True, True, True, True, True]

    assert phase_grad_tab['Grad On field'] == target_on_field
    assert phase_grad_tab['Grad Off field'] == target_off_field
    assert phase_grad_tab['Revert On Off'] == target_revert_on_off
    assert map_dim == {'x mic': 50, 'x pix': 50, 'y mic': 3, 'y pix': 3}
