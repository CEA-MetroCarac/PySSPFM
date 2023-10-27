"""
Example of gen_datas methods
"""
import random
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.datacube_to_nanoloop.plot import plt_signals
from PySSPFM.utils.datacube_to_nanoloop.gen_datas import gen_segments


def pars_segment():
    """
    Segment parameters function

    Returns
    -------
    seg_pars: dict
        Dictionary of segment parameters
    sign_pars: dict
        Dictionary of signal parameters
    hold_dict: dict
        Dictionary of hold time parameters
    noise_pars: dict
        Dictionary of noise parameters
    meas_range: dict
        Dictionary of measurement range
    fit_pars: dict
        Dictionary of fitting parameters
    user_pars: dict
        Dictionary of user parameters
    """
    seg_pars = {'mode': 'dfrt',
                'cut seg [%]': {'start': 10, 'end': 10},
                'filter': False,
                'filter ord': 10}
    sign_pars = {'Min volt (R) [V]': 0,
                 'Max volt (R) [V]': 0,
                 'Nb volt (R)': 10,
                 'Seg sample (R)': 100,
                 'Seg durat (R) [ms]': 50,
                 'Mode (R)': 'Low to High',
                 'Min volt (W) [V]': -10,
                 'Max volt (W) [V]': 10,
                 'Nb volt (W)': 50,
                 'Seg sample (W)': 100,
                 'Seg durat (W) [ms]': 50,
                 'Mode (W)': 'Zero, up'}
    hold_dict = {'start time': 1,
                 'end time': 1,
                 'start samp': 20,
                 'end samp': 20}
    noise_pars = {'type': 'normal',
                  'ampli': 10}
    meas_range = {'amp': [0, 50], 'pha': [0, 180]}
    fit_pars = {'fit pha': True,
                'detect peak': False,
                'sens peak detect': 1.5}
    user_pars = {'file path in': 'gen data module',
                 'root out': 'gen data module out',
                 'seg pars': seg_pars,
                 'fit pars': fit_pars}

    return (seg_pars, sign_pars, hold_dict, noise_pars, meas_range, fit_pars,
            user_pars)


def ex_gen_segments(mode, make_plots=False):
    """
    Example of gen_segments function

    Parameters
    ----------
    mode: str
        Mode of the segments
    make_plots: bool, optional
        Whether to generate plots or not

    Returns
    -------
    dict_meas: dict
        Dictionary containing the generated segments
    """
    out = pars_segment()
    (seg_pars, sign_pars, hold_dict, noise_pars, meas_range, _, _) = out
    np.random.seed(0)
    random.seed(0)

    seg_pars['mode'] = mode
    # ex gen_segments
    dict_meas = gen_segments(
        sign_pars, mode=seg_pars['mode'], seg_noise_pars=noise_pars,
        hold_dict=hold_dict, alea_target_range=meas_range)

    if make_plots:
        fig = plt_signals(dict_meas, unit='nm')
        fig.sfn += f"_{mode}"
        return [fig]
    else:
        return dict_meas


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "seg_to_loop_gen_datas", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_gen_segments('fit', make_plots=True)
    figs += ex_gen_segments('dfrt', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
