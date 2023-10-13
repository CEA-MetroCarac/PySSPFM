"""
Test file methods
"""
from pytest import approx
import numpy as np

from examples.utils.nanoloop.ex_file import example_file


# class TestFile(unittest.TestCase):


def test_file():
    """ Test example_file """

    loop_tabs, fmts, headers, datas_dicts, dict_strs = example_file()

    sum_1 = sum(np.sum(value) for value in datas_dicts['on'].values())
    sum_2 = sum(np.sum(value) for value in datas_dicts['off'].values())
    sum_3 = sum(np.sum(loop) for loop in loop_tabs['on'])
    sum_4 = sum(np.sum(loop) for loop in loop_tabs['off'])

    assert sum_1 == approx(86455.65548)
    assert sum_2 == approx(74628.64881099999)
    assert sum_3 == approx(46128.38957897419)
    assert sum_4 == approx(38651.29668676276)
    assert fmts['on'][0] == '%i'
    assert fmts['on'][1] == '%.2f'
    assert fmts['on'][2] == '%.2f'
    assert fmts['on'][3] == '%.3e'
    assert fmts['on'][4] == '%.3f'
    assert dict_strs['on'] == {'unit': 'nm', 'label': 'On field', 'col': 'y'}
    assert dict_strs['off'] == {'unit': 'nm', 'label': 'Off field', 'col': 'w'}
    assert headers['on'] == ('Loop index	Read Volt (V)	'
                             'Write Volt (V)	Amplitude (nm)	'
                             'Phase (°)	')
    assert headers['on'] == headers['off']