"""
Example of sort_plot methods
"""
import os

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.sort_plot_pixel import main_sort_plot_pixel

from PySSPFM import EXAMPLE_ROOT_PATH_IN


def example_sort_plot(verbose=False, make_plots=False):
    """
    Example of sort_plot functions.

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
    dir_path_in = os.path.join(
        EXAMPLE_ROOT_PATH_IN, "KNN500n_2023-10-05-17h23m_out_dfrt")
    dir_path_in_meas = os.path.join(dir_path_in, "txt_ferro_meas")
    dir_path_in_loop = os.path.join(dir_path_in, "txt_loops")
    file_path_in_pars = os.path.join(
        dir_path_in, "results", "saving_parameters.txt")
    user_pars = {'dir path in': dir_path_in,
                 'dir path in meas': dir_path_in_meas,
                 'dir path in loop': dir_path_in_loop,
                 'file path in pars': file_path_in_pars,
                 'meas key': {'mode': 'off',
                              'meas': 'fit pars: ampli_0'},
                 'list pixels': None,
                 'reverse': False,
                 'del 1st loop': True,
                 'interp fact': 4,
                 'interp func': 'linear'}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "sort_plot", save_example_exe=make_plots, save_test_exe=False)
    # ex main_sort_plot_pixel
    list_file = main_sort_plot_pixel(
        user_pars, dir_path_in, verbose=verbose, show_plots=make_plots,
        save_plots=save_plots, dirname=dir_path_out)

    return list_file


if __name__ == '__main__':
    figs = []
    example_sort_plot(verbose=True, make_plots=True)