"""
Test raw_extraction methods
"""
from pytest import approx, skip
import numpy as np

from PySSPFM.utils.raw_extraction import NanoscopeError
from examples.utils.ex_raw_extraction import \
    ex_data_extraction, ex_csv_meas_sheet_extract


# class TestExtract(unittest.TestCase):

def test_data_extraction_spm():
    """ Test ex_data_extraction '.spm' file """
    try:
        dict_meas, script_dict = ex_data_extraction('spm')
    except NanoscopeError:
        skip("Test skipped (NanoscopeError): spm file can't be opened without "
             "Nanoscope Analysis DLL")

    sum_dict = np.sum(list(dict_meas.values())[0:4])
    tab_script = list(script_dict.values())

    assert sum_dict == approx(13119195.087875232)
    assert tab_script[0] == 1602
    assert tab_script[1] == 80
    assert tab_script[2] == 500
    assert tab_script[3] == 10000
    assert tab_script[4][0] == approx(-10.0)
    assert tab_script[4][1] == approx(10.0)
    assert tab_script[5] == 52
    assert tab_script[6] == 'Zero, up'
    assert tab_script[7] == approx(0)
    assert tab_script[8] == 50
    assert tab_script[9] == 100
    assert tab_script[10][0] == approx(0.0)
    assert tab_script[10][1] == approx(0.0)
    assert tab_script[11] == 1
    assert tab_script[12] == 'Single Read Step'
    assert tab_script[13] == approx(0)
    assert tab_script[14] == 50
    assert tab_script[15] == 100
    assert tab_script[16][0] == 270
    assert tab_script[16][1] == 310


def test_data_extraction_txt():
    """ Test ex_data_extraction '.txt' file """
    dict_meas, script_dict = ex_data_extraction('txt')

    sum_dict = np.sum(list(dict_meas.values())[0:1])

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

    for key, value in target_script.items():
        assert script_dict[key] == value
    assert sum_dict == approx(6417256.821837984)


def test_data_extraction_csv():
    """ Test ex_data_extraction '.csv' file """
    dict_meas, script_dict = ex_data_extraction('csv')

    sum_dict = np.sum(list(dict_meas.values())[0:1])

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

    for key, value in target_script.items():
        assert script_dict[key] == value
    assert sum_dict == approx(6417256.821837984)


def test_data_extraction_xlsx():
    """ Test ex_data_extraction '.xlsx' file """
    dict_meas, script_dict = ex_data_extraction('xlsx')

    sum_dict = np.sum(list(dict_meas.values())[0:1])

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

    for key, value in target_script.items():
        assert script_dict[key] == value
    assert sum_dict == approx(6417256.821837984)


def test_csv_meas_sheet_extract():
    """ Test ex_csv_meas_sheet_extract """
    meas_pars, sign_pars = ex_csv_meas_sheet_extract()

    target_meas = {'Grid x [pix]': 8,
                   'Grid x [um]': 3.55,
                   'Grid y [pix]': 8,
                   'Grid y [um]': 3.55,
                   'Hold force [nN]': 100,
                   'Pressure [MPa]': 50.929581789406505,
                   'Calibration': 'No',
                   'Calib fact [nm/V]': 1,
                   'Q factor': 43.73134328358209,
                   'P [kHz/V]': 125.4,
                   'I [MHz/(V.s)]': 308.8,
                   'Center [kHz]': 290,
                   'Range [kHz]': 20,
                   'Sideband amp [V]': 1,
                   'Sideband freq [kHz]': 3,
                   'External meas': 'Yes',
                   'Sens ampli': 100,
                   'Offset ampli [V]': 0,
                   'Sens phase [mV/°]': 5,
                   'Offset phase [V]': 0,
                   'Bias app': 'Sample',
                   'V_AC [V]': 1,
                   'Date [hh : dd/mm/yyyy]': '13H : 27/06/2022',
                   'Pix durat [sec]': 80.15667999935194,
                   'Grid durat [sec]': 5130.027519958524,
                   'Tip': 'SCM-PIT-V2',
                   'Sign of d33': 'positive',
                   'Sample ref': 'KNN03'}

    target_sign = {'Min volt (W) [V]': -10,
                   'Max volt (W) [V]': 10,
                   'Nb volt (W)': 51,
                   'Mode (W)': 'Zero, up',
                   'Seg durat (W) [ms]': 50,
                   'Seg sample (W)': 100,
                   'Min volt (R) [V]': 0,
                   'Max volt (R) [V]': 0,
                   'Nb volt (R)': 8, 'Mode (R)': 'Low to High',
                   'Seg durat (R) [ms]': 50,
                   'Seg sample (R)': 100,
                   'Hold seg durat (start) [ms]': 7.4399999812158,
                   'Hold sample (start)': 6,
                   'Hold seg durat (end) [ms]': 249.239999370729,
                   'Hold sample (end)': 201}

    for key, value in target_meas.items():
        assert meas_pars[key] == value
    for key, value in target_sign.items():
        assert sign_pars[key] == value
