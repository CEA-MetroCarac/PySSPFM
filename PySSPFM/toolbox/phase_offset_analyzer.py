"""
--> Executable Script
Automatic determination of phase offset for a list of raw sspfm measurement file
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, copy_default_settings_if_not_exist
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.raw_extraction import data_extraction, csv_meas_sheet_extract
from PySSPFM.utils.signal_bias import sspfm_time, sspfm_generator
from PySSPFM.utils.datacube_to_nanoloop.analysis import \
    (cut_function, external_calib, SegmentInfo, SegmentSweep,
     SegmentStable, SegmentStableDFRT)
from PySSPFM.utils.datacube_to_nanoloop.file import get_file_names
from PySSPFM.utils.datacube_to_nanoloop.plot import plt_signals
from PySSPFM.utils.nanoloop.phase import \
    phase_offset_determination, mean_phase_offset
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


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
    header = "phase\n"
    if map_dim is not None:
        header += f"x pix={map_dim['x pix']}, y pix={map_dim['y pix']}, " \
                  f"x mic={map_dim['x mic']}, y mic={map_dim['y mic']}, \n"
    for key in data_dict.keys():
        header += f"{key}{delimiter}"
    data_array = np.array(list(data_dict.values()), dtype=float).T
    np.savetxt(file_path, data_array, header=header, delimiter=delimiter,
               newline='\n', fmt='%s')


def generate_graph_offset(phase_offset_tab):
    """
    Generate graph offset function

    Parameters
    ----------
    phase_offset_tab: dict
        Dictionary containing phase offset values of all the file

    Returns
    -------
    fig: plt.figure
        Generated figure
    """
    figsize = get_setting("figsize")
    graph_offset, ax = plt.subplots(figsize=figsize)
    graph_offset.sfn = 'phase_offset_analysis'
    tab_dict, tab_values = [], []
    for key, value in phase_offset_tab.items():
        tab_values.append(value)
        tab_dict.append({'legend': key})
    plot_dict = {'x lab': 'File index', 'y lab': 'Phase offset [°]', 'fs': 15,
                 'edgew': 1, 'tickl': 2, 'gridw': 1}
    plot_graph(ax, range(len(tab_values[0])), tab_values,
               plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=True)

    return graph_offset


def single_script(file_path_in, user_pars, meas_pars, sign_pars,
                  file_index=None, verbose=False, make_plots=False):
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
    file_index: int, optional
        Index of the file
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Activation key for generating plots

    Returns
    -------
    phase_offset_val: dict
        Dictionary containing phase offset data of a single file
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

    # Generate SS PFM signal segment values
    ss_pfm_bias = sspfm_generator(sign_pars)

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
    _, seg_pars, seg_pars_on, seg_pars_off, phase_offset_val = \
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

        # Generate hist figures and phase offset determination
        dict_str = {'label': tuple_dict[1]['title'],
                    'col': tuple_dict[1]['color']}
        phase_offset_val[tuple_dict[0]], fig_hist = \
            phase_offset_determination([seg.pha for seg in seg_tab],
                                       dict_str=dict_str, make_plots=make_plots)
        figures += [fig_hist]

        if verbose:
            phase_offset_str = f'{phase_offset_val[tuple_dict[0]]:.2f}'\
                if phase_offset_val[tuple_dict[0]] is not None else 'ValueError'
            print(f"- {tuple_dict[0]} phase offset [°]: {phase_offset_str}")

    return phase_offset_val, figures


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
    phase_offset_tab: dict
        Dictionary containing phase offset data of all the file
    figures: list
        Generated figures
    """
    figures = []
    phase_offset_tab = {}

    # Multi processing mode
    multiproc = get_setting("multi_processing")
    if multiproc:
        from PySSPFM.utils.core.multi_proc import \
            run_multi_phase_offset_analyzer
        common_args = {
            "user_pars": user_pars,
            "meas_pars": meas_pars,
            "sign_pars": sign_pars,
            "file_index": None,
            "verbose": verbose,
            "make_plots": False}
        file_paths_in = [os.path.join(dir_path_in, file_name)
                         for file_name in file_names]
        tab_phase_offset_val = \
            run_multi_phase_offset_analyzer(file_paths_in, common_args,
                                            processes=16)
        for elem in tab_phase_offset_val:
            mean_phase_offset_val = mean_phase_offset(elem)
            # Append phase offset values
            if len(list(phase_offset_tab.keys())) == 0:
                for key, value in elem.items():
                    phase_offset_tab[key] = []
                phase_offset_tab["Mean"] = []
            for key, value in elem.items():
                phase_offset_tab[key].append(value)
            phase_offset_tab["Mean"].append(mean_phase_offset_val)

    # Mono processing mode
    else:
        # For each file: single_script
        for index, file_name in enumerate(file_names):
            generate_figures = bool(index == 0 and make_plots)
            phase_offset, fig_main = single_script(
                os.path.join(dir_path_in, file_name), user_pars, meas_pars,
                sign_pars, file_index=index+1, verbose=verbose,
                make_plots=generate_figures)
            figures += fig_main
            mean_phase_offset_val = mean_phase_offset(phase_offset)

            # Append phase offset values
            if len(list(phase_offset_tab.keys())) == 0:
                for key, value in phase_offset.items():
                    phase_offset_tab[key] = []
                phase_offset_tab["Mean"] = []
            for key, value in phase_offset.items():
                phase_offset_tab[key].append(value)
            phase_offset_tab["Mean"].append(mean_phase_offset_val)

    return phase_offset_tab, figures


def main_phase_offset_analyzer(user_pars, dir_path_in, range_file=None,
                               extension="spm", verbose=False,
                               make_plots=False):
    """
    Main function used for phase offset analyzer

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
    phase_offset_tab: dict
        Dictionary containing phase offset data of all the file
    map_dim: dict
        Map dimension in terms of pixels and microns
    figures: list
        Generated figures
    """
    file_names = get_file_names(dir_path_in, file_format=extension)
    file_names = file_names[range_file[0]:range_file[1]] \
        if range_file is not None else file_names

    # Extract parameters from measurement sheet
    meas_pars, sign_pars = csv_meas_sheet_extract(dir_path_in)
    map_dim = {'x pix': meas_pars['Grid x [pix]'],
               'y pix': meas_pars['Grid y [um]'],
               'x mic': meas_pars['Grid x [pix]'],
               'y mic': meas_pars['Grid y [um]']}
    # Multi script
    phase_offset_tab, figures = multi_script(
        dir_path_in, file_names, user_pars, meas_pars, sign_pars,
        verbose=verbose, make_plots=make_plots)

    # Make graph offset
    if make_plots:
        figures += [generate_graph_offset(phase_offset_tab)]
    figures = [item for item in figures if item != []]

    return phase_offset_tab, map_dim, figures


def parameters():
    """
    To complete by user of the script: return parameters for analysis

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
        file_path = os.path.realpath(__file__)
        file_path_user_params = copy_default_settings_if_not_exist(file_path)

        # Load parameters from the specified configuration file
        print(f"user parameters from {os.path.split(file_path_user_params)[1]} "
              f"file")
        config_params = load_parameters_from_file(file_path_user_params)
        dir_path_in = config_params['dir_path_in']
        dir_path_out = config_params['dir_path_out']
        range_file = config_params['range_file']
        extension = config_params['extension']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = {'seg pars': config_params['seg_params'],
                     'fit pars': config_params['fit_params']}
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Get file path for single script
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n\
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # phase_offset_analyzer_2023-10-02-16h38m
        range_file = None
        extension = "spm"
        # extension = 'spm' or 'txt' or 'csv' or 'xlsx'
        verbose = True
        show_plots = True
        save = False
        seg_params = {'mode': 'max',
                      'cut seg [%]': {'start': 5, 'end': 5},
                      'filter type': None,
                      'filter freq 1': 1e3,
                      'filter freq 2': 3e3,
                      'filter ord': 4}
        fit_params = {'fit pha': False,
                      'detect peak': False,
                      'sens peak detect': 1.5}
        user_pars = {'seg pars': seg_params,
                     'fit pars': fit_params}
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, dir_path_in, dir_path_out, range_file, extension, \
        verbose, show_plots, save


def main():
    """ Main function for data analysis. """

    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, range_file, extension, verbose,
     show_plots, save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save, dirname="phase_offset_analyzer",
        lvl=0, create_path=True, post_analysis=False)
    start_time = datetime.now()
    # Main function
    phase_offset_tab, map_dim, figs = main_phase_offset_analyzer(
        user_pars, dir_path_in, range_file=range_file, extension=extension,
        verbose=verbose, make_plots=bool(show_plots or save))
    # Plot figures
    print_plots(figs, show_plots=show_plots, save_plots=save,
                dirname=dir_path_out, transparent=False)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)
        file_path_out = os.path.join(dir_path_out, "phase.txt")
        save_dict_to_txt(phase_offset_tab, file_path=file_path_out,
                         map_dim=map_dim)


if __name__ == '__main__':
    main()
