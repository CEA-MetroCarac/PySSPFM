"""
Example of loop_file_reader methods
"""

import os
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.loop_file_reader import main_loop_file_reader

from settings import EXAMPLE_ROOT_PATH_IN


def example_loop_file_reader(verbose=False, make_plots=False):
    """
    Example of loop_file_reader functions.

    Parameters
    ----------
    verbose: bool, optional
        Flag indicating whether to display verbose output.
    make_plots: bool, optional
        Flag indicating whether to generate plots.

    Returns
    -------
    out: object
        Result of the `main` function.
    """
    # Input and output file management
    file_path_in = os.path.join(
        EXAMPLE_ROOT_PATH_IN, "KNN500n_2023-10-05-17h21m_out_dfrt", "txt_loops",
        "off_f_KNN500n_SSPFM.0_00056.txt")
    csv_path = os.path.join(EXAMPLE_ROOT_PATH_IN, "KNN500n")

    dict_pha = {
        'del 1st loop': True,
        'corr': 'offset',
        'pha fwd': 0,
        'pha rev': 180,
        'func': np.cos,
        'main elec': True,
        'grounded tip': True,
        'positive d33': True,
        'locked elec slope': None
    }

    # ex main_loop_file_reader
    out = main_loop_file_reader(
        file_path_in, csv_path=csv_path, dict_pha=dict_pha,
        del_1st_loop=dict_pha['del 1st loop'],
        verbose=verbose, make_plots=make_plots)

    return out


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_reader", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_loop_file_reader(verbose=True, make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
