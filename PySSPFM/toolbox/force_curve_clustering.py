"""
--> Executable Script
Module used to perform clustering (K-Means or Gaussian Mixture Model) on force
curves extracted from a datacube file (SS PFM) for points on the sample surface.
The force curves are processed (offset correction) and their properties
(adhesion, etc.) are extracted.
    - Generate a clustering analysis for local force curves to identify distinct
    mechanical properties across the sample.
    - Generate a sspfm maps for each mode resulting of clustering analysis
    - Generate a graph of all curve with their cluster for each mode
    resulting of clustering analysis
    - Produce visualizations of force curves with their respective clusters,
    highlighting variations in adhesion and other relevant metrics.
"""

import tkinter.filedialog as tkf
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from PySSPFM.settings import get_setting, get_config
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.core.path_management import sort_filenames
from PySSPFM.utils.raw_extraction import \
    raw_data_extraction_without_script, csv_meas_sheet_extract
from PySSPFM.utils.path_for_runable import save_path_management, \
    create_json_res, copy_json_res
from PySSPFM.utils.datacube_to_nanoloop.analysis import \
    extract_other_properties
from PySSPFM.toolbox.curve_clustering import perform_curve_clustering
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.core.clustering import cbar_map


def save_avg_curve(x_avg, y_avg, dir_path_out):
    """
    Save average loop data to text files, with each file representing
    a key in avg_loop and its corresponding values.

    Parameters
    ----------
    x_avg : list
    y_avg : list
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

    file_path_out = os.path.join(dir_path_out, f'avg_curve.txt')

    # Generate cluster indices and concatenate x and y values
    cluster_index = [cont for cont, loop in enumerate(y_avg) for _ in loop]
    data = np.column_stack((cluster_index, np.concatenate(x_avg),
                            np.concatenate(y_avg)))

    # Save the data with header
    header = "cluster_index\t\tx values\t\ty values"
    np.savetxt(file_path_out, data, delimiter='\t\t', header=header,
               fmt='%s')


def save_labels(cluster_labels, dim_pix, dim_mic, toolbox_path):
    """
    Save clustering labels to a text file, with optional dimensional metadata.

    Parameters
    ----------
    cluster_labels : list
        List of cluster labels.
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
                                 'properties_force_clustering.txt')
    header = f'force_clustering\n{header_lab_add}\n'
    header += 'force_cruve\t\t'

    np.savetxt(file_path_out, np.array(cluster_labels).T, delimiter='\t\t',
               newline='\n', header=header, fmt='%s')


def save_other_properties(tab_other_properties, file_path, map_dim=None):
    """
    Save other properties to a file.

    Parameters
    ----------
    tab_other_properties : list of dict
        List of dictionaries containing the properties to be saved.
    file_path : str
        Path to the file where the properties will be saved.
    map_dim : dict, optional
        Dictionary containing map dimensions with 'x pix', 'y pix',
        'x mic', and 'y mic' as keys (default is None).

    Returns
    -------
    None
    """
    other_properties = {key: [d[key] for d in tab_other_properties] for key in
                        tab_other_properties[0]}
    delimiter = get_setting("delimiter")
    header = "other\n"
    if map_dim is not None:
        header += f"x pix={map_dim['x pix']}, y pix={map_dim['y pix']}, " \
                  f"x mic={map_dim['x mic']}, y mic={map_dim['y mic']}, \n"
    for key in other_properties.keys():
        header += f"{key}{delimiter}"
    data_array = np.array(list(other_properties.values()), dtype=float).T
    np.savetxt(file_path, data_array, header=header, delimiter=delimiter,
               newline='\n', fmt='%s')


def plot_other_properties(tab_other_properties):
    """
    Plots the extracted properties from the SPM data.

    Parameters
    ----------
    tab_other_properties : list of dicts
        List of dictionaries containing the extracted properties for each SPM
        file.

    Returns
    ----------
    fig: matplotlib.figure.Figure
        The matplotlib figure object containing the plots for the extracted
        properties.
    """
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle('Extracted Properties from SPM Data')
    fig.sfn = "graph_other_properties"

    # Flatten the axs array for easier iteration
    axs = axs.ravel()

    # Properties to plot
    properties = ['height', 'deflection', 'deflection error',
                  'adhesion approach', 'adhesion retract']
    labels = ['Mean Height (nm)', 'Mean Deflection (nm)',
              'Deflection Error (nm)',
              'Adhesion approach (nm)', 'Adhesion retract (nm)']

    for i, prop in enumerate(properties):
        values = [d[prop] for d in tab_other_properties]
        axs[i].plot(values, '-', label=f'{labels[i]}')
        axs[i].set_title(labels[i])
        axs[i].grid(True)
        axs[i].legend()

    # Remove the last subplot if there are only 5 properties
    fig.delaxes(axs[5])

    # Adjust layout to make space for the title
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    return [fig]


def extract_stiffness_from_csv(dir_path_in_csv):
    """
    Extract the spring constant from a CSV file within the specified directory.

    Parameters
    ----------
    dir_path_in_csv : str
        Directory path containing the CSV file.

    Returns
    -------
    spring_constant : float or None
        Extracted spring constant value from the CSV file.
        Returns None if not found.
    """
    assert os.path.isdir(dir_path_in_csv), "Invalid directory path"

    spring_constant = None
    file_path_in_csv = ''
    meas_pars_sheet = 'measurement sheet'
    meas_sheet_name = get_setting("default_parameters_file_name")
    if meas_sheet_name in dir_path_in_csv:
        file_path_in_csv = dir_path_in_csv
    else:
        for elem in os.listdir(dir_path_in_csv):
            if meas_sheet_name in elem.replace("~$", ""):
                file_path_in_csv = os.path.join(dir_path_in_csv,
                                                elem.replace("~$", ""))

    excel_meas = pd.read_excel(file_path_in_csv, sheet_name=meas_pars_sheet)

    for idx, _ in excel_meas.iterrows():
        for col in excel_meas.columns:
            if str(excel_meas.at[idx, col]) == "Spring constant k [N/m]":
                # La valeur est à la ligne suivante, même colonne
                spring_constant = float(excel_meas.at[idx + 1, col])
                break

    return spring_constant


def single_script(file_path_in, mode='classic', tip_stiffness=3,
                  hold_samples=(100, 100), verbose=False):
    """
    Data analysis of a measurement file (i.e., a pixel), print the graphs +
    info and save the nanoloop data in a txt file.

    Parameters
    ----------
    file_path_in: str
        Path of the measurement/csv file (in).
    mode: str, optional
        Measurement mode ('classic' or 'dfrt')
    tip_stiffness: float, optional, default 3.0
        The stiffness of the tip used in the measurement in N/m.
    hold_samples: tuple, optional 100
        Number of hold sample for approach and retract.
    verbose: bool, optional
        Activation key for verbosity.

    Returns
    ----------
    height: np.ndarray
        The extracted height data from the SPM file.
    force: np.ndarray
        The calculated force (deflection multiplied by tip stiffness) data.
    other_properties: dict
        Dictionary containing extracted properties.
    """
    assert mode in ['classic', 'dfrt']

    # Print the file name
    _, file_name_in = os.path.split(file_path_in)
    if verbose:
        print(f'- measurement file: {file_name_in}\n')
    _, file_extension = os.path.splitext(file_path_in)
    dict_meas = raw_data_extraction_without_script(
        file_path_in, extension=file_extension[1:],
        mode_dfrt=bool(mode.lower() == 'dfrt'))

    raw_height = dict_meas['height']
    raw_deflection = dict_meas['deflection']

    # Calculate additional properties
    percent_baseline = 30
    other_properties, height, deflection = extract_other_properties(
        {"height": raw_height, "deflection": raw_deflection},
        start_ind=hold_samples[0], end_ind=hold_samples[1],
        percent_baseline=percent_baseline)
    force = deflection * tip_stiffness

    return height, force, other_properties


def main_force_curve_analysis(
        dir_path_in, cluster_pars, extension="spm", mode='classic',
        tip_stiffness=None, dim_pix=None, dim_mic=None, hold_samples=None,
        verbose=False, show_plots=True, save=False,
        dir_path_out=None, csv_file_path=None):
    """
    Main function that orchestrates the script and calls other functions.

    Parameters
    ----------
    dir_path_in: str
        Path to the Spm or txt datacube sspfm directory (in)
    cluster_pars: dict
        User parameters for curve clustering analysis.
    extension: str
        Extension of raw SSPFM measurement files.
    mode: str, optional
        Measurement mode ('classic' or 'dfrt')
    tip_stiffness: float, optional, default 3.0
        The stiffness of the tip used in the measurement in N/m.
    dim_pix : dict, optional
        Dictionary of pixel dimensions.
    dim_mic : dict, optional
        Dictionary of micron dimensions.
    hold_samples: tuple of int, optional (100, 100)
        Number of hold sample for approach and retract.
    verbose: bool, optional
        Activation key for verbosity
    show_plots: bool, optional
        Activation key for figure visualization
    save : bool, optional
        If True, save generated plots and results.
    dir_path_out : str, optional
        Output directory for saving plots and results.
    csv_file_path: str, optional
        File path of the CSV measurement file (measurement sheet model).

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
    map_dim : dict
        Dictionary of pixel and micron dimensions.
    """

    make_plots = bool(show_plots or save)

    # Extract extra analysis info (scan dim + tip stiffness + hold samples)
    if dir_path_in is not None:
        if csv_file_path is None:
            csv_dir_path = dir_path_in
        else:
            csv_dir_path = os.path.split(csv_file_path)[0]
        meas_pars, sign_pars = \
            csv_meas_sheet_extract(csv_dir_path, verbose=verbose)

        if dim_pix is None:
            dim_pix = {"x": meas_pars['Grid x [pix]'],
                       "y": meas_pars['Grid y [pix]']}
        if dim_mic is None:
            dim_mic = {"x": meas_pars['Grid x [um]'],
                       "y": meas_pars['Grid y [um]']}
        if hold_samples is None:
            hold_samples = (sign_pars['Hold sample (start)'],
                            sign_pars['Hold sample (end)'])
        if tip_stiffness is None:
            tip_stiffness = extract_stiffness_from_csv(csv_dir_path)

    map_dim = {'x pix': dim_pix['x'],
               'y pix': dim_pix['y'],
               'x mic': dim_mic['x'],
               'y mic': dim_mic['y']}

    height_tab = []
    force_tab = []
    tab_other_properties = []
    filenames = [filename for filename in os.listdir(dir_path_in) if
                 filename.endswith(extension)]
    sorted_filenames, _, _ = sort_filenames(filenames)

    # Multi processing mode
    multiproc = get_setting("multi_processing")
    if multiproc:
        from PySSPFM.utils.core.multi_proc import run_multi_proc_forcecurve
        file_paths = []
        for filename in sorted_filenames:
            file_paths.append(os.path.join(dir_path_in, filename))
        common_args = {
            "mode": mode,
            "tip_stiffness": tip_stiffness,
            "hold_samples": hold_samples,
            "verbose": verbose
        }
        res = run_multi_proc_forcecurve(file_paths, common_args, processes=16)
        (height_tab, force_tab, tab_other_properties) = res
    else:
        for filename in sorted_filenames:
            file_path = os.path.join(dir_path_in, filename)
            if verbose:
                print(f"- Extract : {filename}")
            height, force, other_properties = single_script(
                file_path, mode=mode, tip_stiffness=tip_stiffness,
                hold_samples=hold_samples, verbose=verbose)

            height_tab.append(height)
            force_tab.append(force)
            tab_other_properties.append(other_properties)

    figs = []
    if make_plots:
        figs += plot_other_properties(tab_other_properties)

    numb_cluster = cluster_pars["nb clusters"]
    method = cluster_pars["method"]
    res = perform_curve_clustering(
        [height_tab, height_tab], [height_tab, force_tab],
        numb_cluster=numb_cluster,
        method=method, relative_mode=False, make_plots=True, plot_axis_y=1)
    (cluster_labels, cluster_info, inertia, x_avg, y_avg, figures) = res
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
            {f"Clustering ({method_str})": cluster_labels}
        colors_lab = {f"Clustering ({method_str})": cmap}
        main_mapping(properties, dim_pix, dim_mic=dim_mic,
                     colors=colors_lab, cbar_lab=cbar_lab,
                     mask=[], show_plots=show_plots,
                     save_plots=save, dir_path_out=dir_path_out)

    # save_results
    if save:
        save_labels(cluster_labels, dim_pix, dim_mic, dir_path_out)
        save_avg_curve(x_avg, y_avg, dir_path_out)

    return (cluster_labels, cluster_info, inertia, x_avg, y_avg,
            tab_other_properties, map_dim)


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)

    - nb_clusters: int
        Number of Clusters for Curve.
        This parameter determines the number of clusters for the
        curve using a machine learning algorithm of clustering.
    - method: str
        Name of the Method Used to Perform the Clustering
        This parameter determines the method used to perform the clustering.
        Implemented methods are K-Means or Gaussian Mixture Model.
        (GMM).
        Choose from : "kmeans", "gmm"

    - mode: str
        Treatment used for segment data analysis
        (extraction of PFM measurements).
        This parameter determines the treatment method used for segment data
        analysis, specifically for the extraction of PFM measurements.
        Two possible values: 'classic' (sweep or single frequency) or 'dfrt'.
    - extension: str, optional
        Extension of files.
        This parameter determines the extension of datacube SSPFM raw file
        measurements.
        Four possible values: 'spm' or 'txt' or 'csv' or 'xlsx'.

    - dir_path_in: str
        Directory containing datacube SSPFM raw file measurements.
        This parameter specifies the directory where the datacube SSPFM raw file
        measurements are stored. It is used to indicate the path to the folder
        containing the files for processing and analysis.
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
        config_params, fname_json = get_config(__file__, fname_json)
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Get file path for single script
        dir_path_in = tkf.askopenfilename()
        # dir_path_in = r'...\KNN500n
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # force_curve_clustering_2023-10-02-16h38m
        csv_file_path = None
        # csv_file_path =
        # r'...\KNN500n\measurement sheet model SSPFM.csv'
        config_params = {
            "dir_path_in": dir_path_in,
            "dir_path_out": dir_path_out,
            "csv_file_path": csv_file_path,
            "verbose": True,
            "show_plots": True,
            "save": False,
            "extension": "spm",
            "mode": "classic",
            "cluster_pars": {
                "nb clusters": 4,
                "method": "kmeans"
            }
        }
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return config_params['extension'], config_params['mode'], \
        config_params['cluster_pars'], config_params['dir_path_in'], \
        config_params['dir_path_out'], config_params['csv_file_path'], \
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
    res = parameters(fname_json=fname_json)
    (extension, mode, cluster_pars, dir_path_in, dir_path_out,
     csv_file_path, verbose, show_plots, save, fname_json,
     config_params) = res
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,  dirname="force_curve_analysis",
        lvl=1, create_path=True, post_analysis=True)
    # Main function
    _, _, _, _, _, tab_other_properties, map_dim = \
        main_force_curve_analysis(
            dir_path_in, cluster_pars=cluster_pars, extension=extension,
            mode=mode,  dim_pix=None, dim_mic=None,
            verbose=verbose, show_plots=show_plots, save=save,
            dir_path_out=dir_path_out, csv_file_path=csv_file_path)

    # Save parameters
    if save:
        if get_setting("extract_parameters") in ['json', 'toml']:
            copy_json_res(fname_json, dir_path_out, verbose=verbose)
        else:
            create_json_res(config_params, dir_path_out,
                            fname="force_curve_clustering_params.json",
                            verbose=verbose)
        file_path_out = os.path.join(dir_path_out, "other_properties.txt")
        save_other_properties(tab_other_properties, file_path=file_path_out,
                              map_dim=map_dim)


if __name__ == '__main__':
    main()
