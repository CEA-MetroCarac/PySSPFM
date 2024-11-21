"""
Example of curve_clustering methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.curve_clustering import main_loop_clustering


def ex_curve_clustering(label_meas, verbose=False, make_plots=False):
    """
    Example of curve_clustering functions.

    Parameters
    ----------
    label_meas: list of str
        List of measurement name for loops (in piezoresponse, amplitude,
        phase, res freq and q fact)
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
    avg_loop_x : dict
        List of average loops (for the x-axis) for each cluster in each mode.
    avg_loop_y : dict
        List of average loops (for the y-axis) for each cluster in each mode.
    """
    example_root_path_in = get_setting("example_root_path_in")

    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
        "best_nanoloops")
    dim_pix = None
    dim_mic = None

    user_pars = {'relative': False,
                 'method': 'kmeans',
                 'label meas': label_meas,
                 'nb clusters off': 5,
                 'nb clusters on': 2,
                 'nb clusters coupled': 4}

    # saving path management
    dir_path_out, save = save_path_example(
        "curve_clustering", save_example_exe=make_plots,
        save_test_exe=False)

    # ex main_loop_clustering
    out = main_loop_clustering(
        user_pars, dir_path_in, verbose=verbose,
        show_plots=make_plots, save=save,
        dir_path_out=dir_path_out, dim_pix=dim_pix, dim_mic=dim_mic)
    (cluster_labels, cluster_info, inertia, avg_loop_x, avg_loop_y) = out

    return cluster_labels, cluster_info, inertia, avg_loop_x, avg_loop_y


if __name__ == '__main__':
    ex_curve_clustering(label_meas=['piezoresponse'],
                        verbose=True, make_plots=True)
    ex_curve_clustering(label_meas=['amplitude', 'phase'],
                        verbose=True, make_plots=True)
