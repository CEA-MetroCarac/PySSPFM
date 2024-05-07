"""
--> Executable Script
Module used to perform a clustering (K-Means or Gaussian Mixture Model) for all
best loop (with a chosen measure, for example piezoresponse), for each pixel
(one loop for each mode) of a sspfm measurement.
Loops can be a composition of several measure, which will be normalized
between 0 and 1 and concatenated (for example amplitude and phase)
    - Generate a sspfm maps for each mode resulting of clustering analysis
    - Generate a graph of all loop with their cluster for each mode
    resulting of clustering analysis
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.clustering import curve_clustering, cbar_map
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.nanoloop_to_hyst.file import extract_properties
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def gen_loop_data(data):
    """
    Extract 2D loops data from a 3-row data array.

    Parameters
    ----------
    data : numpy.ndarray
        2+nb_y_meas-row data array where the first row contains indices,
        the second row contains voltage values, and the other
        row contains y_axis values.

    Returns
    -------
    loops_x : list of list
        Polarization voltage data for each loop.
    loops_y : list of list
        y_axis data for each loop.
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
    loops_x = np.concatenate(data_x, axis=1)
    loops_y = np.concatenate(data_y, axis=1)

    return loops_x, loops_y


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
        List of measurement name for the loop

    Returns
    -------
    loops_x : dict
        Dictionary containing x-axis data for each mode.
    loops_y : dict
        Dictionary containing y-axis data for each mode.
    """

    loops_x, loops_y = {}, {}

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
                loops_x[mode_cluster], loops_y[mode_cluster] = \
                    gen_loop_data([index, data_x, data_y])

    return loops_x, loops_y


def gen_coupled_data(loops_x, loops_y, offsets=None):
    """
    Generate coupled data by subtracting 'off' from 'on' field measurements:
    only for piezoresponse loop

    Parameters
    ----------
    loops_x : dict
        Dictionary containing 'on' and 'off' field measurements for x-axis.
    loops_y : dict
        Dictionary containing 'on' and 'off' field measurements for y-axis.
    offsets: list of float, optional
        List with fit determined vertical offset for off field measurements
        (default: None)

    Returns
    -------
    loops_x : dict
        Updated dictionary containing 'coupled' measurements for x-axis.
    loops_y : dict
        Updated dictionary containing 'coupled' measurements for y-axis.
    """

    if "on" in loops_x.keys() and "off" in loops_x.keys():

        loops_x["coupled"] = loops_x["on"]
        loops_y["coupled"] = [
            [on - off for on, off in zip(loop_y_on, loop_y_off)]
            for loop_y_on, loop_y_off in zip(loops_y["on"], loops_y["off"])]
        if offsets is not None:
            if len(offsets) == len(loops_y["coupled"]):
                for i, loop_y_coupled in enumerate(loops_y["coupled"]):
                    loops_y["coupled"][i] = [elem+offsets[i]
                                             for elem in loop_y_coupled]
    else:
        print("For coupled analysis, both 'on' and 'off' field "
              "measurements should be available.")

    return loops_x, loops_y


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
    name_files = os.listdir(dir_path_in)
    method = user_pars["method"]
    assert method in ["kmeans", "gmm"], \
        "Invalid clustering method. Method must be either 'kmeans' or 'gmm'."

    modes = [key.split()[-1] for key, value in user_pars.items() if
             'clusters' in key and value is not None]
    if user_pars['label meas'] != ['piezoresponse']:
        modes = [lab for lab in modes if lab != 'coupled']
    lab_tab = [['on', 'off', 'coupled'], ['y', 'w', 'r'],
               ['On Field', 'Off Field', 'Coupled']]
    cluster_labels, cluster_info, inertia, centers, avg_loop = \
        {}, {}, {}, {}, {}
    offsets = []
    make_plots = bool(show_plots or save_plots)

    # Extract loop data
    loops_x, loops_y = extract_data(dir_path_in, name_files, modes,
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

    # If "coupled" mode is present, calculate coupled loop
    # (only for piezoresponse)
    if "coupled" in modes:
        loops_x, loops_y = gen_coupled_data(loops_x, loops_y,
                                            offsets=offsets)

    # Perform clustering for each mode
    for mode in modes:
        try:
            numb_cluster = user_pars[f'nb clusters {mode}']
            if isinstance(loops_y[mode], list):
                loops_y[mode] = np.array(loops_y[mode])

            # Clustering
            cluster_labels[mode], cluster_info[mode], inertia[mode], \
                centers[mode] = curve_clustering(
                loops_y[mode], num_clusters=numb_cluster, method=method,
                verbose=verbose)

            # Calculate Average loop by Cluster
            avg_loop[mode] = []
            for cluster_idx in range(numb_cluster):
                cluster_mask = np.array(cluster_labels[mode]) == cluster_idx
                avg_loop[mode].append(
                    np.mean(np.array(loops_y[mode])[cluster_mask], axis=0))

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
                print(f'{mode} :')
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

                # Plot 1 : All Loop by Cluster
                # Legend
                legend_handles = []
                for i in range(numb_cluster):
                    legend_handles.append(
                        Patch(color=colors[i], label=labels[i]))

                figs = []

                # Create graph
                figsize = get_setting("figsize")
                fig1, ax = plt.subplots(figsize=figsize)
                fig1.sfn = f"clusters_centroids_{mode}"
                plot_dict_1 = {
                    'title': f'Clusters with Centroids ({mode})',
                    'x lab': 'Feature 1', 'y lab': 'Feature 2',
                    'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
                plot_graph(ax, [], [], plot_dict=plot_dict_1)

                # Plot data points
                for index in range(numb_cluster):
                    tab_lab = np.array(cluster_labels[mode])
                    cluster_data = loops_y[mode][tab_lab == index]
                    cluster_data = np.array(cluster_data)

                    # Plot data points for the current cluster
                    plt.scatter(cluster_data[:, 0], cluster_data[:, 1],
                                c=[colors[index]],
                                label=f'Cluster {cluster_info[mode][index][4]}')
                # Plot centroids
                plt.scatter(centers[mode][:, 0], centers[mode][:, 1],
                            marker='x', color='black', label='Centroids')
                ax.legend()
                figs += [fig1]

                # Create graph
                figsize = get_setting("figsize")
                fig2, ax = plt.subplots(figsize=figsize)
                fig2.sfn = f"clustering_best_loops_{mode}"
                plot_dict_1 = {
                    'title': f'Clustering ({method_str}): Best Loops ({mode})',
                    'x lab': 'Voltage', 'y lab': 'Y Axis',
                    'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
                plot_graph(ax, [], [], plot_dict=plot_dict_1)
                # Plot each loop
                for i, (elem_x, elem_y) in enumerate(zip(
                        loops_x[mode], loops_y[mode])):
                    color = colors[cluster_labels[mode][i]]
                    plt.plot(elem_x, elem_y, color=color)
                ax.legend(handles=legend_handles)
                figs += [fig2]

                # Plot 2 : Average Loop by Cluster
                # Create graph
                fig3, ax = plt.subplots(figsize=figsize)
                fig3.sfn = f"clustering_average_loops_{mode}"
                plot_dict_3 = {
                    'title': f'Average Loop by Cluster ({mode})',
                    'x lab': 'Voltage', 'y lab': 'Y Axis',
                    'fs': 15, 'edgew': 3, 'tickl': 5, 'gridw': 1}
                plot_graph(ax, [], [], plot_dict=plot_dict_3)
                # Plot Average Loop by Cluster
                for index in range(numb_cluster):
                    color = colors[index]
                    label = f'Cluster {cluster_info[mode][index][4]}'
                    plt.plot(loops_x[mode][0], avg_loop[mode][index],
                             label=label, color=color)
                ax.legend()
                figs += [fig3]

                if save_plots is True:
                    print_plots(figs, show_plots=False, save_plots=save_plots,
                                dirname=dir_path_out)

                # Plot 3 : cluster mapping
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


def parameters():
    """
    To complete by user of the script: return parameters for analysis
    - method: str
        Name of the method used to perform the clustering
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
        # loop_clustering_2023-10-02-16h38m
        dir_path_in_props = None
        # dir_path_in_props = r'...\KNN500n_15h18m02-10-2023_out_dfrt\properties
        verbose = True
        show_plots = True
        save = False

        user_pars = {'method': 'kmeans',
                     'label meas': ['piezoresponse'],
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
        dir_path_in, dir_path_out, save=save,  dirname="loop_clustering",
        lvl=1, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    main_loop_clustering(
        user_pars, dir_path_in, verbose=verbose, show_plots=show_plots,
        save_plots=save, dir_path_out=dir_path_out,
        dir_path_in_props=dir_path_in_props)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()
