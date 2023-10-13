"""
Example of list_map_reader methods
"""

import os

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.list_map_reader import main_list_map_reader

from settings import EXAMPLE_ROOT_PATH_IN


def ex_list_map_reader(verbose=False):
    """
    Example of list_map_reader functions.

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag (default is False).

    Returns
    -------
    figures: list
        List of figures.
    """
    dir_path_in = os.path.join(
        EXAMPLE_ROOT_PATH_IN, "KNN500n_2023-10-05-17h23m_out_dfrt",
        "txt_ferro_meas")

    ind_maps = [['off', 'fit pars: ampli_0'],
                ['off', 'fit pars: slope'],
                ['off', 'fit pars: offset'],
                ['off', 'charac tot fit: x shift'],
                ['off', 'charac tot fit: y shift'],
                ['off', 'charac tot fit: area'],
                ['off', 'charac tot fit: R² hyst']]

    user_pars = {'interp fact': 4,
                 'interp func': 'linear',
                 'man mask': None,
                 'ref': {'mode': 'off',
                         'meas': 'charac tot fit: R² hyst',
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
    figs += ex_list_map_reader(verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)