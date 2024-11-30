"""
Test meas_sheet_generator methods
"""
from pytest import approx, skip

from examples.toolbox.ex_meas_sheet_generator import \
    example_meas_sheet_generator
from PySSPFM.utils.raw_extraction import NanoscopeError


# class TestSignalViewer(unittest.TestCase):


def test_meas_sheet_generator():
    """ Test example_meas_sheet_generator """
    try:
        indexs, values = example_meas_sheet_generator()
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    indexs_target = ['B4', 'C4', 'D4', 'B16', 'C16', 'D16', 'E16', 'F16',
                     'G16', 'H16', 'I16', 'J16', 'K16', 'L16', 'M16', 'N16',
                     'O16', 'P16', 'Q16', 'D22', 'F22']

    assert indexs == indexs_target
    assert values[0] == 'PIT_SSPFM_DFRT_T2ms_map.0_00000.spm'
    assert values[1] == 'PIT_SSPFM_DFRT_T2ms_map.0_00000.spm'
    assert values[2] == '22h : 26/11/2024'
    assert values[3] == -10.0
    assert values[4] == 10.0
    assert values[5] == 50
    assert values[6] == 'Zero, up'
    assert values[7] == approx(1.9999999949504854)
    assert values[8] == 100
    assert values[9] == 0.0
    assert values[10] == 0.0
    assert values[11] == 10
    assert values[12] == 'Single Read Step'
    assert values[13] == approx(1.9999999949504854)
    assert values[14] == 100
    assert values[15] == approx(224.9799994319801)
    assert values[16] == 2183
    assert values[17] == approx(124.97999968445583)
    assert values[18] == 2083
