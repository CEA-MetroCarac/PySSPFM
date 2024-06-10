"""
--> Executable Script
Extracts data from a datacube file (SS PFM) and processes it to obtain local
nanoloops of points on the sample surface.
Inspired by the SS_PFM script from Nanoscope, Bruker.
"""

import tkinter.filedialog as tkf
import os
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from PySSPFM.settings import get_setting, get_config
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.core.path_management import \
    get_filenames_with_conditions, sort_filenames
from PySSPFM.utils.raw_extraction import data_extraction, csv_meas_sheet_extract
from PySSPFM.utils.signal_bias import sspfm_time, sspfm_generator, write_vec
from PySSPFM.utils.nanoloop.plot import main_plot
from PySSPFM.utils.nanoloop.file import save_nanoloop_file, sort_nanoloop_data
from PySSPFM.utils.nanoloop.phase import \
    (phase_calibration, gen_dict_pha, phase_offset_determination,
     apply_phase_offset, mean_phase_offset)
from PySSPFM.utils.nanoloop.analysis import AllMultiLoop
from PySSPFM.utils.datacube_to_nanoloop.gen_data import gen_segments
from PySSPFM.utils.datacube_to_nanoloop.plot import \
    (plt_seg_max, plt_seg_fit, plt_seg_stable,  plt_signals, plt_amp, plt_bias,
     amp_pha_map)
from PySSPFM.utils.datacube_to_nanoloop.file import \
    save_parameters, print_params, get_acquisition_time, get_phase_tab_offset
from PySSPFM.utils.datacube_to_nanoloop.analysis import \
    (cut_function, external_calib, SegmentInfo, SegmentSweep,
     SegmentStable, SegmentStableDFRT, extract_other_properties)
mpl.rcParams.update({'figure.max_open_warning': 0})
PHA_CORR = 'offset'
PHA_FWD = 0
PHA_REV = 180
PHA_FUNC = np.cos
MAIN_ELEC = True
LOCKED_ELEC_SLOPE = None
DEL_1ST_LOOP = True


def single_script(user_pars, file_path_in, meas_pars, sign_pars, phase_offset=0,
                  get_phase_offset=False, mode='max', root_out=None,
                  dir_path_out_fig=None, dir_path_out_nanoloops=None,
                  test_dict=None, verbose=False, show_plots=False,
                  save_plots=False, txt_save=False, index=None):
    """
    Data analysis of a measurement file (i.e., a pixel), print the graphs +
    info and save the nanoloop data in a txt file.

    Parameters
    ----------
    user_pars: dict
        Dictionary of all user parameters for the treatment.
    file_path_in: str
        Path of the measurement/csv file (in).
    meas_pars: dict
        Dictionary of measurement parameters.
    sign_pars: dict
        Dictionary of SSPFM bias signal parameters.
    phase_offset: float, optional
        Phase offset to apply to all phase values.
    get_phase_offset: bool, optional
        Key activation to perform analysis and get phase offset from histogram
        of phase segment values.
    mode: str, optional
        Operating mode for analysis: four possible modes:
        - 'max': for analysis of the resonance with max peak value
        (frequency sweep in resonance)
        - 'fit': for analysis of the resonance with a SHO fit of the peak
        (frequency sweep in resonance)
        - 'single_freq': for analysis performed at single frequency,
        average of segment (in or out of resonance)
        - 'dfrt': for analysis performed with dfrt, average of segment
    root_out: str, optional
        Path of the saving directory (out).
    dir_path_out_fig: str, optional
        Path of the saving directory for the figure (out).
    dir_path_out_nanoloops: str, optional
        Path of the saving directory for the txt nanoloops (out).
    test_dict: dict, optional
        Dictionary of test parameters (used for the test of the module).
    verbose: bool, optional
        Activation key for verbosity.
    show_plots: bool, optional
        Activation key for figure visualization.
    save_plots: bool, optional
        Activation key for figure save.
    txt_save: bool, optional
        Activation key for txt nanoloop save.
    index: int, optional
        Index of the measurement file.

    Returns
    -------
    phase_offset_val: dict
        Dictionary containing phase offset data of a single file resulting from
        analysis of histogram of phase segment values. If 'get_phase_offset' is
        False, this value is None.
    """
    assert mode in ['max', 'fit', 'single_freq', 'dfrt']
    assert root_out or (dir_path_out_nanoloops and dir_path_out_fig)
    make_plots = bool(show_plots or save_plots)
    figs = []

    # Extraction of data measurement in measurement file

    # Print the file name
    _, file_name_in = os.path.split(file_path_in)
    add_str = f'n°{index}' if index else ''
    print(f'- measurement file {add_str}: {file_name_in}\n')
    if verbose:
        print('Beginning single-script analysis -------------------------------'
              '-------------------------------------------\n')

    if test_dict is None:
        dict_meas, _ = data_extraction(
            file_path_in, mode_dfrt=bool(mode.lower() == 'dfrt'),
            verbose=verbose)
    else:
        dict_meas = gen_segments(
            sign_pars, mode=mode, seg_noise_pars=test_dict['seg noise'],
            hold_dict=test_dict['hold pars'], loop_pars=test_dict['loop pars'],
            alea_target_range=test_dict['alea target range'])

    # Init and cut measurements
    if sign_pars['Min volt (R) [V]'] == sign_pars['Max volt (R) [V]']:
        sign_pars['Mode (R)'] = 'Single Read Step'
    cut_dict, _ = cut_function(sign_pars)

    # Print SS PFM bias info
    print_params(meas_pars, sign_pars, user_pars, verbose=verbose)

    # Find unit and calculate new amplitude value if a calibration is performed
    calibration = bool(meas_pars['Calibration'].lower == 'yes')
    unit = 'a.u'
    if calibration:
        unit = 'nm'
        dict_meas['amp'] = [elem * meas_pars['Calib fact [nm/V]'] for elem in
                            dict_meas['amp']]

    # Detect on / off field
    if mode in ['dfrt', 'single_freq']:
        on_field_mode, off_field_mode = True, True
    else:
        on_field_mode = bool(sign_pars['Nb meas (W)'] != 0)
        off_field_mode = bool(sign_pars['Nb meas (R)'] != 0)
        freq_ini = sign_pars['Low freq [kHz]']
        freq_end = sign_pars['High freq [kHz]']

    # If measurement are performed from an external source of AFM
    if meas_pars['External meas'].lower() == 'yes':
        par = external_calib(dict_meas['amp'], dict_meas['pha'],
                             meas_pars=meas_pars)
        (dict_meas['amp'], dict_meas['pha']) = par

    # If input phase in radians, convert it in degrees
    rad_phase = get_setting('radians_input_phase')
    if rad_phase:
        dict_meas['pha'] = 360/(2*np.pi)*np.array(dict_meas['pha'])

    # Generate SS PFM signal segment values
    ss_pfm_bias = sspfm_generator(sign_pars)

    # SS PFM signal determination
    par = sspfm_time(ss_pfm_bias, sign_pars)
    (_, ss_pfm_bias_calc) = par

    # Apply offset to all phase values
    if user_pars['pha pars']['method'] is not None:
        dict_meas['pha'] = apply_phase_offset(
            dict_meas['pha'], phase_offset, phase_min=-180, phase_max=180)

    if make_plots:
        fig = plt_bias(ss_pfm_bias_calc, ss_pfm_bias, dict_meas)
        figs.append(fig)

    if len(dict_meas['tip_bias']) < 1:
        dict_meas['tip_bias'] = ss_pfm_bias_calc

    # Plot SS PFM and amplitude signal
    if make_plots:
        fig = plt_amp(dict_meas, unit=unit)
        figs.append(fig)

    # Plot raw signals in time
    if make_plots:
        fig = plt_signals(dict_meas, unit=unit)
        figs.append(fig)

    # Extract other properties in terms of height and deflection
    other_properties = extract_other_properties(
        dict_meas, sign_pars['Hold sample (start)'],
        sign_pars['Hold sample (end)'])
    other_properties["phase offset"] = phase_offset

    # Init parameters
    cut_seg = user_pars['seg pars']['cut seg [%]']
    seg_tab, seg_tab_on_f, seg_tab_off_f = [], [], []
    seg_dict, seg_pars, seg_pars_on, seg_pars_off, phase_offset_val = \
        {}, {}, {}, {}, {}
    filter_type = user_pars['seg pars']['filter type']
    filter_freq_1 = user_pars['seg pars']['filter freq 1'] if \
        filter_type in ['low', 'high', 'bandpass', 'bandstop'] else None
    filter_freq_2 = user_pars['seg pars']['filter freq 2'] if \
        filter_type in ['low', 'high', 'bandpass', 'bandstop'] else None
    if filter_type in ['bandpass', 'bandstop']:
        filter_freq = (filter_freq_1, filter_freq_2)
    elif filter_type in ['low', 'high']:
        filter_freq = np.min([filter_freq_1, filter_freq_2])
    else:
        filter_freq = None
    filter_order = user_pars['seg pars']['filter ord'] if \
        filter_type else None
    if on_field_mode:
        seg_pars_on['index cut'] = cut_dict['on f']
        seg_pars_on['ite'] = sign_pars['Seg sample (W)']
        seg_pars_on['type'] = 'write'
        seg_pars_on['add'] = [0, 0]
        seg_pars_on['title map'] = 'On Field Map'
        seg_pars['On field'] = seg_pars_on
    if off_field_mode:
        seg_pars_off['index cut'] = cut_dict['off f']
        seg_pars_off['ite'] = sign_pars['Seg sample (R)']
        seg_pars_off['type'] = 'read'
        seg_pars_off['add'] = [0, 1]
        seg_pars_off['title map'] = 'Off Field Map'
        seg_pars['Off field'] = seg_pars_off

    # Fill segment list
    for tuple_dict in seg_pars.items():
        seg_tab = []
        if verbose:
            print('Cut performing: ', tuple_dict[0])
        for cont, elem in enumerate(tuple_dict[1]['index cut']):
            # init segment with SegmentInfo
            segment_info = SegmentInfo(
                elem, elem + tuple_dict[1]['ite'], dict_meas['times'],
                write_volt=ss_pfm_bias[cont * 2 + tuple_dict[1]['add'][0]],
                read_volt=ss_pfm_bias[cont * 2 + tuple_dict[1]['add'][1]],
                type_seg=tuple_dict[1]['type'], mode=mode,
                numb=cont * 2 + tuple_dict[1]['add'][1])
            # SegmentSweep
            if mode in ['max', 'fit']:
                method_segment = 'sweep'
                seg_tab.append(SegmentSweep(
                    segment_info, dict_meas,
                    start_freq_init=freq_ini, end_freq_init=freq_end,
                    cut_seg=cut_seg, filter_type=filter_type,
                    filter_cutoff_frequency=filter_freq,
                    filter_order=filter_order,
                    fit_pars=user_pars['fit pars']))
                freq_range = {'start': freq_ini, 'end': freq_end}
            else:
                target_keys = ['amp', 'pha', 'freq',
                               'amp sb_l', 'pha sb_l', 'freq sb_l',
                               'amp sb_r', 'pha sb_r', 'freq sb_r']
                freq_range = None
                flag = bool(all(key in dict_meas for key in target_keys))
                if flag:
                    # SegmentStableDFRT
                    method_segment = 'stable_dfrt'
                    seg_tab.append(SegmentStableDFRT(
                        segment_info, dict_meas, cut_seg=cut_seg,
                        filter_type=filter_type,
                        filter_cutoff_frequency=filter_freq,
                        filter_order=filter_order))
                else:
                    # SegmentStable
                    method_segment = 'stable'
                    seg_tab.append(SegmentStable(
                        segment_info, dict_meas, cut_seg=cut_seg,
                        filter_type=filter_type,
                        filter_cutoff_frequency=filter_freq,
                        filter_order=filter_order))
            # Plot segments
            if cont in (0, len(tuple_dict[1]['index cut']) - 1) and make_plots:
                fig = []
                if mode in ['dfrt', 'single_freq']:
                    fig = plt_seg_stable(seg_tab[cont], unit=unit)
                elif mode == 'fit':
                    if seg_tab[cont].error == '':
                        fig = plt_seg_fit(
                            seg_tab[cont], unit=unit,
                            fit_pha=user_pars['fit pars']['fit pha'])
                else:
                    if seg_tab[cont].error == '':
                        fig = plt_seg_max(seg_tab[cont], unit=unit)
                figs.append(fig)

        # Perform analysis and get phase offset from histogram of phase segment
        # values
        if get_phase_offset:
            phase_offset_val[tuple_dict[0]], _ = \
                phase_offset_determination([seg.pha for seg in seg_tab],
                                           dict_str=None, make_plots=False)
        else:
            phase_offset_val = None

        # Plot segment maps
        if make_plots:
            fig = amp_pha_map(
                seg_tab, dict_meas,
                sign_pars['Hold sample (start)'],
                sign_pars['Hold sample (end)'],
                freq_range=freq_range,
                read_nb_voltages=sign_pars['Nb volt (R)'],
                cut_seg=cut_seg, mapping_label=tuple_dict[1]['title map'],
                unit=unit, mode=mode)
            figs.append(fig)
        seg_dict[tuple_dict[0]] = seg_tab

    for tuple_dict in seg_dict.items():
        if tuple_dict[0] == 'On field':
            seg_tab_on_f = tuple_dict[1]
        if tuple_dict[0] == 'Off field':
            seg_tab_off_f = tuple_dict[1]

    # Init of treatment parameters
    dict_pha = gen_dict_pha(meas_pars, pha_corr=PHA_CORR, pha_fwd=PHA_FWD,
                            pha_rev=PHA_REV, func=PHA_FUNC, main_elec=MAIN_ELEC,
                            locked_elec_slope=LOCKED_ELEC_SLOPE)

    # Generate nanoloops array
    label, col = ['Off field', 'On field'], ['w', 'y']
    loop_tab, pha_calib = [], {}
    for cont_list, seg_tab in enumerate([seg_tab_off_f, seg_tab_on_f]):
        if method_segment in ['sweep', 'stable_dfrt']:
            dict_res = {'Amplitude': [elem.amp for elem in seg_tab],
                        'Phase': [elem.pha for elem in seg_tab],
                        'Res Freq': [elem.res_freq for elem in seg_tab],
                        'Q Fact': [elem.q_fact for elem in seg_tab]}
        else:
            dict_res = {'Amplitude': [elem.amp for elem in seg_tab],
                        'Phase': [elem.pha for elem in seg_tab],
                        'Res Freq': [elem.res_freq for elem in seg_tab],
                        'Sigma Amp': [elem.inc_amp for elem in seg_tab],
                        'Sigma Pha': [elem.inc_pha for elem in seg_tab],
                        'Sigma Res Freq': [elem.inc_res_freq
                                           for elem in seg_tab]}
        par = sort_nanoloop_data(
            ss_pfm_bias, sign_pars['Nb volt (W)'], sign_pars['Nb volt (R)'],
            dict_res, unit=unit)
        (nanoloops, fmt, header) = par

        if make_plots:
            # Phase treatment
            dict_str = {'label': label[cont_list],
                        'col': col[cont_list]}
            par = phase_calibration(nanoloops['Phase'], nanoloops['Write Volt'],
                                    dict_pha, dict_str=dict_str,
                                    make_plots=make_plots)
            (_, pha_calib, figs_1) = par
            for fig in figs_1:
                figs.append(fig)
            # Create list of nanoloops
            read_volt = 0
            (amplitude, phase, res_freq, q_fact, amp_sigma, pha_sigma,
             res_freq_sigma, loop_tab) = [], [], [], [], [], [], [], []
            for i in range(1, sign_pars['Nb volt (R)'] + 1):
                amplitude.append([])
                phase.append([])
                res_freq.append([])
                q_fact.append([])
                amp_sigma.append([])
                pha_sigma.append([])
                res_freq_sigma.append([])
                for cont, elem in enumerate(nanoloops['Index Pix']):
                    if elem == i:
                        amplitude[i - 1].append(nanoloops['Amplitude'][cont])
                        phase[i - 1].append(nanoloops['Phase'][cont])
                        if nanoloops['Res Freq']:
                            res_freq[i - 1].append(nanoloops['Res Freq'][cont])
                        if nanoloops['Q Fact']:
                            q_fact[i - 1].append(nanoloops['Q Fact'][cont])
                        if nanoloops['Sigma Amp']:
                            amp_sigma[i - 1].append(
                                nanoloops['Sigma Amp'][cont])
                        if nanoloops['Sigma Pha']:
                            pha_sigma[i - 1].append(
                                nanoloops['Sigma Pha'][cont])
                        if nanoloops['Sigma Res Freq']:
                            res_freq_sigma[i - 1].append(
                                nanoloops['Sigma Res Freq'][cont])
                        read_volt = nanoloops['Read Volt'][cont]
                write_v = write_vec(sign_pars)
                multi_loop_amp, multi_loop_pha = amplitude[i - 1], phase[i - 1]
                multi_loop_res_freq = res_freq[i - 1] \
                    if nanoloops['Res Freq'] else None
                multi_loop_q_fact = q_fact[i - 1] \
                    if nanoloops['Q Fact'] else None
                multi_loop_amp_sigma = amp_sigma[i - 1] \
                    if nanoloops['Sigma Amp'] else None
                multi_loop_pha_sigma = pha_sigma[i - 1] \
                    if nanoloops['Sigma Pha'] else None
                multi_loop_res_freq_sigma = res_freq_sigma[i - 1] \
                    if nanoloops['Sigma Res Freq'] else None

                loop_tab.append(AllMultiLoop(
                    write_v, multi_loop_amp, multi_loop_pha, pha_calib,
                    read_volt, mode=label[cont_list],
                    res_freq=multi_loop_res_freq, q_fact=multi_loop_q_fact,
                    amp_sigma=multi_loop_amp_sigma,
                    pha_sigma=multi_loop_pha_sigma,
                    res_freq_sigma=multi_loop_res_freq_sigma,
                    q_fact_sigma=None))

        # Save nanoloop data in txt file
        if txt_save:
            save_dict = {'label': label[cont_list],
                         'unit': unit,
                         'mode': mode}
            if dir_path_out_nanoloops is None:
                nanoloops_folder_name = \
                    get_setting('default_nanoloops_folder_name')
                dir_path_out_nanoloops = os.path.join(
                    root_out, nanoloops_folder_name)
            save_nanoloop_file(
                dir_path_out_nanoloops, file_name_in[:-4], nanoloops, fmt,
                header, other_properties, mode=save_dict['label'])
        # Plot loops
        if make_plots:
            plot_dict = {'label': label[cont_list], 'col': col[cont_list],
                         'unit': unit}
            figs_2 = main_plot(loop_tab, pha_calib, dict_str=plot_dict,
                               del_1st_loop=DEL_1ST_LOOP)

            for fig in figs_2:
                figs.append(fig)

    if dir_path_out_fig is None:
        figures_folder_name = get_setting('default_figures_folder_name')
        dir_path_out_fig = os.path.join(root_out, figures_folder_name)
    print_plots(figs, save_plots=save_plots, show_plots=show_plots,
                dirname=dir_path_out_fig, transparent=False)
    plt.close('all')

    return phase_offset_val


def multi_script(user_pars, dir_path_in, meas_pars, sign_pars, mode='max',
                 file_format='.spm', root_out=None, verbose=False, save=False):
    """
    Data analysis of a list of spm files in a directory by using the single
    script for each file and save the parameters in a text file.

    Parameters
    ----------
    user_pars: dict
        Dictionary of all user parameters for the treatment
    dir_path_in: str
        Path of the measurement/csv file directory (in)
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        SSPFM bias signal parameters
    mode: str, optional
        Operating mode for analysis: four possible modes:
        - 'max': for analysis of the resonance with max peak value
        (frequency sweep in resonance)
        - 'fit': for analysis of the resonance with a SHO fit of the peak
        (frequency sweep in resonance)
        - 'single_freq': for analysis performed at single frequency,
        average of segment (in or out of resonance)
        - 'dfrt': for analysis performed with dfrt, average of segment
    file_format: str, optional
        Format of the measurement file analyzed: '.spm' or '.txt'
    root_out: str, optional
        Path of the saving directory (out)
    verbose: bool, optional
        Activation key for verbosity
    save: bool, optional
        If True, save the txt loop and figures

    Returns
    -------
    None
    """
    assert root_out

    # Create the saving folder, init date, starting time and measurement time
    t0, raw_date = time.time(), datetime.now()
    date = raw_date.strftime('%Y-%m-%d %H;%M')
    exp_meas_time = get_acquisition_time(dir_path_in, file_format=file_format)
    get_phase_offset = bool(user_pars["pha pars"]["method"] == "dynamic")

    # Get phase offset list from phase file if filled by user
    phase_file_path = user_pars["pha pars"]["phase_file_path"]
    if phase_file_path is not None:
        phase_tab = get_phase_tab_offset(phase_file_path)
    else:
        phase_tab = None

    # Start single script for each measurement file
    file_names = get_filenames_with_conditions(dir_path_in,
                                               extension=file_format)
    file_names, _, _ = sort_filenames(file_names)
    if 'SS_PFM_bias.txt' in file_names:
        file_names.remove('SS_PFM_bias.txt')
    i = 0

    # Multi processing mode
    multiproc = get_setting("multi_processing")
    if multiproc:
        from PySSPFM.utils.core.multi_proc import run_multi_proc_s1
        file_paths = []
        for file in file_names:
            file_paths.append(os.path.join(dir_path_in, file))
        phase_offset = user_pars["pha pars"]["offset"]
        common_args = {
            "user_pars": user_pars,
            "meas_pars": meas_pars,
            "sign_pars": sign_pars,
            "phase_offset": phase_offset,
            "get_phase_offset": False,
            "mode": mode,
            "root_out": root_out,
            "dir_path_out_fig": None,
            "dir_path_out_nanoloops": None,
            "test_dict": None,
            "verbose": verbose,
            "show_plots": False,
            "save_plots": False,
            "txt_save": save,
            "index": 0}
        if phase_file_path is not None:
            common_args = {key: value for key, value in common_args.items()
                           if not key == "phase_offset"}
        run_multi_proc_s1(file_paths, phase_tab, common_args, processes=16)

    # Mono processing mode
    else:
        for i, elem in enumerate(file_names):
            if elem.endswith(file_format) and not \
                    elem.endswith('SS_PFM_bias.txt'):
                # FInd phase offset value
                if phase_tab is not None:
                    phase_offset = phase_tab[i]
                elif user_pars["pha pars"]["method"] is None:
                    phase_offset = 0
                elif i == 0 or user_pars["pha pars"]["method"] == "static":
                    phase_offset = user_pars["pha pars"]["offset"]
                elif user_pars["pha pars"]["method"] == "dynamic":
                    phase_offset = mean_phase_offset(phase_offset_val)
                else:
                    raise NotImplementedError(
                        "setting 'pha_params' / 'method' should be in "
                        "['static', 'dynamic', None]")
                file_path_in = os.path.join(dir_path_in, elem)
                phase_offset_val = \
                    single_script(user_pars, file_path_in, meas_pars, sign_pars,
                                  phase_offset=phase_offset,
                                  get_phase_offset=get_phase_offset, mode=mode,
                                  root_out=root_out, verbose=verbose,
                                  txt_save=save, index=i+1)

    if save:
        if verbose:
            print('\nSS PFM parameter analysis ...\n')

        # Find number of segment
        _, nb_seg_tot = cut_function(sign_pars)
        meas_pars['nb seg'] = nb_seg_tot

        # Save all the parameters in a text file
        save_parameters(root_out, t0, date, exp_meas_time, user_pars,
                        meas_pars, sign_pars, i)


def main_script(user_pars, file_path_in, verbose=False, show_plots=False,
                save=False, root_out=None):
    """
    Main function that orchestrates the script and calls other functions.

    Parameters
    ----------
    user_pars: dict
        Dictionary of user parameters for data processing
    file_path_in: str
        Path to the Spm or txt datacube sspfm file (in)
    verbose: bool, optional
        Activation key for verbosity
    show_plots: bool, optional
        Activation key for figure visualization
    save: bool, optional
        If True, save the txt loop and figures
    root_out: str, optional
        Root directory for saving output files

    Returns
    -------
    None
    """
    # Single Script
    seg_pars = user_pars['seg pars']
    mode = seg_pars['mode']
    file_format = '.' + file_path_in.split('.')[-1]
    if verbose:
        print('\n############################################')
        print('\nsingle script analysis in progress ...\n')

    dir_path_in = os.path.split(file_path_in)[0]
    meas_pars, sign_pars = csv_meas_sheet_extract(dir_path_in)

    if root_out is None:
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d-%Hh%Mm")
        root_out = dir_path_in + \
            f'_{date_str}_out_{user_pars["seg pars"]["mode"]}'
    if not os.path.isdir(root_out) and save is True:
        os.makedirs(root_out)
    phase_offset = user_pars["pha pars"]["offset"]
    _ = single_script(user_pars, file_path_in, meas_pars, sign_pars,
                      phase_offset=phase_offset, get_phase_offset=False,
                      mode=mode, root_out=root_out, verbose=verbose,
                      show_plots=show_plots, save_plots=save)

    if verbose:
        print('\nsingle script analysis end with success !')
        print('############################################\n')

    # Multi Script
    if verbose:
        print('\n############################################')
        print('\nmulti_script_analysis in progress ...\n')

    multi_script(user_pars, dir_path_in, meas_pars, sign_pars, mode=mode,
                 file_format=file_format, root_out=root_out, save=save)

    if verbose:
        print('\nmulti script analysis end with success !')
        print('############################################\n')

    # Ending
    if verbose:
        print('\n############################################\n')
        for _ in range(3):
            print('\n.')
            time.sleep(1)
        print('\n\nData analysis end with success !')
        print('############################################\n')


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)

    - mode: str
        Treatment Method for Extracting PFM Amplitude and Phase from Segments
        This parameter determines the treatment method used for data analysis.
        It specifies how PFM (Piezoresponse Force Microscopy) amplitude and
        phase data are extracted from segments, as well as how signal
        treatment is performed within the segment.
        Four possible values:
            --> 'max': Peak maximum treatment (frequency sweep in resonance)
            --> 'fit': Peak fit treatment (frequency sweep in resonance)
            --> 'single_freq': Average of segment
            (single frequency, in or out of resonance)
            --> 'dfrt': Average of segment (dfrt)
    - cut_seg_perc: dict('start':, 'end':) of int
        Segment Trimming Percentage
        Description: This parameter specifies the percentage of the segment
        length to be trimmed from both the start and end of the segment.
        It allows you to exclude a certain portion of the segment from analysis
         at the beginning and end (in term of %)
    - filter type: str
        Type of Filter for Measurements
        This parameter specifies the type of filter to be applied to
        the measurements.
        There are six possible values:
            --> 'mean': Apply a Mean filter.
            --> 'low': Apply a Low Butterworth filter.
            --> 'high': Apply a High Butterworth filter.
            --> 'bandpass': Apply a Bandpass Butterworth filter.
            --> 'bandstop': Apply a Bandstop Butterworth filter.
            --> None: Do not apply any filter.
    - filter freq 1: float
        Filter Cutoff Frequency, First Value
        This parameter controls the cutoff frequency in Hz of the filter used.
        Value: Float representing single cutoff frequency value if the filter
        type is "low" or "high", or the first cutoff frequency value if the
        filter type is "bandpass" or "bandstop".
        Active if: This parameter is active when the 'filter type' option is
        neither "mean" nor None.
    - filter freq 2: float
        Filter Cutoff Frequency, Second Value
        This parameter controls the cutoff frequency in Hz of the filter used.
        Value: Float representing second cutoff frequency value if the filter
        type is "bandpass" or "bandstop".
        Active if: This parameter is active when the 'filter type' option is
        either "bandpass" or "bandstop".
    - filter ord: int
        Filter Order
        This parameter controls the order of the filter used. A higher value
        results in stronger filtering of the signal.
        Value: An integer value, with a minimum value of 1.
        Active if: This parameter is active when the 'filter type' option is
        not None.
    - fit pha: bool
        Indicator for Fitting Phase Measurements
        This parameter determines whether phase measurements should undergo
        a fitting process during data processing.
        This parameter is active when the data processing mode is set to 'fit.
    - detect peak: bool
        Peak Detection for Peak Fitting
        This parameter controls the peak detection for segments during
        data processing. When set to True, it enables the detection of segments
        for which there is no peak, and the fitting process is not performed
        for those segments.
       Active if: This parameter is active when the 'fit' mode is selected.
    - sens peak detect: float
        Sensitivity of Peak Detection
        This parameter determines how sensitive the peak detection algorithm
        is. A higher value makes the peak detection process more stringent,
        meaning it will be harder to detect peaks.
        Active if: This parameter is active when the 'fit' mode is selected
        and peak detection is enabled.
    - phase_file_path: str
        Path of Phase Offset List File.
        This parameter contains the path of phase offset list file (On
        Field / Off Field / Mean) associated to each datacube file,
        to be applied to each file.
        If None, phase offset value will be determined with 'static' or
        'dynamic' 'method' parameter.
    - method: str
        Treatment Method for Phase Offset Application on Measurements.
        This parameter determines the treatment method used for phase offset
        application to measurements.
        It specifies how phase offset is performed in analysis.
        Three possible values:
            - 'static': Phase offset value remains constant and is specified
            by the user.
            - 'dynamic': Phase offset value is determined for each file
            through specific phase analysis and is applied to the subsequent
            file (useful for long measurements with phase drift).
            - None: No phase offset processing is performed: raw phase values
            are used for analysis.
        Active if: This parameter is active when "phase_file_path"
        parameters is None.
    - offset: float
        Phase offset value applied to measurements.
        This parameter allows the user to specify a constant phase offset value
        for the analysis, which is applied to all phase values.
        It is used in conjunction with the 'static' treatment method for phase
        offset application on measurements.
        Active if: This parameter is active when "phase_file_path"
        parameters is None. If it's the case, this parameter is active for
        the analysis of the first raw measurement file in all cases, and for
        all raw measurement files when the selected 'method' for phase offset
        analysis is 'static'.

    file_path_in: str
        Path of datacube SSPFM raw file measurements.
        This parameter specifies the path where datacube SSPFM raw file
        measurements are located. It is used to indicate the path to the file
        containing these measurements.
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
        config_params = get_config(__file__, fname_json)
        file_path_in = config_params['file_path_in']
        root_out = config_params['root_out']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = {'seg pars': config_params['seg_params'],
                     'fit pars': config_params['fit_params'],
                     'pha pars': config_params['pha_params']}
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Get file path for single script
        file_path_in = tkf.askopenfilename()
        # file_path_in = r'...\KNN500n\KNN500n.0_00001.spm
        root_out = None
        # root_out = r'...\KNN500n_15h18m02-10-2023_out_max
        verbose = True
        show_plots = True
        save = True
        seg_params = {'mode': 'max',
                      'cut seg [%]': {'start': 5, 'end': 5},
                      'filter type': None,
                      'filter freq 1': 1e3,
                      'filter freq 2': 3e3,
                      'filter ord': 4}
        fit_params = {'fit pha': False,
                      'detect peak': False,
                      'sens peak detect': 1.5}
        pha_params = {'phase_file_path': None,
                      'method': 'static',
                      'offset': 0}
        user_pars = {'seg pars': seg_params,
                     'fit pars': fit_params,
                     'pha pars': pha_params}
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, file_path_in, root_out, verbose, show_plots, save


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
    (user_pars, file_path_in, root_out, verbose, show_plots, save) = res

    # Main function
    main_script(user_pars, file_path_in, verbose=verbose, show_plots=show_plots,
                save=save, root_out=root_out)


if __name__ == '__main__':
    main()
