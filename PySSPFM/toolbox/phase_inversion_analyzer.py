"""
--> Executable Script
Automatic determination of phase inversion for a list of raw sspfm measurement
file
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, copy_default_settings_if_not_exist, get_config
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.path_management import \
    get_filenames_with_conditions, sort_filenames
from PySSPFM.utils.raw_extraction import data_extraction, csv_meas_sheet_extract
from PySSPFM.utils.signal_bias import sspfm_time, sspfm_generator
from PySSPFM.utils.datacube_to_nanoloop.analysis import \
    (cut_function, external_calib, SegmentInfo, SegmentSweep,
     SegmentStable, SegmentStableDFRT)
from PySSPFM.utils.datacube_to_nanoloop.file import get_phase_tab_offset
from PySSPFM.utils.datacube_to_nanoloop.plot import plt_signals
from PySSPFM.utils.nanoloop.phase import phase_bias_grad
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def revert_on_off(positive_pha_grad):
    """
    Revert On/Off gradient polarity if necessary.

    Parameters
    ----------
    positive_pha_grad : dict
        Dictionary containing 'Grad On field' and 'Grad Off field' keys.

    Returns
    -------
    revert: bool
        True if polarity needs to be reverted, False otherwise.
    """

    if ('Grad On field' in positive_pha_grad.keys() and
            'Grad Off field' in positive_pha_grad.keys()):

        grad_on = positive_pha_grad['Grad On field']
        grad_off = positive_pha_grad['Grad Off field']

        if (grad_on and grad_off) or (not grad_on and not grad_off):
            revert = False
        else:
            revert = True
    else:
        revert = False

    return revert


def apply_phase_offset(pha_tab, phase_offset=90, phase_min=-180, phase_max=180):
    """
    Apply phase offset to phase values.

    Parameters
    ----------
    pha_tab : list
        List of phase values.
    phase_offset : float, optional
        Phase offset to apply (default is 90).
    phase_min : float, optional
        Minimum phase value (default is -180).
    phase_max : float, optional
        Maximum phase value (default is 180).

    Returns
    -------
    new_pha_tab: list
        List of phase values with applied offset.
    """

    lim_min = phase_min + phase_offset
    lim_max = phase_max + phase_offset
    delta_phase = phase_max - phase_min
    new_pha_tab = [pha_val + delta_phase if pha_val < lim_min
                   else pha_val - delta_phase if pha_val >= lim_max
                   else pha_val for pha_val in pha_tab]

    return new_pha_tab


def save_dict_to_txt(data_dict, file_path, map_dim=None):
    """
    Save dictionary data to a text file --> this file can be read with map
    readers

    Parameters
    ----------
    data_dict : dict
        Dictionary containing data to be saved.
    file_path : str
        Path to the output text file.
    map_dim: dict, optional
        Map dimension in terms of pixels and microns

    Returns
    -------
    None
    """
    delimiter = get_setting("delimiter")
    header = "phase inversion\n"
    if map_dim is not None:
        header += f"x pix={map_dim['x pix']}, y pix={map_dim['y pix']}, " \
                  f"x mic={map_dim['x mic']}, y mic={map_dim['y mic']}, \n"
    for key in data_dict.keys():
        header += f"{key}{delimiter}"
    data_array = np.array(list(data_dict.values()), dtype=float).T
    np.savetxt(file_path, data_array, header=header, delimiter=delimiter,
               newline='\n', fmt='%s')


def single_script(file_path_in, user_pars, meas_pars, sign_pars,
                  phase_offset=0, file_index=None, verbose=False,
                  make_plots=False, plot_nanoloops=False):
    """
    Single script function

    Parameters
    ----------
    file_path_in: str
        Path of input file
    user_pars: dict
        User parameters
    meas_pars: dict
        Dictionary of measurement parameters.
    sign_pars: dict
        Dictionary of SSPFM bias signal parameters.
    phase_offset: float, optional
        Phase offset to apply to all phase values.
    file_index: int, optional
        Index of the file
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Activation key for generating main plots
    plot_nanoloops: bool, optional
        Activation key for nanoloop plots

    Returns
    -------
    positive_pha_grad : dict
        Dictionary containing 'Grad On field' and 'Grad Off field' keys.
    figures: list
        Generated figures
    """
    figures = []
    mode = user_pars['seg pars']['mode']

    if verbose and file_index is not None:
        print(f"\nFile n°{file_index}: {os.path.split(file_path_in)[1]}")

    # Extract sspfm measurement from file
    dict_meas, _ = data_extraction(
        file_path_in, mode_dfrt=bool(mode.lower() == 'dfrt'), verbose=False)

    # Init and cut measurements
    if sign_pars['Min volt (R) [V]'] == sign_pars['Max volt (R) [V]']:
        sign_pars['Mode (R)'] = 'Single Read Step'
    cut_dict, _ = cut_function(sign_pars)

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

    # Apply offset to all phase values --> reduces noise on the phase
    dict_meas['pha'] = apply_phase_offset(
        dict_meas['pha'], phase_offset=phase_offset, phase_min=-180,
        phase_max=180)

    # SS PFM signal determination
    par = sspfm_time(ss_pfm_bias, sign_pars)
    (_, ss_pfm_bias_calc) = par

    if len(dict_meas['tip_bias']) < 1:
        dict_meas['tip_bias'] = ss_pfm_bias_calc

    # Plot raw signals in time
    if make_plots:
        fig = plt_signals(dict_meas, unit=unit)
        figures.append(fig)

    # Init parameters
    cut_seg = user_pars['seg pars']['cut seg [%]']
    seg_dict, seg_pars, seg_pars_on, seg_pars_off, positive_pha_grad = \
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
        seg_pars_on['title'] = 'On Field'
        seg_pars_on['color'] = 'y'
        seg_pars['On field'] = seg_pars_on
    if off_field_mode:
        seg_pars_off['index cut'] = cut_dict['off f']
        seg_pars_off['ite'] = sign_pars['Seg sample (R)']
        seg_pars_off['type'] = 'read'
        seg_pars_off['add'] = [0, 1]
        seg_pars_off['title'] = 'Off Field'
        seg_pars_off['color'] = 'w'
        seg_pars['Off field'] = seg_pars_off

    # Fill segment list
    for tuple_dict in seg_pars.items():
        seg_tab = []
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
                seg_tab.append(SegmentSweep(
                    segment_info, dict_meas,
                    start_freq_init=freq_ini, end_freq_init=freq_end,
                    cut_seg=cut_seg, filter_type=filter_type,
                    filter_cutoff_frequency=filter_freq,
                    filter_order=filter_order,
                    fit_pars=user_pars['fit pars']))
            else:
                target_keys = ['amp', 'pha', 'freq',
                               'amp sb_l', 'pha sb_l', 'freq sb_l',
                               'amp sb_r', 'pha sb_r', 'freq sb_r']
                flag = bool(all(key in dict_meas for key in target_keys))
                if flag:
                    # SegmentStableDFRT
                    seg_tab.append(SegmentStableDFRT(
                        segment_info, dict_meas, cut_seg=cut_seg,
                        filter_type=filter_type,
                        filter_cutoff_frequency=filter_freq,
                        filter_order=filter_order))
                else:
                    # SegmentStable
                    seg_tab.append(SegmentStable(
                        segment_info, dict_meas, cut_seg=cut_seg,
                        filter_type=filter_type,
                        filter_cutoff_frequency=filter_freq,
                        filter_order=filter_order))

        # Generate grad figures
        dict_str = {'label': tuple_dict[1]['title'],
                    'col': tuple_dict[1]['color']}

        # Calculate phase grad with bias
        write_voltage = ss_pfm_bias[::2]
        phase = [seg.pha for seg in seg_tab]
        fig_grad, positive_pha_grad[f"Grad {tuple_dict[0]}"] = \
            phase_bias_grad(phase, write_voltage, bias_pola_target=None,
                            bias_pha_target=None, dict_str=dict_str,
                            make_plots=make_plots)

        figures += [fig_grad]

        if verbose:
            phase_inversion_str = \
                f'{positive_pha_grad[f"Grad {tuple_dict[0]}"]}' \
                if positive_pha_grad[f"Grad {tuple_dict[0]}"] is not None \
                else 'ValueError'
            print(f"- {tuple_dict[0]} phase bias grad: {phase_inversion_str}")

        seg_dict[tuple_dict[0]] = seg_tab

    if plot_nanoloops:
        del_first_loop = True
        start_index = 1 if del_first_loop else 0
        nb_loop = sign_pars['Nb volt (R)']
        period = (sign_pars['Nb volt (W)'] - 1)*2
        if 'On field' in seg_dict:
            pha_segs_on = [seg.pha for seg in seg_dict['On field']]
            pha_segs_on = np.array(pha_segs_on).reshape(nb_loop, period)
            pha_segs_on = np.array([np.mean(elem[start_index:])
                                    for elem in pha_segs_on.T])
        if 'Off field' in seg_dict:
            pha_segs_off = [seg.pha for seg in seg_dict['Off field']]
            pha_segs_off = np.array(pha_segs_off).reshape(nb_loop, period)
            pha_segs_off = np.array([np.mean(elem[start_index:])
                                     for elem in pha_segs_off.T])
        ss_pfm_cycle = ss_pfm_bias[::2][:period]
        fig, ax = plt.subplots()
        if 'On field' in seg_dict:
            ax.plot(ss_pfm_cycle, pha_segs_on, label='On Field')
        if 'Off field' in seg_dict:
            ax.plot(ss_pfm_cycle, pha_segs_off, label='Off Field')
        plt.legend()
        figures += [fig]
        print_plots(figures, show_plots=True, save_plots=False,
                    dirname=None, transparent=False)

    return positive_pha_grad, figures


def multi_script(dir_path_in, file_names, user_pars, meas_pars, sign_pars,
                 verbose=False, make_plots=False):
    """
    Multi-script function

    Parameters
    ----------
    dir_path_in: str
        Input directory path
    file_names: list of str
        List of file names
    user_pars: dict
        User parameters
    meas_pars: dict
        Dictionary of measurement parameters.
    sign_pars: dict
        Dictionary of SSPFM bias signal parameters.
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Activation key for generating plots

    Returns
    -------
    phase_grad_tab : list
        Containing a list of dictionaries with 'Grad On field' and
        'Grad Off field' keys.
    figures: list
        Generated figures
    """
    figures = []
    phase_grad_tab = {}

    # Get phase offset list from phase file if filled by user
    phase_file_path = user_pars["pha pars"]["phase_file_path"]
    if phase_file_path is not None:
        phase_tab = get_phase_tab_offset(phase_file_path)
    else:
        phase_tab = None

    # Multi processing mode
    multiproc = get_setting("multi_processing")
    if multiproc:
        from PySSPFM.utils.core.multi_proc import \
            run_multi_phase_inversion_analyzer
        phase_offset = user_pars["pha pars"]["offset"]
        common_args = {
            "user_pars": user_pars,
            "meas_pars": meas_pars,
            "sign_pars": sign_pars,
            "phase_offset": phase_offset,
            "file_index": None,
            "verbose": verbose,
            "make_plots": False}
        file_paths_in = [os.path.join(dir_path_in, file_name)
                         for file_name in file_names]
        if phase_file_path is not None:
            common_args = {key: value for key, value in common_args.items()
                           if not key == "phase_offset"}
        tab_phase_grad = \
            run_multi_phase_inversion_analyzer(
                file_paths_in, phase_tab, common_args, processes=16)

        # Append phase grad bias values
        for elem in tab_phase_grad:
            revert = revert_on_off(elem)
            if len(list(phase_grad_tab.keys())) == 0:
                for key, value in elem.items():
                    phase_grad_tab[key] = []
                phase_grad_tab["Revert On Off"] = []
            for key, value in elem.items():
                phase_grad_tab[key].append(value)
            phase_grad_tab["Revert On Off"].append(revert)

    # Mono processing mode
    else:
        # For each file: single_script
        for index, file_name in enumerate(file_names):
            generate_figures = bool(index == 0 and make_plots)
            if phase_tab is None:
                phase_offset = user_pars["pha pars"]["offset"]
            else:
                phase_offset = phase_tab[index]
            phase_grad, fig_main = single_script(
                os.path.join(dir_path_in, file_name), user_pars, meas_pars,
                sign_pars, phase_offset=phase_offset, file_index=index+1,
                verbose=verbose, make_plots=generate_figures)
            figures += fig_main
            revert = revert_on_off(phase_grad)

            # Append phase grad bias values
            if len(list(phase_grad_tab.keys())) == 0:
                for key, value in phase_grad.items():
                    phase_grad_tab[key] = []
                phase_grad_tab["Revert On Off"] = []
            for key, value in phase_grad.items():
                phase_grad_tab[key].append(value)
            phase_grad_tab["Revert On Off"].append(revert)

    return phase_grad_tab, figures


def main_phase_inversion_analyzer(user_pars, dir_path_in, range_file=None,
                                  extension="spm", verbose=False,
                                  make_plots=False):
    """
    Main function used for phase inversion analyzer

    Parameters
    ----------
    user_pars: dict
        Dictionary of all user parameters for the treatment.
    dir_path_in: str
        Input directory path
    range_file: list, optional
        Number of files to process
    extension : str, optional
        File extension (default is "spm")
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Activation key for generating figures

    Returns
    -------
    phase_grad_tab : list
        Containing a list of dictionaries with 'Grad On field' and
        'Grad Off field' keys.
    map_dim: dict
        Map dimension in terms of pixels and microns
    figures: list
        Generated figures
    """
    file_names = get_filenames_with_conditions(dir_path_in, extension=extension)
    file_names, _, _ = sort_filenames(file_names)
    file_names = file_names[range_file[0]:range_file[1]] \
        if range_file is not None else file_names

    # Extract parameters from measurement sheet
    meas_pars, sign_pars = csv_meas_sheet_extract(dir_path_in)
    map_dim = {'x pix': meas_pars['Grid x [pix]'],
               'y pix': meas_pars['Grid y [pix]'],
               'x mic': meas_pars['Grid x [um]'],
               'y mic': meas_pars['Grid y [um]']}
    # Multi script
    phase_grad_tab, figures = multi_script(
        dir_path_in, file_names, user_pars, meas_pars, sign_pars,
        verbose=verbose, make_plots=make_plots)

    figures = [item for item in figures if item != []]

    return phase_grad_tab, map_dim, figures


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
        If None, phase offset value will be determined with static or dynamic
        method.
    - offset: float
        Phase offset value applied to measurements.
        This parameter allows the user to specify a constant phase offset value
        for the analysis, which is applied to all phase values.
        Active if: This parameter is active when "phase_file_path"
        parameters is None.
    - dir_path_in: str
        Directory path of datacube SSPFM raw file measurements.
        This parameter specifies the directory path where datacube SSPFM
        raw file measurements are located. It is used to indicate the path
        to the directory containing these measurements.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - range_file: list
        Considered file index for the analysis.
        This parameter is used to specify a range of file indices to be
        processed within a directory. If set to None, all files in the
         directory are processed.
    - extension: str
        Extension of raw SSPFM measurement files.
        This parameter determines the file extension type of raw SSPFM
        measurement files.
        Four possible values: 'spm', 'txt', 'csv', or 'xlsx'.
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
        dir_path_in = config_params['dir_path_in']
        dir_path_out = config_params['dir_path_out']
        range_file = config_params['range_file']
        extension = config_params['extension']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = {'seg pars': config_params['seg_params'],
                     'fit pars': config_params['fit_params'],
                     'pha pars': config_params['pha_params']}
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Get file path for single script
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n\
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # phase_inversion_analyzer_2023-10-02-16h38m
        range_file = None
        extension = "spm"
        # extension = 'spm' or 'txt' or 'csv' or 'xlsx'
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
                      'offset': 0}
        user_pars = {'seg pars': seg_params,
                     'fit pars': fit_params,
                     'pha pars': pha_params}
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, dir_path_in, dir_path_out, range_file, extension, \
        verbose, show_plots, save


def main(fname_json=None):
    """
    Main function for data analysis.

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)
    """
    # Extract parameters
    (user_pars, dir_path_in, dir_path_out, range_file, extension, verbose,
     show_plots, save) = parameters(fname_json=fname_json)
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,
        dirname="phase_inversion_analyzer",
        lvl=0, create_path=True, post_analysis=False)
    start_time = datetime.now()
    # Main function
    res = main_phase_inversion_analyzer(
        user_pars, dir_path_in, range_file=range_file, extension=extension,
        verbose=verbose, make_plots=bool(show_plots or save))
    (phase_grad_tab, map_dim, figs) = res
    # Plot figures
    print_plots(figs, show_plots=show_plots, save_plots=save,
                dirname=dir_path_out, transparent=False)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)
        file_path_out = os.path.join(dir_path_out, "phase_inversion.txt")
        save_dict_to_txt(phase_grad_tab, file_path=file_path_out,
                         map_dim=map_dim)


if __name__ == '__main__':
    main()
