"""
Example of force_curve_clustering methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.force_curve_clustering import main_force_curve_analysis


def ex_force_curve_clustering(verbose=False, make_plots=False):
    """
    Example of force_curve_clustering functions.

    Parameters
    ----------
    verbose: bool, optional
        Activation key for verbosity (default is False).
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    cluster_labels : list
        List of cluster labels.
    cluster_info : list
        List of cluster information.
    inertia : float
        Inertia (within-cluster sum of squares).
    x_avg : list
        List of average curves (for the x-axis) for each cluster.
    y_avg : list
        List of average curves (for the y-axis) for each cluster.
    tab_other_properties : list
        List of other properties extracted from the curves.
    """
    example_root_path_in = get_setting("example_root_path_in")

    dir_path_in = os.path.join(example_root_path_in, "PZT100n")
    dim_pix = {'x': 7, 'y': 3}
    dim_mic = {'x': 7, 'y': 3}
    extension = "spm"
    mode = "classic"
    cluster_pars = {'nb clusters': 3,
                    'method': 'kmeans'}

    # saving path management
    dir_path_out, save = save_path_example(
        "force_curve_clustering", save_example_exe=make_plots,
        save_test_exe=False)

    # ex main_loop_clustering
    out = main_force_curve_analysis(
        dir_path_in, cluster_pars, extension=extension, mode=mode,
        dim_pix=dim_pix, dim_mic=dim_mic, verbose=verbose,
        show_plots=make_plots, save=save,
        dir_path_out=dir_path_out)
    (cluster_labels, cluster_info, inertia, x_avg, y_avg,
     tab_other_properties, _) = out
    return (cluster_labels, cluster_info, inertia, x_avg, y_avg,
            tab_other_properties)


if __name__ == '__main__':
    figs = []
    ex_force_curve_clustering(verbose=True, make_plots=True)
