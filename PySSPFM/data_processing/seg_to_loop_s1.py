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

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.raw_extraction import data_extraction
from PySSPFM.utils.signal_bias import sspfm_time, sspfm_generator, write_vec
from PySSPFM.utils.nanoloop.plot import plot_sspfm_loops
from PySSPFM.utils.nanoloop.file import txt_loop, sort_loop
from PySSPFM.utils.nanoloop.phase import phase_calibration, gen_dict_pha
from PySSPFM.utils.nanoloop.analysis import MultiLoop
from PySSPFM.utils.datacube_to_nanoloop.gen_datas import gen_segments
from PySSPFM.utils.datacube_to_nanoloop.plot import \
    (plt_seg_max, plt_seg_fit, plt_seg_dfrt,  plt_signals, plt_amp, plt_bias,
     amp_pha_map)
from PySSPFM.utils.datacube_to_nanoloop.file import save_txt_file, print_pars
from PySSPFM.utils.raw_extraction import csv_meas_sheet_extract
from PySSPFM.utils.datacube_to_nanoloop.analysis import \
    init_parameters, zi_calib, Segment

mpl.rcParams.update({'figure.max_open_warning': 0})
PHA_CORR = 'offset'
PHA_FWD = 0
PHA_REV = 180
PHA_FUNC = np.cos
MAIN_ELEC = True
LOCKED_ELEC_SLOPE = None
DEL_1ST_LOOP = True


def single_script(user_pars, file_path_in, meas_pars, sign_pars, mode='dfrt',
                  root_out=None, dir_path_out_fig=None,
                  dir_path_out_txt_loops=None, test_dict=None,
                  verbose=False, show_plots=False, save_plots=False,
                  txt_save=False):
    """
    Data analysis of a measurement file (i.e., a pixel), print the graphs +
    info and save the loop data in a txt file.

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
    mode: str, optional
        Operating mode for analysis: three possible modes:
        - 'max' for analysis of the resonance with max peak value.
        - 'fit' for analysis of the resonance with a SHO fit of the peak.
        - 'dfrt' for analysis performed with the dfrt.
    root_out: str, optional
        Path of the saving directory (out).
    dir_path_out_fig: str, optional
        Path of the saving directory for the figure (out).
    dir_path_out_txt_loops: str, optional
        Path of the saving directory for the txt loops (out).
    test_dict: dict, optional
        Dictionary of test parameters (used for the test of the module).
    verbose: bool, optional
        Activation key for verbosity.
    show_plots: bool, optional
        Activation key for figure visualization.
    save_plots: bool, optional
        Activation key for figure save.
    txt_save: bool, optional
        Activation key for txt loop save.

    Returns
    -------
    None
    """
    assert mode in ['max', 'fit', 'dfrt']
    assert root_out or (dir_path_out_txt_loops and dir_path_out_fig)
    make_plots = bool(show_plots or save_plots)
    figs = []

    # Extraction of data measurement in measurement file

    # Print the file name
    _, file_name_in = os.path.split(file_path_in)
    print(f'- measurement file: {file_name_in}\n')
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

    par = init_parameters(dict_meas, sign_pars, verbose=verbose)
    cut_dict, sign_pars['Mode (R)'] = par
    # Print SS PFM bias info
    print_pars(meas_pars, sign_pars, user_pars, verbose=verbose)

    # Find unit and calculate new amplitude value if a calibration is performed
    calibration = bool(meas_pars['Calibration'].lower == 'yes')
    unit = 'a.u'
    if calibration:
        unit = 'nm'
        dict_meas['amp'] = [elem * meas_pars['Calib fact [nm/V]'] for elem in
                            dict_meas['amp']]

    # Detect on / off field
    if mode == 'dfrt':
        on_field_mode, off_field_mode = True, True
        freq_ini, freq_end = 200, 300
        par = zi_calib(dict_meas['amp'], dict_meas['pha'], meas_pars=meas_pars)
        (dict_meas['amp'], dict_meas['pha']) = par
    else:
        on_field_mode = bool(sign_pars['Nb meas (W)'] != 0)
        off_field_mode = bool(sign_pars['Nb meas (R)'] != 0)
        freq_ini = sign_pars['Low freq [kHz]']
        freq_end = sign_pars['High freq [kHz]']

    # Generate SS PFM signal segment values
    ss_pfm_bias = sspfm_generator(sign_pars)

    # SS PFM signal determination
    par = sspfm_time(ss_pfm_bias, sign_pars,
                     start_hold_time=cut_dict['start hold time exp'])
    (time_bias_calc, ss_pfm_bias_calc) = par
    time_bias_calc = np.concatenate([cut_dict['start hold seg'], time_bias_calc,
                                     cut_dict['end hold seg']])
    ss_pfm_bias_calc = \
        np.concatenate([np.zeros(len(cut_dict['start hold seg'])),
                        ss_pfm_bias_calc,
                        np.zeros(len(cut_dict['end hold seg']))])
    if make_plots:
        fig = plt_bias(time_bias_calc, ss_pfm_bias_calc, ss_pfm_bias, dict_meas)
        figs.append(fig)

    if len(dict_meas['tip_bias']) < 1:
        dict_meas['times_bias'] = time_bias_calc
        dict_meas['tip_bias'] = ss_pfm_bias_calc

    # Plot SS PFM and amplitude signal
    if make_plots:
        fig = plt_amp(dict_meas, unit=unit)
        figs.append(fig)

    # Plot raw signals in time
    if make_plots:
        fig = plt_signals(dict_meas, unit=unit)
        figs.append(fig)

    # Init parameters
    cut_seg = user_pars['seg pars']['cut seg [%]']
    seg_tab, seg_tab_on_f, seg_tab_off_f = [], [], []
    seg_dict, seg_pars, seg_pars_on, seg_pars_off = {}, {}, {}, {}
    filter_order = user_pars['seg pars']['filter ord'] if \
        user_pars['seg pars']['filter'] else None
    if on_field_mode:
        seg_pars_on['index cut'] = cut_dict['index on field']
        seg_pars_on['ite'] = sign_pars['Seg sample (W)']
        seg_pars_on['type'] = 'write'
        seg_pars_on['add'] = [0, 0]
        seg_pars_on['title map'] = 'On Field Map'
        seg_pars['On field'] = seg_pars_on
    if off_field_mode:
        seg_pars_off['index cut'] = cut_dict['index off field']
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
            seg_tab.append(Segment(
                elem, elem + tuple_dict[1]['ite'], dict_meas,
                start_freq_init=freq_ini, end_freq_init=freq_end,
                write_volt=ss_pfm_bias[cont * 2 + tuple_dict[1]['add'][0]],
                read_volt=ss_pfm_bias[cont * 2 + tuple_dict[1]['add'][1]],
                type_seg=tuple_dict[1]['type'], mode=mode,
                numb=cont * 2 + tuple_dict[1]['add'][1],
                cut_seg=cut_seg, filter_order=filter_order,
                fit_pars=user_pars['fit pars']))
            # Plot segments
            if cont in (0, len(tuple_dict[1]['index cut']) - 1) and \
                    seg_tab[cont].error == '' and make_plots:
                if mode == 'dfrt':
                    fig = plt_seg_dfrt(seg_tab[cont], unit=unit)
                elif mode == 'fit':
                    fig = plt_seg_fit(seg_tab[cont], unit=unit,
                                      fit_pha=user_pars['fit pars']['fit pha'])
                else:
                    fig = plt_seg_max(seg_tab[cont], unit=unit)
                figs.append(fig)
        # Plot segment maps
        if make_plots:
            fig = amp_pha_map(seg_tab, dict_meas,
                              cut_dict['index hold'],
                              freq_range={'start': freq_ini, 'end': freq_end},
                              read_nb_voltages=sign_pars['Nb volt (R)'],
                              cut_seg=cut_seg,
                              mapping_label=tuple_dict[1]['title map'],
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
        dict_res = {'Amplitude': [elem.amp for elem in seg_tab],
                    'Phase': [elem.pha for elem in seg_tab],
                    'Freq res': [elem.res_freq for elem in seg_tab],
                    'Q fact': [elem.q_fact for elem in seg_tab]}
        par = sort_loop(ss_pfm_bias, sign_pars['Nb volt (W)'],
                        sign_pars['Nb volt (R)'], dict_res, unit=unit)
        (nanoloops, fmt, header) = par

        if make_plots:
            # Phase treatment
            dict_str = {'label': label[cont_list],
                        'col': col[cont_list]}
            par = phase_calibration(nanoloops[4], nanoloops[2], dict_pha,
                                    dict_str=dict_str, make_plots=make_plots)
            (_, pha_calib, figs_1) = par
            for fig in figs_1:
                figs.append(fig)
            # Create list of loops
            read_volt = 0
            amplitude, phase, loop_tab = [], [], []
            for i in range(1, sign_pars['Nb volt (R)'] + 1):
                amplitude.append([])
                phase.append([])
                for cont, elem in enumerate(nanoloops[0]):
                    if elem == i:
                        amplitude[i - 1].append(nanoloops[3][cont])
                        phase[i - 1].append(nanoloops[4][cont])
                        read_volt = nanoloops[1][cont]
                write_v = write_vec(sign_pars)
                loop_tab.append(MultiLoop(write_v, amplitude[i - 1],
                                          phase[i - 1], read_volt, pha_calib,
                                          label[cont_list]))

        # Save loop data in txt file
        if txt_save:
            save_dict = {'label': label[cont_list],
                         'unit': unit,
                         'mode': mode}
            if dir_path_out_txt_loops is None:
                dir_path_out_txt_loops = os.path.join(root_out, 'txt_loops')
            txt_loop(dir_path_out_txt_loops, file_name_in[:-4], nanoloops,
                     fmt, header, mode=save_dict['label'])

        # Plot loops
        if make_plots:
            plot_dict = {'label': label[cont_list], 'col': col[cont_list],
                         'unit': unit}
            figs_2 = plot_sspfm_loops(loop_tab, pha_calib, dict_str=plot_dict,
                                      del_1st_loop=DEL_1ST_LOOP)

            for fig in figs_2:
                figs.append(fig)

    if dir_path_out_fig is None:
        dir_path_out_fig = os.path.join(root_out, 'results', 'figs')
    print_plots(figs, save_plots=save_plots, show_plots=show_plots,
                dirname=dir_path_out_fig, transparent=False)
    plt.close('all')


def multi_script(user_pars, dir_path_in, meas_pars, sign_pars, mode='dfrt',
                 file_format='.spm', root_out=None, dir_path_out_res=None,
                 verbose=False, save=False):
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
        Operating mode for analysis: three possible modes:
        - 'max' for analysis of the resonance with max peak value
        - 'fit' for analysis of the resonance with a SHO fit of the peak
        - 'dfrt' for analysis performed with the dfrt
    file_format: str, optional
        Format of the measurement file analyzed: '.spm' or '.txt'
    root_out: str, optional
        Path of the saving directory (out)
    dir_path_out_res: str, optional
        Path of the saving directory for results (out)
    verbose: bool, optional
        Activation key for verbosity
    save: bool, optional
        If True, save the txt loop and figures

    Returns
    -------
    None
    """
    assert root_out or dir_path_out_res

    # Create the saving folder, init date and starting time
    t0, date = time.time(), datetime.now()
    date = date.strftime('%Y-%m-%d %H;%M')

    # Start single script for each measurement file
    i = 0
    file_path_in = ''
    for elem in os.listdir(dir_path_in):
        if elem.endswith(file_format) and not elem.endswith('SS_PFM_bias.txt'):
            file_path_in = os.path.join(dir_path_in, elem)
            single_script(user_pars, file_path_in, meas_pars, sign_pars,
                          mode=mode, root_out=root_out, verbose=verbose,
                          txt_save=save)
            i += 1

    if save:
        if verbose:
            print('\nSS PFM parameter analysis ...\n')

        # Data extraction from measurement file and identification
        dict_meas, _ = data_extraction(
            file_path_in, mode_dfrt=bool(mode == 'dfrt'), verbose=verbose)

        # Find measurement parameters (cut and read mode parameters)
        cut_dict, sign_pars['Mode (R)'] = init_parameters(dict_meas, sign_pars)
        meas_pars['nb seg'] = cut_dict['nb seg']
        meas_pars['exp time [s]'] = cut_dict['experimental time']
        meas_pars['start hold time exp [s]'] = cut_dict['start hold time exp']
        meas_pars['end hold time exp [s]'] = cut_dict['end hold time exp']
        meas_pars['theoretic time [s]'] = cut_dict['theoretical time']

        # Save all the parameters in a text file
        if dir_path_out_res is None:
            dir_path_out_res = os.path.join(root_out, 'results')
        save_txt_file(dir_path_out_res, t0, date, user_pars, meas_pars,
                      sign_pars, i)


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
    file_format = file_path_in[-4:]

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

    single_script(user_pars, file_path_in, meas_pars, sign_pars, mode=mode,
                  root_out=root_out, verbose=verbose, show_plots=show_plots,
                  save_plots=save)

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


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - mode: str
        Treatment Method for Extracting PFM Amplitude and Phase from Segments
        This parameter determines the treatment method used for data analysis.
        It specifies how PFM (Piezoresponse Force Microscopy) amplitude and
        phase data are extracted from segments, as well as how signal
        treatment is performed within the segment.
        Three possible values:
            --> 'max': Peak maximum treatment (sweep)
            --> 'fit': Peak fit treatment (sweep)
            --> 'dfrt': Average of segment
    - cut_seg_perc: dict('start':, 'end':) of int
        Segment Trimming Percentage
        Description: This parameter specifies the percentage of the segment
        length to be trimmed from both the start and end of the segment.
        It allows you to exclude a certain portion of the segment from analysis
         at the beginning and end (in term of %)
    - filter: bool
        Noise Reduction Filter for Measurements
        This parameter controls whether a noise reduction filter should be
        applied to the measurements.
    - filter ord: int
        Filter Order for Noise Reduction
        This parameter controls the order of the filter used for noise
        reduction. A higher value results in stronger filtering of the signal.
        Value: An integer value, with a minimum value of 1.
        Active if: This parameter is active when the 'filter' option is enabled.
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
                  'filter': False,
                  'filter ord': 10}

    fit_params = {'fit pha': False,
                  'detect peak': False,
                  'sens peak detect': 1.5}

    user_pars = {'seg pars': seg_params,
                 'fit pars': fit_params}

    return user_pars, file_path_in, root_out, verbose, show_plots, save


def main():
    """ Main function for data analysis. """
    # Extract parameters
    out = parameters()
    (user_pars, file_path_in, root_out, verbose, show_plots, save) = out
    # Main function
    main_script(user_pars, file_path_in, verbose=verbose, show_plots=show_plots,
                save=save, root_out=root_out)


if __name__ == '__main__':
    main()
