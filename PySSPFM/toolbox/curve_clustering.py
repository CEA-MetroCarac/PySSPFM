"""
--> Executable Script
Module used to perform a clustering (K-Means) for all best curve
(with a chosen measure, for example piezoresponse), for each pixel 
(one curve for each mode) of a sspfm measurement.
Curve can be a composition of several measure, which will be normalized
between 0 and 1 and concatenated (for example amplitude and phase)
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
import matplotlib.colors as mcolors
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.nanoloop_to_hyst.file import extract_properties
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def gen_curve_data(data):
    """
    Extract 2D curves data from a 3-row data array.

    Parameters
    ----------
    data : numpy.ndarray
        2+nb_y_meas-row data array where the first row contains indices,
        the second row contains voltage values, and the other
        row contains y_axis values.

    Returns
    -------
    curves_x : list of list
        Polarization voltage data for each curve.
    curves_y : list of list
        y_axis data for each curve.
    """

    data_x, data_y = [], []

    # Segmentation
    index_changes = np.where(data[0][:-1] != data[0][1:])[0] + 1
    for cont, teab_meas in enumerate(data[2]):
        data_x.append([])
        data_y.append([])
        data_x[cont] = np.split(data[1], index_changes)
        data_y[cont] = np.split(teab_meas, index_changes)

    # Normalize data_y if len > 2 (for multi data y)
    if len(data_y) >= 2:
        for cont, tab_data_y in enumerate(data_y):
            min_val = np.min(tab_data_y)
            max_val = np.max(tab_data_y)
            data_y[cont] = (tab_data_y - min_val) / (max_val - min_val)

    # Concatenation for multi data y
    curves_x = np.concatenate(data_x, axis=1)
    curves_y = np.concatenate(data_y, axis=1)

    return curves_x, curves_y


def extract_data(dir_path_in, name_files, modes, tab_label):
    """
    Extract data from files based on modes and cluster counts.

    Parameters
    ----------
    dir_path_in : str
        Directory path where the data files are located.
    name_files : list of str
        List of file names to process.
    modes : list of str
        List of modes to consider.
    tab_label: list of str
        List of measurement name for the curve

    Returns
    -------
    curves_x : dict
        Dictionary containing x-axis data for each mode.
    curves_y : dict
        Dictionary containing y-axis data for each mode.
    """

    curves_x, curves_y = {}, {}

    for name_file in name_files:
        mode_cluster = ""
        for mode in modes:
            if mode in name_file:
                mode_cluster = mode
                break
        if mode_cluster:
            if mode_cluster != "coupled":
                path = os.path.join(dir_path_in, name_file)
                with open(path, 'r', encoding="latin-1") as file:
                    header = file.readlines()[1]
                    header = header.replace('\n', '').replace('# ', '')
                    tab_header = header.split('\t\t')
                data = np.loadtxt(path, skiprows=2).T
                data_dict = {}
                for key, data_row in zip(tab_header, data):
                    data_dict[key] = data_row
                index = data_dict['index pix']
                data_x = data_dict['voltage']
                data_y = [data_dict[label] for label in tab_label]
                curves_x[mode_cluster], curves_y[mode_cluster] = \
                    gen_curve_data([index, data_x, data_y])

    return curves_x, curves_y


def gen_coupled_data(curves_x, curves_y, offsets=None):
    """
    Generate coupled data by subtracting 'off' from 'on' field measurements:
    only for piezoresponse curve

    Parameters
    ----------
    curves_x : dict
        Dictionary containing 'on' and 'off' field measurements for x-axis.
    curves_y : dict
        Dictionary containing 'on' and 'off' field measurements for y-axis.
    offsets: list of float, optional
        List with fit determined vertical offset for off field measurements
        (default: None)

    Returns
    -------
    curves_x : dict
        Updated dictionary containing 'coupled' measurements for x-axis.
    curves_y : dict
        Updated dictionary containing 'coupled' measurements for y-axis.
    """

    if "on" in curves_x.keys() and "off" in curves_x.keys():

        curves_x["coupled"] = curves_x["on"]
        curves_y["coupled"] = [
            [on - off for on, off in zip(curve_y_on, curve_y_off)]
            for curve_y_on, curve_y_off in zip(curves_y["on"], curves_y["off"])]
        if offsets is not None:
            if len(offsets) == len(curves_y["coupled"]):
                for i, curve_y_coupled in enumerate(curves_y["coupled"]):
                    curves_y["coupled"][i] = [elem+offsets[i]
                                              for elem in curve_y_coupled]
    else:
        print("For coupled analysis, both 'on' and 'off' field "
              "measurements should be available.")

    return curves_x, curves_y


def cbar_map(colors, numb_cluster):
    """
    Generate a colormap and colorbar labels for clustering visualization.

    Parameters
    ----------
    colors : list of tuple
        List of RGB color tuples.
    numb_cluster : int
        Number of clusters.

    Returns
    -------
    cmap : matplotlib.colors.ListedColormap
        Colormap.
    cbar_lab : dict
        Dictionary of colorbar labels.
    """

    # Create a ListedColormap using the provided colors
    cmap = mcolors.ListedColormap(colors)

    # Generate colorbar labels
    lab_clust = list(range(numb_cluster))
    x1 = min(lab_clust)
    x2 = max(lab_clust)
    y1 = x1 + (numb_cluster - 1) / (numb_cluster * 2)
    y2 = x2 - (numb_cluster - 1) / (numb_cluster * 2)
    slope = (y2 - y1) / (x2 - x1)
    offset = y1 - x1 * slope
    coordinate = [slope * elem + offset for elem in lab_clust]
    cbar_lab = {"Clustering (K-Means)": [[chr(65+i) for i in lab_clust],
                                         coordinate]}

    return cmap, cbar_lab


def cluster_kmeans(curve_data, num_clusters=3):
    """
    Perform K-Means clustering on curve data.

    Parameters
    ----------
    curve_data : numpy.ndarray
        Curve data for clustering.
    num_clusters : int, optional
        Number of clusters to create. Default is 3.

    Returns
    -------
    cluster_labels : list
        Cluster indices for each data point
    cluster_info : list
        Information about each cluster.
    inertia : float
        Inertia (within-cluster sum of squares).
    """

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(curve_data)
    cluster_labels = kmeans.labels_

    # Calculate intra-cluster inertia (within-cluster sum of squares)
    inertia = kmeans.inertia_

    # Count the number of points in each cluster
    cluster_counts = np.bincount(cluster_labels)

    # Calculate cluster centers
    cluster_centers = kmeans.cluster_centers_

    # Calculate pairwise distances between cluster centers
    distances = pairwise_distances(cluster_centers, metric='euclidean')

    # Reference cluster (position 0) = cluster with maximum of points
    arg_ref = np.argmax(cluster_counts)
    # Other cluster sorted with distance of the reference cluster
    sorted_indices = [arg_ref] + list(np.argsort(distances[arg_ref]))[1:]

    # Change of cluster_labels with sorted indexs
    cluster_labels = [sorted_indices.index(i) for i in cluster_labels]

    # All cluster info
    cluster_info = []
    for i in range(num_clusters):
        target = np.sort(distances[i])[1]
        near_clust_index = list(distances[i]).index(target)
        near_clust_name = chr(65 + sorted_indices.index(near_clust_index))
        # [0]: distance ref, [1]: distance near, [2]: name near,
        # [3]: nb of points, [4]: clust name
        tab = [distances[arg_ref][i],
               distances[i][near_clust_index],
               near_clust_name,
               cluster_counts[i],
               chr(65 + sorted_indices.index(i))]
        cluster_info.append(tab)
    # sort cluster_info with distance of the reference cluster
    sort_tab = np.argsort([line[0] for line in cluster_info])
    cluster_info = [cluster_info[arg] for arg in sort_tab]

    return cluster_labels, cluster_info, inertia


def main_curve_clustering(
        user_pars, dir_path_in, verbose=False, show_plots=True,
        save_plots=False, dir_path_out=None, dim_pix=None, dim_mic=None,
        dir_path_in_props=None):
    """
    Perform curve clustering analysis.

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
    avg_curve : dict
        List of average curve for each cluster in each mode.
    """

    name_files = os.listdir(dir_path_in)
    modes = [key.split()[-1] for key, value in user_pars.items() if
             'clusters' in key and value is not None]
    if user_pars['label meas'] != ['piezoresponse']:
        modes = [lab for lab in modes if lab != 'coupled']
    lab_tab = [['on', 'off', 'coupled'], ['y', 'w', 'r'],
               ['On Field', 'Off Field', 'Coupled']]
    cluster_labels, cluster_info, inertia, avg_curve = {}, {}, {}, {}
    offsets = []
    make_plots = bool(show_plots or save_plots)

    # Extract curve data
    curves_x, curves_y = extract_data(dir_path_in, name_files, modes,
                                      user_pars['label meas'])

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

    # If "coupled" mode is present, calculate coupled curve
    # (only for piezoresponse)
    if "coupled" in modes:
        curves_x, curves_y = gen_coupled_data(curves_x, curves_y,
                                              offsets=offsets)

    # Perform clustering for each mode
    for mode in modes:
        try:
            # K-Means
            numb_cluster = user_pars[f'nb clusters {mode}']
            res = cluster_kmeans(curves_y[mode], numb_cluster)
            cluster_labels[mode], cluster_info[mode], inertia[mode] = res

            # Calculate Average curve by Cluster
            avg_curve[mode] = []
            for cluster_idx in range(numb_cluster):
                cluster_mask = np.array(cluster_labels[mode]) == cluster_idx
                avg_curve[mode].append(
                    np.mean(np.array(curves_y[mode])[cluster_mask], axis=0))

            # Clustering results in str
            labels = []
            for i in range(numb_cluster):
                labels.append(f'Cluster {cluster_info[mode][i][4]}, '
                              f'{cluster_info[mode][i][3]} points'
                              ', near dist '
                              f'({cluster_info[mode][i][2]}) : '
                              f'{cluster_info[mode][i][1]:.2e}'
                              ', ref (A) dist : '
                              f'{cluster_info[mode][i][0]:.2e}')

            if verbose:
                print(f'\n{mode} :')
                _ = [print(label) for label in labels]

            # Generate plots if specified
            if make_plots:
                # Color of figures
                color_curve_clustering = get_setting("color_curve_clustering")
                cbar = plt.get_cmap(color_curve_clustering)
                colors = [cbar((numb_cluster - i) / numb_cluster)
                          for i in range(numb_cluster)]
                cmap, cbar_lab = cbar_map(colors, numb_cluster)

                # Plot 1 : All Curve by Cluster
                # Legend
                legend_handles = []
                for i in range(numb_cluster):
                    legend_handles.append(Patch(color=colors[i],
                                                label=labels[i]))

                figs = []

                # Create graph
                figsize = get_setting("figsize")
                fig1, ax = plt.subplots(figsize=figsize)
                fig1.sfn = f"clustering_best_loops_{mode}"
                plot_dict_1 = {
                    'title': f'Clustering (K-Means): Best Loops ({mode})',
                    'x lab': 'Voltage', 'y lab': 'Y Axis',
                    'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
                plot_graph(ax, [], [], plot_dict=plot_dict_1)
                # Plot each curve
                for i, (elem_x, elem_y) in enumerate(zip(
                        curves_x[mode], curves_y[mode])):
                    color = colors[cluster_labels[mode][i]]
                    plt.plot(elem_x, elem_y, color=color)
                ax.legend(handles=legend_handles)
                figs += [fig1]

                # Plot 2 : Average Curve by Cluster
                # Create graph
                fig2, ax = plt.subplots(figsize=figsize)
                fig2.sfn = f"clustering_average_loops_{mode}"
                plot_dict_3 = {
                    'title': f'Average Curve by Cluster ({mode})',
                    'x lab': 'Voltage', 'y lab': 'Y Axis',
                    'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
                plot_graph(ax, [], [], plot_dict=plot_dict_3)
                # Plot Average Curve by Cluster
                for index in range(numb_cluster):
                    color = colors[index]
                    label = f'Cluster {cluster_info[mode][index][4]}'
                    plt.plot(curves_x[mode][0], avg_curve[mode][index],
                             label=label, color=color)
                ax.legend()
                figs += [fig2]
                if save_plots is True:
                    print_plots(figs, show_plots=False, save_plots=save_plots,
                                dirname=dir_path_out)

                # Plot 3 : cluster mapping
                properties = {"Clustering (K-Means)": cluster_labels[mode]}
                colors_lab = {"Clustering (K-Means)": cmap}
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

    return cluster_labels, cluster_info, inertia, avg_curve


def parameters():
    """
    To complete by user of the script: return parameters for analysis
    - label_meas: list of str
        List of Measurement Name for Curves
        This parameter contains a list of measurement name in order to create
        the curve to be analyzed using a machine learning algorithm
        of clustering (K-Means). If several name are filled, the curve will be
        normalized and concatenated.
        Choose from : piezoresponse, amplitude, phase, res freq and q fact
    - nb_clusters_off: int
        Number of Clusters for Off-Field Curve.
        This parameter determines the number of clusters for the
        off-field curve using a machine learning algorithm
        of clustering (K-Means).
        Used in the analysis of off-field curve.
    - nb_clusters_on: int
        Number of Clusters for On-Field Curve.
        This parameter determines the number of clusters for the
        on-field curve using a machine learning algorithm
        of clustering (K-Means).
        Used in the analysis of on-field curve.
    - nb_clusters_coupled: int
        Number of Clusters for Differential Curve.
        This parameter determines the number of clusters for the
        differential curve using a machine learning algorithm
        of clustering (K-Means).
        Only valid only for a piezoresponse curve.
        Used in the analysis of differential component only for piezoresponse
        curve.

    - dir_path_in: str
        Input Directory for Best Loop TXT Files (default: 'best_nanoloops').
        This parameter specifies the directory path for the best loop .txt
        files generated after the second step of the analysis.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - dir_path_in_props: str
        Properties files directory
        (optional, default: properties).
        This parameter specifies the directory containing the properties text
        files generated after the 2nd step of the analysis.
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
        script_directory = os.path.realpath(__file__)
        file_path_user_params = script_directory.split('.')[0] + \
            f'_params.{get_setting("extract_parameters")}'
        # Load parameters from the specified configuration file
        print(f"user parameters from {os.path.split(file_path_user_params)[1]} "
              f"file")
        config_params = load_parameters_from_file(file_path_user_params)
        dir_path_in = config_params['dir_path_in']
        dir_path_out = config_params['dir_path_out']
        dir_path_in_props = config_params['dir_path_in_props']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = config_params['user_pars']
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Select txt best loops folder (.txt)
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt\best_nanoloops
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # curve_clustering_2023-10-02-16h38m
        dir_path_in_props = None
        # dir_path_in_props = r'...\KNN500n_15h18m02-10-2023_out_dfrt\properties
        verbose = True
        show_plots = True
        save = False

        user_pars = {'label meas': ['piezoresponse'],
                     'nb clusters off': 4,
                     'nb clusters on': 4,
                     'nb clusters coupled': 4}

    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, dir_path_in, dir_path_out, dir_path_in_props, verbose, \
        show_plots, save


def main():
    """ Main function for data analysis. """
    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, dir_path_in_props, verbose,
     show_plots, save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,  dirname="curve_clustering",
        lvl=1, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    main_curve_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=show_plots,
        save_plots=save, dir_path_out=dir_path_out,
        dir_path_in_props=dir_path_in_props)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()