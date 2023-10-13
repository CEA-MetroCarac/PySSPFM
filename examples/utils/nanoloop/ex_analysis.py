"""
Example of analysis and plot methods
"""
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop.plot import \
    plot_sspfm_loops, plot_multiloop, plot_ckpfm
from PySSPFM.utils.nanoloop.gen_datas import gen_loops
from PySSPFM.utils.nanoloop.analysis import MultiLoop, MeanLoop, gen_ckpfm_meas


def init_pars():
    """
    Initialize the physical parameters for nanoloop generation.

    Returns
    -------
    pars: dict
        Dictionary of physical parameters for nanoloop generation.
        Contains sub-dictionaries for 'write', 'read', 'elec', and 'ferro'
        parameters.
    pha_calib: dict
        Dictionary of phase calibration parameters.
        Contains the 'type' of treatment, 'dict phase' mapping phase labels to
        values, and 'reverse' flag.
    pha_val: dict
        Phase forward and reverse value
    noise_pars: dict
        Dictionary of noise parameters.
        Contains the 'type' of noise and its 'ampli' (relative amplitude in %).
    """
    # Write parameters
    write_pars = {'range': [-10, 10], 'nb': 201, 'mode': 'Zero, up'}

    # Read parameters
    read_pars = {'range': [-1, 1], 'nb': 4}

    # Electrostatic parameters
    elec_pars = {'cpd': 0.3, 'slope': -2}

    # Ferroelectric parameters
    ferro_pars = {'amp': 5, 'coer l': -4, 'coer r': 3, 'sw slope': 1,
                  'offset': 1}

    # Noise parameters
    noise_pars = {'type': 'normal', 'ampli': 10}

    # Phase calibration parameters
    pha_calib = {'corr': 'offset',
                 'dict phase meas': {'low': 180, 'high': 0},
                 'dict phase target': {'low': 180, 'high': 0},
                 'func': np.cos,
                 'reverse': False}

    pha_val = {"fwd": 0, "rev": 180}

    # Consolidate all parameters into a single dictionary
    pars = {'write': write_pars, 'read': read_pars, 'elec': elec_pars,
            'ferro': ferro_pars}

    return pars, pha_calib, pha_val, noise_pars


def example_analysis(mode, make_plots=False, verbose=False):
    """
    Example of analysis and plot functions.

    Parameters
    ----------
    mode: str
        Mode of the analysis ('on' or 'off').
    make_plots: bool, optional
        Flag indicating whether to generate plots.
    verbose: bool, optional
        Flag indicating whether to print verbose output.

    Returns
    -------
    results: tuple or list
        Depending on the value of `make_plots`, either a list of figures or a
        tuple of analysis results.
    """
    # Initialize parameters
    pars, pha_calib, pha_val, noise_pars = init_pars()
    np.random.seed(0)

    # Generate loop data
    out = gen_loops(pars, noise_pars=noise_pars, pha_val=pha_val)
    write_voltage, read_voltage, amp, pha = out

    # Set plot properties based on the mode
    if mode == 'on':
        plot_dict = {'label': 'On field', 'col': 'y', 'unit': 'u.a'}
    elif mode == 'off':
        plot_dict = {'label': 'Off field', 'col': 'w', 'unit': 'u.a'}
    else:
        raise IOError('mode must be: "on" or "off"')

    figs_analysis = []
    loop_tab = []
    ckpfm_loop_dict = {}
    for elem_volt, elem_amp, elem_pha in zip(
            write_voltage, amp[mode], pha[mode]):
        # ex MultiLoop
        loop_tab.append(MultiLoop(
            list(elem_volt), list(elem_amp), list(elem_pha),
            read_voltage[len(loop_tab)], pha_calib, mode=plot_dict['label']))

    # Generate and plot SSPFM loops
    figs_loop = plot_sspfm_loops(loop_tab, pha_calib, dict_str=plot_dict)
    figs_analysis.extend(figs_loop)

    # Store initial PFM measurement
    amp_0, pha_0 = loop_tab[0].amp[0], loop_tab[0].pha[0]
    init_meas = {'amp': amp_0, 'pha': pha_0}
    if verbose:
        print(f'{mode} field: initial amp: {amp_0}, initial amp: {pha_0}')

    # Generate and plot CKPFM measurement
    if mode == 'off':
        # ex gen_ckpfm_meas
        ckpfm_loop_dict = gen_ckpfm_meas(loop_tab)
        fig = plot_ckpfm(ckpfm_loop_dict, dict_str=plot_dict)
        figs_analysis.append(fig)

    # ex MeanLoop
    mean_loop = MeanLoop(loop_tab)

    # Plot MeanLoop
    fig = plot_multiloop(mean_loop, dict_str=plot_dict)
    figs_analysis.append(fig)

    if make_plots:
        return figs_analysis
    else:
        return loop_tab, mean_loop, init_meas, ckpfm_loop_dict


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_analysis", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_analysis('on', make_plots=True, verbose=True)
    figs += example_analysis('off', make_plots=True, verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
