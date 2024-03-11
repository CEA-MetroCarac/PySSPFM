"""
Example of analysis and plot methods
"""
import random as rand
import numpy as np

from examples.utils.nanoloop_to_hyst.ex_gen_data import gen_pars
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop.plot import plot_all_loop
from PySSPFM.utils.nanoloop.analysis import nanoloop_treatment
from PySSPFM.utils.nanoloop.phase import gen_dict_pha
from PySSPFM.utils.nanoloop_to_hyst.gen_data import gen_data_dict
from PySSPFM.utils.nanoloop_to_hyst.analysis import \
    (sort_prop, gen_analysis_mode, find_best_nanoloop, hyst_analysis,
     electrostatic_analysis)


def ex_sort_prop(verbose=False):
    """
    Example of ex_sort_prop function.

    Parameters
    ----------
    verbose: bool, optional
        Flag indicating whether to print verbose output. Default is False.

    Returns
    -------
    properties: dict
        Sorted properties dictionary.
    """
    rand.seed(0)

    # Generate properties dictionary
    properties = {}
    for lab in ['on', 'off', 'coupled']:
        properties[lab] = {}
        for i in range(1, 65):
            properties[lab][f' - file n°{i}'] = {}
            for j in range(20):
                properties[lab][f' - file n°{i}'][f'prop n°{j}'] = \
                    float(rand.randint(0, 10))

    # ex sort_prop
    properties = sort_prop(properties)

    if verbose:
        print('\t- ex sort_prop:')
        for key, value in properties['on'].items():
            print(f'\t\t{key}: {value}')

    return properties


def example_analysis(analysis='mean_off', make_plots=False, verbose=False):
    """
    Example of analysis and plot functions.

    Parameters
    ----------
    analysis: str, optional
        Type of analysis to perform. Default is 'mean_off'.
    make_plots: bool, optional
        Flag indicating whether to generate plots. Default is False.
    verbose: bool, optional
        Flag indicating whether to print verbose output. Default is False.

    Returns
    -------
    list or tuple
        List of figures when make_plots is True, otherwise a tuple of analysis
        results.
    """
    np.random.seed(0)

    if verbose:
        print(f'\n- {analysis} analysis:')

    # Define read voltage range and mode based on analysis type
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

    meas_pars = {'SSPFM Bias app': 'Sample',
                 'Sign of d33': 'positive'}
    dict_pha = gen_dict_pha(meas_pars, 'offset', main_elec=False)

    # Generate parameter and sign parameter dictionaries
    pars, sign_pars, pha_val = gen_pars(read_volt_range=read_volt_range)

    # ex gen_analysis_mode
    analysis_mode = gen_analysis_mode(mode=mode,
                                      read_mode=sign_pars['Mode (R)'])

    if verbose:
        print('\t- ex analysis_mode:')
        print(f'\t\tanalysis_mode: {analysis_mode}')

    # ex gen_data_dict
    datas_dict, dict_str = gen_data_dict(
        pars, q_fact=1., mode=mode, pha_val=pha_val)

    if verbose:
        print('\t- ex gen_data_dict:')
        print(f'\t\tdict_str: {dict_str}')

    # Treat nanoloop data
    loop_tab, pha_calib, _ = nanoloop_treatment(
        datas_dict, sign_pars, dict_pha=dict_pha, dict_str=dict_str)

    if make_plots:
        figs_loop = plot_all_loop(
            loop_tab, pha_calib=pha_calib, dict_str=dict_str)
    else:
        figs_loop = []

    # ex find_best_nanoloop
    out = find_best_nanoloop(
        loop_tab, dict_pha['counterclockwise'], dict_pha['grounded tip'],
        analysis_mode=analysis_mode, del_1st_loop=False, model='sigmoid',
        asymmetric=False, method="least_square", locked_elec_slope=None)
    x_hyst, y_hyst, best_loop, read_volt, bckgnd_tab = out

    if verbose:
        print('\t- ex find_best_nanoloop:')
        print(f'\t\tread_volt: {read_volt}')
        print(f'\t\tbckgnd_tab: {bckgnd_tab}')

    # ex hyst_analysis
    out = hyst_analysis(x_hyst, y_hyst, best_loop, dict_pha['counterclockwise'],
                        dict_pha['grounded tip'], dict_str=dict_str,
                        infl_threshold=10, sat_threshold=90, model='sigmoid',
                        asymmetric=False, method='least_square',
                        analysis_mode=analysis_mode, locked_elec_slope=None,
                        make_plots=make_plots)
    _, props_tot, props_no_bckgnd, figs_hyst = out

    if verbose:
        print('\t- ex hyst_analysis:')
        print(f'\t\tread_volt: {props_tot}')
        print(f'\t\tbckgnd_tab: {props_no_bckgnd}')

    # ex electrostatic_analysis
    sat_domain = [props_tot['x sat r'], props_tot['x sat l']]
    electrostatic_dict, figs_elec = electrostatic_analysis(
        best_loop, analysis_mode=analysis_mode, sat_domain=sat_domain,
        make_plots=make_plots, dict_str=dict_str, read_volt=read_volt,
        bckgnd_tab=bckgnd_tab, func=dict_pha["func"])

    if verbose:
        print('\t- ex electrostatic_analysis:')
        for key in electrostatic_dict.keys():
            print(f'\t\t{key}: {electrostatic_dict[key]}')

    if make_plots:
        figures = figs_loop + figs_hyst + figs_elec
        for fig in figures:
            fig.sfn += f"_{analysis}"
        return figures
    else:
        return (analysis_mode, datas_dict, dict_str, x_hyst, y_hyst, best_loop,
                read_volt, bckgnd_tab, props_tot, props_no_bckgnd,
                electrostatic_dict)


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_to_hyst_analysis", save_example_exe=True,
        save_test_exe=False)
    figs = []
    ex_sort_prop(verbose=True)
    figs += example_analysis(analysis='multi_off', make_plots=True,
                             verbose=True)
    figs += example_analysis(analysis='mean_off', make_plots=True,
                             verbose=True)
    figs += example_analysis(analysis='mean_on', make_plots=True,
                             verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
