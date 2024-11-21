"""
--> Executable Script
Module used to perform a clustering (K-Means or Gaussian Mixture Model) for a
list of curve (amplitude, phase, piezoresponse, q_factor, resonance
frequency ...), for each pixel of a sspfm measurement.
Curves can be a composition of several measure, which will be normalized
between 0 and 1 and concatenated (for example amplitude and phase)
    - Generate a sspfm maps for each mode resulting of clustering analysis
    - Generate a graph of all curve with their cluster for each mode
    resulting of clustering analysis
"""

import os
import tkinter.filedialog as tkf
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, get_config
from PySSPFM.utils.core.clustering import \
    (data_clustering, cbar_map, plot_all_curve_clustering,
     plot_avg_curve_clustering, data_pca, plot_pca_plane)
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop_to_hyst.file import extract_properties
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.path_for_runable import save_path_management, \
    copy_json_res, create_json_res
from PySSPFM.utils.file_clustering import extract_loop_data, gen_coupled_data


def save_avg_loop(avg_loop_x, avg_loop_y, dir_path_out):
    """
    Save average loop data to text files, with each file representing
    a key in avg_loop and its corresponding values.

    Parameters
    ----------
    avg_loop_x : dict
        Dictionary where each key represents the mode (off, on, coupled), and
        each value (x-axis) is a list of loops, where each loop is an array of
        values.
    avg_loop_y : dict
        Dictionary where each key represents the mode (off, on, coupled), and
        each value (y-axis) is a list of loops, where each loop is an array of
        values.
    dir_path_out : str
        Path to the output directory where text files will be saved.

    Returns
    -------
    None
        This function does not return any values. It saves output files
        directly to the specified directory.
    """

    if not os.path.exists(dir_path_out):
        os.makedirs(dir_path_out)

    for key, y_value in avg_loop_y.items():
        file_path_out = os.path.join(dir_path_out, f'avg_loop_{key}.txt')

        # Generate cluster indices and concatenate x and y values
        cluster_index = [cont for cont, loop in enumerate(y_value)
                         for _ in loop]
        data = np.column_stack((cluster_index, np.concatenate(avg_loop_x[key]),
                                np.concatenate(y_value)))

        # Save the data with header
        header = "cluster_index\t\tx values\t\ty values"
        np.savetxt(file_path_out, data, delimiter='\t\t', header=header,
                   fmt='%s')


def save_labels(cluster_labels, dim_pix, dim_mic, toolbox_path):
    """
    Save clustering labels to a text file, with optional dimensional metadata.

    Parameters
    ----------
    cluster_labels : dict
        Dictionary where each key represents a label and each value is
        the data associated with that label.
    dim_pix : dict, optional
        Dictionary containing pixel dimensions with 'x' and 'y' keys.
    dim_mic : dict, optional
        Dictionary containing micrometer dimensions with 'x' and 'y' keys.
    toolbox_path : str
        Path to the toolbox directory from which root path is derived.

    Returns
    -------
    None
        This function does not return any values. It saves output files
        directly to the specified directory.
    """
    root_path_out = os.path.abspath(os.path.join(toolbox_path, '..', '..'))
    properties_path_out = os.path.join(root_path_out, "properties")
    if not os.path.isdir(properties_path_out):
        os.makedirs(properties_path_out)

    header_lab_add = ''
    if (dim_pix is not None) and (dim_mic is not None):
        dict_dim = {'x pix': dim_pix['x'], 'y pix': dim_pix['y'],
                    'x mic': dim_mic['x'], 'y mic': dim_mic['y']}
        header_lab_tab = [f'{key}={val}, ' for key, val in dict_dim.items()]
        header_lab_add = ''.join(header_lab_tab)

    file_path_out = os.path.join(properties_path_out,
                                 'properties_clustering.txt')
    header = f'clustering\n{header_lab_add}\n'

    tab_props = []

    for key, value in cluster_labels.items():
        header += f'{key}\t\t'
        tab_props.append(value)

    np.savetxt(file_path_out, np.array(tab_props).T, delimiter='\t\t',
               newline='\n', header=header, fmt='%s')


def normalize_and_concatenate_curves(curve_sets):
    """
    Normalize a set of curves grouped in a list and concatenate them
    after normalization.

    Parameters
    ----------
    curve_sets : list of lists or arrays
        List of curve sets where each element is a set of curves
        (list or array).

    Returns
    -------
    concatenated_curve_data : list of arrays
        List of concatenated normalized curves for each set of curves.
    """
    normalization_params = []

    # Calculate normalization coefficients a and b for each set of curves
    for curves in curve_sets:
        curves_array = np.array(curves)
        mean_curve = np.mean(curves_array, axis=0)
        a_coef = 1 / (np.max(mean_curve) - np.min(mean_curve))
        b_coef = np.min(mean_curve)
        normalization_params.append((a_coef, b_coef))

    def normalize_curve(curve, a_coef, b_coef):
        return a_coef * (np.array(curve) - b_coef)

    concatenated_curve_data = []

    # Apply normalization and concatenate the curves
    for curve_group in zip(*curve_sets):
        normalized_curves = []
        for i, curve in enumerate(curve_group):
            a_coef, b_coef = normalization_params[i]
            normalized_curve = normalize_curve(curve, a_coef, b_coef)
            normalized_curves.append(normalized_curve)
        concatenated_curve_data.append(np.concatenate(normalized_curves))

    return concatenated_curve_data


def perform_curve_clustering(data_x, data_y, numb_cluster=3,
                             method="kmeans", relative_mode=False, mode=None,
                             verbose=False, make_plots=False,
                             plot_axis_y=None):
    """
    Perform curve clustering.

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
    relative_mode : bool, optional
        Whether to perform relative (each curve (i.e data_y) vary between 0
        and 1) analysis (default is False).
    mode: str, optional
        Mode of processing (off, on coupled ...) (default is None).
    verbose : bool, optional
        Whether to display verbose information (default is False).
    make_plots : bool, optional
        Whether to generate plots (default is False).
    plot_axis_y : int, optional
        Index of the y-axis data to be used for plotting if multiple datasets
        are provided.  If None (default), the combined dataset is used for
        plotting as y values. This parameter allows the user  to specify which
        dataset (by index) to visualize when multiple y datasets are present.

    Returns
    -------
    cluster_labels : list
        List of cluster labels.
    cluster_info : list
        List of cluster information.
    inertia : float
        Inertia value.
    x_avg : list
        List of average x data by cluster.
    y_avg : list
        List of average y data by cluster.
    figures : list
        List of generated figures.
    """
    mode = "" if mode is None else mode

    def convert_array(iterable):
        if isinstance(iterable, list):
            iterable = np.array(iterable)
            return iterable
        elif isinstance(iterable, np.ndarray):
            return iterable
        else:
            raise TypeError(
                "The variable must be either a list or a NumPy array.")

    data_x = convert_array(data_x)
    data_y = convert_array(data_y)
    dim = data_x.shape[0]

    # Handling multiple concatenated curves
    proc_step1_xdata = np.concatenate(data_x, axis=1)

    if dim > 1:
        proc_step1_ydata = normalize_and_concatenate_curves(data_y)
    # Each curve vary between 0 and 1
    elif relative_mode:
        proc_step1_ydata = [
            [(sub_elem - np.min(elem)) / (np.max(elem) - np.min(elem))
             for sub_elem in elem] for elem in data_y[0]]
    else:
        proc_step1_ydata = data_y[0]

    # Init the clustering with PCA analysis
    proc_step2_ydata = data_pca(proc_step1_ydata, dimension=2)

    # Data clustering
    cluster_labels, cluster_info, inertia, centers = data_clustering(
        proc_step2_ydata, num_clusters=numb_cluster, method=method,
        verbose=verbose)

    # Calculate Average data by Cluster
    y_avg, x_avg = [], []
    if plot_axis_y is None:
        x_s = proc_step1_xdata
        y_s = proc_step1_ydata
    else:
        x_s = data_x[plot_axis_y]
        y_s = data_y[plot_axis_y]
    for cluster_idx in range(numb_cluster):
        cluster_mask = np.array(cluster_labels) == cluster_idx
        x_avg.append(
            np.mean(np.array(x_s)[cluster_mask], axis=0))
        y_avg.append(
            np.mean(np.array(y_s)[cluster_mask], axis=0))

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
        print('\n')

    # Generate plots if specified
    figures = []
    if make_plots:

        # Color of figures
        color_curve_clustering = get_setting("color_curve_clustering")
        cbar = plt.get_cmap(color_curve_clustering)
        colors = [cbar((numb_cluster - i) / numb_cluster)
                  for i in range(numb_cluster)]

        figures += plot_pca_plane(
            proc_step2_ydata, label_clust=cluster_labels,
            colors=colors, centers=centers,
            figname=f"clusters_centroids_{mode}")
        figures += plot_all_curve_clustering(
            x_s, y_s, numb_cluster,
            cluster_labels, cluster_info, colors,
            figname=f"clustering_best_curves_{mode}")
        figures += plot_avg_curve_clustering(
            x_avg, y_avg, numb_cluster,
            cluster_info, colors, figname=f"clustering_average_curves_{mode}")

    return cluster_labels, cluster_info, inertia, x_avg, y_avg, figures


def main_loop_clustering(
        user_pars, dir_path_in, verbose=False, show_plots=True,
        save=False, dir_path_out=None, dim_pix=None, dim_mic=None,
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
    save : bool, optional
        If True, save generated plots and results.
    dir_path_out : str, optional
        Output directory for saving plots and results.
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
    avg_loop_x : dict
        List of average loop (for x axis) for each cluster in each mode.
    avg_loop_y : dict
        List of average loop (for y axis) for each cluster in each mode.
    """

    method = user_pars["method"]
    assert method in ["kmeans", "gmm"], \
        "Invalid clustering method. Method must be either 'kmeans' or 'gmm'."
    make_plots = bool(show_plots or save)

    modes = [key.split()[-1] for key, value in user_pars.items() if
             'clusters' in key and value is not None]
    if user_pars['label meas'] != ['piezoresponse']:
        modes = [lab for lab in modes if lab != 'coupled']
    lab_tab = [['on', 'off', 'coupled'], ['y', 'w', 'r'],
               ['On Field', 'Off Field', 'Coupled']]
    cluster_labels, cluster_info, inertia, avg_loop_x, avg_loop_y = \
        {}, {}, {}, {}, {}
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

            res = perform_curve_clustering(
                    loops_x[mode], loops_y[mode],
                    numb_cluster=numb_cluster,
                    method=method, relative_mode=user_pars['relative'],
                    mode=mode, verbose=verbose, make_plots=make_plots)
            (cluster_labels[mode], cluster_info[mode], inertia[mode],
             avg_loop_x[mode], avg_loop_y[mode], figures) = res

            if make_plots:
                if save is True:
                    print_plots(figures, show_plots=False,
                                save_plots=save, dirname=dir_path_out)

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
                             save_plots=save, dir_path_out=dir_path_out)
        except KeyError:
            print(f"KeyError management with except: no {mode} mode available "
                  f"for analysis")
            continue

    # save_results
    if save:
        save_labels(cluster_labels, dim_pix, dim_mic, dir_path_out)
        save_avg_loop(avg_loop_x, avg_loop_y, dir_path_out)

    return cluster_labels, cluster_info, inertia, avg_loop_x, avg_loop_y


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)

    - relative: bool
        Activation key for relative clustering analysis.
        This parameter serves as an activation key to perform clustering
        analysis on relative curves (all curves vary between 0 and 1).
        Always active for combined curves of multiple measurements.
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

    - dir_path_in: str
        Input Directory for Curve Files (default: 'best_nanoloops').
        This parameter specifies the directory path for the curve
        files, to perform clustering analysis.
    - dir_path_out: str
        Saving directory for analysis results
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the results of the
        analysis will be saved.
    - dir_path_in_props: str
        Properties files directory
        (optional, default: properties).
        This parameter specifies the directory containing the properties files,
        which is a text file generated after the 2nd step of the analysis.
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
        # Select curve folder
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt\best_nanoloops
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # curve_clustering_2023-10-02-16h38m
        dir_path_in_props = None
        # dir_path_in_props = r'...\KNN500n_15h18m02-10-2023_out_dfrt\properties
        config_params = {
            "dir_path_in": dir_path_in,
            "dir_path_out": dir_path_out,
            "dir_path_in_props": dir_path_in_props,
            "verbose": True,
            "show_plots": True,
            "save": False,
            'user_pars': {'relative': False,
                          'method': 'kmeans',
                          'label meas': ['piezoresponse'],
                          'nb clusters off': 4,
                          'nb clusters on': 4,
                          'nb clusters coupled': 4}
        }
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return config_params['user_pars'], config_params['dir_path_in'], \
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
    (user_pars, dir_path_in, dir_path_out, dir_path_in_props,
     verbose, show_plots, save, fname_json,
     config_params) = parameters(fname_json=fname_json)
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,  dirname="curve_clustering",
        lvl=1, create_path=True, post_analysis=True)
    # Main function
    main_loop_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=show_plots,
        save=save, dir_path_out=dir_path_out,
        dir_path_in_props=dir_path_in_props)
    # Save parameters
    if save:
        if get_setting("extract_parameters") in ['json', 'toml']:
            copy_json_res(fname_json, dir_path_out, verbose=verbose)
        else:
            create_json_res(config_params, dir_path_out,
                            fname="curve_clustering_params.json",
                            verbose=verbose)


if __name__ == '__main__':
    main()
