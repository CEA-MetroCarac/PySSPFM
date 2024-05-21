"""
Module used for the scripts of sspfm 1st step data analysis
(convert datacube to nanoloop)
    - Open and read files
    - Print info
    - Save measurements and parameters
"""

import time
import os
from datetime import datetime
import numpy as np

from PySSPFM.settings import get_setting


def save_parameters(dir_path_out, t0, date, exp_meas_time, user_pars,
                    meas_pars, sign_pars, nb_file):
    """
    Save all measurement and treatment parameters in a txt file

    Parameters
    ----------
    dir_path_out: str
        Directory path of saving params file (out)
    t0: float
        Time passed (in nb of second since 01/01/1970), at the moment of save
        initialization
    date: str
        Date (Year-Month-Day Hour:Minute), at the moment of save initialization
    exp_meas_time: float
        Experimental measurement time in seconds
    user_pars: dict
        All user parameters for the treatment
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        sspfm bias signal parameters
    nb_file: int
        Number of sspfm file analyzed

    Returns
    -------
    None
    """
    if not os.path.isdir(dir_path_out):
        os.makedirs(dir_path_out)

    treatment_time = time.time() - t0
    treatment_time_hms_th = time.strftime('%Hh:%Mm:%Ss',
                                          time.gmtime(treatment_time))
    treatment_time_hms_exp = time.strftime('%Hh:%Mm:%Ss',
                                           time.gmtime(exp_meas_time))

    info = {
        'start of analysis': date,
        'analysis duration (theoretical)': treatment_time_hms_th,
        'nb file analyzed': nb_file,
        'analysis duration (real)': treatment_time_hms_exp
    }

    parameters_file_name = get_setting('default_parameters_file_name')
    file_path_out = os.path.join(dir_path_out, parameters_file_name)

    with open(file_path_out, 'w', encoding='utf-8') as file:
        titles = ['### Experiment parameters ###\n',
                  '\n\n### Treatment parameters: first step ###\n']
        subtitles = [
            '\n- Global parameters\n',
            '\n- SS PFM parameters\n',
            '\n- Info\n',
            '\n- Segment parameters\n',
            '\n- Fit parameters\n'
        ]

        cont = 0
        for title, list_dico in zip(titles, [[meas_pars, sign_pars],
                                             [info, user_pars['seg pars'],
                                              user_pars['fit pars']]]):
            file.write(title)
            for dico in list_dico:
                file.write(subtitles[cont])
                for key, value in dico.items():
                    line = f"{key}: {value}\n"
                    file.write(line)
                cont += 1
                if user_pars['seg pars']['mode'] != 'fit' and cont == 4:
                    break


def print_params(meas_pars, sign_pars, user_pars, verbose=False):
    """
    Print all parameters of the measure and treatment

    Parameters
    ----------
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        sspfm bias signal parameters
    user_pars: dict
        All user parameters for the treatment
    verbose: bool, optional
        If True, print all pars

    Returns
    -------
    None
    """
    list_dict = [meas_pars, sign_pars, user_pars['seg pars']]
    label_dict = ['- Meas parameters', '- Signal parameters',
                  '- User parameters']

    if user_pars['seg pars']['mode'] == 'fit':
        list_dict.append(user_pars['fit pars'])
        label_dict.append('- Fit parameters')

    if verbose:
        for dictio, lab in zip(list_dict, label_dict):
            print(f'------------\n{lab}')
            for key, value in dictio.items():
                print(key, ':', value)


def get_acquisition_time(folder_path, file_format='.spm'):
    """
    Get acquisition time of the latest file in the folder

    Parameters
    ----------
    folder_path: str
        Path of the folder containing measurement files
    file_format: str, optional
        File extension to filter relevant files, default is '.spm'

    Returns
    -------
    time_diff_seconds: float
        Time difference in seconds relative to the first file
    """
    # List files in the folder
    files = os.listdir(folder_path)

    # Filter relevant files
    valid_files = [file for file in files if file.endswith(file_format)]

    # Sort files by modification date
    valid_files.sort(key=lambda x: os.path.getmtime(
        os.path.join(folder_path, x)))

    # Extract modification dates and create file indices
    dates = [datetime.fromtimestamp(os.path.getmtime(
        os.path.join(folder_path, file))) for file in valid_files]

    # Calculate time difference in seconds relative to the first file
    time_diff_seconds = [(date - dates[0]).total_seconds() for date in dates]

    return time_diff_seconds[-1]


def get_phase_tab_offset(phase_file_path):
    """
    Get phase tab offset from file.

    Parameters
    ----------
    phase_file_path : str
        Path to the phase file.

    Returns
    -------
    phase_tab : numpy.ndarray
        Phase offset data.
    """

    # Load data from the text file
    data = np.genfromtxt(phase_file_path, delimiter='\t\t', skip_header=3)

    # Extract the headers
    with open(phase_file_path, 'r', encoding='latin-1') as file:
        headers = file.readlines()[2][2:].strip().split('\t\t')

    # Create a dictionary using the extracted headers
    phase_dict = dict(zip(headers, data.T))

    # Get phase offset
    phase_tab = phase_dict.get("Mean", phase_dict[list(phase_dict.keys())[0]])

    return phase_tab
