"""
Example of global_map_reader methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.global_map_reader import main_global_map_reader


def ex_global_map_reader(verbose=False, make_plots=False):
    """
    Example of global_map_reader functions.

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag (default is False).
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    mask: array-like
        Mask array.
    coef_arr: array-like
        Coefficient array.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
        "properties")

    user_params = {'interp fact': 4,
                   'interp func': 'linear',
                   'revert mask': {'on': False,
                                   'off': False,
                                   'coupled': False,
                                   'other': False},
                   'man mask': {'on': None,
                                'off': None,
                                'coupled': None,
                                'other': None},
                   'ref': {'on': {'prop': 'charac tot fit: R_2 hyst',
                                  'fmt': '.5f',
                                  'min val': 0.92,
                                  'max val': None,
                                  'interactive': False},
                           'off': {'prop': 'charac tot fit: R_2 hyst',
                                   'fmt': '.5f',
                                   'min val': 0.90,
                                   'max val': None,
                                   'interactive': False},
                           'coupled': {'prop': 'r_2',
                                       'fmt': '.5f',
                                       'min val': 0.995,
                                       'max val': None,
                                       'interactive': False},
                           'other': {'prop': 'deflection error',
                                     'fmt': '.2f',
                                     'min val': None,
                                     'max val': 5,
                                     'interactive': False}}}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "global_map_reader", save_example_exe=make_plots, save_test_exe=False)
    # ex main_global_map_reader
    mask, coef_arr = main_global_map_reader(
        user_params, verbose=verbose, show_plots=make_plots,
        save_plots=save_plots, dir_path_in=dir_path_in,
        dir_path_out=dir_path_out, index_lim=[5, 9])

    return mask, coef_arr


if __name__ == '__main__':
    figs = []
    ex_global_map_reader(verbose=True, make_plots=True)
