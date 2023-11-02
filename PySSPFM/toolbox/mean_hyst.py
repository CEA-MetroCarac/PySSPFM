"""
--> Executable Script
Perform mean of hysteresis nanoloops (on / off / coupled) by reading a
certain set of txt file nanoloops defined by the user
The set of files can be chosen manually or with a mask application of a chosen
condition on a chosen reference property
Inspired by: Kelley et al. "Ferroelectricity in Hafnia Controlled via Surface
Electrochemical State". 10.48550/arXiv.2207.12525
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop.file import extract_nanoloop_data
from PySSPFM.utils.nanoloop.analysis import nanoloop_treatment, MeanLoop
from PySSPFM.utils.nanoloop.phase import gen_dict_pha
from PySSPFM.utils.map.main import gen_mask_ref, plot_and_save_maps
from PySSPFM.utils.nanoloop_to_hyst.file import \
    generate_file_nanoloop_paths, print_parameters, extract_properties
from PySSPFM.utils.nanoloop_to_hyst.plot import plot_differential_analysis
from PySSPFM.utils.nanoloop_to_hyst.analysis import gen_analysis_mode
from PySSPFM.utils.nanoloop_to_hyst.electrostatic import \
    gen_differential_loop, linreg_differential
from PySSPFM.utils.nanoloop_to_hyst.analysis import \
    find_best_nanoloop, hyst_analysis, electrostatic_analysis
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def single_script(file, user_pars, meas_pars, sign_pars,
                  analysis_mode='mean_loop'):
    """
    Find the best nanoloop for a single considered txt nanoloop file

    Parameters
    ----------
    file: str
        Path of the single considered file (txt nanoloop save) (in)
    user_pars: dict
        All user parameters for the treatment
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        sspfm bias signal parameters
    analysis_mode: str, optional
        Operating mode for the reader: three possible modes:
        - 'on_f_loop' for on-field measurement
        - 'mean_loop' for off-field measurement with a constant value of
        read voltage
        - 'multi_loop' for off-field measurement with different values of
        read voltage

    Returns
    -------
    best_loop: loop (MultiLoop or MeanLoop) object
        Best nanoloop depending on the analysis mode
    dict_str: dict
        Used for figure annotation
    """
    assert analysis_mode in ['multi_loop', 'mean_loop', 'on_f_loop']

    data_dict, dict_str = extract_nanoloop_data(file)

    dict_pha = gen_dict_pha(meas_pars, user_pars['pha corr'],
                            pha_fwd=user_pars['pha fwd'],
                            pha_rev=user_pars['pha rev'],
                            func=user_pars['pha func'],
                            main_elec=user_pars['main elec'],
                            locked_elec_slope=user_pars['locked elec slope'])

    loop_tab, _, _ = nanoloop_treatment(
        data_dict, sign_pars, dict_pha=dict_pha, dict_str=dict_str,
        q_fact=meas_pars['Q factor'])
    _, _, best_loop, _, _ = find_best_nanoloop(
        loop_tab, dict_pha['counterclockwise'],
        grounded_tip=dict_pha['grounded tip'], analysis_mode=analysis_mode,
        del_1st_loop=user_pars['del 1st loop'], model=user_pars['func'],
        asymmetric=user_pars['asymmetric'], method=user_pars['method'],
        locked_elec_slope=user_pars['locked elec slope'])

    return best_loop, dict_str


def find_best_nanoloops(user_pars, mask, mode='off', verbose=False):
    """
    Find the best nanoloops for all considered txt loop files

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    mask: list(n) of int
        List of index for mask
    mode: str, optional
        Type of measurement mode: 'on', 'off', 'coupled'
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    best_loops: list(m) of loop (MultiLoop or MeanLoop) object
        List of best loops depending on the analysis mode
    analysis_mode: str
        Operating mode for the reader: three possible modes:
        - 'on_f_loop' for on-field measurement
        - 'mean_loop' for off-field measurement with a constant value of
        read voltage
        - 'multi_loop' for off-field measurement with different values of
        read voltage
    dict_str: dict
        Used for figure annotation
    """
    res = print_parameters(user_pars['file path in pars'])
    meas_pars, sign_pars, _, _, _ = res

    file_paths_in = generate_file_nanoloop_paths(
        user_pars['dir path in loop'], mode=f'{mode}_f')
    file_paths_in_sel = [path[0] for cont, path in enumerate(file_paths_in)
                         if cont not in mask]
    analysis_mode = gen_analysis_mode(mode=mode,
                                      read_mode=sign_pars['Mode (R)'])

    best_loops, dict_str = [], None
    for cont, file_path_in in enumerate(file_paths_in_sel):
        file_name_in = os.path.split(file_path_in)[1]
        if verbose:
            if cont == 0:
                print(f'\tanalysis mode: {analysis_mode}')
            print(f' - file n°{cont + 1}: {file_name_in}')
        best_loop, dict_str = single_script(
            file_path_in, user_pars, meas_pars, sign_pars,
            analysis_mode=analysis_mode)
        best_loops.append(best_loop)

    return best_loops, analysis_mode, dict_str


def mean_analysis_on_off(user_pars, best_loops, analysis_mode='mean_loop',
                         dict_str=None, make_plots=False):
    """
    Compute the mean of all loops (on or off field) and perform analysis (
    fit...) on it

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    best_loops: list(m) of loop (MultiLoop or MeanLoop) object
        List of best loops depending on analysis mode
    analysis_mode: str, optional
        Operating mode for the reader: three possible modes:
        - 'on_f_loop' for on-field measurement
        - 'mean_loop' for off-field measurement with a constant value of read
        voltage
        - 'multi_loop' for off-field measurement with different values of
        read voltage
    dict_str: dict, optional
        Dict used for figure annotation
    make_plots: bool, optional
        Activation key for figures generation

    Returns
    -------
    mean_best_loop: MultiLoop or MeanLoop object
        Mean best MultiLoop or MeanLoop object
    mean_best_hyst: Hysteresis object
        Mean best Hysteresis object
    figures: list(p) of Matplotlib figures
    """
    figures = []

    # Compute the mean of all best_loops
    mean_best_loop = MeanLoop(best_loops, del_1st_loop=False)

    x_hyst = [np.array(mean_best_loop.write_volt_right),
              np.array(mean_best_loop.write_volt_left)]
    y_hyst = [np.array(mean_best_loop.piezorep_right),
              np.array(mean_best_loop.piezorep_left)]

    res = print_parameters(user_pars['file path in pars'])
    meas_pars, _, _, _, _ = res
    dict_pha = gen_dict_pha(meas_pars, user_pars['pha corr'],
                            pha_fwd=user_pars['pha fwd'],
                            pha_rev=user_pars['pha rev'],
                            func=user_pars['pha func'],
                            main_elec=user_pars['main elec'],
                            locked_elec_slope=user_pars['locked elec slope'])

    res = hyst_analysis(x_hyst, y_hyst, mean_best_loop,
                        dict_pha['counterclockwise'], dict_pha['grounded tip'],
                        dict_str=dict_str,
                        infl_threshold=user_pars['inf thresh'],
                        sat_threshold=user_pars['sat thresh'],
                        model=user_pars['func'],
                        asymmetric=user_pars['asymmetric'],
                        method=user_pars['method'],
                        analysis_mode=analysis_mode,
                        locked_elec_slope=user_pars['locked elec slope'],
                        make_plots=make_plots)

    (mean_best_hyst, props_tot, props_no_bckgnd, hyst_figs) = res
    figures += hyst_figs

    props = {}
    for key, value in zip(
            ['offset', 'slope', 'ampli_0', 'ampli_1', 'coef_0', 'coef_1',
             'x0_0', 'x0_1'], mean_best_hyst.params):
        props[f'fit pars: {key}'] = value
    for key, value in props_tot.items():
        props[f'charac tot fit: {key}'] = value
    for key, value in props_no_bckgnd.items():
        props[f'charac ferro fit: {key}'] = value

    if user_pars['sat mode'] == 'auto':
        sat_domain = [min([props_tot['x sat r'], props_tot['x sat l']]),
                      max([props_tot['x sat r'], props_tot['x sat l']])]
    elif user_pars['sat mode'] == 'set':
        sat_domain = [user_pars['sat domain']['min'],
                      user_pars['sat domain']['max']]
    else:
        raise NotImplementedError("sat domain must be 'auto' or 'set'")
    res = electrostatic_analysis(mean_best_loop, analysis_mode=analysis_mode,
                                 sat_domain=sat_domain,
                                 make_plots=make_plots, dict_str=dict_str,
                                 func=user_pars['pha func'])
    (electrostatic_dict, figs_elec) = res
    for key, value in electrostatic_dict.items():
        props[key] = value
    figures += figs_elec

    return mean_best_loop, mean_best_hyst, figures


def mean_analysis_coupled(best_loops, bias_min=-5., bias_max=5.,
                          selected_offsets_off=None, make_plots=False):
    """
    Compute the mean of all coupled loops and perform coupled analysis on it

    Parameters
    ----------
    best_loops: dict(2) (on and off field) of list(m) of (MultiLoop or MeanLoop)
        Dict of on and off field best loops depending on analysis mode
    bias_min: float, optional
        Initial minimum value of write voltage axis range for the differential
        analysis (in V)
    bias_max: float, optional
        Initial maximum value of write voltage axis range for the differential
        analysis (in V)
    selected_offsets_off: list, optional
        List of off field hysteresis offset for selected best loops
    make_plots: bool, optional
        Activation key for figures generation

    Returns
    -------
    mean_diff_piezorep: list(q) of float
        List of mean differential piezoresponse
    fit_res: tuple(5)
        Result of linear regression of mean differential piezoresponse
    figures: list(1) of Matplotlib figure
    """
    figure, all_diff_piezorep_left, all_diff_piezorep_right = [], [], []
    write_volt_left, write_volt_right = [], []

    for cont, (best_loop_on, best_loop_off) in \
            enumerate(zip(best_loops['on'], best_loops['off'])):
        if selected_offsets_off is not None:
            offset_off = selected_offsets_off[cont]
        else:
            offset_off = 0.0
        res = gen_differential_loop(
            best_loop_on, best_loop_off, offset_off=offset_off)
        (write_volt_left, diff_piezorep_left, write_volt_right,
         diff_piezorep_right, _) = res
        all_diff_piezorep_left.append(diff_piezorep_left)
        all_diff_piezorep_right.append(diff_piezorep_right)

    mean_diff_piezorep_left = np.mean(np.array(all_diff_piezorep_left), axis=0)
    mean_diff_piezorep_right = np.mean(np.array(all_diff_piezorep_right),
                                       axis=0)

    mean_diff_piezorep = []
    for elem_left, elem_right in zip(np.flip(mean_diff_piezorep_left),
                                     mean_diff_piezorep_right):
        mean_diff_piezorep.append(np.mean([elem_left, elem_right]))

    mean_piezorep_grad = np.gradient(mean_diff_piezorep, write_volt_right)

    res = linreg_differential(
        write_volt_right, mean_diff_piezorep, bias_min, bias_max)
    (_, _, fit_res) = res
    (a_diff, y_0_diff, _, r_square, diff_fit) = fit_res

    figures = []
    if make_plots:
        figure = plot_differential_analysis(
            write_volt_left, write_volt_right, diff_fit,
            mean_diff_piezorep_left, mean_diff_piezorep_right,
            mean_diff_piezorep, mean_piezorep_grad, a_diff, y_0_diff, r_square,
            bias_min=bias_min, bias_max=bias_max)
        figures += [figure]

    return mean_diff_piezorep, fit_res, figures


def main_mean_hyst(user_pars, verbose=False, make_plots=False):
    """
    Main function used for mean loop analysis

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Activation key for figures generation

    Returns
    -------
    Figures or data of analysis result
    """
    assert os.path.exists(user_pars['dir path in prop']), \
        f"{user_pars['dir path in prop']} doesn't exist"
    assert os.path.exists(user_pars['dir path in loop']), \
        f"{user_pars['dir path in loop']} doesn't exist"
    assert os.path.exists(user_pars['file path in pars']), \
        f"{user_pars['file path in pars']} doesn't exist"
    figures = []
    mode = user_pars['mode']
    mask, mask_pars = user_pars['mask']['man mask'], user_pars['mask']
    lab_dict = {'on': ['on_f', 'y', 'On Field'],
                'off': ['off_f', 'w', 'Off Field'],
                'coupled': ['coupled', 'r', 'Coupled']}

    properties, dim_pix, dim_mic = extract_properties(
        user_pars['dir path in prop'])
    mean_best_loop, mean_best_hyst = None, None
    mean_diff_piezorep = []
    fit_res = ()

    if mask is None:
        dict_map = {'label': lab_dict[mode][2], 'col': lab_dict[mode][1]}
        ref_mode = user_pars['mask']['ref']['mode']
        ref = properties[ref_mode][mask_pars['ref']['prop']]
        _, _, mask = gen_mask_ref(
            ref, dim_pix, dim_mic=dim_mic, min_val=mask_pars['ref']['min val'],
            max_val=mask_pars['ref']['max val'],
            mode_man=mask_pars['ref']['interactive'],
            ref_str=mask_pars['ref']["prop"], dict_map=dict_map)

        if make_plots:
            dict_interp = {'fact': user_pars['interp fact'],
                           'func': user_pars['interp func']}
            prop_key = {'mode': ref_mode, 'prop': mask_pars['ref']['prop']}
            full_mask = np.arange(len(ref))
            highlight_pix = [indx for indx in full_mask if indx not in mask]
            fig_map = plot_and_save_maps(
                ref, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp, mask=[],
                prop_str=prop_key['prop'], highlight_pix=highlight_pix)
            figures.append(fig_map)

    if verbose:
        print(f'mask: {mask}')

    if mode in ['on', 'off']:
        res = find_best_nanoloops(user_pars, mask, mode=mode, verbose=verbose)
        best_loops, analysis_mode, dict_str = res
        res = mean_analysis_on_off(user_pars, best_loops, analysis_mode,
                                   dict_str, make_plots=make_plots)
        mean_best_loop, mean_best_hyst, on_off_fig = res
        figures.extend(on_off_fig)

    elif mode == 'coupled':
        best_loops = {}
        for mode_lab in ['on', 'off']:
            res = find_best_nanoloops(
                user_pars, mask, mode=mode_lab, verbose=verbose)
            best_loops[mode_lab], analysis_mode, dict_str = res
        offsets_off = properties['off']['charac tot fit: y shift']
        selected_offsets_off = [val for cont, val in enumerate(offsets_off) if
                                cont not in mask]
        elec_offset = get_setting('elec offset')
        selected_offsets_off = selected_offsets_off if elec_offset else None
        res = mean_analysis_coupled(
            best_loops,
            bias_min=user_pars['diff domain']['min'],
            bias_max=user_pars['diff domain']['max'],
            selected_offsets_off=selected_offsets_off, make_plots=make_plots)
        mean_diff_piezorep, fit_res, coupled_fig = res
        figures.extend(coupled_fig)

    else:
        raise IOError("'mode' should be 'on' or 'off' or 'coupled'")

    if make_plots:
        return figures
    elif mode in ['on', 'off']:
        return mean_best_loop, mean_best_hyst
    else:
        return mean_diff_piezorep, fit_res


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - mode: str
        Measurement mode used for analysis.
        This parameter specifies the mode used for analysis.
        Three possible values: 'on,' 'off,' or 'coupled.'
    - man_mask: list
        Manual mask for selecting specific files.
        This parameter is a list of pixel indices.
        - If the list of pixels is empty ( [] ), all files are selected.
        - If the list of pixels is None, the criterion of selection is made
        with the reference property.
        - If the list of pixels is [a, b, c ...], files of index a, b, c [...]
        are not selected.
    - ref: dict
        --> construct a mask with a criterion selection on ref values
        (valid if man_mask is None)
        - mode: str --> mode of reference property chosen
        - prop: str --> reference property chosen
        - min val: float --> minimum value of ref required (if None no minimum
        value criterion) (valid if interactive is False)
        - max val: float --> maximum value of ref required (if None no maximum
        value criterion) (valid if interactive is False)
        - fmt: str --> format of printed value in the map
        - interactive: bool --> if True, user select interactively the criterion
        selection
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
    - main_elec: bool
        Dominant Electrostatics in On Field Mode
        It determines whether the electrostatics are higher than
        ferroelectric effects. In other words, it indicates if the
        electrostatics are responsible for the phase loop's sense of
        rotation in the On Field mode.
        Active if On Field mode is selected.
    - locked_elec_slope: str
        Locked Electrostatic Slope
        It specifies and locks the sign of the electrostatic slope in
        the loop whatever measurement parameters
        (theory: grounded tip: negative, bottom: positive).
        Value: 'negative', 'positive', or None
        Active if: On Field mode is selected.
    - diff_domain: dict
        Voltage Range for Linear Differential Component
        This parameter defines the voltage range considered for the linear part
        of the differential component. It specifies the voltage range for
        differential analysis.
        If left empty or set to None, no limit is applied.
        Active if: coupled mode is selected.
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
    - interp fact: int
        Interpolation factor for sspfm maps interpolation.
        This parameter determines the level of interpolation to be applied to
        SSPFM maps.
        Active if: Mask is built on ref property (i.e. list of pixels is
        None)."
    - interp_func: str
        Interpolation function
        This parameter specifies the interpolation function used for sspfm
        maps interpolation. It can take one of the following values:
        'linear', or 'cubic'.
        Active if: Mask is built on ref property (i.e. list of pixels is
        None)."

    - dir_path_in: str
        Results of analysis directory.
        This parameter specifies the directory containing the results of
        analysis generated after the 1st and 2nd step of the analysis.
        Default: 'title_meas_out_mode'
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - dir_path_in_prop: str
        Properties files directory
        This parameter specifies the directory containing the properties text
        files generated after the 2nd step of the analysis.
        Optional, Default: 'properties'
    - dir_path_in_loop: str
        Txt loop files directory.
        This parameter specifies the directory containing the loop text files
        generated after the 1st step of the analysis.
        Optional, Default: 'nanoloops'
    - file_path_in_pars: str
        Measurement and analysis parameters txt file.
        This parameter specifies the file containing measurement and analysis
        parameters generated after the 2nd step of the analysis.
        Optional, Default: 'parameters.txt'

    - verbose: bool
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.
    - show_plots: bool
        Activation key for generating matplotlib figures during analysis.
        This parameter serves as an activation key for generating
        matplotlib figures during the analysis process.
    - save: bool
        Activation key for saving results of analysis.
        This parameter serves as an activation key for saving results
        generated during the analysis process.
    """
    dir_path_in = tkf.askdirectory()
    # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt
    properties_folder_name = get_setting('properties folder name')
    dir_path_in_prop = os.path.join(dir_path_in, properties_folder_name)
    # dir_path_in_prop = r'...\KNN500n_15h18m02-10-2023_out_dfrt\properties
    nanoloops_folder_name = get_setting('nanoloops folder name')
    dir_path_in_loop = os.path.join(dir_path_in, nanoloops_folder_name)
    # dir_path_in_loop = r'...\KNN500n_15h18m02-10-2023_out_dfrt\nanoloops
    parameters_file_name = get_setting('parameters file name')
    file_path_in_pars = os.path.join(dir_path_in, parameters_file_name)
    # file_path_in_pars = r'...\KNN500n_15h18m02-10-2023_out_dfrt\results\
    # saving_parameters.txt
    dir_path_out = None
    # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
    # mean_loop_2023-10-02-16h38m
    verbose = True
    show_plots = True
    save = False

    user_pars = {'dir path in prop': dir_path_in_prop,
                 'dir path in loop': dir_path_in_loop,
                 'file path in pars': file_path_in_pars,
                 'mode': 'off',
                 'mask': {'man mask': None,
                          'ref': {'prop': 'charac tot fit: area',
                                  'mode': 'off',
                                  'min val': 0.005,
                                  'max val': None,
                                  'fmt': '.2f',
                                  'interactive': False}},
                 'func': 'sigmoid',
                 'method': 'least_square',
                 'asymmetric': False,
                 'inf thresh': 10,
                 'sat thresh': 90,
                 'del 1st loop': True,
                 'pha corr': 'offset',
                 'pha fwd': 0,
                 'pha rev': 180,
                 'pha func': np.cos,
                 'main elec': True,
                 'locked elec slope': None,
                 'diff domain': {'min': -5., 'max': 5.},
                 'sat mode': 'set',
                 'sat domain': {'min': -9., 'max': 9.},
                 'interp fact': 4,
                 'interp func': 'linear'}

    return user_pars, dir_path_in, dir_path_out, verbose, show_plots, save


def main():
    """ Main function for data analysis. """
    figs = []
    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, verbose, show_plots, save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save, dirname="mean_loop", lvl=0,
        create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    figs += main_mean_hyst(
        user_pars, verbose=verbose, make_plots=bool(show_plots or save))
    # Plot figures
    print_plots(figs, show_plots=show_plots, save_plots=save,
                dirname=dir_path_out, transparent=False)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=True)


if __name__ == '__main__':
    main()
