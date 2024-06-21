"""
Example of vector_clustering methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.vector_clustering import main_vector_clustering


def ex_vector_clustering(label_meas, obj="loop", verbose=False,
                         make_plots=False):
    """
    Example of loop_clustering functions.

    Parameters
    ----------
    label_meas: list of str
        List of measurement name for vectors (in deflection,
        height sensor, piezoresponse, amplitude,
        phase, res freq and q fact)
    obj: str, optional
        Object on which the clustering analysis will be performed
        (in loop or vector) (default is loop).
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

    if obj == "loop":
        dir_path_in = os.path.join(
            example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
            "best_nanoloops")
        dim_pix = None
        dim_mic = None
    else:
        dir_path_in = os.path.join(example_root_path_in, "PZT100n")
        dim_pix = {'x': 7, 'y': 3}
        dim_mic = {'x': 7, 'y': 3}

    user_pars = {'object': obj,
                 'relative': False,
                 'pca': True,
                 'method': 'kmeans'}
    loop_pars = {'label meas': label_meas,
                 'nb clusters off': 5,
                 'nb clusters on': 2,
                 'nb clusters coupled': 4}
    curve_pars = {"extension": "spm",
                  "mode": "dfrt",
                  "label meas": label_meas,
                  "nb clusters": 4}

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "vector_clustering", save_example_exe=make_plots,
        save_test_exe=False)
    # ex main_vector_clustering
    out = main_vector_clustering(
        user_pars, loop_pars, curve_pars, dir_path_in, verbose=verbose,
        show_plots=make_plots, save_plots=save_plots,
        dir_path_out=dir_path_out, dim_pix=dim_pix, dim_mic=dim_mic)
    (cluster_labels, cluster_info, inertia, avg_vector) = out

    return cluster_labels, cluster_info, inertia, avg_vector


if __name__ == '__main__':
    figs = []
    ex_vector_clustering(label_meas=['deflection'], obj="curve",
                         verbose=True, make_plots=True)
    ex_vector_clustering(label_meas=['deflection', 'height'], obj="curve",
                         verbose=True, make_plots=True)
    ex_vector_clustering(label_meas=['piezoresponse'], obj="loop",
                         verbose=True, make_plots=True)
    ex_vector_clustering(label_meas=['amplitude', 'phase'], obj="loop",
                         verbose=True, make_plots=True)
