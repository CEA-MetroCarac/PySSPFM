"""
Example of datacube_to_nanoloop_s1 methods
"""
from examples.utils.datacube_to_nanoloop.ex_gen_data import pars_segment
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.data_processing.datacube_to_nanoloop_s1 import single_script


def ex_single_script(make_plots=False, verbose=False):
    """
    Example of single_script function.

    Parameters
    ----------
    make_plots (bool, optional)
        Whether to make plots or not. Defaults to False.
    verbose (bool, optional)
        Whether to display verbose output or not. Defaults to False.

    Returns
    -------
    phase_offset_val: dict
        Dictionary containing phase offset data of a single file resulting from
        analysis of histogram of phase segment values. If 'get_phase_offset' is
        False, this value is None.
    """
    # Configuration parameters
    seg_pars, sign_pars, hold_dict, _, _, _, user_pars = pars_segment()

    # Measurement parameters
    meas_pars = {
        'External meas': 'Yes',
        'Sens ampli': 0.1,
        'Offset ampli [V]': 0.5,
        'Sens phase [mV/°]': 1000,
        'Offset phase [V]': 0,
        'Calibration': 'no',
        'Calib fact [nm/V]': 1,
        'SSPFM Bias app': 'Sample',
        'Sign of d33': 'positive',
    }

    # Segment noise parameters
    seg_noise_pars = {
        'type': 'normal',
        'ampli': 1
    }

    # Target mode and range
    target_mode = 'nanoloop'
    alea_target_range = {
        'amp': [20, 50],
        'pha': [0, 180]
    }

    # Nanoloop noise parameters
    nanoloop_noise_pars = {
        'type': 'normal',
        'lvl': 10
    }

    # Electrode parameters
    elec_pars = {
        'cpd': 0.3,
        'slope': -3
    }

    # Ferroelectric parameters
    ferro_pars = {
        'amp': 5,
        'coer l': -3,
        'coer r': 3,
        'sw slope': 1,
        'offset': 0
    }

    # Write parameters
    write_pars = {
        'range': [sign_pars['Min volt (W) [V]'], sign_pars['Max volt (W) [V]']],
        'nb': sign_pars['Nb volt (W)'],
        'mode': sign_pars['Mode (W)']
    }

    # Read parameters
    read_pars = {
        'range': [sign_pars['Min volt (R) [V]'], sign_pars['Max volt (R) [V]']],
        'nb': sign_pars['Nb volt (R)']
    }

    # Nanoloop parameters
    nanoloop_pars = {
        'write': write_pars,
        'read': read_pars,
        'elec': elec_pars,
        'ferro': ferro_pars,
        'noise': nanoloop_noise_pars
    }

    # Segment dictionary based on target mode
    if target_mode == 'alea':
        seg_dict = {
            'seg noise': seg_noise_pars,
            'hold pars': hold_dict,
            'alea target range': alea_target_range,
            'loop pars': None
        }
    else:
        seg_dict = {
            'seg noise': seg_noise_pars,
            'hold pars': hold_dict,
            'alea target range': None,
            'loop pars': nanoloop_pars
        }
    get_phase_offset = bool(user_pars["pha pars"]["method"] == "dynamic")
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "datacube_to_nanoloop_s1", save_example_exe=make_plots,
        save_test_exe=not make_plots)
    txt_save = save_plots
    # ex single_script
    phase_offset_val = single_script(
        user_pars, '', meas_pars, sign_pars,
        phase_offset=user_pars['pha pars']['offset'],
        get_phase_offset=get_phase_offset, mode=seg_pars['mode'],
        root_out=dir_path_out, test_dict=seg_dict,
        verbose=verbose, show_plots=make_plots, save_plots=save_plots,
        txt_save=txt_save)

    return phase_offset_val


if __name__ == '__main__':
    _ = ex_single_script(make_plots=True, verbose=True)
