"""
Example of analysis methods
"""
import numpy as np
import matplotlib.pyplot as plt

from examples.utils.datacube_to_nanoloop.ex_gen_data import \
    ex_gen_segments, pars_segment
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.datacube_to_nanoloop.plot import \
    plt_seg_max, plt_seg_fit, plt_seg_dfrt
from PySSPFM.utils.datacube_to_nanoloop.analysis import \
    Segment, zi_calib, init_parameters

from PySSPFM.settings import FIGSIZE


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
            # ex Segment
            segs[key].append(Segment(start_ind, end_ind, dict_meas,
                                     sweep_freq['start'], sweep_freq['end'],
                                     write_volt=read_volt, read_volt=write_volt,
                                     type_seg=type_seg,
                                     mode=seg_pars['mode'], numb=i,
                                     cut_seg=seg_pars['cut seg [%]'],
                                     fit_pars=fit_pars))

    return segs, dict_meas


def ex_calib(make_plots=False):
    """
    Example of zi_calib and amplitude_calib functions.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots. Defaults to False.

    Returns
    -------
    (dict_meas_dfrt_amp_zi, dict_meas_dfrt_pha_zi, dict_meas_dfrt_amp_cal):
    tuple
        Processed measurement values if `make_plots` is False.
    """
    _, _, _, _, meas_range, _, _ = pars_segment()
    calib_amp = 0.5
    meas_pars = {'Sens 1': 0.1,
                 'Offset 1 [V]': 0.5,
                 'Sens 2 [mV/°]': 1000,
                 'Offset 2 [V]': 0}

    # ZI values
    meas_range['amp'] = np.array(meas_range['amp']) * meas_pars['Sens 1']
    meas_range['amp'] += meas_pars['Offset 1 [V]']
    meas_range['pha'] = [elem * meas_pars['Sens 2 [mV/°]'] / 1000 +
                         meas_pars['Offset 2 [V]']
                         for elem in np.array(meas_range['pha'])]

    # Calib
    meas_range['amp'] /= calib_amp

    # ex gen_segments
    dict_meas = ex_gen_segments('dfrt', make_plots=False)

    # ex zi_calib
    out = zi_calib(dict_meas['amp'], dict_meas['pha'], meas_pars=meas_pars)
    (dict_meas_dfrt_amp_zi, dict_meas_dfrt_pha_zi) = out

    # ex amplitude_calib
    dict_meas_dfrt_amp_cal = [elem * calib_amp for elem in
                              dict_meas_dfrt_amp_zi]

    if make_plots:
        fig, ax = plt.subplots(3, 2, figsize=FIGSIZE, sharex='all')
        fig.sfn = "ex_calib"
        plot_dict = {'title': 'zi signal', 'x lab': '',
                     'y lab': 'amplitude zi (V)', 'fs': 13, 'edgew': 3,
                     'tickl': 5, 'gridw': 1, 'lw': 1}
        tab_dict = {'form': 'b-'}
        plot_graph(ax[0, 0], dict_meas['times'], dict_meas['amp'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'r-'}, 'phase (°)'
        plot_graph(ax[0, 1], dict_meas['times'], dict_meas['pha'],
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        (tab_dict, plot_dict['title'], plot_dict['y lab']) = \
            ({'form': 'b-'}, 'signal (no calib)', 'amplitude (a.u)')
        plot_graph(ax[1, 0], dict_meas['times'], dict_meas_dfrt_amp_zi,
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'r-'}, 'phase (°)'
        plot_graph(ax[1, 1], dict_meas['times'], dict_meas_dfrt_pha_zi,
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        (tab_dict, plot_dict['title'], plot_dict['y lab'], plot_dict['x lab']) \
            = ({'form': 'b-'}, 'signal (calib)', 'amplitude (a.u)', 'time (s)')
        plot_graph(ax[2, 0], dict_meas['times'], dict_meas_dfrt_amp_cal,
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict, plot_dict['y lab'] = {'form': 'r-'}, 'phase (°)'
        plot_graph(ax[2, 1], dict_meas['times'], dict_meas_dfrt_pha_zi,
                   plot_dict=plot_dict, tabs_dict=tab_dict)

        return [fig]
    else:
        return (dict_meas_dfrt_amp_zi, dict_meas_dfrt_pha_zi,
                dict_meas_dfrt_amp_cal)


def ex_init_parameters(make_plots=False, verbose=False):
    """
    Example of init_parameters function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots. Defaults to False.
    verbose: bool, optional
        Flag indicating whether to print verbose information. Defaults to False.

    Returns
    -------
    cut_dict: dict
        Dictionary containing the processed measurement values.
    sign_pars['Mode (R)']: str
        The value of 'Mode (R)' in the `sign_pars` dictionary after
        initialization.
    """
    _, sign_pars, _, _, _, _, _ = pars_segment()
    dict_meas = ex_gen_segments('dfrt', make_plots=False)

    if verbose:
        print('- ex init_parameters:')
        print(f'read mode before init_parameters: {sign_pars["Mode (R)"]}')

    # ex init_parameters
    cut_dict, sign_pars['Mode (R)'] = init_parameters(dict_meas, sign_pars,
                                                      verbose=verbose,
                                                      make_plots=make_plots)

    if verbose:
        print(f'read mode after init_parameters: {sign_pars["Mode (R)"]}')

    if make_plots:
        fig = cut_dict['fig']
        fig.sfn = "ex_init_parameters"
        return [fig]
    else:
        return cut_dict, sign_pars['Mode (R)']


def ex_segments(analysis, mode, make_plots=False):
    """
    Example of Segment object and the functions plt_seg, plt_seg_max,
    plt_seg_fit, plt_seg_dfrt.

    Parameters
    ----------
    analysis: str
        The type of analysis to perform. Possible values: 'max', 'fit', 'dfrt'.
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
        elif analysis == 'dfrt':
            fig = plt_seg_dfrt(segs[mode][4], unit=unit)
        else:
            raise IOError('analysis must be: "max", "fit" or "dfrt"')
        fig.sfn += f"_{mode}"
        return [fig]
    else:
        return segs[mode][4]


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "datacube_to_nanoloop_analysis", save_example_exe=True,
        save_test_exe=False)
    figs = []
    figs += ex_calib(make_plots=True)
    figs += ex_init_parameters(make_plots=True, verbose=True)
    figs += ex_segments('max', 'off f', make_plots=True)
    figs += ex_segments('max', 'on f', make_plots=True)
    figs += ex_segments('fit', 'off f', make_plots=True)
    figs += ex_segments('fit', 'on f', make_plots=True)
    figs += ex_segments('dfrt', 'off f', make_plots=True)
    figs += ex_segments('dfrt', 'on f', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
