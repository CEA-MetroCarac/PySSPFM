"""
--> Executable Script
Module used to perform a clustering (K-Means or Gaussian Mixture Model) for all
best curve (with a chosen measure, for example deflection), for each pixel
(one curve for each mode) of a sspfm measurement.
Curve can be a composition of several measure, which will be normalized
between 0 and 1 and concatenated (for example height and deflection)
    - Generate a sspfm maps for each mode resulting of clustering analysis
    - Generate a graph of all curve with their cluster for each mode
    resulting of clustering analysis
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from PySSPFM.settings import get_setting, copy_default_settings_if_not_exist
from PySSPFM.utils.core.clustering import curve_clustering, cbar_map
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.core.path_management import \
    get_filenames_with_conditions, sort_filenames
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars
from PySSPFM.utils.raw_extraction import \
    data_identification, extr_data_table, csv_meas_sheet_extract, NanoscopeError


def data_extraction(file_path_in, extension="spm", mode_dfrt=False):
    """
    Extracts data from different types of files.

    Parameters
    ----------
    file_path_in : str
        Path to the input file.
    extension : str, optional
        File extension. Default is "spm".
    mode_dfrt: bool, optional
        If mode_dfrt is True, a dfrt measure is performed and vice versa

    Returns
    -------
    dict_meas : dict
        Dictionary containing measurement data.
    """
    if "spm" in extension:

        try:
            from PySSPFM.utils.datacube_reader import DataExtraction  # noqa
        except (NotImplementedError, NameError) as error:
            message = "To open DATACUBE spm file (Bruker), nanoscope module " \
                      "is required and NanoScope Analysis software (Bruker) " \
                      "should be installed on the computer"
            raise NanoscopeError(message) from error

        # DataExtraction object is used to extract info from .spm file
        data_extract = DataExtraction(file_path_in)

        # .spm file basic info
        data_extract.data_extraction()

        # .spm file info: raw data
        data_extract.data_extraction(raw_data=True)
        raw_dict = data_extract.raw_dict

        # Data identification
        dict_meas = data_identification(
            raw_dict, type_file=extension, mode_dfrt=mode_dfrt)

    else:
        dict_meas, _ = extr_data_table(file_path_in, mode_dfrt=mode_dfrt)

    return dict_meas


def extract_data(dir_path_in, tab_label, mode="classic", extension="spm"):
    """
    Extract data from files based on modes and cluster counts.

    Parameters
    ----------
    dir_path_in : str
        Directory path where the data files are located.
    tab_label: list of str
        List of measurement name for the curve
    extension: str, optional
        Extension of files.
        Four possible values: 'spm' or 'txt' or 'csv' or 'xlsx'.
    mode: str
        Mode of measurement used (extraction of measurements).
        Two possible values: 'classic' (sweep or single frequency) or 'dfrt'.

    Returns
    -------
    curves_x : dict
        Dictionary containing x-axis data for each mode.
    curves_y : dict
        Dictionary containing y-axis data for each mode.
    """

    filenames = get_filenames_with_conditions(dir_path_in, prefix=None,
                                              extension=extension)
    sorted_filenames, _, _ = sort_filenames(filenames)

    data_lab_x = {}
    data_lab_y = {}
    for label in tab_label:
        data_lab_x[label] = []
        data_lab_y[label] = []

    for filename in sorted_filenames:
        file_path_in = os.path.join(dir_path_in, filename)
        dict_meas = data_extraction(file_path_in, extension=extension,
                                    mode_dfrt=bool(mode.lower() == 'dfrt'))
        for label in tab_label:
            data_lab_x[label].append(dict_meas["times"])
            data_lab_y[label].append(dict_meas[label])

    # Normalize curve_y if len > 2 (for multi data y)
    if len(data_lab_y) >= 2:
        curve_x = list(data_lab_x.values())
        curve_y = list(data_lab_y.values())
        for cont, (tab_data_x, tab_data_y) in enumerate(zip(curve_x, curve_y)):
            min_val = np.min(tab_data_y)
            max_val = np.max(tab_data_y)
            curve_x[cont] = tab_data_x
            curve_y[cont] = (tab_data_y - min_val) / (max_val - min_val)
        curve_x = np.concatenate(curve_x, axis=1)
        curve_y = np.concatenate(curve_y, axis=1)
    else:
        curve_x = data_lab_x[tab_label[0]]
        curve_y = data_lab_y[tab_label[0]]

    return curve_x, curve_y


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
    cluster_labels : dict
        Cluster indices for each data point for each mode.
    cluster_info : dict
        Information about each cluster for each mode.
    inertia : dict
        Inertia (within-cluster sum of squares) for each mode.
    avg_curve : dict
        List of average curve for each cluster in each mode.
    """
    method = user_pars["method"]
    assert method in ["kmeans", "gmm"], \
        "Invalid clustering method. Method must be either 'kmeans' or 'gmm'."
    make_plots = bool(show_plots or save_plots)

    # Extract curve data
    curves_x, curves_y = extract_data(dir_path_in, user_pars['label meas'],
                                      mode=user_pars['mode'],
                                      extension=user_pars['extension'])

    # Extract extra analysis info (scan dim + vertical offset (off field))
    if dir_path_in is not None:
        if csv_path is None:
            csv_path = dir_path_in
        else:
            csv_path, _ = os.path.split(csv_path)
        csv_meas, _ = csv_meas_sheet_extract(csv_path, verbose=verbose)
        dim_pix = {'x': csv_meas['Grid x [pix]'], 'y': csv_meas['Grid y [pix]']}
        dim_mic = {'x': csv_meas['Grid x [um]'], 'y': csv_meas['Grid y [um]']}

    numb_cluster = user_pars['nb clusters']
    if isinstance(curves_y, list):
        curves_y = np.array(curves_y)

    cluster_labels, cluster_info, inertia, centers = curve_clustering(
        curves_y, num_clusters=numb_cluster, method=method, verbose=verbose)

    # Calculate Average curve by Cluster
    avg_curve = []
    for cluster_idx in range(numb_cluster):
        cluster_mask = np.array(cluster_labels) == cluster_idx
        avg_curve.append(
            np.mean(np.array(curves_y)[cluster_mask], axis=0))

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
    if make_plots:

        # Color of figures
        color_curve_clustering = get_setting("color_curve_clustering")
        cbar = plt.get_cmap(color_curve_clustering)
        colors = [cbar((numb_cluster - i) / numb_cluster)
                  for i in range(numb_cluster)]
        method_str = "K-Means" if method == "kmeans" else "GMM"
        cmap, cbar_lab = cbar_map(colors, numb_cluster, method_str)

        # Plot 1 : All Curve by Cluster
        # Legend
        legend_handles = []
        for i in range(numb_cluster):
            legend_handles.append(
                Patch(color=colors[i], label=labels[i]))

        figs = []

        # Create graph
        figsize = get_setting("figsize")
        fig1, ax = plt.subplots(figsize=figsize)
        fig1.sfn = "clusters_centroids"
        plot_dict_1 = {
            'title': 'Clusters with Centroids',
            'x lab': 'Feature 1', 'y lab': 'Feature 2',
            'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
        plot_graph(ax, [], [], plot_dict=plot_dict_1)

        # Plot data points
        for index in range(numb_cluster):
            tab_lab = np.array(cluster_labels)
            cluster_data = curves_y[tab_lab == index]
            cluster_data = np.array(cluster_data)

            # Plot data points for the current cluster
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1],
                        c=[colors[index]],
                        label=f'Cluster {cluster_info[index][4]}')
        # Plot centroids
        plt.scatter(centers[:, 0], centers[:, 1],
                    marker='x', color='black', label='Centroids')
        ax.legend()
        figs += [fig1]

        # Create graph
        figsize = get_setting("figsize")
        fig2, ax = plt.subplots(figsize=figsize)
        fig2.sfn = "clustering_best_loops"
        plot_dict_1 = {
            'title': f'Clustering ({method_str}): Best Loops',
            'x lab': 'Voltage', 'y lab': 'Y Axis',
            'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
        plot_graph(ax, [], [], plot_dict=plot_dict_1)
        # Plot each curve
        for i, (elem_x, elem_y) in enumerate(zip(
                curves_x, curves_y)):
            color = colors[cluster_labels[i]]
            plt.plot(elem_x, elem_y, color=color)
        ax.legend(handles=legend_handles)
        figs += [fig2]

        # Plot 2 : Average Curve by Cluster
        # Create graph
        fig3, ax = plt.subplots(figsize=figsize)
        fig3.sfn = "clustering_average_loops"
        plot_dict_3 = {
            'title': 'Average Curve by Cluster',
            'x lab': 'Voltage', 'y lab': 'Y Axis',
            'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
        plot_graph(ax, [], [], plot_dict=plot_dict_3)
        # Plot Average Curve by Cluster
        for index in range(numb_cluster):
            color = colors[index]
            label = f'Cluster {cluster_info[index][4]}'
            plt.plot(curves_x[0], avg_curve[index],
                     label=label, color=color)
        ax.legend()
        figs += [fig3]

        if save_plots is True:
            print_plots(figs, show_plots=False, save_plots=save_plots,
                        dirname=dir_path_out)

        # Plot 3 : cluster mapping
        properties = \
            {f"Clustering ({method_str})": cluster_labels}
        colors_lab = {f"Clustering ({method_str})": cmap}
        main_mapping(properties, dim_pix, dim_mic=dim_mic,
                     colors=colors_lab, cbar_lab=cbar_lab,
                     dict_map=None, mask=[], show_plots=show_plots,
                     save_plots=save_plots, dir_path_out=dir_path_out)

    return cluster_labels, cluster_info, inertia, avg_curve


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis
    - extension: str, optional
        Extension of files.
        This parameter determines the extension type of curve files.
        Four possible values: 'spm' or 'txt' or 'csv' or 'xlsx'.
    - mode: str
        Mode of measurement used (extraction of measurements).
        This parameter determines the method used for measurements,
        specifically for the extraction measurements.
        Two possible values: 'classic' (sweep or single frequency) or 'dfrt'.
    - method: str
        Name of the method used to perform the clustering
        This parameter determines the method used to perform the clustering.
        Implemented methods are K-Means or Gaussian Mixture Model (GMM).
        Choose from : "kmeans", "gmm"
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
        Input Directory for Curves Files.
        This parameter specifies the directory path for curve files.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - csv_file_path: str
        File path of the CSV measurement file (measurement sheet model).
        This parameter specifies the file path to the CSV file containing
        measurement parameters. It is used to indicate the location of the
        CSV file, which serves as the source of measurement data for processing.
        If left empty, the system will automatically select the CSV file path.
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
        # if fname_json is provided, use it, else use the default one
        if fname_json is not None:
            file_path_user_params = fname_json
        else:
            file_path = os.path.realpath(__file__)
            file_path_user_params = copy_default_settings_if_not_exist(file_path)

        # Load parameters from the specified configuration file
        print(f"user parameters from {os.path.split(file_path_user_params)[1]} "
              f"file")
        config_params = load_parameters_from_file(file_path_user_params)
        dir_path_in = config_params['dir_path_in']
        dir_path_out = config_params['dir_path_out']
        csv_file_path = config_params['csv_file_path']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = config_params['user_pars']
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Select txt curve folder
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # curve_clustering_2023-10-02-16h38m
        csv_file_path = None
        # csv_file_path =
        # r'...\KNN500n\measurement sheet model SSPFM ZI DFRT.csv'
        verbose = True
        show_plots = True
        save = False

        user_pars = {'extension': 'spm',
                     'mode': 'classic',
                     'method': 'kmeans',
                     'label meas': ['deflection'],
                     'nb clusters': 4}

    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, dir_path_in, dir_path_out, csv_file_path, verbose, \
        show_plots, save


def main(fname_json=None):
    """ Main function for data analysis. """
    # Extract parameters
    (user_pars, dir_path_in, dir_path_out, csv_file_path, verbose,
     show_plots, save) = parameters(fname_json=fname_json)
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,  dirname="curve_clustering",
        lvl=1, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    main_curve_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=show_plots,
        save_plots=save, dir_path_out=dir_path_out,
        csv_path=csv_file_path)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()
