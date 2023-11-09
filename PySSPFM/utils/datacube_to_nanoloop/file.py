"""
Module used for the scripts of sspfm 1st step data analysis
(convert datacube to nanoloop)
    - Open and read files
    - Print info
    - Save measurements and parameters
"""

import time
import os

from PySSPFM.settings import get_setting


def save_parameters(dir_path_out, t0, date, user_pars, meas_pars, sign_pars,
                    nb_file):
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
    treatment_time_h_m_s = time.strftime('%Hh:%Mm:%Ss',
                                         time.gmtime(treatment_time))

    info = {
        'start of analysis': date,
        'analysis duration': treatment_time_h_m_s,
        'nb file analyzed': nb_file
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
