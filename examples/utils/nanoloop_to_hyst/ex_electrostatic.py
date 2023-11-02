"""
Example of electrostatic and plot methods
"""
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.core.basic_func import linear
from PySSPFM.utils.core.noise import noise
from PySSPFM.utils.nanoloop.gen_data import gen_nanoloops
from PySSPFM.utils.nanoloop.analysis import MultiLoop
from PySSPFM.utils.nanoloop_to_hyst.plot import plot_nanoloop_on_off
from PySSPFM.utils.nanoloop_to_hyst.electrostatic import \
    btfly_analysis, sat_analysis, offset_analysis, differential_analysis


def pars_gen():
    """
    Generate physical parameters and dictionary for figure annotation.

    Returns
    -------
    pars: dict
        Dictionary of physical parameters.
    dict_str: dict
        Dictionary of string annotations.
    """
    np.random.seed(0)

    # Define write parameters
    write_pars = {'range': [-10, 10],
                  'nb': 201,
                  'mode': 'Zero, up'}

    # Define read parameters
    read_pars = {'range': [0, 0],
                 'nb': 1}

    # Define electrostatic parameters
    elec_pars = {'cpd': 0.3,
                 'slope': -5}

    # Define ferroelectric parameters
    ferro_pars = {'amp': 5,
                  'coer l': -4,
                  'coer r': 4,
                  'sw slope': 1,
                  'offset': 0}

    # Combine all parameters into a dictionary
    pars = {'write': write_pars,
            'read': read_pars,
            'elec': elec_pars,
            'ferro': ferro_pars}

    # Define string annotations for on and off fields
    dict_str = {
        'on': {'col': 'y', 'label': 'On field', 'unit': 'nm', 'index': 1},
        'off': {'col': 'w', 'label': 'Off field', 'unit': 'nm', 'index': 1}}

    return pars, dict_str


def multiloop_gen():
    """
    Generate Multiloop objects for On and Off fields.

    Returns
    -------
    loop: dict
        Dictionary of Multiloop objects.
    dict_str: dict
        Dictionary of string annotations.
    """
    # Define noise parameters
    noise_pars = {'type': 'normal', 'ampli': 5}
    pha_val = {'fwd': 0, 'rev': 180}

    # Generate physical parameters and string annotations
    pars, dict_str = pars_gen()

    # Generate loop data
    out = gen_nanoloops(pars, noise_pars=noise_pars, pha_val=pha_val)
    write_voltage, read_voltage, amplitude, phase = out

    mode = ['On field', 'Off field']
    loop = {}

    # Create Multiloop objects for On and Off fields
    for cont, key in enumerate(['on', 'off']):
        loop[key] = MultiLoop(list(write_voltage[0]), list(amplitude[key][0]),
                              list(phase[key][0]), read_voltage,
                              pha_calib={"func": np.cos, "corr": 'raw'},
                              mode=mode[cont])

    return loop, dict_str


def measure_pfm(loop):
    """
    Generate PFM measurements from a loop.

    Parameters
    ----------
    loop: MultiLoop
        Object containing loop data.

    Returns
    -------
    write: dict
        Dictionary of write voltages.
    amp: dict
        Dictionary of amplitudes.
    pha: dict
        Dictionary of phases.
    piezorep: dict
        Dictionary of piezorep values.
    """
    # Extract loop data
    write = {'left': loop.write_volt_left,
             'right': loop.write_volt_right}
    amp = {'left': loop.amp_left,
           'right': loop.amp_right}
    pha = {'left': loop.pha_left,
           'right': loop.pha_right}
    piezorep = {'left': loop.piezorep_left,
                'right': loop.piezorep_right}

    return write, amp, pha, piezorep


def ex_btfly_analysis(make_plots=False, verbose=False):
    """
    Example of btfly_analysis function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots, by default False.
    verbose: bool, optional
        Flag indicating whether to print verbose information, by default
        False.

    Returns
    -------
    imprint: float or None
        Imprint value calculated from the analysis.
    fig: matplotlib.figure.Figure or None
        Figure object containing the plots when make_plots is True,
        None otherwise.
    """
    loop, dict_str = multiloop_gen()

    # Measure PFM for 'on' loop
    write, amp, _, _ = measure_pfm(loop['on'])

    # ex btfly_analysis
    imprint, fig = btfly_analysis(
        write, amp, make_plots=make_plots, dict_str=dict_str['on'])

    if verbose:
        print('\t- ex_btfly_analysis:')
        print(f'\t\timprint: {imprint}')

    if make_plots:
        fig.sfn = 'ex_btfly_analysis'
        return [fig]
    else:
        return imprint


def ex_sat_analysis(make_plots=False, verbose=False):
    """
    Example of sat_analysis function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots, by default False.
    verbose: bool, optional
        Flag indicating whether to print verbose information, by default
        False.

    Returns
    -------
    sat_res: float or None
        Saturation analysis result.
    figs_sat: list of matplotlib.figure.Figure or None
        List of figure objects containing the plots when make_plots is True,
        None otherwise.
    """
    loop, dict_str = multiloop_gen()

    # Measure PFM for 'on' loop
    write, amp, pha, piezorep = measure_pfm(loop['on'])

    # ex sat_analysis
    sat_res, figs_sat = sat_analysis(write, amp, pha, piezorep,
                                     sat_domain=[-5, 5], make_plots=make_plots,
                                     dict_str=dict_str['on'], func=np.cos)

    if verbose:
        print('\t- ex_sat_analysis:')
        print(f'\t\tres: {sat_res}')

    if make_plots:
        figs_sat[0].sfn = 'ex_sat_analysis_1'
        figs_sat[1].sfn = 'ex_sat_analysis_2'
        return figs_sat
    else:
        return sat_res


def ex_offset_analysis(make_plots=False, verbose=False):
    """
    Example of offset_analysis function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots, by default False.
    verbose: bool, optional
        Flag indicating whether to print verbose information, by default
        False.

    Returns
    -------
    offset_res: float or None
        Offset analysis result.
    fig: matplotlib.figure.Figure or None
        Figure object containing the plot when make_plots is True,
        None otherwise.
    """
    # Generate noise parameters
    noise_pars = {'type': 'normal',
                  'ampli': 10}

    # Generate parameters and dictionary
    pars, dict_str = pars_gen()

    # Generate read voltage values
    read_volt = np.linspace(-5, 5, 11)

    # Compute offset using linear function
    offset = linear(read_volt, -pars['elec']['slope'] * pars['elec']['cpd'],
                    pars['elec']['slope'])

    # Apply noise to offset
    offset = noise(offset, noise_pars)

    # ex offset_analysis
    offset_res, fig = offset_analysis(read_volt, offset, make_plots=make_plots,
                                      dict_str=dict_str['off'])

    if verbose:
        print('\t- ex_offset_analysis:')
        print(f'\t\tres: {offset_res}')

    if make_plots:
        fig.sfn = 'ex_offset_analysis'
        return [fig]
    else:
        return offset_res


def ex_differential_analysis(make_plots=False, verbose=False):
    """
    Example of differential_analysis function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots, by default False.
    verbose: bool, optional
        Flag indicating whether to print verbose information, by default
        False.

    Returns
    -------
    diff_res: float or None
        Differential analysis result.
    """
    # Generate Multiloop objects
    loop, dict_str = multiloop_gen()

    # ex differential_analysis
    out = differential_analysis(
        loop['on'], loop['off'], dict_str=dict_str['on'], make_plots=make_plots)

    # Unpack the output
    (_, _, diff_res, fig) = out

    if verbose:
        print('\t- ex_differential_analysis:')
        print(f'\t\tres: {diff_res}')

    if make_plots:
        fig.sfn = 'ex_differential_analysis'
        return [fig]
    else:
        return diff_res


def ex_plot_nanoloop_on_off():
    """
    Example of plot_nanoloop_on_off function.

    Returns
    -------
    list
        List containing the figure object.
    """
    # Generate Multiloop objects
    loop, dict_str = multiloop_gen()

    # ex plot_nanoloop_on_off
    fig = plot_nanoloop_on_off(loop['on'], loop['off'], dict_str=dict_str['on'])
    fig.sfn = 'ex_plot_nanoloop_on_off'

    return [fig]


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_to_hyst_electrostatic", save_example_exe=True,
        save_test_exe=False)
    figs = []
    figs += ex_btfly_analysis(make_plots=True, verbose=True)
    figs += ex_sat_analysis(make_plots=True, verbose=True)
    figs += ex_offset_analysis(make_plots=True, verbose=True)
    figs += ex_differential_analysis(make_plots=True, verbose=True)
    figs += ex_plot_nanoloop_on_off()
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
