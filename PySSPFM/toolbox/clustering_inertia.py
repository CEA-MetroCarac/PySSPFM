"""
Determines the inertia based on the number of clusters used in order to
determine the optimal number of clusters.
"""

import tkinter.filedialog as tkf
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, get_config
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.toolbox.vector_clustering import main_vector_clustering
from PySSPFM.utils.path_for_runable import \
    save_path_management, copy_json_res, create_json_res


def plot_inertia(tab_index_cluster, dict_inertia):
    """
    Plots the inertia for different numbers of clusters on a graph.

    Parameters
    ----------
    tab_index_cluster : list
        Cluster indices, typically a range of integers indicating cluster
        counts.
    dict_inertia : dict
        Dictionary where keys are cluster indices and values are the
        corresponding inertia values.

    Returns
    -------
    fig : Figure
        The figure object containing the plot.
    ax_graph : Axes
        The axes object of the plot.
    """
    figsize = get_setting("figsize")
    fig, ax_graph = plt.subplots(figsize=figsize)
    fig.sfn = 'clustering_inertia'
    plot_dict = {'x lab': 'Number of cluster', 'y lab': 'Inertia [a.u]',
                 'fs': 15, 'edgew': 1, 'tickl': 2, 'gridw': 1}
    tab_dict = [{'label': key} for key in dict_inertia.keys()]
    plot_graph(ax_graph, tab_index_cluster, list(dict_inertia.values()),
               plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=True)

    return fig, ax_graph


def main_clustering_inertia(
        user_pars, loop_pars, curve_pars, dir_path_in, verbose=False,
        show_plots=True, save_plots=False, dir_path_out=None,
        dir_path_in_props=None):

    """
    Perform vector clustering analysis.

    Parameters
    ----------
    user_pars : dict
        User parameters.
    loop_pars : dict
        User parameters for loop clustering analysis.
    curve_pars : dict
        User parameters for curve clustering analysis.
    dir_path_in : str
        Path of vector (loop or curve) txt directory (in).
    verbose : bool, optional
        Activation key for verbosity.
    show_plots : bool, optional
        Activation key for figure visualization.
    save_plots : bool, optional
        If True, save generated plots.
    dir_path_out : str, optional
        Output directory for saving plots.
    dir_path_in_props : str, optional
        Directory path for input properties.

    Returns
    -------
    dict
        Returns a dictionary containing inertia information for each clustering
        mode and the average vector for each cluster.
    """

    tab_index_cluster = range(2, user_pars['lim cluster']+1)
    dict_inertia = {}

    for cont, index_cluster in enumerate(tab_index_cluster):

        if verbose:
            print(f"\nNumber of cluster: {index_cluster}\n")

        # Init cluster index
        loop_pars['nb clusters off'] = index_cluster
        loop_pars['nb clusters on'] = index_cluster
        loop_pars['nb clusters coupled'] = index_cluster
        curve_pars['nb clusters'] = index_cluster

        # Clustering
        _, _, inertia, _ = main_vector_clustering(
            user_pars, loop_pars, curve_pars, dir_path_in, verbose=verbose,
            show_plots=False, save_plots=False, dir_path_out=dir_path_out,
            dir_path_in_props=dir_path_in_props)

        # Append inertia values
        if isinstance(inertia, dict):
            for key in inertia.keys():
                if cont == 0:
                    dict_inertia[key] = []
                dict_inertia[key].append(inertia[key])
        else:
            if cont == 0:
                dict_inertia['curve'] = []
            dict_inertia.append(inertia)

    # Plots the inertia as a function of the number of clusters
    make_plots = bool(show_plots or save_plots)
    if make_plots:
        fig, _ = plot_inertia(tab_index_cluster, dict_inertia)

    # Show or save figure
    if make_plots:
        print_plots([fig], show_plots=show_plots, save_plots=save_plots,
                    dirname=dir_path_out, transparent=False)

    return dict_inertia


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)

    - object: str
        Name of the Object Processed with Clustering Analysis
        This parameter determines the name of the object used to perform the
        clustering.
        Implemented objects are Loops (best nanoloops associated with each
        pixel) or Curves (raw SSPFM measurements associated with each
        pixel).
        Choose from: "loop", "curve"
    - relative: bool
        Activation key for relative clustering analysis.
        This parameter serves as an activation key to perform clustering
        analysis on relative vectors (all vectors vary between 0 and 1).
        Always active for combined vectors of multiple measurements.
    - pca: bool
        Activation key for performing PCA before clustering analysis.
        This parameter serves as an activation key to perform PCA (Principal
        Component Analysis) before clustering analysis.
    - method: str
        Name of the Method Used to Perform the Clustering
        This parameter determines the method used to perform the clustering.
        Implemented methods are K-Means or Gaussian Mixture Model.
        (GMM).
        Choose from : "kmeans", "gmm"
    - lim_cluster: int
        Maximum limit of the number of clusters to determine inertia.
        This parameter sets the maximum number of clusters for which inertia
        values are calculated and associated.

    - label_meas: list of str
        List of Measurement Name for Loops
        This parameter contains a list of measurement name in order to create
        the loop to be analyzed using a machine learning algorithm
        of clustering. If several name are filled, the loop will be
        normalized and concatenated.
        Choose from : piezoresponse, amplitude, phase, res freq and q fact

    - extension: str, optional
        Extension of files.
        This parameter determines the extension type of curve files.
        Four possible values: 'spm' or 'txt' or 'csv' or 'xlsx'.
    - mode: str
        Mode of measurement used (extraction of measurements).
        This parameter determines the method used for measurements,
        specifically for the extraction measurements.
        Two possible values: 'classic' (sweep or single frequency) or 'dfrt'.
    - label_meas: list of str
        List of Measurement Name for Curves
        This parameter contains a list of measurement name in order to create
        the curve to be analyzed using a machine learning algorithm
        of clustering. If several name are filled, the curve will be
        normalized and concatenated.

    - dir_path_in: str
        Input Directory for Vector Files (default: 'best_nanoloops').
        This parameter specifies the directory path for the vector
        files, to perform clustering analysis.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - dir_path_in_props: str
        Properties files directory
        (optional, default: properties).
        This parameter specifies the directory containing the properties
        files.
        For loop clustering : text file generated after the 2nd step
        of the analysis.
        For curve clustering : CSV measurement file (measurement sheet model).
    - verbose: bool
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.
    - show_plots: bool
        Activation key for generating matplotlib figures during analysis.
        This parameter serves as an activation key for generating
        matplotlib figures during the analysis process.
    - save: bool
        Activation key for saving results of analysis.
        This parameter serves as an activation key for saving results
        generated during the analysis process.
    """
    if get_setting("extract_parameters") in ['json', 'toml']:
        config_params, fname_json = get_config(__file__, fname_json)
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Select vector folder
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt\best_nanoloops
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # vector_clustering_2023-10-02-16h38m
        dir_path_in_props = None
        # dir_path_in_props = r'...\KNN500n_15h18m02-10-2023_out_dfrt\properties
        config_params = {
            "dir_path_in": dir_path_in,
            "dir_path_out": dir_path_out,
            "dir_path_in_props": dir_path_in_props,
            "verbose": True,
            "show_plots": True,
            "save": False,
            "user_pars": {
                "object": "loop",
                "relative": False,
                "pca": True,
                "method": "kmeans",
                "lim cluster": 10
            },
            "loop_pars": {
                "label meas": ["piezoresponse"]
            },
            "curve_pars": {
                "extension": "spm",
                "mode": "classic",
                "label meas": ["deflection"]
            }
        }
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return config_params['user_pars'], config_params['loop_pars'], \
        config_params['curve_pars'], config_params['dir_path_in'], \
        config_params['dir_path_out'], config_params['dir_path_in_props'], \
        config_params['verbose'], config_params['show_plots'], \
        config_params['save'], fname_json, config_params


def main(fname_json=None):
    """
    Main function for data analysis.

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)
    """
    # Extract parameters
    (user_pars, loop_pars, curve_pars, dir_path_in, dir_path_out,
     dir_path_in_props, verbose, show_plots, save, fname_json,
     config_params) = parameters(fname_json=fname_json)
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,  dirname="clustering_inertia",
        lvl=1, create_path=True, post_analysis=True)
    # Main function
    main_clustering_inertia(
        user_pars, loop_pars, curve_pars, dir_path_in, verbose=verbose,
        show_plots=show_plots, save_plots=save, dir_path_out=dir_path_out,
        dir_path_in_props=dir_path_in_props)
    # Save parameters
    if save:
        if get_setting("extract_parameters") in ['json', 'toml']:
            copy_json_res(fname_json, dir_path_out, verbose=verbose)
        else:
            create_json_res(config_params, dir_path_out,
                            fname="clustering_inertia_params.json",
                            verbose=verbose)


if __name__ == '__main__':
    main()
