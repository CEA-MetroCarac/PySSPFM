"""
Example of gen_datas methods
"""
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.nanoloop_to_hyst.gen_datas import gen_datas_dict
from PySSPFM.utils.nanoloop.analysis import treat_loop
from PySSPFM.utils.nanoloop.plot import plot_all_loop
from PySSPFM.utils.core.figure import print_plots


def gen_pars(read_volt_range=None):
    """
    Generate all parameters of the loop and sspfm voltage signal.

    Parameters
    ----------
    read_volt_range: list, optional
        List specifying the range of read voltage, defaults to None.

    Returns
    -------
    pars: dict
        Dictionary containing all parameters.
    sign_pars: dict
        Dictionary containing sign parameters.
    pha_val: dict, optional
        Dict of phase forward and reverse value.
    """
    # Set default value for read_volt_range
    read_volt_range = read_volt_range or [0, 0]

    # Determine read mode based on read_volt_range
    read_mode = 'Single Read Step' if read_volt_range[0] == read_volt_range[1] \
        else 'Low to High'

    elec_pars = {'cpd': 0.9,
                 'slope': -.4}

    ferro_pars = {'amp': 10,
                  'coer l': -2,
                  'coer r': 2,
                  'sw slope': 1,
                  'offset': 0}

    # Noise (relative amplitude in %)
    noise_pars = {'type': 'normal',
                  'ampli': 10}

    sign_pars = {'Min volt (R) [V]': read_volt_range[0],
                 'Max volt (R) [V]': read_volt_range[1],
                 'Nb volt (R)': 5,
                 'Mode (R)': read_mode,
                 'Seg durat (R) [ms]': 500,
                 'Seg sample (R)': 100,
                 'Min volt (W) [V]': -10,
                 'Max volt (W) [V]': 10,
                 'Nb volt (W)': 51,
                 'Mode (W)': 'Zero, up',
                 'Seg durat (W) [ms]': 500,
                 'Seg sample (W)': 100}

    write_pars = {'range': [sign_pars['Min volt (W) [V]'],
                            sign_pars['Max volt (W) [V]']],
                  'nb': sign_pars['Nb volt (W)'],
                  'mode': sign_pars['Mode (W)']}
    read_pars = {'range': [sign_pars['Min volt (R) [V]'],
                           sign_pars['Max volt (R) [V]']],
                 'nb': sign_pars['Nb volt (R)']}
    pars = {'write': write_pars,
            'read': read_pars,
            'elec': elec_pars,
            'ferro': ferro_pars,
            'noise': noise_pars}

    pha_val = {'fwd': 0, 'rev': 180}

    return pars, sign_pars, pha_val


def example_gen_datas(analysis='mean_off', make_plots=False, verbose=False):
    """
    Example of gen_datas function.

    Parameters
    ----------
    analysis: str, optional
        Type of analysis, defaults to 'mean_off'.
    make_plots: bool, optional
        Whether to generate plots, defaults to False.
    verbose: bool, optional
        Whether to print verbose output, defaults to False.

    Returns
    -------
    datas_dict: dict
        Dictionary containing generated data (when make_plots=False).
    dict_str: str
        String representation of the datas_dict (when make_plots=False).
    """
    np.random.seed(0)

    if verbose:
        print(f'\t- {analysis} analysis:')

    # Determine read_volt_range and mode based on analysis
    if analysis == 'multi_off':
        read_volt_range = [-2, 2]
        mode = 'off'
    elif analysis == 'mean_off':
        read_volt_range = [0, 0]
        mode = 'off'
    elif analysis == 'mean_on':
        read_volt_range = [0, 0]
        mode = 'on'
    else:
        raise IOError('analysis must be: "multi_off", "mean_off" or "mean_on"')

    # Gen pars
    pars, sign_pars, pha_val = gen_pars(read_volt_range=read_volt_range)

    # ex gen_datas_dict
    datas_dict, dict_str = gen_datas_dict(pars, q_fact=100., mode=mode,
                                          pha_val=pha_val)

    if verbose:
        print(f'\t\tdict_str: {dict_str}')

    if make_plots:
        # Perform treatment and generate plots
        out = treat_loop(datas_dict, sign_pars, dict_str=dict_str)
        loop_tab, pha_calib, _ = out
        figs_loop = plot_all_loop(loop_tab, pha_calib=pha_calib,
                                  dict_str=dict_str)
        for fig in figs_loop:
            fig.sfn += f"_{analysis}"
        return figs_loop
    else:
        return datas_dict, dict_str


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "hyst_to_map_gen_datas", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_gen_datas(analysis='multi_off', make_plots=True,
                              verbose=True)
    figs += example_gen_datas(analysis='mean_off', make_plots=True,
                              verbose=True)
    figs += example_gen_datas(analysis='mean_on', make_plots=True, verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
