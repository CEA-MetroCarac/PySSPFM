"""
--> Executable Script
Module used to perform a clustering (K-Means) for all best hysteresis
(for each pixel, one hysteresis for each mode) of a sspfm measurement
    - Generate a sspfm maps for each mode resulting of clustering analysis
    - Generate a graph of all hysteresis with their cluster for each mode
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

from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.hyst_to_map.file import extract_measures
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars

from settings import FIGSIZE, ELECTROSTATIC_OFFSET, COLOR_HYSTERESIS_CLUSTERING


def hyst_2d(datas):
    """
    Extract 2D hysteresis data from a 3-row data array.

    Parameters
    ----------
    datas : numpy.ndarray
        3-row data array where the first row contains indices,
        the second row contains voltage values, and the third
        row contains piezorepsonse values.

    Returns
    -------
    hysts_x : list of list
        Object containing voltage data for each hysteresis loop.
    hysts_y : list of list
        Object containing piezorep data for each hysteresis loop.
    """

    cont = 1
    hysts_x = [[]]
    hysts_y = [[]]
    for index, voltage, piezorep in zip(datas[0], datas[1], datas[2]):
        if cont != index:
            cont += 1
            hysts_x.append([])
            hysts_y.append([])
        hysts_x[cont - 1].append(voltage)
        hysts_y[cont - 1].append(piezorep)

    return hysts_x, hysts_y


def extract_data(dir_path_in, name_files, modes):
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

    Returns
    -------
    hysts_x : dict
        Dictionary containing x-axis data for each mode.
    hysts_y : dict
        Dictionary containing y-axis data for each mode.
    """

    hysts_x = {}
    hysts_y = {}

    for name_file in name_files:
        mode_cluster = ""
        for mode in modes:
            if mode in name_file:
                mode_cluster = mode
                break
        if mode_cluster:
            if mode_cluster != "coupled":
                path = os.path.join(dir_path_in, name_file)
                datas = np.loadtxt(path, skiprows=2).T
                hysts_x[mode_cluster], hysts_y[mode_cluster] = hyst_2d(datas)

    return hysts_x, hysts_y


def coupled_data(hysts_x, hysts_y, offsets=None):
    """
    Generate coupled data by subtracting 'off' from 'on' field measurements.

    Parameters
    ----------
    hysts_x : dict
        Dictionary containing 'on' and 'off' field measurements for x-axis.
    hysts_y : dict
        Dictionary containing 'on' and 'off' field measurements for y-axis.
    offsets: list of float
        List with fit determined vertical offset for off field measurements

    Returns
    -------
    hysts_x : dict
        Updated dictionary containing 'coupled' measurements for x-axis.
    hysts_y : dict
        Updated dictionary containing 'coupled' measurements for y-axis.
    """

    if "on" in hysts_x.keys() and "off" in hysts_x.keys():

        hysts_x["coupled"] = hysts_x["on"]
        hysts_y["coupled"] = [
            [on - off for on, off in zip(hyst_y_on, hyst_y_off)]
            for hyst_y_on, hyst_y_off in zip(hysts_y["on"], hysts_y["off"])]
        if offsets is not None:
            if len(offsets) == len(hysts_y["coupled"]):
                for i, hyst_y_coupled in enumerate(hysts_y["coupled"]):
                    hysts_y["coupled"][i] = [elem+offsets[i]
                                             for elem in hyst_y_coupled]
    else:
        print("For coupled analysis, both 'on' and 'off' field "
              "measurements should be available.")

    return hysts_x, hysts_y


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


def cluster_kmeans(hysteresis_data, num_clusters=3):
    """
    Perform K-Means clustering on hysteresis data.

    Parameters
    ----------
    hysteresis_data : numpy.ndarray
        Hysteresis data for clustering.
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
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(
        hysteresis_data)
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


def main_hysteresis_clustering(
        user_pars, dir_path_in, verbose=False, show_plots=True,
        save_plots=False, dir_path_out=None, dim_pix=None, dim_mic=None,
        dir_path_in_meas=None):
    """
    Perform hysteresis clustering analysis.

    Parameters
    ----------
    user_pars : dict
        User parameters.
    dir_path_in : str
        Path of best loops measurements txt directory (in).
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
    dir_path_in_meas : str, optional
        Directory path for input measurements.

    Returns
    -------
    cluster_labels : dict
        Cluster indices for each data point for each mode.
    cluster_info : dict
        Information about each cluster for each mode.
    inertia : dict
        Inertia (within-cluster sum of squares) for each mode.
    avg_hysteresis : dict
        List of average hysteresis for each cluster in each mode.
    """

    name_files = os.listdir(dir_path_in)
    modes = [elem.split()[-1] for elem in user_pars.keys() if
             'clusters' in elem]
    lab_tab = [['on', 'off', 'coupled'], ['y', 'w', 'r'],
               ['On Field', 'Off Field', 'Coupled']]
    cluster_labels, cluster_info, inertia, avg_hysteresis = {}, {}, {}, {}
    offsets = []
    make_plots = bool(show_plots or save_plots)

    # Extract hysteresis data
    hysts_x, hysts_y = extract_data(dir_path_in, name_files, modes)

    # Extract extra analysis info (scan dim + vertical offset (off field))
    if dir_path_in is not None:
        if dir_path_in_meas is None:
            root = os.path.split(dir_path_in)[0]
            dir_path_in_meas = os.path.join(root, "txt_ferro_meas")
        measurements, dim_pix, dim_mic = extract_measures(dir_path_in_meas)
        offsets = measurements['off']['fit pars: offset'] \
            if ELECTROSTATIC_OFFSET else None

    # If "coupled" mode is present, calculate coupled hysteresis
    if "coupled" in modes:
        hysts_x, hysts_y = coupled_data(hysts_x, hysts_y, offsets=offsets)

    # Perform clustering for each mode
    for mode in modes:
        try:
            # K-Means
            numb_cluster = user_pars[f'nb clusters {mode}']
            res = cluster_kmeans(hysts_y[mode], numb_cluster)
            cluster_labels[mode], cluster_info[mode], inertia[mode] = res

            # Calculate Average Hysteresis by Cluster
            avg_hysteresis[mode] = []
            for cluster_idx in range(numb_cluster):
                cluster_mask = np.array(cluster_labels[mode]) == cluster_idx
                avg_hysteresis[mode].append(
                    np.mean(np.array(hysts_y[mode])[cluster_mask], axis=0))

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
                cbar = plt.get_cmap(COLOR_HYSTERESIS_CLUSTERING)
                colors = [cbar((numb_cluster - i) / numb_cluster)
                          for i in range(numb_cluster)]
                cmap, cbar_lab = cbar_map(colors, numb_cluster)

                # Plot 1 : All Hysteresis by Cluster
                # Legend
                legend_handles = []
                for i in range(numb_cluster):
                    legend_handles.append(Patch(color=colors[i],
                                                label=labels[i]))

                figs = []

                # Create graph
                fig1, ax = plt.subplots(figsize=FIGSIZE)
                fig1.sfn = f"clustering_best_loops_{mode}"
                plot_dict_1 = {
                    'title': f'Clustering (K-Means): Best Loops ({mode})',
                    'x lab': 'Voltage', 'y lab': 'Piezoresponse',
                    'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
                plot_graph(ax, [], [], plot_dict=plot_dict_1)
                # Plot each hysteresis
                for i, (elem_x, elem_y) in enumerate(zip(
                        hysts_x[mode], hysts_y[mode])):
                    color = colors[cluster_labels[mode][i]]
                    plt.plot(elem_x, elem_y, color=color)
                ax.legend(handles=legend_handles)
                figs += [fig1]

                # Plot 2 : Average Hysteresis by Cluster
                # Create graph
                fig2, ax = plt.subplots(figsize=FIGSIZE)
                fig2.sfn = f"clustering_average_loops_{mode}"
                plot_dict_3 = {
                    'title': f'Average Hysteresis by Cluster ({mode})',
                    'x lab': 'Voltage', 'y lab': 'Piezoresponse',
                    'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
                plot_graph(ax, [], [], plot_dict=plot_dict_3)
                # Plot Average Hysteresis by Cluster
                for index in range(numb_cluster):
                    color = colors[index]
                    label = f'Cluster {cluster_info[mode][index][4]}'
                    plt.plot(hysts_x[mode][0], avg_hysteresis[mode][index],
                             label=label, color=color)
                ax.legend()
                figs += [fig2]
                if save_plots is True:
                    print_plots(figs, show_plots=False, save_plots=save_plots,
                                dirname=dir_path_out)

                # Plot 3 : cluster mapping
                measurements = {"Clustering (K-Means)": cluster_labels[mode]}
                colors_lab = {"Clustering (K-Means)": cmap}
                indx = lab_tab[0].index(mode)
                dict_map = {'label': lab_tab[2][indx], 'col': lab_tab[1][indx]}
                main_mapping(measurements, dim_pix, dim_mic=dim_mic,
                             colors=colors_lab, cbar_lab=cbar_lab,
                             dict_map=dict_map, mask=[], show_plots=show_plots,
                             save_plots=save_plots, dir_path_out=dir_path_out)
        except KeyError:
            print(f"KeyError management with except: no {mode} mode available "
                  f"for analysis")
            continue

    return cluster_labels, cluster_info, inertia, avg_hysteresis


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - nb_clusters_off: int
        Number of Clusters for Off-Field Hysteresis Loop.
        This parameter determines the number of clusters for the
        off-field hysteresis loop using a machine learning algorithm
        of clustering (K-Means).
        Used in the analysis of off-field hysteresis loop.
    - nb_clusters_on: int
        Number of Clusters for On-Field Hysteresis Loop.
        This parameter determines the number of clusters for the
        on-field hysteresis loop using a machine learning algorithm
        of clustering (K-Means).
        Used in the analysis of on-field hysteresis loop.
    - nb_clusters_coupled: int
        Number of Clusters for Differential Hysteresis Loop.
        This parameter determines the number of clusters for the
        differential hysteresis loop using a machine learning algorithm
        of clustering (K-Means).
        Used in the analysis of differential hysteresis loop.

    - dir_path_in: str
        Input Directory for Best Loop TXT Files (default: 'txt_best_loops').
        This parameter specifies the directory path for the best loop .txt
        files generated after the second step of the analysis.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - dir_path_in_meas: str
        Ferroelectric measurements files directory
        (optional, default: txt_ferro_meas).
        This parameter specifies the directory containing the ferroelectric
         measurements text files generated after the 2nd step of the analysis.
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
    # Select txt best loops folder (.txt)
    dir_path_in = tkf.askdirectory()
    # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt\txt_best_loops
    dir_path_out = None
    # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
    # hysteresis_clustering_2023-10-02-16h38m
    dir_path_in_meas = None
    # dir_path_in_meas = r'...\KNN500n_15h18m02-10-2023_out_dfrt\txt_ferro_meas
    verbose = True
    show_plots = True
    save = False

    user_pars = {'nb clusters off': 4,
                 'nb clusters on': 4,
                 'nb clusters coupled': 4}

    return user_pars, dir_path_in, dir_path_out, dir_path_in_meas, verbose, \
        show_plots, save


def main():
    """ Main function for data analysis. """
    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, dir_path_in_meas, verbose,
     show_plots, save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,  dirname="hysteresis_clustering",
        lvl=1, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    main_hysteresis_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=show_plots,
        save_plots=save, dir_path_out=dir_path_out,
        dir_path_in_meas=dir_path_in_meas)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()
