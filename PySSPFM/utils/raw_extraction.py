"""
Module used for extraction of .spm or .txt datacube file (SS PFM) data and
csv measurement sheet
Inspired by SS_PFM script, Nanoscope, Bruker
"""

import os
import pandas as pd
import numpy as np

from PySSPFM.settings import get_setting


class NanoscopeError(Exception):
    """ NanoscopeError object """
    def __init__(self, message=""):
        """
        Object used to generate error when spm files can't be opened with
        nanoscope module (NanoScope Analysis DLL is required)

        Parameters
        ----------
        message: str, optional
            Custom error message (default is an empty string).
        """
        self.message = message
        super().__init__(self.message)


def data_identification(raw_dict, type_file, mode_dfrt=False):
    """
    Extract and identify all the measurements contained in a table file
    (txt, csv, xlsx)

    Parameters
    ----------
    raw_dict: dict
        Dict with all measurements of the measurement file
    type_file: str
        Type of the raw measurement file (spm or table)
    mode_dfrt: bool, optional
        If mode_dfrt is True, a dfrt measure is performed and vice versa

    Returns
    -------
    dict_meas: dict
        Dict of all measurements in the extracted file
    """
    dict_meas = {}
    strg = 'dfrt' if mode_dfrt else 'classic'
    key_measurement_extraction = get_setting("key meas extract")
    dict_identify_mea = key_measurement_extraction[type_file][strg]

    for key, value in dict_identify_mea.items():
        try:
            dict_meas[value] = raw_dict[key]
        except KeyError:
            print(f'KeyError on {key}.\n'
                  f'The available keys are: {raw_dict.keys()}')
    if 'deflection' not in dict_meas:
        dict_meas['deflection'] = []
    if 'tip_bias' not in dict_meas:
        dict_meas['times_bias'], dict_meas['tip_bias'] = [], []

    return dict_meas


def extr_bias_pars(file_path_in_bias):
    """
    Identify and extract SS PFM bias data of txt saving file

    Parameters
    ----------
    file_path_in_bias: str
        Path of txt saving file with all SS PFM signal parameters (in)

    Returns
    -------
    script_dict: dict
        Dict of all SS PFM signal parameters
    """
    script_dict = {}
    with open(file_path_in_bias, encoding='utf-8') as sspfm_bias_file:
        for line in sspfm_bias_file:
            strip_line = line.strip()
            split_line = strip_line.split(': ')
            try:
                script_dict[split_line[0]] = eval(split_line[-1])
            except (NameError, SyntaxError):
                script_dict[split_line[0]] = split_line[-1]

    return script_dict


def extr_data_spm(file_path_in, mode_dfrt=False, verbose=False):
    """
    Data extraction from spm file and identification

    Parameters
    ----------
    file_path_in: str
        Path of the spm measurement file (in)
    mode_dfrt: bool, optional
        If mode_dfrt is True, a dfrt measure is performed and vice versa
    verbose: bool, optional
        If True, print name of signal in extracted measurement file

    Returns
    ----------
    dict_meas: dict
        All measurement in extracted file
    script_dict: dict
        All parameters for sspfm voltage signal and other measurement
        parameters
    """

    try:
        from PySSPFM.utils.datacube_reader import \
            DataExtraction, script_info # noqa
    except (NotImplementedError, NameError) as error:
        message = "To open DATACUBE spm file (Bruker), nanoscope module is " \
                  "required and NanoScope Analysis software (Bruker) should " \
                  "be installed on the computer"
        raise NanoscopeError(message) from error

    # DataExtraction object is used to extract info from .spm file
    data_extract = DataExtraction(file_path_in)

    # .spm file basic info
    data_extract.data_extraction()
    info_dict = data_extract.info_dict

    # Extraction of SS PFM bias info organized in terms of ramp script
    # parameters
    script_dict = script_info(info_dict)

    # .spm file info: raw data
    data_extract.data_extraction(raw_data=True)
    raw_dict = data_extract.raw_dict

    if verbose:
        print(f'Measurement in spm file: {list(raw_dict.keys())}\n')

    # Data identification
    dict_meas = data_identification(
        raw_dict, type_file='spm', mode_dfrt=mode_dfrt)

    return dict_meas, script_dict


def extr_data_table(file_path_in, mode_dfrt=False):
    """
    Extract and identify data from a raw measurement table file
    (txt, csv, xlsx).
    Lines header and delimiter should be adjusted according to the input raw
    measurement file

    Parameters
    ----------
    file_path_in: str
        Path of the measurement file (input)
    mode_dfrt: bool, optional
        If True, perform a dfrt measurement; otherwise, perform the default
        measurement.

    Returns
    -------
    dict_meas: dict
        All measurement in extracted file
    script_dict: dict
        All parameters for sspfm voltage signal and other measurement
        parameters
    """
    # Extraction of SS PFM bias info organized in terms of ramp script
    # parameters
    root_in, _ = os.path.split(file_path_in)
    script_dict = script_dict_from_meas_sheet(root_in)

    file_type = os.path.splitext(file_path_in)[1][1:]
    header_lines = get_setting('header lines')

    # Extract and identify measurements from the file
    if file_type == 'txt':
        delimiter = get_setting('delimiter')
        index_line_meas_name = get_setting('index line meas name')
        raw_data = np.genfromtxt(
            file_path_in, delimiter=delimiter, skip_header=header_lines).T
        # Extraire le header
        with open(file_path_in, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            meas_names = \
                lines[index_line_meas_name].strip("# \n").split(delimiter)
    elif file_type == 'csv':
        data_frame = pd.read_csv(file_path_in)[header_lines-1:]
        raw_data = np.array(data_frame[1:]).T
        meas_names = data_frame.columns.tolist()
    elif file_type == 'xlsx':
        data_frame = pd.read_excel(file_path_in)[header_lines-1:]
        raw_data = np.array(data_frame[1:]).T
        meas_names = data_frame.columns.tolist()
    else:
        raise IOError("file_type should be 'txt', 'csv', or 'xlsx'")
    raw_dict = dict(zip(meas_names, raw_data))
    dict_meas = data_identification(
        raw_dict, type_file='table', mode_dfrt=mode_dfrt)

    return dict_meas, script_dict


def data_extraction(file_path_in, mode_dfrt=False, verbose=False):
    """
    Data extraction from measurement file and identification

    Parameters
    ----------
    file_path_in: str
        Path of the measurement file (in)
    mode_dfrt: bool, optional
        If mode_dfrt is True, a dfrt measure is performed and vice versa
    verbose: bool, optional
        If True, print name of signal in extracted measurement file

    Returns
    ----------
    dict_meas: dict
       All measurement in extracted file
    script_dict: dict
        All parameters for sspfm voltage signal and other measurement
        parameters
    """
    assert os.path.isfile(file_path_in)

    if file_path_in.endswith('.spm'):
        dict_meas, script_dict = extr_data_spm(
            file_path_in, mode_dfrt=mode_dfrt, verbose=verbose)
    else:
        dict_meas, script_dict = extr_data_table(
            file_path_in, mode_dfrt=mode_dfrt)

    return dict_meas, script_dict


def script_dict_from_meas_sheet(dir_path_in_csv, verbose=False):
    """
    Extract script parameters from a CSV measurement sheet

    Parameters
    ----------
    dir_path_in_csv: str
        Directory path containing the CSV measurement sheet (in)
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    script_dict: dict
        A dictionary containing script parameters
    """
    _, csv_sspfm_bias = csv_meas_sheet_extract(dir_path_in_csv, verbose=False)

    script_dict = {
        'Write Voltage Range (V)': (
            csv_sspfm_bias.get('Min volt (W) [V]'),
            csv_sspfm_bias.get('Max volt (W) [V]')
        ),
        'Write Number of Voltages': csv_sspfm_bias.get('Nb volt (W)'),
        'Write Wave Form': csv_sspfm_bias.get('Mode (W)'),
        'Measurements Per Write': csv_sspfm_bias.get('Nb meas (W)'),
        'Write Segment Duration (ms)': csv_sspfm_bias.get('Seg durat (W) [ms]'),
        'Write Samples Per Segment': csv_sspfm_bias.get('Seg sample (W)'),
        'Read Voltage Range (V)': (
            csv_sspfm_bias.get('Min volt (R) [V]'),
            csv_sspfm_bias.get('Max volt (R) [V]')
        ),
        'Read Number of Voltages': csv_sspfm_bias.get('Nb volt (R)'),
        'Read Wave Form': csv_sspfm_bias.get('Mode (R)'),
        'Measurements Per Read': csv_sspfm_bias.get('Nb meas (R)'),
        'Read Segment Duration (ms)': csv_sspfm_bias.get('Seg durat (R) [ms]'),
        'Read Samples Per Segment': csv_sspfm_bias.get('Seg sample (R)')
    }

    low_freq = csv_sspfm_bias.get('Low freq [kHz]')
    high_freq = csv_sspfm_bias.get('High freq [kHz]')
    script_dict['Frequency Range (kHz)'] = (low_freq, high_freq)

    if verbose:
        print("Script parameters extracted successfully.")

    return script_dict


def csv_meas_sheet_extract(dir_path_in_csv, verbose=False):
    """
    Extract parameters saved in a csv file

    Parameters
    ----------
    dir_path_in_csv: str
        Path of the csv file directory
    verbose: bool, optional
        If True, print name of csv file

    Returns
    -------
    csv_meas: dict
        All measurement parameters saved in the csv file
    csv_sspfm_bias: dict
        All sspfm bias parameters saved in the csv file
    """
    assert os.path.isdir(dir_path_in_csv), "Invalid directory path"

    file_path_in_csv = ''
    meas_pars_sheet = 'measure parameters'
    bias_pars_sheet = 'sspfm bias parameters'

    for elem in os.listdir(dir_path_in_csv):
        if elem.endswith('.csv') and 'measurement sheet' in elem:
            file_path_in_csv = os.path.join(dir_path_in_csv, elem)
            if verbose:
                name = os.path.split(file_path_in_csv)[1]
                print(f'- meas sheet name: "{name}"\n')

    excel_meas = pd.read_excel(file_path_in_csv, sheet_name=meas_pars_sheet)
    csv_meas = dict(zip(excel_meas['Parameter'].tolist(),
                        excel_meas['Value'].tolist()))

    excel_sspfm_bias = pd.read_excel(file_path_in_csv,
                                     sheet_name=bias_pars_sheet)
    csv_sspfm_bias = dict(zip(excel_sspfm_bias['Parameter'].tolist(),
                              excel_sspfm_bias['Value'].tolist()))

    return csv_meas, csv_sspfm_bias
