"""
File and directory path management for clustering script
"""

import os
import numpy as np

from PySSPFM.utils.core.path_management import \
    get_filenames_with_conditions, sort_filenames
from PySSPFM.utils.raw_extraction import \
    csv_meas_sheet_extract, raw_data_extraction_without_script


def curve_extraction(dir_path_in, tab_label, mode="classic", extension="spm"):
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
    curves_x : list
        List containing x-axis data for each mode.
    curves_y : list
        List containing y-axis data for each mode.
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
        dict_meas = raw_data_extraction_without_script(
            file_path_in, extension=extension,
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


def extract_map_dim_from_csv(csv_path, dir_path_in=None, verbose=False):
    """
    Extract map dimensions from CSV.

    Parameters
    ----------
    csv_path : str or None
        Path to the CSV file or directory path.
    dir_path_in : str, optional
        Directory path (default is None).
    verbose : bool, optional
        Whether to display verbose information (default is False).

    Returns
    -------
    dim_pix : dict
        Dictionary containing pixel dimensions.
    dim_mic : dict
        Dictionary containing micron dimensions.
    """
    # Extract extra analysis info (scan dim)
    if csv_path is None:
        csv_path = dir_path_in
    else:
        csv_path, _ = os.path.split(csv_path)
    csv_meas, _ = csv_meas_sheet_extract(csv_path, verbose=verbose)
    dim_pix = \
        {'x': csv_meas['Grid x [pix]'], 'y': csv_meas['Grid y [pix]']}
    dim_mic = \
        {'x': csv_meas['Grid x [um]'], 'y': csv_meas['Grid y [um]']}

    return dim_pix, dim_mic


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

    loops_x, loops_y = [], []

    # Segmentation
    index_changes = np.where(data[0][:-1] != data[0][1:])[0] + 1
    for cont, teab_meas in enumerate(data[2]):
        loops_x.append([])
        loops_y.append([])
        loops_x[cont] = np.split(data[1], index_changes)
        loops_y[cont] = np.split(teab_meas, index_changes)

    return loops_x, loops_y


def extract_loop_data(dir_path_in, modes, tab_label):
    """
    Extract data from files based on modes and cluster counts.

    Parameters
    ----------
    dir_path_in : str
        Directory path where the data files are located.
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

    name_files = os.listdir(dir_path_in)

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
