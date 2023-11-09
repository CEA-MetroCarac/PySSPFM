"""
Example of hysteresis_clustering methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.hysteresis_clustering import main_hysteresis_clustering


def ex_hysteresis_clustering(verbose=False, make_plots=False):
    """
    Example of hysteresis_clustering functions.

    Parameters
    ----------
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    cluster_labels : dict
        Cluster indices for each data point for each mode.
    cluster_info : dict
        Information about each cluster for each mode.
    inertia : dict
        Inertia (within-cluster sum of squares) for each mode.
    avg_hysteresis : dict
        Contain all list of average hysteresis for each cluster in each mode.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-10-05-17h23m_out_dfrt",
        "best_nanoloops")
    user_pars = {'nb clusters off': 5,
                 'nb clusters on': 2,
                 'nb clusters coupled': 4}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "hysteresis_clustering", save_example_exe=make_plots,
        save_test_exe=False)
    # ex main_hysteresis_clustering
    out = main_hysteresis_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=make_plots,
        save_plots=save_plots, dir_path_out=dir_path_out)
    (cluster_labels, cluster_info, inertia, avg_hysteresis) = out

    return cluster_labels, cluster_info, inertia, avg_hysteresis


if __name__ == '__main__':
    figs = []
    ex_hysteresis_clustering(verbose=True, make_plots=True)
