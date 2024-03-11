"""
Test spm_data_extractor methods
"""
from pytest import approx, skip

from examples.toolbox.ex_spm_data_extractor import example_spm_data_extractor
from PySSPFM.utils.raw_extraction import NanoscopeError


# class TestSignalViewer(unittest.TestCase):


def test_spm_data_extractor():
    """ Test example_spm_data_extractor """
    try:
        raw_dict, sspfm_pars, other_pars = example_spm_data_extractor()
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    # print(sum(raw_dict['Height Sensor (nm)']))
    # print(sum(raw_dict['DeflectionIn1B (nm)']))
    # print(sum(raw_dict['Tip Bias (V)']))
    # print(sum(raw_dict['Input3 (V)']))
    # print(sum(raw_dict['HS PR Inphase (mV)']))
    # print(sum(raw_dict['HS PR Quadrature (mV)']))
    # print(sum(raw_dict['time']))

    target_sspfm_pars = {
        'Write Voltage Range V': (-10.0, 10.0),
        'Write Number of Voltages': 50,
        'Write Wave Form': 'Zero, up',
        'Read Voltage Range V': (0.0, 0.0),
        'Read Number of Voltages': 10,
        'Read Wave Form': 'Single Read Step',
        'Hold seg durat (start) [ms]': 224.9799994319801,
        'Hold seg durat (end) [ms]': 124.97999968445583,
        'Hold sample (start)': 2183,
        'Hold sample (end)': 2083,
        'Seg durat (W) [ms]': 1.9999999949504854,
        'Seg durat (R) [ms]': 1.9999999949504854,
        'Seg sample (W)': 100,
        'Seg sample (R)': 100}

    target_other_pars = {
        'Drive Amplitude (mV)': 1000,
        'Frequency Range (kHz)': (250.0, 290.0),
        'Measurements Per Read': 0,
        'Measurements Per Write': 0,
        'Ramp Size (nm)': 500,
        'Tip Velocity (nm/s)': 250000}

    assert sum(raw_dict['Height Sensor (nm)']) == approx(-161194473.8288371)
    assert sum(raw_dict['DeflectionIn1B (nm)']) == approx(3641189.304666089)
    assert sum(raw_dict['Tip Bias (V)']) == approx(352189.1660686493)
    assert sum(raw_dict['Input3 (V)']) == approx(21524.888588209647)
    assert sum(raw_dict['HS PR Inphase (mV)']) == approx(-16577.014125154652)
    assert sum(raw_dict['HS PR Quadrature (mV)']) == approx(-23542.98436844107)
    assert sum(raw_dict['time']) == approx(437165.7685962211)

    assert sspfm_pars == target_sspfm_pars
    assert other_pars == target_other_pars
