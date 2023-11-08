"""
Example of map_correlation methods
"""

import os

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.map_correlation import main_map_correlation

from PySSPFM.settings import EXAMPLE_ROOT_PATH_IN


def ex_map_correlation(verbose=False, make_plots=False):
    """
    Example of map_correlation functions.

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag (default is False).
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    coef_arr: dict
        Dictionary containing correlation coefficients.
    """
    dir_path_in = os.path.join(
        EXAMPLE_ROOT_PATH_IN, "KNN500n_2023-10-05-17h23m_out_dfrt",
        "properties")
    ind_maps = None

    user_pars = {'dir path in': dir_path_in,
                 'dir path out': None,
                 'ind maps': ind_maps,
                 'mask': None,
                 'revert mask': False}

    # ex main_map_correlation
    coef_arr, figures = main_map_correlation(user_pars, dir_path_in)

    if verbose:
        for key in coef_arr.keys():
            print(f'\n -{key}')
            print(coef_arr[key])
    if make_plots:
        return figures
    else:
        return coef_arr


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "map_correlation", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_map_correlation(verbose=True, make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
