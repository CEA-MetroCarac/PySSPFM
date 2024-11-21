"""
Example of clustering_inertia methods
"""

import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.clustering_inertia import main_clustering_inertia


def ex_clustering_inertia(verbose=False, make_plots=False):
    """
    Example of clustering_inertia functions.

    Parameters
    ----------
    verbose: bool, optional
        Activation key for verbosity (default is False).
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    dict_inertia : dict
        Inertia (within-cluster sum of squares) for each mode.
    """
    example_root_path_in = get_setting("example_root_path_in")

    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
        "best_nanoloops")

    user_pars = {'relative': False,
                 'method': 'kmeans',
                 'lim cluster': 10,
                 'label meas': ['piezoresponse']}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "clustering_inertia", save_example_exe=make_plots,
        save_test_exe=False)

    # ex main_clustering_inertia
    dict_inertia = main_clustering_inertia(
        user_pars, dir_path_in, verbose=verbose,
        show_plots=make_plots, save_plots=save_plots,
        dir_path_out=dir_path_out)

    return dict_inertia


if __name__ == '__main__':
    figs = []
    ex_clustering_inertia(verbose=True, make_plots=True)
