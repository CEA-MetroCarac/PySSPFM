"""
Test spm_converter methods
"""
from pytest import approx, skip
import numpy as np

from PySSPFM.utils.raw_extraction import NanoscopeError
from examples.toolbox.ex_spm_converter import example_spm_converter


# class TestExtract(unittest.TestCase):

def test_spm_converter_txt():
    """ Test example_spm_converter in txt file """
    try:
        dict_meas, script_dict = example_spm_converter('txt')
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    sum_dict = np.sum([np.sum(val) for val in dict_meas.values()])

    target_script = {'Write Voltage Range (V)': (-10, 10),
                     'Write Number of Voltages': 51,
                     'Write Wave Form': 'Zero, up',
                     'Measurements Per Write': None,
                     'Write Segment Duration (ms)': 50,
                     'Write Samples Per Segment': 100,
                     'Read Voltage Range (V)': (0, 0),
                     'Read Number of Voltages': 8,
                     'Read Wave Form': 'Low to High',
                     'Measurements Per Read': None,
                     'Read Segment Duration (ms)': 50,
                     'Read Samples Per Segment': 100,
                     'Frequency Range (kHz)': (None, None)}

    assert sum_dict == approx(9691899.026586428)
    for key, value in target_script.items():
        assert script_dict[key] == value


def test_spm_converter_csv():
    """ Test example_spm_converter in csv file """
    try:
        dict_meas, script_dict = example_spm_converter('csv')
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    sum_dict = np.sum([np.sum(val) for val in dict_meas.values()])

    target_script = {'Write Voltage Range (V)': (-10, 10),
                     'Write Number of Voltages': 51,
                     'Write Wave Form': 'Zero, up',
                     'Measurements Per Write': None,
                     'Write Segment Duration (ms)': 50,
                     'Write Samples Per Segment': 100,
                     'Read Voltage Range (V)': (0, 0),
                     'Read Number of Voltages': 8,
                     'Read Wave Form': 'Low to High',
                     'Measurements Per Read': None,
                     'Read Segment Duration (ms)': 50,
                     'Read Samples Per Segment': 100,
                     'Frequency Range (kHz)': (None, None)}

    assert sum_dict == approx(9692740.52322312)
    for key, value in target_script.items():
        assert script_dict[key] == value


def test_spm_converter_xlsx():
    """ Test example_spm_converter in xlsx file """
    try:
        dict_meas, script_dict = example_spm_converter('xlsx')
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    sum_dict = np.sum([np.sum(val) for val in dict_meas.values()])

    target_script = {'Write Voltage Range (V)': (-10, 10),
                     'Write Number of Voltages': 51,
                     'Write Wave Form': 'Zero, up',
                     'Measurements Per Write': None,
                     'Write Segment Duration (ms)': 50,
                     'Write Samples Per Segment': 100,
                     'Read Voltage Range (V)': (0, 0),
                     'Read Number of Voltages': 8,
                     'Read Wave Form': 'Low to High',
                     'Measurements Per Read': None,
                     'Read Segment Duration (ms)': 50,
                     'Read Samples Per Segment': 100,
                     'Frequency Range (kHz)': (None, None)}

    assert sum_dict == approx(9692740.52322312)
    for key, value in target_script.items():
        assert script_dict[key] == value
