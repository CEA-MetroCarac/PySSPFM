"""
--> Executable Script
Extract all data from a spm file (SSPFM script and raw measurements)
"""

import tkinter.filedialog as tkf
import matplotlib.pyplot as plt
import numpy as np

from PySSPFM.settings import get_setting, get_config
from PySSPFM.utils.core.figure import plot_graph, print_plots
from PySSPFM.utils.raw_extraction import NanoscopeError
from PySSPFM.utils.signal_bias import extract_sspfm_bias_pars, sspfm_time


def plot_sspfm_voltage(ss_pfm_times_calc, ss_pfm_bias_calc, nb_segment=None):
    """
    Plot SSPFM voltage.

    Parameters
    ----------
    ss_pfm_times_calc: array-like
        Times for SSPFM measurement
    ss_pfm_bias_calc: array-like
        SSPFM bias values
    nb_segment: int, optional
        Number of segments

    Returns
    -------
    fig: plt.figure
    """

    add_str = f'\nnb seg = {nb_segment}' if nb_segment else ""
    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = 'sspfm_bias_extracted'
    plot_dict = {'title': 'SS PFM Bias', 'x lab': 'Time [s]',
                 'y lab': 'SS PFM BIAS [V]'}
    legend = 'sspfm bias' + add_str
    tab_dict_1 = {'legend': legend, 'form': 'g-', 'lw': 1}
    plot_graph(ax, ss_pfm_times_calc, ss_pfm_bias_calc, plot_dict=plot_dict,
               tabs_dict=tab_dict_1, plot_leg=True)
    return fig


def main_spm_data_extractor(file_path_in, nb_hold_seg_start=1,
                            nb_hold_seg_end=1, verbose=False, make_plots=False):
    """
    Main function to extract data from SPM file.

    Parameters
    ----------
    file_path_in: str
        Path of SPM file
    nb_hold_seg_start: int, optional
        Number of hold segments at the start (default is 1)
    nb_hold_seg_end: int, optional
        Number of hold segments at the end (default is 1)
    verbose: bool, optional
        Verbosity flag (default is False)
    make_plots: bool, optional
        Flag to generate plots (default is False)

    Returns
    -------
    raw_dict: dict
        Dictionary containing raw data
    sspfm_pars: dict
        Dictionary containing SSPFM parameters
    other_pars: dict
        Dictionary containing other parameters
    """
    try:
        from PySSPFM.utils.datacube_reader import \
            DataExtraction, script_info # noqa
    except (NotImplementedError, NameError) as error:
        message = "To open DATACUBE spm file (Bruker), nanoscope module is " \
                  "required and NanoScope Analysis software (Bruker) should " \
                  "be installed on the computer"
        raise NanoscopeError(message) from error

    # Extract data from measurement file: tip bias list of values
    data_extract = DataExtraction(file_path_in)
    data_extract.data_extraction(raw_data=True)
    info_dict = data_extract.info_dict
    script_dict = script_info(info_dict)
    raw_dict = data_extract.raw_dict

    # Generate dict of bias parameters
    tip_bias = list(info_dict['tip_bias'])[nb_hold_seg_start:-nb_hold_seg_end]
    dict_elec = extract_sspfm_bias_pars(tip_bias)

    # Construct sspfm_pars dictionary
    sspfm_pars = dict_elec
    hold_durat_init = np.sum(info_dict['durs'][:nb_hold_seg_start])*1000
    hold_durat_end = np.sum(info_dict['durs'][-nb_hold_seg_end:])*1000
    hold_sample_init = np.sum(info_dict['samps'][:nb_hold_seg_start])
    hold_sample_end = np.sum(info_dict['samps'][-nb_hold_seg_end:])
    sspfm_pars['Hold seg durat (start) [ms]'] = hold_durat_init
    sspfm_pars['Hold seg durat (end) [ms]'] = hold_durat_end
    sspfm_pars['Hold sample (start)'] = hold_sample_init
    sspfm_pars['Hold sample (end)'] = hold_sample_end
    sspfm_pars['Seg durat (W) [ms]'] = info_dict['durs'][nb_hold_seg_start]*1000
    sspfm_pars['Seg durat (R) [ms]'] = \
        info_dict['durs'][nb_hold_seg_start+1]*1000
    sspfm_pars['Seg sample (W)'] = info_dict['samps'][nb_hold_seg_start]
    sspfm_pars['Seg sample (R)'] = info_dict['samps'][nb_hold_seg_start+1]

    # Construct other_pars dictionary
    key_ignored = ['Total # Segments', 'Total Script Time (s)',
                   'Write Voltage Range (V)', 'Write Number of Voltages',
                   'Write Wave Form', 'Write Segment Duration (ms)',
                   'Write Samples Per Segment', 'Read Voltage Range (V)',
                   'Read Number of Voltages', 'Read Wave Form',
                   'Read Segment Duration (ms)', 'Read Samples Per Segment']
    other_pars = {}
    for key, value in script_dict.items():
        if key not in key_ignored:
            other_pars[key] = value

    # Print all data extracted from SPM file
    if verbose:
        print("- Measurement extracted:")
        for key in raw_dict.keys():
            print(f'\t{key}')
        print("\n- SSPFM parameters:")
        for key, value in sspfm_pars.items():
            print(f'\t{key}: {value}')
        print("\n- Other parameters:")
        for key, value in other_pars.items():
            print(f'\t{key}: {value}')

    # Plot SSPFM bias
    if make_plots:
        ss_pfm_times_calc, ss_pfm_bias_calc = sspfm_time(
            tip_bias, sspfm_pars, gen_hold_segment=True)
        fig = plot_sspfm_voltage(ss_pfm_times_calc, ss_pfm_bias_calc,
                                 nb_segment=len(info_dict["tip_bias"]))

        return [fig]
    else:
        return raw_dict, sspfm_pars, other_pars


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis

    - nb_hold_seg_start: int
        Number of hold segments at the start of measurement.
        This parameter is used to specify the number of hold segments at the
        beginning of the SSPFM signal.
    - nb_hold_seg_end: int
        Number of hold segments at the end of measurement.
        This parameter is used to specify the number of hold segments at the
        end of the SSPFM signal.

    file_path_in: str
        Path of datacube SSPFM (.spm) raw file measurements.
        This parameter specifies the path where datacube SSPFM (.spm) raw file
         measurements are located. It is used to indicate the path to the file
        containing these measurements.
    - verbose: bool
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.
    - show_plots: bool
        Activation key for generating matplotlib figures during analysis.
        This parameter serves as an activation key for generating
        matplotlib figures during the analysis process.
    """
    if get_setting("extract_parameters") in ['json', 'toml']:
        config_params, _ = get_config(__file__, fname_json)
        file_path_in = config_params['file_path_in']
        nb_hold_seg_start = config_params['nb_hold_seg_start']
        nb_hold_seg_end = config_params['nb_hold_seg_end']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Get file path
        file_path_in = tkf.askopenfilename()
        # file_path_in = r'...\KNN500n\KNN500n.0_00001.spm
        nb_hold_seg_start = 1
        nb_hold_seg_end = 1
        verbose = True
        show_plots = True
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return file_path_in, nb_hold_seg_start, nb_hold_seg_end, verbose, show_plots


def main(fname_json=None):
    """
    Main function for data analysis.

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)
    """
    # Extract parameters
    (file_path_in, nb_hold_seg_start, nb_hold_seg_end, verbose,
     show_plots) = parameters(fname_json=fname_json)# Generate default path out
    # Main function
    res = main_spm_data_extractor(
        file_path_in, nb_hold_seg_start=nb_hold_seg_start,
        nb_hold_seg_end=nb_hold_seg_end, verbose=verbose, make_plots=show_plots)
    # Plot figures
    if show_plots:
        print_plots(res, show_plots=show_plots, save_plots=False,
                    dirname=None, transparent=False)


if __name__ == '__main__':
    main()
