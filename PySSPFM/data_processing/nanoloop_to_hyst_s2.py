"""
--> Executable Script
Generate hysteresis properties from nanoloops by reading data from TXT files.
Inspired by SS_PFM script, Nanoscope, Bruker
"""

import os
import tkinter.filedialog as tkf
import time
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, get_config
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop.file import extract_nanoloop_data
from PySSPFM.utils.nanoloop.plot import plot_ckpfm
from PySSPFM.utils.nanoloop.phase import gen_dict_pha
from PySSPFM.utils.nanoloop.analysis import nanoloop_treatment, gen_ckpfm_meas
from PySSPFM.utils.nanoloop_to_hyst.file import \
    (generate_file_nanoloop_paths, save_properties, save_best_nanoloops,
     extract_main_elec_tab)
from PySSPFM.utils.nanoloop_to_hyst.plot import plot_nanoloop_on_off
from PySSPFM.utils.nanoloop_to_hyst.electrostatic import differential_analysis
from PySSPFM.utils.nanoloop_to_hyst.gen_data import gen_data_dict
from PySSPFM.utils.nanoloop_to_hyst.analysis import \
    gen_analysis_mode, find_best_nanoloop, hyst_analysis, electrostatic_analysis
from PySSPFM.utils.path_for_runable import create_json_res, copy_json_res
from PySSPFM.utils.raw_extraction import csv_meas_sheet_extract

DEFAULT_LIMIT = {'min': -5., 'max': 5.}
DEFAULT_FRACTION_LIMIT = 4


def single_analysis(file_path_in, user_pars, meas_pars, sign_pars,
                    analysis_mode='on_f_loop', cont=1, test_dict=None,
                    make_plots=False):
    """
    Analyze data from a measurement file (pixel), extract nanoloop data from
    a txt
    file, find the best nanoloop based on the analysis mode, fit and
    extract properties from hysteresis, and analyze the electrostatic
    component.

    Parameters
    ----------
    file_path_in: str
        Path of the txt nanoloop file (input).
    user_pars: dict
        User-defined parameters for the analysis.
    meas_pars: dict
        Measurement parameters.
    sign_pars: dict
        SSPFM bias signal parameters.
    analysis_mode: str, optional
        Operating mode for the analysis: 'on_f_loop', 'mean_loop', or
        'multi_loop'.
    cont: int, optional
        Index of the corresponding file.
    test_dict: dict, optional
        Dictionary of test parameters (used for testing the module).
    make_plots: bool, optional
        Flag to generate figures.

    Returns
    -------
    best_loop: loop (MultiLoop or MeanLoop) object
        Best nanoloop depending on the analysis mode for the pixel.
    properties: dict
        Properties of the pixel (result of single analysis).
    other_properties: dict
        Other properties about the segment (topography, mechanical measurement).
    dict_str: dict
        Dictionary used for figure annotation.
    figs: list of matplotlib.pyplot.Figure
        Figures of the single analysis.
    """
    assert analysis_mode in ['multi_loop', 'mean_loop', 'on_f_loop']

    figs, bckgnd_tab, read_volt, properties = [], [], [], {}

    if test_dict is None:
        data_dict, dict_str, other_properties = \
            extract_nanoloop_data(file_path_in)
    else:
        pha_val = {"fwd": user_pars["pha fwd"], "rev": user_pars["pha rev"]}
        data_dict, dict_str = gen_data_dict(
            test_dict, meas_pars['Q factor'], mode=test_dict['mode'],
            pha_val=pha_val)
        other_properties = {}
    dict_str['index'] = cont

    dict_pha = gen_dict_pha(
        meas_pars, user_pars['pha corr'], pha_fwd=user_pars['pha fwd'],
        pha_rev=user_pars['pha rev'], func=user_pars['pha func'],
        main_elec=user_pars['main elec'],
        locked_elec_slope=user_pars['locked elec slope'])

    # Check if measurement are performed in or out of resonance
    if 'Resonance' in meas_pars.keys():
        resonance = bool(meas_pars['Resonance'] == 'Resonance')
    else:
        resonance = False

    par = nanoloop_treatment(
        data_dict, sign_pars, dict_pha=dict_pha, dict_str=dict_str,
        q_fact_scalar=meas_pars['Q factor'], resonance=resonance)
    loop_tab, _, init_meas = par

    if analysis_mode == 'mean_loop':
        properties['amp 0'] = init_meas['amp']
        properties['pha 0'] = init_meas['pha']

    if analysis_mode == 'multi_loop':
        ckpfm_dict = gen_ckpfm_meas([loop.piezorep for loop in loop_tab])
        if make_plots:
            fig = plot_ckpfm(ckpfm_dict, dict_str=dict_str)
            figs.append(fig)

    par = find_best_nanoloop(
        loop_tab, dict_pha['counterclockwise'], dict_pha['grounded tip'],
        analysis_mode=analysis_mode, del_1st_loop=user_pars['del 1st loop'],
        model=user_pars['func'], method=user_pars['method'],
        locked_elec_slope=dict_pha['locked elec slope'])
    x_hyst, y_hyst, best_loop, read_volt, bckgnd_tab = par

    # properties : mean res freq et q factor
    if best_loop.res_freq:
        properties['res freq'] = np.mean(best_loop.res_freq.y_meas)
    if best_loop.q_fact:
        properties['q fact'] = np.mean(best_loop.q_fact.y_meas)

    # filter nan values
    nan_indices = np.isnan(x_hyst) | np.isnan(y_hyst)
    nan_ind = np.any(nan_indices, axis=0)
    x_hyst_filtered = []
    y_hyst_filtered = []
    for row_x, row_y in zip(x_hyst, y_hyst):
        filtered_row_x = [value for value, mask in zip(row_x, nan_ind)
                          if not mask]
        filtered_row_y = [value for value, mask in zip(row_y, nan_ind)
                          if not mask]
        x_hyst_filtered.append(filtered_row_x)
        y_hyst_filtered.append(filtered_row_y)

    par = hyst_analysis(
        x_hyst_filtered, y_hyst_filtered, best_loop,
        dict_pha['counterclockwise'], dict_pha['grounded tip'],
        dict_str=dict_str, infl_threshold=user_pars['inf thresh'],
        sat_threshold=user_pars['sat thresh'], model=user_pars['func'],
        asymmetric=user_pars['asymmetric'], method=user_pars['method'],
        analysis_mode=analysis_mode,
        locked_elec_slope=dict_pha['locked elec slope'],
        make_plots=make_plots)
    best_hyst, props_tot, props_no_bckgnd, figs_hyst = par
    figs += figs_hyst

    for key in ['offset', 'slope', 'ampli_0', 'ampli_1', 'coef_0', 'coef_1',
                'x0_0', 'x0_1']:
        value = best_hyst.params[key].value
        if key in ['ampli_0', 'ampli_1']:
            value = abs(value)
        properties[f'fit pars: {key}'] = value
    for key, value in props_tot.items():
        properties[f'charac tot fit: {key}'] = value
    for key, value in props_no_bckgnd.items():
        properties[f'charac ferro fit: {key}'] = value

    if user_pars['sat mode'] == 'auto':
        sat_domain = [min([props_tot['x sat r'], props_tot['x sat l']]),
                      max([props_tot['x sat r'], props_tot['x sat l']])]
    elif user_pars['sat mode'] == 'set':
        sat_domain = [user_pars['sat domain']['min'],
                      user_pars['sat domain']['max']]
    else:
        raise NotImplementedError("sat domain must be 'auto' or 'set'")
    par = electrostatic_analysis(
        best_loop, analysis_mode=analysis_mode, sat_domain=sat_domain,
        make_plots=make_plots, dict_str=dict_str, read_volt=read_volt,
        bckgnd_tab=bckgnd_tab, func=user_pars['pha func'])
    electrostatic_dict, figs_elec = par
    for key, value in electrostatic_dict.items():
        properties[key] = value
    figs += figs_elec

    return best_loop, properties, other_properties, dict_str, figs


def coupled_analysis(best_loops, offset_off=0.0, limit=None, dict_str=None,
                     make_plots=False):
    """
    Perform differential analysis between on and off field measurements.

    Parameters
    ----------
    best_loops: dict
        Dictionary containing on and off field best nanoloops (MultiLoop or
        MeanLoop).
    offset_off: float, optional
        Offset of off field fit hysteresis (electrostatic constant component).
    limit: dict of float, optional
        Initial values of the write voltage axis range for the differential
        analysis (in V).
    dict_str: dict, optional
        Dictionary used for figure annotation.
    make_plots: bool, optional
        Activation key for figure generation.

    Returns
    -------
    properties: dict
        Dictionary of properties of the pixel (result of coupled analysis).
    figs: list of matplotlib.pyplot.Figure
        Figures of coupled analysis.
    """
    limit = limit or DEFAULT_LIMIT
    figs = []
    _, _, properties, fig = differential_analysis(
        best_loops['on'], best_loops['off'], offset_off=offset_off,
        bias_min=limit['min'], bias_max=limit['max'], dict_str=dict_str,
        make_plots=make_plots)

    if make_plots:
        figs.append(fig)
        fig = plot_nanoloop_on_off(
            best_loops['on'], best_loops['off'], dict_str=dict_str)
        figs.append(fig)

    return properties, figs


def single_script(tab_path_in, user_pars, meas_pars, sign_pars, cont=1,
                  limit=None, test_dicts=None, make_plots=False, verbose=False):
    """
    Data analysis of a measurement file (i.e., a pixel).

    Parameters
    ----------
    tab_path_in: list of str
        List of mode-specific text files containing loop data for a pixel.
    user_pars: dict
        User-defined parameters for the treatment.
    meas_pars: dict
        Measurement parameters.
    sign_pars: dict
        SSPFM bias signal parameters.
    cont: int, optional
        Index of the corresponding files.
    limit: dict, optional
        Initial values of the write voltage axis range for differential
        analysis (in V).
    test_dicts: dict, optional
        Dictionary used for testing the function with corresponding parameters.
    make_plots: bool, optional
        Activation key for figure generation.
    verbose: bool, optional
        Activation key for verbosity.

    Returns
    -------
    best_loops: dict
        Best loops depending on analysis mode.
    properties: dict
        Measurements of the pixel (result of single script analysis).
    other_properties: dict
        Other properties about the segment (topography, mechanical measurement).
    figs: list of matplotlib.pyplot.Figure
        Figures of single and coupled analysis.
    """
    best_loops = {'on': [], 'off': []}
    figs, add_str, dict_str, properties, other_properies = [], '', '', {}, {}

    for sub_cont, file_path_in in enumerate(tab_path_in):
        file_name_in = os.path.split(file_path_in)[1]
        mode = file_name_in.split('_')[0]
        analysis_mode = gen_analysis_mode(
            mode, read_mode=sign_pars['Mode (R)'])
        if sub_cont == 1:
            add_str = 'b'

        if verbose:
            print(f' - file n°{cont + 1}{add_str}: {file_name_in}')
            if cont == 0:
                print(f'\tanalysis mode: {analysis_mode}')

        test_dict = test_dicts[cont * 2 + sub_cont] if test_dicts else None

        par = single_analysis(
            file_path_in, user_pars, meas_pars, sign_pars,
            analysis_mode=analysis_mode, cont=cont, test_dict=test_dict,
            make_plots=make_plots)

        best_loops[mode], properties[mode], other_properies[mode], dict_str, \
            single_figs = par
        figs.extend(single_figs)

    if add_str == 'b':
        elec_offset = get_setting('electrostatic_offset')
        offset_off = properties['off']['charac tot fit: y shift'] \
            if elec_offset else 0
        par = coupled_analysis(
            best_loops, offset_off=offset_off, limit=limit, dict_str=dict_str,
            make_plots=make_plots)
        properties['coupled'], coupled_figs = par
        figs.extend(coupled_figs)

    return best_loops, properties, other_properies, figs


def multi_script(user_pars, dir_path_in, meas_pars, sign_pars,
                 test_dicts=None, verbose=False, show_plots=False, save=False,
                 root_out=None, dir_path_out_fig=None,
                 dir_path_out_props=None, dir_path_out_best_loops=None):
    """
    Data analysis of txt files list in a directory by using single script
    for each file.

    Parameters
    ----------
    user_pars: dict
        Dictionary of all user parameters for the treatment.
    dir_path_in: str
        Path of the txt loop files directory (in).
    meas_pars: dict
        Dictionary of measurement parameters.
    sign_pars: dict
        Dictionary of sspfm bias signal parameters.
    test_dicts: list(n), optional
        List of dictionaries used for testing the function with corresponding
        parameters.
    verbose: bool, optional
        Activate verbosity.
    show_plots: bool, optional
        Activate figure plotting.
    save: bool, optional
        Activate saving of text measurements.
    root_out: str, optional
        Path of saving directory for sspfm analysis (out).
    dir_path_out_fig: str, optional
        Path of the saving directory for figures.
    dir_path_out_props: str, optional
        Path of the saving directory for txt properties.
    dir_path_out_best_loops: str, optional
        Path of the saving directory for best loops.
    """
    if root_out is None:
        root_out, _ = os.path.split(dir_path_in)

    if save:
        if not os.path.isdir(root_out):
            os.makedirs(root_out)
        figures_folder_name = get_setting('default_figures_folder_name')
        dir_path_out_fig = dir_path_out_fig or os.path.join(
            root_out, figures_folder_name)
        if not os.path.isdir(dir_path_out_fig):
            os.makedirs(dir_path_out_fig)

    if test_dicts is not None:
        file_paths_in = [[] for _ in range(int(len(test_dicts) / 2))]
        modes = []
        for elem in test_dicts:
            if elem['mode'] not in modes:
                modes.append(elem['mode'])
        for i, file_path_in in enumerate(file_paths_in):
            for mode in modes:
                file_path_in.append(f'{mode}_f_file{i + 1}.txt')

    else:
        file_paths_in = generate_file_nanoloop_paths(dir_path_in)

    if verbose:
        print('\nSingle script analysis in progress ...')
        print('Single script for:')

    all_properties = {'on': {}, 'off': {}, 'coupled': {}}
    tab_best_loops = {'on': [], 'off': []}
    if user_pars['diff mode'] == 'auto':
        write_range = sign_pars['Max volt (W) [V]'] - \
                      sign_pars['Min volt (W) [V]']
        write_fraction = write_range / DEFAULT_FRACTION_LIMIT
        limit = {'min': sign_pars['Min volt (W) [V]'] + write_fraction,
                 'max': sign_pars['Max volt (W) [V]'] - write_fraction}
    else:
        limit = user_pars['diff domain']
    make_plots = bool(show_plots or save)
    _, properties, other_properties, figs = single_script(
        file_paths_in[0], user_pars, meas_pars, sign_pars, cont=0, limit=limit,
        test_dicts=test_dicts, make_plots=make_plots, verbose=verbose)
    print_plots(figs, save_plots=save, show_plots=show_plots,
                dirname=dir_path_out_fig, transparent=False)

    for key, value in properties.items():
        all_properties[key] = {sub_key: [] for sub_key in value}
        all_properties['other'] = {key: [] for key in
                                   list(other_properties.values())[0].keys()}

    if user_pars["main_elec_file_path"]:
        main_elec_tab = extract_main_elec_tab(user_pars["main_elec_file_path"])
        tab_user_pars = []
        for revert_val in main_elec_tab:
            user_pars_copy = {
                key: (bool(int(revert_val) == 1))
                if key == "main elec" else value
                for key, value in user_pars.items()}
            tab_user_pars.append(user_pars_copy)
    else:
        main_elec_tab = None
        tab_user_pars = None

    # Multi processing mode
    multiproc = get_setting("multi_processing")
    if multiproc:
        from PySSPFM.utils.core.multi_proc import run_multi_proc_s2

        common_args = {
            "user_pars": user_pars,
            "meas_pars": meas_pars,
            "sign_pars": sign_pars,
            "cont": 1,
            "limit": None,
            "test_dicts": None,
            "make_plots": False,
            "verbose": verbose
        }
        if user_pars["main_elec_file_path"] is not None:
            common_args = {
                key: value for key, value in common_args.items()
                if not key == "user_pars"}
        res = run_multi_proc_s2(file_paths_in, tab_user_pars, common_args,
                                processes=16)
        (list_best_loops, list_properties, list_other_properties) = res
        for elem_best_loops, elem_properties, elem_other_properties in \
                zip(list_best_loops, list_properties, list_other_properties):
            for key, value in elem_properties.items():
                for sub_key, sub_value in value.items():
                    all_properties[key][sub_key].append(sub_value)
            for key, value in list(elem_other_properties.values())[0].items():
                all_properties['other'][key].append(value)
            for key, value in elem_best_loops.items():
                tab_best_loops[key].append(value)

    # Mono processing mode
    else:
        for cont, tab_path_in in enumerate(file_paths_in):
            if user_pars["main_elec_file_path"] is not None:
                user_pars["main elec"] = main_elec_tab[cont]
            best_loops, properties, other_properties, _ = single_script(
                tab_path_in, user_pars, meas_pars, sign_pars, cont=cont,
                test_dicts=test_dicts, verbose=verbose)
            for key, value in properties.items():
                for sub_key, sub_value in value.items():
                    all_properties[key][sub_key].append(sub_value)
            for key, value in list(other_properties.values())[0].items():
                all_properties['other'][key].append(value)
            for key, value in best_loops.items():
                tab_best_loops[key].append(value)
            plt.close('all')

    dim_pix = {'x': meas_pars['Grid x [pix]'],
               'y': meas_pars['Grid y [pix]']}
    dim_mic = {'x': meas_pars['Grid x [um]'],
               'y': meas_pars['Grid y [um]']}

    if save:
        properties_folder_name = get_setting('default_properties_folder_name')
        dir_path_out_props = dir_path_out_props or os.path.join(
            root_out, properties_folder_name)
        best_nanoloops_folder_name = \
            get_setting('default_best_nanoloop_folder_name')
        dir_path_out_best_loops = dir_path_out_best_loops or os.path.join(
            root_out, best_nanoloops_folder_name)
        save_best_nanoloops(tab_best_loops, dir_path_out_best_loops)
        save_properties(all_properties, dir_path_out_props, dim_pix=dim_pix,
                        dim_mic=dim_mic)


def main_script(user_pars, dir_path_in, verbose=False, show_plots=False,
                save=False, root_out=None):
    """
    Root function that orchestrates the script and calls other functions.

    Parameters
    ----------
    user_pars : dict
        Dictionary of user parameters for the treatment.
    dir_path_in : str
        Directory containing input text loop files.
    verbose : bool, optional
        Activate verbosity.
    show_plots : bool, optional
        Activate figure plotting.
    save : bool, optional
        Activate saving of text measurements.
    root_out : str, optional
        Path of the directory for saving sspfm analysis results.

    Returns
    -------
    str
        The output directory used for the analysis.
    """
    # Multi Script
    if verbose:
        print('\n############################################')
        print('\nanalysis in progress ...\n')

    if root_out is None:
        root_out, _ = os.path.split(dir_path_in)

    meas_pars, sign_pars = csv_meas_sheet_extract(root_out)

    multi_script(user_pars, dir_path_in, meas_pars, sign_pars,
                 verbose=verbose, show_plots=show_plots, save=save)

    # Ending
    if verbose:
        print('\n############################################\n')
        for _ in range(3):
            print('\n.')
            time.sleep(1)
        print('\n\nData analysis completed successfully!')
        print('############################################\n')

    return root_out


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)

    - func: algebraic func
        Function used for hysteresis fit.
        This parameter specifies the algebraic function used to fit
         hysteresis branches.
        sigmoid or arctan
    - method: str
        Method used for the fit.
        This parameter specifies the fitting method used for the analysis.
        'leastsq' or 'least_square' (faster but harder to converge) or
        'nelder' (vice versa)
    - asymmetric: bool
        Asymmetric Hysteresis Fit
        This parameter determines whether an asymmetric fit of hysteresis
        should be performed. An asymmetric fit allows each branch of the
         hysteresis curve to have a different slope coefficient.
    - inf_thresh: float
        Inflection Point Threshold
        This parameter defines the threshold, expressed as a percentage of
        the hysteresis amplitude, used to calculate the value of the
        inflection point at the beginning of the hysteresis switch.
    - sat_thresh: float
        Saturation Point Threshold
        This parameter defines the threshold, expressed as a percentage of
        the hysteresis amplitude, used to calculate the value of the
        saturation point at the end of the hysteresis switch.
    - del_1st_loop: bool
        Delete First Loop
        If this parameter is set to True, it deletes the first loop of the
        analysis, which is typically used for calculating the mean hysteresis.
        This can be useful when the first write voltage values are equal to
        zero, indicating that the material is in a pristine state, and the
        loop shape would be different from the polarized state.
        Deleting the first loop helps to avoid artifacts in the analysis.
    - pha_corr: str
        Phase Correction Mode
        This parameter specifies the correction mode for the value of the
        phase nanoloop. There are four possible correction modes:
        - 'raw': No correction is applied.
        - 'offset': Offset correction is applied.
        - 'affine': Affine correction is applied.
        - 'up_down': Phase is set to the up value or down value.
    - pha_fwd: float
        Phase Forward Target Value
        This parameter represents the target value for the phase in the
        forward direction. It is used to generate a multiplied coefficient
        equal to 1 between amplitude and piezoresponse.
    - pha_rev: float
        Phase Reverse Target Value
        This parameter represents the target value for the phase in the
        reverse direction. It is used to generate a multiplied coefficient
        equal to -1 between amplitude and piezoresponse.
    - pha_func: algebraic func
        Piezoresponse Function
        This parameter represents the function used to determine the
        piezoresponse from amplitude and phase.
        The piezoresponse (PR) is calculated as PR = amp * func(pha),
        where 'amp' is the amplitude and 'pha' is the phase.
        Value: Algebraic function (np.cos or np.sin)
    - main_elec_file_path: str
        Path of Boolean Values for Dominant Electrostatics in On Field Mode
        for Each File
        This parameter contains the path of boolean value for dominant
        electrostatics in on field mode for each file. It determines whether
        the electrostatics are higher than ferroelectric effects. In other
        words, it indicates if the electrostatics are responsible for the
        phase loop's sense of rotation in the On Field mode.
        If None, the value will be determined with 'main_elec' parameter.
    - main_elec: bool
        Dominant Electrostatics in On Field Mode
        It determines whether the electrostatics are higher than
        ferroelectric effects. In other words, it indicates if the
        electrostatics are responsible for the phase loop's sense of
        rotation in the On Field mode.
        Active if "phase_file_path" parameters is None and if On Field mode is
        selected.
    - locked_elec_slope: str
        Locked Electrostatic Slope
        It specifies and locks the sign of the electrostatic slope in
        the loop whatever measurement parameters
        (theory: grounded tip: negative, bottom: positive).
        Value: 'negative', 'positive', or None
        Active if On Field mode is selected.
    - diff_mode: str
        Differential Analysis Mode
        This parameter determines the mode for conducting differential
        analysis, which helps in identifying the linear part of the
        differential loop. The specific mode can be set by the user or
        determined automatically.
        Possible values:
        - 'set': User-defined differential domain in the diff_domain parameter.
        - 'auto': Automatic calculation.
        Active if: Differential mode is selected.
    - diff_domain: dict
        Voltage Range for Linear Differential Component
        This parameter defines the voltage range considered for the linear part
        of the differential component. It specifies the voltage range for
        differential analysis.
        If left empty or set to None, no limit is applied.
        Active if: Differential mode is selected.
    - sat_mode: str
        Saturation Electrostatic Analysis Mode
        This parameter determines the mode for analyzing the saturation
        electrostatic component, which defines the saturation domain of the
        loop.
        Possible values:
        - 'set': User-defined saturation domain in the sat_domain parameter.
        - 'auto': Automatic calculation from hysteresis fit.
        Active if: On Field mode is selected.
    - sat_domain: dict
        Voltage Range for Saturation Electrostatic Analysis
        This parameter sets the voltage range for the saturation part of
        hysteresis loop.
        If left empty or set to None, the limit is not considered.
        Active if: On Field mode is selected and saturation mode is set to
        'set'.

    - dir_path_in: str
        Directory path for text loop files generated after the first step of
        the analysis (default: 'nanoloops')
        This parameter specifies the directory path where the text loop files
        generated after the first step of the analysis are located
    - root_out: str
        Saving directory for the result of analysis (out).
        If None saving folder created automatically as
        'title_meas'_'yyyy-mm-dd-HHhMMm'_out_'mode' in the same root
    - verbose: bool
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.
    - show_plots: bool
        Activation key for generating matplotlib figures during analysis.
        This parameter serves as an activation key for generating
        matplotlib figures during the analysis process.
    - save: bool
        Activation key for saving results of the analysis.
        This parameter serves as an activation key for saving results
        generated after the analysis process.
    """
    if get_setting("extract_parameters") in ['json', 'toml']:
        config_params, fname_json = get_config(__file__, fname_json)
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_max\nanoloops
        root_out = None
        # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_max
        config_params = {
            "dir_path_in": dir_path_in,
            "root_out": root_out,
            "verbose": True,
            "show_plots": True,
            "save": True,
            "user_pars": {
                "func": "sigmoid",
                "method": "least_square",
                "asymmetric": False,
                "inf thresh": 10,
                "sat thresh": 90,
                "del 1st loop": True,
                "pha corr": "raw",
                "pha fwd": 0,
                "pha rev": 180,
                "pha func": "np.cos",
                "main_elec_file_path": None,
                "main elec": True,
                "locked elec slope": None,
                "diff mode": "set",
                "diff domain": {
                    "min": -5.0,
                    "max": 5.0
                },
                "sat mode": "set",
                "sat domain": {
                    "min": -9.0,
                    "max": 9.0
                }
            }
        }
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return config_params['user_pars'], config_params['dir_path_in'], \
        config_params['root_out'], config_params['verbose'], \
        config_params['show_plots'], config_params['save'], fname_json, \
        config_params


def main(fname_json=None):
    """
    Main function for data analysis.

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)
    """
    # Extract parameters
    res = parameters(fname_json=fname_json)
    (user_pars, dir_path_in, root_out, verbose, show_plots, save, fname_json,
     config_params) = res
    # Main function
    root_out = main_script(user_pars, dir_path_in, verbose=verbose,
                           show_plots=show_plots, save=save, root_out=root_out)
    # Save parameters
    if save:
        if get_setting("extract_parameters") in ['json', 'toml']:
            copy_json_res(fname_json, root_out, verbose=verbose)
        else:
            create_json_res(config_params, root_out,
                            fname="nanoloop_to_hyst_s2_params.json",
                            verbose=verbose)


if __name__ == '__main__':
    main()
