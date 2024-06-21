"""
Module used for the scripts of sspfm 1st step data analysis
(convert datacube to nanoloop)
    - Open and read files
    - Print info
    - Save measurements and parameters
"""

import numpy as np


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
