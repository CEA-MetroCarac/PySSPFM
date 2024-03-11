"""
Example of analysis methods
"""
import os
import numpy as np
import matplotlib.pyplot as plt

from examples.utils.datacube_to_nanoloop.ex_gen_data import \
    ex_gen_segments, pars_segment
from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.datacube_to_nanoloop.plot import \
    plt_seg_max, plt_seg_fit, plt_seg_stable
from PySSPFM.utils.datacube_to_nanoloop.analysis import \
    (SegmentInfo, SegmentSweep, SegmentStable, external_calib, cut_function,
     extract_other_properties)
from PySSPFM.utils.raw_extraction import data_extraction, csv_meas_sheet_extract


def list_segs(mode, nb_seg_str='all'):
    """
    Generate a list of Segment objects.

    Parameters
    ----------
    mode: str
        Mode of operation.
    nb_seg_str: str, optional
        Number of segments to generate. Defaults to 'all'.

    Returns
    -------
    segs: dict
        Dictionary of Segment objects for on field and off field segments.
    dict_meas: dict
        Dictionary of measurement values.
    """
    np.random.seed(0)
    sweep_freq = {'start': 200, 'end': 400}
    seg_pars, sign_pars, hold_dict, _, _, fit_pars, _ = pars_segment()
    dict_meas = ex_gen_segments(mode, make_plots=False)
    seg_pars['mode'] = mode
    segs = {'on f': [], 'off f': []}
    ite = sign_pars['Seg sample (W)'] + sign_pars['Seg sample (R)']
    nb_seg = (sign_pars['Nb volt (W)'] - 1) * 2 * sign_pars['Nb volt (R)'] if \
        nb_seg_str == 'all' else int(nb_seg_str)

    for i in range(nb_seg):
        for cont, nb_samp in enumerate([sign_pars['Seg sample (W)'],
                                        sign_pars['Seg sample (R)']]):
            if cont == 0:
                read_volt = dict_meas['sspfm bias'][i]
                write_volt = dict_meas['sspfm bias'][i]
                type_seg = 'write'
                key = 'on f'
                start_ind = i * ite + hold_dict['start samp']
                end_ind = start_ind + nb_samp
            else:
                read_volt = dict_meas['sspfm bias'][i]
                write_volt = dict_meas['sspfm bias'][i - 1]
                type_seg = 'read'
                key = 'off f'
                start_ind = i * ite + sign_pars['Seg sample (W)']
                start_ind += hold_dict['start samp']
                end_ind = start_ind + nb_samp

            # ex SegmentInfo
            segment_info = SegmentInfo(
                start_ind, end_ind, dict_meas['times'],
                write_volt=write_volt, read_volt=read_volt, type_seg=type_seg,
                mode=seg_pars['mode'], numb=i)
            # ex SegmentSweep
            if mode in ['max', 'fit']:
                segs[key].append(SegmentSweep(
                    segment_info, dict_meas,
                    start_freq_init=sweep_freq['start'],
                    end_freq_init=sweep_freq['end'],
                    cut_seg=seg_pars['cut seg [%]'], fit_pars=fit_pars))
            # ex SegmentStable
            else:
                segs[key].append(SegmentStable(
                    segment_info, dict_meas, cut_seg=seg_pars['cut seg [%]']))

    return segs, dict_meas


def ex_calib(make_plots=False):
    """
    Example of external_calib and amplitude_calib functions.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots. Defaults to False.

    Returns
    -------
    (dict_meas_amp, dict_meas_pha, dict_meas_amp_cal):
    tuple
        Processed measurement values if `make_plots` is False.
    """
    _, _, _, _, meas_range, _, _ = pars_segment()
    calib_amp = 0.5
    meas_pars = {'Sens ampli': 0.1,
                 'Offset ampli [V]': 0.5,
                 'Sens phase [mV/°]': 1000,
                 'Offset phase [V]': 0}

    # external values
    meas_range['amp'] = np.array(meas_range['amp']) * meas_pars['Sens ampli']
    meas_range['amp'] += meas_pars['Offset ampli [V]']
    meas_range['pha'] = [elem * meas_pars['Sens phase [mV/°]'] / 1000 +
                         meas_pars['Offset phase [V]']
                         for elem in np.array(meas_range['pha'])]

    # Calib
    meas_range['amp'] /= calib_amp

    # ex gen_segments
    dict_meas = ex_gen_segments('dfrt', make_plots=False)

    # ex external_calib
    out = external_calib(dict_meas['amp'], dict_meas['pha'],
                         meas_pars=meas_pars)
    (dict_meas_amp, dict_meas_pha) = out

    # ex amplitude_calib
    dict_meas_amp_cal = [elem * calib_amp for elem in dict_meas_amp]

    if make_plots:
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(3, 2, figsize=figsize, sharex='all')
        fig.sfn = "ex_calib"
        plot_dict = {'title': 'external signal', 'x lab': '',
                     'y lab': 'amplitude (V)', 'fs': 13, 'edgew': 3,
                     'tickl': 5, 'gridw': 1, 'lw': 1}
        tab_dict = {'form': 'b-'}
        plot_graph(ax[0, 0], dict_meas['times'], dict_meas['amp'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'r-'}, 'phase (°)'
        plot_graph(ax[0, 1], dict_meas['times'], dict_meas['pha'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        (tab_dict, plot_dict['title'], plot_dict['y lab']) = \
            ({'form': 'b-'}, 'signal (no calib)', 'amplitude (a.u)')
        plot_graph(ax[1, 0], dict_meas['times'], dict_meas_amp,
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'r-'}, 'phase (°)'
        plot_graph(ax[1, 1], dict_meas['times'], dict_meas_pha,
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        (tab_dict, plot_dict['title'], plot_dict['y lab'], plot_dict['x lab']) \
            = ({'form': 'b-'}, 'signal (calib)', 'amplitude (a.u)', 'time (s)')
        plot_graph(ax[2, 0], dict_meas['times'], dict_meas_amp_cal,
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'r-'}, 'phase (°)'
        plot_graph(ax[2, 1], dict_meas['times'], dict_meas_pha,
                   plot_dict=plot_dict, tabs_dict=tab_dict)

        return [fig]
    else:
        return dict_meas_amp, dict_meas_pha, dict_meas_amp_cal


def ex_cut_function(verbose=False):
    """
    Example of cut_function function.

    Parameters
    ----------
    verbose: bool, optional
        Flag indicating whether to print verbose information. Defaults to False.

    Returns
    -------
    cut_dict: dict
        Dictionary containing the processed measurement values.
    nb_seg_tot: int
        Total number of segments.
    """
    _, sign_pars, _, _, _, _, _ = pars_segment()

    # ex cut_function
    cut_dict, nb_seg_tot = cut_function(sign_pars)

    if verbose:
        print("Total number of segments:", nb_seg_tot)
        print("Cut dictionary:")
        for key, value in cut_dict.items():
            print(f"{key}: {value}")

    return cut_dict, nb_seg_tot


def ex_segments(analysis, mode, make_plots=False):
    """
    Example of Segment object and the functions plt_seg, plt_seg_max,
    plt_seg_fit, plt_seg_stable.

    Parameters
    ----------
    analysis: str
        The type of analysis to perform. Possible values: 'max', 'fit',
        'dfrt', 'single_freq'.
    mode: str
        The mode of operation. Possible values: 'on f', 'off f'.
    make_plots: bool, optional
        Flag indicating whether to generate plots. Defaults to False.

    Returns
    -------
    seg: Segment object
        The selected Segment object based on the analysis and mode.
    """
    assert mode in ['on f', 'off f']

    _, _, _, _, _, fit_pars, _ = pars_segment()
    unit = 'nm'

    segs, _ = list_segs(mode=analysis, nb_seg_str='5')

    if make_plots:
        if analysis == 'max':
            fig = plt_seg_max(segs[mode][4], unit=unit)
        elif analysis == 'fit':
            fig = plt_seg_fit(segs[mode][4], unit=unit,
                              fit_pha=fit_pars['fit pha'])
        elif analysis in ['dfrt', 'single_freq']:
            fig = plt_seg_stable(segs[mode][4], unit=unit)
        else:
            raise IOError('analysis must be: "max", "fit", "single_freq" or '
                          '"dfrt"')
        fig.sfn += f"_{mode}"
        return [fig]
    else:
        return segs[mode][4]


def ex_extract_other_properties(make_plots=False):
    """
    Example of extract_other_properties function

    Parameters
    ----------
    make_plots: bool, optional
        Flag to indicate whether to generate plots or not (default is False)

    Returns
    -------
    fig: plt.figure or dict
        If make_plots is True, returns a list containing the generated figure.
        If make_plots is False, returns a dictionary containing extracted other
        properties.
    """
    # In and out file management + data extraction
    dir_path_in = os.path.join(get_setting("example_root_path_in"), "KNN500n")
    files = [file for file in os.listdir(dir_path_in)
             if file.endswith(".txt")]
    _, sign_pars = csv_meas_sheet_extract(dir_path_in)
    tab_other_properties = {}

    for cont, file in enumerate(files):
        file_path_in = os.path.join(dir_path_in, file)
        dict_meas, _ = data_extraction(file_path_in, mode_dfrt=True,
                                       verbose=False)

        # ex extract_other_properties
        other_properties = extract_other_properties(
            dict_meas, sign_pars['Hold sample (start)'],
            sign_pars['Hold sample (end)'])

        # append other_properties
        if cont == 0:
            tab_other_properties = {key: [] for key in other_properties.keys()}
        for key, value in other_properties.items():
            tab_other_properties[key].append(value)

    if make_plots:
        x_list = range(len(tab_other_properties['height']))
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(3, 2, figsize=figsize, sharex='all')
        fig.sfn = "ex_extract_other_properties"
        plot_dict = {'title': '', 'x lab': 'file index',
                     'y lab': 'height', 'fs': 13, 'edgew': 3,
                     'tickl': 5, 'gridw': 1, 'lw': 1}
        tab_dict = {'form': 'r-'}
        plot_graph(ax[0, 0], x_list, tab_other_properties['height'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'g-'}, 'diff height'
        plot_graph(ax[0, 1], x_list, tab_other_properties['diff height'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'b-'}, 'deflection'
        plot_graph(ax[1, 0], x_list, tab_other_properties['deflection'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'm-'}, 'deflection error'
        plot_graph(ax[1, 1], x_list, tab_other_properties['deflection error'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'c-'}, 'adhesion'
        plot_graph(ax[2, 0], x_list, tab_other_properties['adhesion'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        ax[2, 1].set_visible(False)
        plt.tight_layout()

        return [fig]
    else:
        return tab_other_properties


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "datacube_to_nanoloop_analysis", save_example_exe=True,
        save_test_exe=False)
    figs = []
    figs += ex_calib(make_plots=True)
    ex_cut_function(verbose=True)
    figs += ex_segments('max', 'off f', make_plots=True)
    figs += ex_segments('max', 'on f', make_plots=True)
    figs += ex_segments('fit', 'off f', make_plots=True)
    figs += ex_segments('fit', 'on f', make_plots=True)
    figs += ex_segments('dfrt', 'off f', make_plots=True)
    figs += ex_segments('dfrt', 'on f', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
