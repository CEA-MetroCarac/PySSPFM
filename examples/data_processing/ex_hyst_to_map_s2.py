"""
Example of hyst_to_map_s2 methods
"""
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.data_processing.hyst_to_map_s2 import multi_script


def main_pars():
    """
    Generate main_pars: treatment + measurement + ferro parameters.

    Returns
    -------
    user_pars: dict
        Dictionary containing user parameters.
    sign_pars: dict
        Dictionary containing sign parameters.
    meas_pars: dict
        Dictionary containing measurement parameters.
    ferro_pars_1: dict
        Dictionary containing ferro parameters for phase 1.
    ferro_pars_2: dict
        Dictionary containing ferro parameters for phase 2.
    """
    # Define user parameters
    user_pars = {'func': 'sigmoid',
                 'asymmetric': False,
                 'method': 'leastsq',
                 'inf thresh': 10,
                 'sat thresh': 90,
                 'del 1st loop': False,
                 'pha corr': 'offset',
                 'pha fwd': 0,
                 'pha rev': 180,
                 'pha func': np.cos,
                 'main elec': True,
                 'locked elec slope': None,
                 'diff mode': 'set',
                 'diff domain': {'min': -5., 'max': 5.},
                 'sat mode': 'set',
                 'sat domain': {'min': -9., 'max': 9.}}

    # Define sign parameters
    sign_pars = {
        'Min volt (R) [V]': 0,
        'Max volt (R) [V]': 0,
        'Nb volt (R)': 10,
        'Seg sample (R)': 100,
        'Seg durat (R) [ms]': 50,
        'Mode (R)': 'Single Read Step',
        'Min volt (W) [V]': -10,
        'Max volt (W) [V]': 10,
        'Nb volt (W)': 50,
        'Seg sample (W)': 100,
        'Seg durat (W) [ms]': 50,
        'Mode (W)': 'Zero, up'
    }

    # Define measurement parameters
    meas_pars = {'Q factor': 1.,
                 'Bias app': 'Sample',
                 'Sign of d33': 'positive'}

    # Define ferro parameters for phase 1
    ferro_pars_1 = {
        'amp': 10,
        'coer l': -2,
        'coer r': 2,
        'sw slope': 1,
        'offset': 0
    }

    # Define ferro parameters for phase 2
    ferro_pars_2 = {
        'amp': 15,
        'coer l': -1,
        'coer r': 1,
        'sw slope': 1.5,
        'offset': -0.4
    }

    return user_pars, sign_pars, meas_pars, ferro_pars_1, ferro_pars_2


def loop_dict_gen(ferro_pars, sign_pars):
    """
    Generate loop_dict to construct a loop.

    Parameters
    ----------
    ferro_pars: dict
        Dictionary containing ferro parameters.
    sign_pars: dict
        Dictionary containing sign parameters.

    Returns
    -------
    loop_dict: dict
        Dictionary representing the loop.
    """
    # Set random seed
    np.random.seed(0)

    # Define loop noise parameters
    loop_noise_pars = {'type': 'normal', 'ampli': 10}

    # Define electrode parameters
    elec_pars = {'cpd': 0.3, 'slope': -3}

    # Define write parameters
    write_pars = {
        'range': [sign_pars['Min volt (W) [V]'], sign_pars['Max volt (W) [V]']],
        'nb': sign_pars['Nb volt (W)'],
        'mode': sign_pars['Mode (W)']
    }

    # Define read parameters
    read_pars = {
        'range': [sign_pars['Min volt (R) [V]'], sign_pars['Max volt (R) [V]']],
        'nb': sign_pars['Nb volt (R)']
    }

    # Construct the loop dictionary
    loop_dict = {
        'write': write_pars,
        'read': read_pars,
        'elec': elec_pars,
        'ferro': ferro_pars,
        'noise': loop_noise_pars,
        'mode': ''
    }

    return loop_dict


def ex_multi_script(make_plots=False, verbose=False):
    """
    Example of multi_script function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).
    verbose: bool, optional
        Verbosity flag (default is False).

    Returns
    ----------
    None
    """
    modes = ['off', 'on']
    nb_pix_x = 8
    nb_pix_y = 8
    index_pix_phase_2 = [2, 3, 4, 10, 11, 12, 13, 14, 18, 19, 20, 28]

    user_pars, sign_pars, meas_pars, ferro_pars_1, ferro_pars_2 = main_pars()

    # Update measurement parameters
    meas_pars['Grid x [pix]'] = nb_pix_x
    meas_pars['Grid y [pix]'] = nb_pix_y
    meas_pars['Grid x [um]'] = 3.5
    meas_pars['Grid y [um]'] = 3.5

    nb_file = nb_pix_x * nb_pix_y

    loop_dicts = []

    # Generate loop dictionaries for each pixel and mode
    for i in range(nb_file):
        for mode in modes:
            # Select ferro phase parameters
            ferro_pars = ferro_pars_1
            if i in index_pix_phase_2:
                ferro_pars = ferro_pars_2

            # Generate loop dictionary
            loop_dict = loop_dict_gen(ferro_pars, sign_pars)
            loop_dict['mode'] = mode
            loop_dicts.append(loop_dict)

    # saving path management
    dir_path_out, save = save_path_example(
        "hyst_to_map_s2", save_example_exe=make_plots, save_test_exe=False)
    # ex multi_script
    multi_script(user_pars, '', meas_pars, sign_pars, 0, '',
                 test_dicts=loop_dicts, verbose=verbose, show_plots=make_plots,
                 save=save, root_out=dir_path_out)


if __name__ == '__main__':
    figs = []

    ex_multi_script(make_plots=True, verbose=True)
