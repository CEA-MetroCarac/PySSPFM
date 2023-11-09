"""
Example of sort_plot_pixel methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.sort_plot_pixel import main_sort_plot_pixel


def example_sort_plot_pixel(verbose=False, make_plots=False):
    """
    Example of sort_plot_pixel functions.

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag (default is False).
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    list_file: list
        List of files.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-10-05-17h23m_out_dfrt")
    dir_path_in_props = os.path.join(dir_path_in, "properties")
    dir_path_in_loop = os.path.join(dir_path_in, "nanoloops")
    file_path_in_pars = os.path.join(dir_path_in, "parameters.txt")
    user_pars = {'dir path in': dir_path_in,
                 'dir path in prop': dir_path_in_props,
                 'dir path in loop': dir_path_in_loop,
                 'file path in pars': file_path_in_pars,
                 'prop key': {'mode': 'off',
                              'prop': 'fit pars: ampli_0'},
                 'list pixels': None,
                 'reverse': False,
                 'del 1st loop': True,
                 'interp fact': 4,
                 'interp func': 'linear'}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "sort_plot_pixel", save_example_exe=make_plots, save_test_exe=False)
    # ex main_sort_plot_pixel
    list_file = main_sort_plot_pixel(
        user_pars, dir_path_in, verbose=verbose, show_plots=make_plots,
        save_plots=save_plots, dirname=dir_path_out)

    return list_file


if __name__ == '__main__':
    figs = []
    example_sort_plot_pixel(verbose=True, make_plots=True)
