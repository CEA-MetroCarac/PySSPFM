"""
--> Executable Script
Automatic fill of measurement sheet
(measurement_file_name, date, sspfm electric signal parameters)
"""

import os
import shutil
import tkinter.filedialog as tkf
import datetime
import numpy as np
import openpyxl

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.datacube_reader import DataExtraction
from PySSPFM.utils.signal_bias import extract_sspfm_bias_pars
from PySSPFM.utils.datacube_to_nanoloop.file import get_file_names


def write_measurement_sheet(file_path_out, values, indexs):
    """
    Write measurement sheet.

    Parameters
    ----------
    file_path_out : str
        Output CSV file path
    values : list
        Values to write
    indexs : list
        Cell indices

    Returns
    -------
    None
    """
    data_frame = openpyxl.load_workbook(file_path_out)
    data_frame_sheet = data_frame['measurement sheet']
    for value, index in zip(values, indexs):
        data_frame_sheet[index] = value
    data_frame.save(file_path_out.replace(".xlsx", ".csv"))


def get_segments_sample_and_time(info_dict, nb_hold_seg_start=1,
                                 nb_hold_seg_end=1):
    """
    Get segments sample and time.

    Parameters
    ----------
    info_dict : dict
        Dictionary containing information about segments
    nb_hold_seg_start: int, optional
        Number of hold segments at the start (default is 1)
    nb_hold_seg_end: int, optional
        Number of hold segments at the end (default is 1)

    Returns
    -------
    hold_init_sample : int
        Initial sample of holding segment
    hold_init_time : float
        Initial time of holding segment
    hold_end_sample : int
        End sample of holding segment
    hold_end_time : float
        End time of holding segment
    write_sample : int
        Sample of writing segment
    write_time : float
        Time of writing segment
    read_sample : int
        Sample of reading segment
    read_time : float
        Time of reading segment
    """
    hold_init_sample = np.sum(info_dict['samps'][:nb_hold_seg_start])
    hold_end_sample = np.sum(info_dict['samps'][-nb_hold_seg_end:])
    hold_init_time = np.sum(info_dict['durs'][:nb_hold_seg_start])*1000
    hold_end_time = np.sum(info_dict['durs'][-nb_hold_seg_end:])*1000
    write_sample = info_dict['samps'][nb_hold_seg_start+1]
    write_time = info_dict['durs'][nb_hold_seg_start + 1]*1000
    read_sample = info_dict['samps'][nb_hold_seg_start+2]
    read_time = info_dict['durs'][nb_hold_seg_start + 2]*1000

    return hold_init_sample, hold_init_time, hold_end_sample, hold_end_time, \
        write_sample, write_time, read_sample, read_time


def main_meas_sheet_generator(file_path_in, dir_path_out, extension=".spm",
                              nb_hold_seg_start=1, nb_hold_seg_end=1,
                              verbose=False):
    """
    Main function used for measurement sheet generator

    Parameters
    ----------
    file_path_in : str
        Input path for the model of CSV file
    dir_path_out : str
        Output directory path for the location of the new CSV file
    extension : str, optional
        File extension (default is ".spm")
    nb_hold_seg_start: int, optional
        Number of hold segments at the start (default is 1)
    nb_hold_seg_end: int, optional
        Number of hold segments at the end (default is 1)
    verbose: bool, optional
        Activation key for verbosity.

    Returns
    -------
    indexs: list of str
        Indexes of the modified cells
    values: list
        Values of the modified cells
    """
    file_path_out = os.path.join(dir_path_out, os.path.split(file_path_in)[1])
    file_path_out = file_path_out.replace(".csv", ".xlsx")
    shutil.copyfile(file_path_in, file_path_out)
    # Get date and file path
    file_names_ordered = get_file_names(dir_path_out, file_format=extension)
    meas_file_path = os.path.join(dir_path_out, file_names_ordered[0])
    raw_date = os.path.getmtime(meas_file_path)
    raw_datetime = datetime.datetime.fromtimestamp(raw_date)
    date = raw_datetime.strftime("%Hh : %d/%m/%Y")
    # Extract data from measurement file: tip bias list of values
    data_extract = DataExtraction(meas_file_path)
    data_extract.data_extraction()
    info_dict = data_extract.info_dict
    # Generate dict of bias parameters
    tip_bias = list(info_dict['tip_bias'][nb_hold_seg_start:-nb_hold_seg_end])
    dict_elec = extract_sspfm_bias_pars(tip_bias)
    res = get_segments_sample_and_time(
        info_dict, nb_hold_seg_start=nb_hold_seg_start,
        nb_hold_seg_end=nb_hold_seg_end)
    (hold_init_sample, hold_init_time, hold_end_sample, hold_end_time,
     write_sample, write_time, read_sample, read_time) = res
    freq_start = int(info_dict['freq_start']/1000)
    freq_end = int((info_dict['freq_start'] + info_dict['freq_size'])/1000)
    # List of values and indexs of cells to modify
    indexs = ["B4", "C4", "D4",
              "B16", "C16", "D16", "E16", "F16", "G16", "H16", "I16",
              "J16", "K16", "L16", "M16", "N16", "O16", "P16", "Q16",
              "D22", "F22"]
    values = [file_names_ordered[0], file_names_ordered[-1], date,
              dict_elec['Write Voltage Range V'][0],
              dict_elec['Write Voltage Range V'][1],
              dict_elec['Write Number of Voltages'],
              dict_elec['Write Wave Form'],
              write_time, write_sample,
              dict_elec['Read Voltage Range V'][0],
              dict_elec['Read Voltage Range V'][1],
              dict_elec['Read Number of Voltages'],
              dict_elec['Read Wave Form'],
              read_time, read_sample,
              hold_init_time, hold_init_sample, hold_end_time, hold_end_sample,
              freq_start, freq_end]
    if verbose:
        for index, value in zip(indexs, values):
            print(f"cell {index}: {value}")
    # Write in measurement sheet
    write_measurement_sheet(file_path_out, values, indexs)
    os.remove(file_path_out.replace(".csv", ".xlsx"))

    return indexs, values


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - nb_hold_seg_start: int
        Number of hold segments at the start of measurement.
        This parameter is used to specify the number of hold segments at the
        beginning of the SSPFM signal.
    - nb_hold_seg_end: int
        Number of hold segments at the end of measurement.
        This parameter is used to specify the number of hold segments at the
        end of the SSPFM signal.

    file_path_in: str
        Path of datacube SSPFM (.spm) raw file measurements.
        This parameter specifies the path where datacube SSPFM (.spm) raw file
         measurements are located. It is used to indicate the path to the file
        containing these measurements.
    - extension: str
        Extension of raw SSPFM measurement files.
        This parameter determines the file extension type of raw SSPFM
        measurement files.
        Four possible values: 'spm', 'txt', 'csv', or 'xlsx'.
    - dir_path_out: str
        Directory for the generated CSV measurement sheet
        This parameter specifies the directory where the measurement files
        and the generated CSV measurement sheet resulting from the script will
        be saved.
    - verbose: bool
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.
    - show_plots: bool
        Activation key for generating matplotlib figures during analysis.
        This parameter serves as an activation key for generating
        matplotlib figures during the analysis process.
    """
    if get_setting("extract_parameters") in ['json', 'toml']:
        script_directory = os.path.realpath(__file__)
        file_path_user_params = script_directory.split('.')[0] + \
            f'_params.{get_setting("extract_parameters")}'
        # Load parameters from the specified configuration file
        print(f"user parameters from {os.path.split(file_path_user_params)[1]} "
              f"file")
        config_params = load_parameters_from_file(file_path_user_params)
        file_path_in = config_params['file_path_in']
        dir_path_out = config_params['dir_path_out']
        nb_hold_seg_start = config_params['nb_hold_seg_start']
        nb_hold_seg_end = config_params['nb_hold_seg_end']
        verbose = config_params['verbose']
        extension = config_params['extension']
    elif get_setting("extract_parameters") == 'python':
        # Get directory path
        file_path_in = tkf.askopenfilename()
        # file_path_in = r'...\KNN500n\measurement sheet model SSPFM DFRT.csv
        dir_path_out = None
        # dir_path_out = r'...\other_meas_dir
        nb_hold_seg_start = 1
        nb_hold_seg_end = 1
        verbose = True
        extension = 'spm'
        # extension = 'spm' or 'txt' or 'csv' or 'xlsx'
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return file_path_in, dir_path_out, nb_hold_seg_start, nb_hold_seg_end, \
        extension, verbose


def main():
    """ Main function for data analysis. """

    # Extract parameters
    out = parameters()
    (file_path_in, dir_path_out, nb_hold_seg_start, nb_hold_seg_end, extension,
     verbose) = out
    # Main function
    main_meas_sheet_generator(
        file_path_in, dir_path_out, extension=extension,
        nb_hold_seg_start=nb_hold_seg_start, nb_hold_seg_end=nb_hold_seg_end,
        verbose=verbose)


if __name__ == '__main__':
    main()
