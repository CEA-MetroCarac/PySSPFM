"""
Test extract_params_from_file methods
"""
import pytest

from examples.utils.core.ex_extract_params_from_file import \
    ex_load_parameters_from_file


# class TestSignalBias(unittest.TestCase):


def test_load_parameters_from_file():
    """ Test load_parameters_from_file """

    params_dict = ex_load_parameters_from_file()

    target_params_dict = {
        'dir_path_in': 'path/to/your/directory',
        'dir_path_out': None,
        'verbose': True,
        'show_plots': True,
        'save': False,
        'user_pars': {
            'mode': 'off',
            'mask': {
                'revert mask': False,
                'man mask': None,
                'ref': {
                    'prop': 'charac tot fit: area',
                    'mode': 'off',
                    'min val': 0.005,
                    'max val': None,
                    'fmt': '.2f',
                    'interactive': False}},
            'func': 'sigmoid',
            'method': 'least_square',
            'asymmetric': False,
            'inf thresh': 10,
            'sat thresh': 90,
            'del 1st loop': True,
            'pha corr': 'offset',
            'pha fwd': 0,
            'pha rev': 180,
            'pha func': 'np.cos',
            'main elec': True,
            'locked elec slope': None,
            'diff domain': {'min': -5.0, 'max': 5.0},
            'sat mode': 'set',
            'sat domain': {'min': -9.0, 'max': 9.0},
            'interp fact': 4,
            'interp func': 'linear'}}

    assert params_dict == target_params_dict
