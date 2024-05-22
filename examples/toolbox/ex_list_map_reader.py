"""
Example of list_map_reader methods
"""

import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.list_map_reader import main_list_map_reader


def ex_list_map_reader_properties(verbose=False):
    """
    Example of list_map_reader functions for properties directory.

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag (default is False).

    Returns
    -------
    figures: list
        List of figures.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
        "properties")

    ind_maps = [['off', 'fit pars: ampli_0'],
                ['off', 'charac tot fit: x shift'],
                ['off', 'charac tot fit: y shift'],
                ['off', 'charac tot fit: area'],
                ['off', 'charac tot fit: R_2 hyst']]

    user_pars = {'interp fact': 4,
                 'interp func': 'linear',
                 'meas time': 1.5,
                 'revert mask': False,
                 'man mask': None,
                 'ref': {'mode': 'off',
                         'prop': 'charac tot fit: R_2 hyst',
                         'fmt': '.5f',
                         'min val': 0.90,
                         'max val': None,
                         'interactive': False},
                 'ind maps': ind_maps}

    # ex main_list_map_reader
    figures = main_list_map_reader(user_pars, dir_path_in, verbose=verbose)

    return figures


def ex_list_map_reader_phase_inversion(verbose=False):
    """
    Example of list_map_reader functions for phase inversion directory.

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag (default is False).

    Returns
    -------
    figures: list
        List of figures.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_toolbox",
        "phase_inversion_analyzer_2024-05-21-18h13m")

    ind_maps = [['phase_inversion', 'Grad On field'],
                ['phase_inversion', 'Grad Off field'],
                ['phase_inversion', 'Revert On Off']]

    user_pars = {'interp fact': 1,
                 'interp func': 'linear',
                 'meas time': 1.5,
                 'revert mask': False,
                 'man mask': [],
                 'ref': {'mode': 'off',
                         'prop': 'charac tot fit: R_2 hyst',
                         'fmt': '.5f',
                         'min val': 0.90,
                         'max val': None,
                         'interactive': False},
                 'ind maps': ind_maps}

    # ex main_list_map_reader
    figures = main_list_map_reader(user_pars, dir_path_in, verbose=verbose)

    return figures


def ex_list_map_reader_phase_offset(verbose=False):
    """
    Example of list_map_reader functions for phase offset directory.

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag (default is False).

    Returns
    -------
    figures: list
        List of figures.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_toolbox",
        "phase_offset_analyzer_2024-05-21-18h18m")

    ind_maps = [['phase_offset', 'On field'],
                ['phase_offset', 'Off field'],
                ['phase_offset', 'Mean']]

    user_pars = {'interp fact': 1,
                 'interp func': 'linear',
                 'meas time': 1.5,
                 'revert mask': False,
                 'man mask': [],
                 'ref': {'mode': 'off',
                         'prop': 'charac tot fit: R_2 hyst',
                         'fmt': '.5f',
                         'min val': 0.90,
                         'max val': None,
                         'interactive': False},
                 'ind maps': ind_maps}

    # ex main_list_map_reader
    figures = main_list_map_reader(user_pars, dir_path_in, verbose=verbose)

    return figures


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "list_map_reader", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_list_map_reader_properties(verbose=True)
    figs += ex_list_map_reader_phase_inversion(verbose=True)
    figs += ex_list_map_reader_phase_offset(verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
