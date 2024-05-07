"""
Example of curve_clustering methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.curve_clustering import main_curve_clustering


def ex_curve_clustering(label_meas, verbose=False, make_plots=False):
    """
    Example of curve_clustering functions.

    Parameters
    ----------
    label_meas: list of str
        List of measurement name for curves (in piezoresponse, amplitude,
        phase, res freq and q fact)
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    cluster_labels : list
        Cluster indices for each data point
    cluster_info : list
        Information about each cluster.
    inertia : float
        For K-Means : Inertia (within-cluster sum of squares).
        For GMM : Bayesian Information Criterion.
    avg_curve: numpy.ndarray
        List of average curve.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(example_root_path_in, "PZT100n")
    user_pars = {"extension": "spm",
                 "mode": "dfrt",
                 'method': 'kmeans',
                 'label meas': label_meas,
                 'nb clusters': 3}
    dim_pix = {'x': 7, 'y': 3}
    dim_mic = {'x': 7, 'y': 3}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "curve_clustering", save_example_exe=make_plots,
        save_test_exe=False)
    # ex main_curve_clustering
    out = main_curve_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=make_plots,
        save_plots=save_plots, dir_path_out=dir_path_out, dim_pix=dim_pix,
        dim_mic=dim_mic)
    (cluster_labels, cluster_info, inertia, avg_curve) = out

    return cluster_labels, cluster_info, inertia, avg_curve


if __name__ == '__main__':
    figs = []
    ex_curve_clustering(label_meas=['deflection'], verbose=True,
                        make_plots=True)
    ex_curve_clustering(label_meas=['deflection', 'height'], verbose=True,
                        make_plots=True)
