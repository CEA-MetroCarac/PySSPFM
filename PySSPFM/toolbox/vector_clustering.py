"""
--> Executable Script
Module used to perform a clustering (K-Means or Gaussian Mixture Model) for a
list of vector (loop (amplitude, phase, piezoresponse, q_factor, resonance
frequency ...) or curve (deflection, height sensor ...), with a chosen
measure), for each pixel of a sspfm measurement.
Vectors can be a composition of several measure, which will be normalized
between 0 and 1 and concatenated (for example amplitude and phase)
    - Generate a sspfm maps for each mode resulting of clustering analysis
    - Generate a graph of all vector with their cluster for each mode
    resulting of clustering analysis
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, copy_default_settings_if_not_exist, get_config
from PySSPFM.utils.core.clustering import \
    (data_clustering, cbar_map, plot_clustering_centroids,
     plot_all_vector_clustering, plot_avg_vector_clustering, data_pca,
     plot_pca_plane)
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop_to_hyst.file import extract_properties
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars
from PySSPFM.utils.file_clustering import \
    (extract_loop_data, gen_coupled_data, extract_map_dim_from_csv,
     curve_extraction)


def perform_vector_clustering(data_x, data_y, numb_cluster=3,
                              method="kmeans", pca_mode=False,
                              relative_mode=False, verbose=False,
                              make_plots=False):
    """
    Perform vector clustering.

    Parameters
    ----------
    data_x : array_like
        Input data for x-axis.
    data_y : array_like
        Input data for y-axis.
    numb_cluster : int, optional
        Number of clusters (default is 3).
    method : str, optional
        Clustering method (default is "kmeans").
    pca_mode : bool, optional
        Whether to perform PCA analysis (default is False).
    relative_mode : bool, optional
        Whether to perform relative (each vector (i.e data_y) vary between 0
        and 1) analysis (default is False).
    verbose : bool, optional
        Whether to display verbose information (default is False).
    make_plots : bool, optional
        Whether to generate plots (default is False).

    Returns
    -------
    cluster_labels : list
        List of cluster labels.
    cluster_info : list
        List of cluster information.
    inertia : float
        Inertia value.
    avg_data : list
        List of average data by cluster.
    figures : list
        List of generated figures.
    """

    # Each vector vary between 0 and 1
    if relative_mode:
        data_y = [
            [(sub_elem - np.min(elem)) / (np.max(elem) - np.min(elem))
             for sub_elem in elem] for elem in data_y]

    # Init the clustering with PCA analysis
    if pca_mode is True:
        processed_data = data_pca(data_y, dimension=2)
    else:
        processed_data = data_y

    # Data clustering
    cluster_labels, cluster_info, inertia, centers = data_clustering(
        processed_data, num_clusters=numb_cluster, method=method,
        verbose=verbose)

    # Calculate Average data by Cluster
    avg_data = []
    for cluster_idx in range(numb_cluster):
        cluster_mask = np.array(cluster_labels) == cluster_idx
        avg_data.append(
            np.mean(np.array(data_y)[cluster_mask], axis=0))

    # Clustering results in str
    labels = []
    for i in range(numb_cluster):
        labels.append(f'Cluster {cluster_info[i][4]}, '
                      f'{cluster_info[i][3]} points'
                      ', near dist '
                      f'({cluster_info[i][2]}) : '
                      f'{cluster_info[i][1]:.2e}'
                      ', ref (A) dist : '
                      f'{cluster_info[i][0]:.2e}')

    if verbose:
        _ = [print(label) for label in labels]

    # Generate plots if specified
    figures = []
    if make_plots:

        # Color of figures
        color_curve_clustering = get_setting("color_curve_clustering")
        cbar = plt.get_cmap(color_curve_clustering)
        colors = [cbar((numb_cluster - i) / numb_cluster)
                  for i in range(numb_cluster)]

        if pca_mode is True:
            figures += plot_pca_plane(
                processed_data, label_clust=cluster_labels,
                colors=colors, centers=centers)
        else:
            figures += plot_clustering_centroids(
                data_y, numb_cluster, cluster_labels,
                cluster_info, centers, colors)
        figures += plot_all_vector_clustering(
            data_x, data_y, numb_cluster,
            cluster_labels, cluster_info, colors)
        figures += plot_avg_vector_clustering(
            data_x[0], avg_data, numb_cluster,
            cluster_info, colors)

    return cluster_labels, cluster_info, inertia, avg_data, figures


def main_loop_clustering(
        user_pars, dir_path_in, verbose=False, show_plots=True,
        save_plots=False, dir_path_out=None, dim_pix=None, dim_mic=None,
        dir_path_in_props=None):
    """
    Perform loop clustering analysis.

    Parameters
    ----------
    user_pars : dict
        User parameters.
    dir_path_in : str
        Path of best nanoloops measurements txt directory (in).
    verbose : bool, optional
        Activation key for verbosity.
    show_plots : bool, optional
        Activation key for figure visualization.
    save_plots : bool, optional
        If True, save generated plots.
    dir_path_out : str, optional
        Output directory for saving plots.
    dim_pix : dict, optional
        Dictionary of pixel dimensions.
    dim_mic : dict, optional
        Dictionary of micron dimensions.
    dir_path_in_props : str, optional
        Directory path for input properties.

    Returns
    -------
    cluster_labels : dict
        Cluster indices for each data point for each mode.
    cluster_info : dict
        Information about each cluster for each mode.
    inertia : dict
        Inertia (within-cluster sum of squares) for each mode.
    avg_loop : dict
        List of average loop for each cluster in each mode.
    """

    method = user_pars["method"]
    assert method in ["kmeans", "gmm"], \
        "Invalid clustering method. Method must be either 'kmeans' or 'gmm'."
    make_plots = bool(show_plots or save_plots)

    modes = [key.split()[-1] for key, value in user_pars.items() if
             'clusters' in key and value is not None]
    if user_pars['label meas'] != ['piezoresponse']:
        modes = [lab for lab in modes if lab != 'coupled']
    lab_tab = [['on', 'off', 'coupled'], ['y', 'w', 'r'],
               ['On Field', 'Off Field', 'Coupled']]
    cluster_labels, cluster_info, inertia, avg_loop = \
        {}, {}, {}, {}
    offsets = []

    # Extract loop data
    loops_x, loops_y = extract_loop_data(
        dir_path_in, modes, user_pars['label meas'])

    # Extract extra analysis info (scan dim + vertical offset (off field))
    if dir_path_in is not None:
        if dir_path_in_props is None:
            root = os.path.split(dir_path_in)[0]
            properties_folder_name = \
                get_setting('default_properties_folder_name')
            dir_path_in_props = os.path.join(root, properties_folder_name)
        properties, dim_pix, dim_mic = extract_properties(dir_path_in_props)
        elec_offset = get_setting('electrostatic_offset')
        offsets = properties['off']['fit pars: offset'] \
            if elec_offset else None

    # If "coupled" mode is present, calculate coupled loop
    # (only for piezoresponse)
    if "coupled" in modes:
        loops_x, loops_y = gen_coupled_data(loops_x, loops_y,
                                            offsets=offsets)

    # Perform clustering for each mode
    for mode in modes:
        try:
            if verbose:
                print(f'{mode} :')
            numb_cluster = user_pars[f'nb clusters {mode}']
            if isinstance(loops_y[mode], list):
                loops_y[mode] = np.array(loops_y[mode])\

            res = perform_vector_clustering(
                    loops_x[mode], loops_y[mode],
                    numb_cluster=numb_cluster,
                    method=method, pca_mode=user_pars['pca'],
                    relative_mode=user_pars['relative'],
                    verbose=verbose, make_plots=make_plots)
            (cluster_labels[mode], cluster_info[mode], inertia[mode],
             avg_loop[mode], figures) = res

            if make_plots:
                if save_plots is True:
                    print_plots(figures, show_plots=False,
                                save_plots=save_plots, dirname=dir_path_out)

                # Plot 3 : cluster mapping
                # Color of figures
                color_curve_clustering = get_setting("color_curve_clustering")
                cbar = plt.get_cmap(color_curve_clustering)
                colors = [cbar((numb_cluster - i) / numb_cluster)
                          for i in range(numb_cluster)]
                method_str = "K-Means" if method == "kmeans" else "GMM"
                cmap, cbar_lab = cbar_map(colors, numb_cluster, method_str)
                properties = \
                    {f"Clustering ({method_str})": cluster_labels[mode]}
                colors_lab = {f"Clustering ({method_str})": cmap}
                indx = lab_tab[0].index(mode)
                dict_map = {'label': lab_tab[2][indx], 'col': lab_tab[1][indx]}
                main_mapping(properties, dim_pix, dim_mic=dim_mic,
                             colors=colors_lab, cbar_lab=cbar_lab,
                             dict_map=dict_map, mask=[], show_plots=show_plots,
                             save_plots=save_plots, dir_path_out=dir_path_out)
        except KeyError:
            print(f"KeyError management with except: no {mode} mode available "
                  f"for analysis")
            continue

    return cluster_labels, cluster_info, inertia, avg_loop


def main_curve_clustering(
        user_pars, dir_path_in, verbose=False, show_plots=True,
        save_plots=False, dir_path_out=None, dim_pix=None, dim_mic=None,
        csv_path=None):
    """
    Perform curve clustering analysis.

    Parameters
    ----------
    user_pars : dict
        User parameters.
    dir_path_in : str
        Path of curve measurement directory (in).
    verbose : bool, optional
        Activation key for verbosity.
    show_plots : bool, optional
        Activation key for figure visualization.
    save_plots : bool, optional
        If True, save generated plots.
    dir_path_out : str, optional
        Output directory for saving plots.
    dim_pix : dict, optional
        Dictionary of pixel dimensions.
    dim_mic : dict, optional
        Dictionary of micron dimensions.
    csv_path : str, optional
        Path of csv params measurement file (in)

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

    method = user_pars["method"]
    assert method in ["kmeans", "gmm"], \
        "Invalid clustering method. Method must be either 'kmeans' or 'gmm'."
    make_plots = bool(show_plots or save_plots)
    numb_cluster = user_pars['nb clusters']
    # Extract curve data
    curves_x, curves_y = curve_extraction(
        dir_path_in, user_pars['label meas'], mode=user_pars['mode'],
        extension=user_pars['extension'])

    # Extract extra analysis info (scan dim)
    if dim_pix is None and dir_path_in is not None:
        dim_pix, dim_mic = extract_map_dim_from_csv(
            csv_path, dir_path_in=dir_path_in, verbose=verbose)

    if isinstance(curves_y, list):
        curves_y = np.array(curves_y)

    res = perform_vector_clustering(
        curves_x, curves_y, numb_cluster=numb_cluster,
        method=method, pca_mode=user_pars['pca'], verbose=verbose,
        make_plots=make_plots)

    (cluster_labels, cluster_info, inertia, avg_curve, figures) = res

    if make_plots:
        if save_plots is True:
            print_plots(figures, show_plots=False, save_plots=save_plots,
                        dirname=dir_path_out)

        # Plot 3 : cluster mapping
        color_curve_clustering = get_setting("color_curve_clustering")
        cbar = plt.get_cmap(color_curve_clustering)
        colors = [cbar((numb_cluster - i) / numb_cluster)
                  for i in range(numb_cluster)]
        method_str = "K-Means" if method == "kmeans" else "GMM"
        cmap, cbar_lab = cbar_map(colors, numb_cluster, method_str)
        properties = \
            {f"Clustering ({method_str})": cluster_labels}
        colors_lab = {f"Clustering ({method_str})": cmap}
        main_mapping(properties, dim_pix, dim_mic=dim_mic,
                     colors=colors_lab, cbar_lab=cbar_lab,
                     dict_map=None, mask=[], show_plots=show_plots,
                     save_plots=save_plots, dir_path_out=dir_path_out)

    return cluster_labels, cluster_info, inertia, avg_curve


def main_vector_clustering(
        user_pars, loop_pars, curve_pars, dir_path_in, verbose=False,
        show_plots=True, save_plots=False, dir_path_out=None, dim_pix=None,
        dim_mic=None, dir_path_in_props=None):
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
    dim_pix : dict, optional
        Dictionary of pixel dimensions.
    dim_mic : dict, optional
        Dictionary of micron dimensions.
    dir_path_in_props : str, optional
        Directory path for input properties.

    Returns
    -------
    cluster_labels : dict
        Cluster indices for each data point for each mode.
    cluster_info : dict
        Information about each cluster for each mode.
    inertia : dict
        Inertia (within-cluster sum of squares) for each mode.
    avg_vector : dict
        List of average vector for each cluster in each mode.
    """

    user_pars_merged = user_pars.copy()

    if user_pars["object"] == "curve":
        user_pars_merged.update(curve_pars)
        cluster_labels, cluster_info, inertia, avg_vector = \
            main_curve_clustering(user_pars_merged, dir_path_in,
                                  verbose=verbose,
                                  show_plots=show_plots,
                                  save_plots=save_plots,
                                  dir_path_out=dir_path_out,
                                  dim_pix=dim_pix, dim_mic=dim_mic,
                                  csv_path=dir_path_in_props)

    elif user_pars["object"] == "loop":
        user_pars_merged.update(loop_pars)
        cluster_labels, cluster_info, inertia, avg_vector = \
            main_loop_clustering(user_pars_merged, dir_path_in, verbose=verbose,
                                 show_plots=show_plots,
                                 save_plots=save_plots,
                                 dir_path_out=dir_path_out,
                                 dim_pix=dim_pix, dim_mic=dim_mic,
                                 dir_path_in_props=dir_path_in_props)

    else:
        raise IOError("object parameter should be in ['curve', 'loop']")

    return cluster_labels, cluster_info, inertia, avg_vector


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

    - label_meas: list of str
        List of Measurement Name for Loops
        This parameter contains a list of measurement name in order to create
        the loop to be analyzed using a machine learning algorithm
        of clustering. If several name are filled, the loop will be
        normalized and concatenated.
        Choose from : piezoresponse, amplitude, phase, res freq and q fact
    - nb_clusters_off: int
        Number of Clusters for Off-Field Loop.
        This parameter determines the number of clusters for the
        off-field loop using a machine learning algorithm
        of clustering.
        Used in the analysis of off-field loop.
    - nb_clusters_on: int
        Number of Clusters for On-Field Loop.
        This parameter determines the number of clusters for the
        on-field loop using a machine learning algorithm
        of clustering.
        Used in the analysis of on-field loop.
    - nb_clusters_coupled: int
        Number of Clusters for Differential Loop.
        This parameter determines the number of clusters for the
        differential loop using a machine learning algorithm
        of clustering.
        Only valid only for a piezoresponse loop.
        Used in the analysis of differential component only for piezoresponse
        loop.

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
    - nb_clusters: int
        Number of Clusters for Curve.
        This parameter determines the number of clusters for the
        curve using a machine learning algorithm of clustering.

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
        config_params = get_config(__file__, fname_json)
        dir_path_in = config_params['dir_path_in']
        dir_path_out = config_params['dir_path_out']
        dir_path_in_props = config_params['dir_path_in_props']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = config_params['user_pars']
        loop_pars = config_params['loop_pars']
        curve_pars = config_params['curve_pars']
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
        verbose = True
        show_plots = True
        save = False

        user_pars = {'object': 'loop',
                     'relative': False,
                     'pca': True,
                     'method': 'kmeans'}
        loop_pars = {'label meas': ['piezoresponse'],
                     'nb clusters off': 4,
                     'nb clusters on': 4,
                     'nb clusters coupled': 4}
        curve_pars = {'extension': 'spm',
                      'mode': 'classic',
                      'label meas': ['deflection'],
                      'nb clusters': 4}

    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, loop_pars, curve_pars, dir_path_in, dir_path_out, \
        dir_path_in_props, verbose, show_plots, save


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
     dir_path_in_props, verbose, show_plots, save) = \
        parameters(fname_json=fname_json)
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,  dirname="vector_clustering",
        lvl=1, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    main_vector_clustering(
        user_pars, loop_pars, curve_pars, dir_path_in, verbose=verbose,
        show_plots=show_plots, save_plots=save, dir_path_out=dir_path_out,
        dir_path_in_props=dir_path_in_props)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()
