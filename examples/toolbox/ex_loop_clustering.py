"""
Example of loop_clustering methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.loop_clustering import main_loop_clustering


def ex_loop_clustering(label_meas, verbose=False, make_plots=False):
    """
    Example of loop_clustering functions.

    Parameters
    ----------
    label_meas: list of str
        List of measurement name for loops (in piezoresponse, amplitude,
        phase, res freq and q fact)
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
    avg_loop : dict
        Contain all list of average loop for each cluster in each mode.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
        "best_nanoloops")
    user_pars = {'method': 'kmeans',
                 'label meas': label_meas,
                 'nb clusters off': 5,
                 'nb clusters on': 2,
                 'nb clusters coupled': 4}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "loop_clustering", save_example_exe=make_plots,
        save_test_exe=False)
    # ex main_loop_clustering
    out = main_loop_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=make_plots,
        save_plots=save_plots, dir_path_out=dir_path_out)
    (cluster_labels, cluster_info, inertia, avg_loop) = out

    return cluster_labels, cluster_info, inertia, avg_loop


if __name__ == '__main__':
    figs = []
    ex_loop_clustering(label_meas=['piezoresponse'], verbose=True,
                       make_plots=True)
    ex_loop_clustering(label_meas=['amplitude', 'phase'], verbose=True,
                       make_plots=True)
