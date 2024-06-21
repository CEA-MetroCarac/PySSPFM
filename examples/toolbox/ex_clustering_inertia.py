"""
Example of clustering_inertia methods
"""

import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.clustering_inertia import main_clustering_inertia


def ex_clustering_inertia(verbose=False, make_plots=False):
    """
    Example of loop_clustering functions.

    Parameters
    ----------
    verbose: bool, optional
        Activation key for verbosity (default is False).
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
    avg_vector : dict
        Contain all list of average vector for each cluster in each mode.
    """
    example_root_path_in = get_setting("example_root_path_in")

    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
        "best_nanoloops")

    user_pars = {'object': "loop",
                 'relative': False,
                 'pca': True,
                 'method': 'kmeans',
                 'lim cluster': 10}
    loop_pars = {'label meas': ['piezoresponse']}
    curve_pars = {"extension": "spm",
                  "mode": "dfrt",
                  "label meas": ['deflection']}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "vector_clustering", save_example_exe=make_plots,
        save_test_exe=False)
    # ex main_vector_clustering
    dict_inertia = main_clustering_inertia(
        user_pars, loop_pars, curve_pars, dir_path_in, verbose=verbose,
        show_plots=make_plots, save_plots=save_plots,
        dir_path_out=dir_path_out)

    return dict_inertia


if __name__ == '__main__':
    figs = []
    ex_clustering_inertia(verbose=True, make_plots=True)
