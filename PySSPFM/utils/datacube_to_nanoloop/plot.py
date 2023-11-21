"""
Module used for the scripts of sspfm 1st step data analysis
(convert datacube to nanoloop)
    - Plot functions
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.figure import plot_graph, plot_map


def amp_pha_map(seg_tab, dict_meas, index_hold, freq_range=None,
                read_nb_voltages=None, cut_seg=None, mapping_label='',
                unit='a.u', mode='dfrt', colo=None):
    """
    Plot a figure with tip bias, and 2 maps of amplitude and phase with
    frequency for each segment
    García-Zaldívar et al. : « Nanomechanical Measurements of PLZT Ceramic
    during Switching Events ». Ceramics International 48, nᵒ 7 2022.
    https://doi.org/10.1016/j.ceramint.2021.12.222.

    Parameters
    ----------
    seg_tab: list or numpy.array of Segment
        List of segment types
    dict_meas: dict
        All measurements in extracted file
    index_hold: dict
        Index for start and end hold segment
    freq_range: dict, optional
        Dict of min and max frequency of the sweep (in kHz)
    read_nb_voltages: int, optional
        Number of read voltage values
    cut_seg: dict, optional
        Dict of percent cut of the start and end of the segment
    mapping_label: str, optional
        Title of the figure
    unit: str, optional
        Unit label for amplitude measurement:
        - 'a.u' if no calibration is performed
        - 'nm' in the other case
    mode: str, optional
        Operating mode for analysis: four possible modes:
        - 'max': for analysis of the resonance with max peak value
        (frequency sweep in resonance)
        - 'fit': for analysis of the resonance with a SHO fit of the peak
        (frequency sweep in resonance)
        - 'single_freq': for analysis performed at single frequency,
        average of segment (in or out of resonance)
        - 'dfrt': for analysis performed with dfrt, average of segment
    colo: str, optional
        Map coloration ('coolwarm', 'jet' ...)

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    assert mode in ['max', 'fit', 'dfrt', 'single_freq']
    freq_range = freq_range or {'start': 0, 'end': 1}

    time_range = {'start': dict_meas['times'][index_hold['start'][1] + 1],
                  'end': dict_meas['times'][index_hold['end'][0] - 1]}

    # Init figure
    figsize = get_setting("figsize")
    fig, axs = plt.subplots(3, 1, figsize=figsize, sharex='all')
    fig.sfn = f'amp_pha_{mapping_label.replace(" ", "_").lower()}'
    fig.suptitle(mapping_label, fontsize=24, fontweight='heavy')

    # Align graph with maps
    divider = make_axes_locatable(axs[0])
    ax_bis = divider.append_axes("right", size="2%", pad=0.05)
    for direction in ['top', 'bottom', 'left', 'right']:
        ax_bis.spines[direction].set_color('none')
    ax_bis.tick_params(labelbottom=True, labelcolor='w', top=False,
                       bottom=False, left=False, right=False, labelsize=0)

    # Tip bias plotting
    plot_dict = {'x lab': '', 'y lab': 'SS PFM bias [V]', 'fs': 15, 'edgew': 1,
                 'tickl': 2, 'gridw': 1}
    tab_dict = {'form': 'g-'}
    plot_graph(axs[0], dict_meas['times_bias'], dict_meas['tip_bias'],
               plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=False)

    amp_tab, pha_tab = [], []
    for cont, seg in enumerate(seg_tab):
        amp_tab.append(seg.amp_tab_init)
        pha_tab.append(seg.pha_tab_init)

    y_label = {'amp': f'Amplitude [{unit}]', 'pha': 'Phase [°]'}

    for cont, (meas_tab, key) in enumerate(zip(
            [amp_tab, pha_tab], ['amp', 'pha'])):
        # Sub plotting
        extent = [time_range['start'], time_range['end'], freq_range['start'],
                  freq_range['end']]
        if mode in ['dfrt', 'single_freq']:
            y_lab = ''
            axs[1].set_yticklabels('')
            axs[2].set_yticklabels('')
        else:
            y_lab = 'Freq [kHz]'
        plot_dict = {'x lab': '', 'y lab': y_lab}
        colo = colo or get_setting("color_amp_pha_map")
        colorbar_dict = {'lab': y_label[key], 'col': colo}
        plot_map(fig, axs[cont + 1], np.transpose(np.array(meas_tab)),
                 extent=extent, plot_dict=plot_dict,
                 colorbar_dict=colorbar_dict)

    # x-axis range for the plotting
    for ax in [axs[0], axs[1], axs[2]]:
        ax.set_xlim(left=time_range['start'], right=time_range['end'])

    # Each new sspfm tip bias cycle is highlighted
    if (read_nb_voltages, cut_seg) is not None:
        offset = dict_meas['times'][index_hold['start'][1] + 1]
        increment = dict_meas['times'][index_hold['end'][0] - 1] - offset
        for i in range(read_nb_voltages + 1):
            position = i / read_nb_voltages * increment + offset
            delta_freq = freq_range['end'] - freq_range['start']
            freq_start = cut_seg['start'] / 100 * delta_freq
            freq_start += freq_range['start']
            freq_end = freq_range['end'] - cut_seg['end'] / 100 * delta_freq
            axs[0].axvline(position, c='k', ls='--')
            for ax in [axs[1], axs[2]]:
                for elem in [position, freq_start, freq_end]:
                    ax.axvline(elem, c='k', ls='--')

    fig.text(0.5, 0.05, 'Times [s]', fontsize=15, color='black', ha='center')

    return fig


def plt_bias(time_bias_calc, ss_pfm_bias_calc, ss_pfm_bias, dict_meas):
    """
    Plot SS PFM signal calculated

    Parameters
    ----------
    time_bias_calc: list or numpy.array
        Array of time values corresponding to ss_pfm_bias_calc, calculated
        from ss_pfm_bias (in s)
    ss_pfm_bias_calc: list or numpy.array
        Array of voltage values corresponding to time_bias_calc, calculated
        from ss_pfm_bias (in V)
    ss_pfm_bias: list or numpy.array
        Array of SS PFM bias values (in V)
    dict_meas: dict
        All measurements in extracted file

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = 'sspfm_bias'

    if len(dict_meas['tip_bias']) == 0:
        y_tabs = [ss_pfm_bias_calc, np.zeros(len(dict_meas['times']))]
    else:
        y_tabs = [ss_pfm_bias_calc, dict_meas['tip_bias']]

    x_tabs = [time_bias_calc, dict_meas['times']]

    plot_dict = {'title': 'SS PFM Bias', 'x lab': 'Time [s]',
                 'y lab': 'SS PFM BIAS [V]'}

    tab_dict_1 = {'legend': f'sspfm bias calc\nnb seg = {len(ss_pfm_bias)}',
                  'form': 'g-', 'lw': 1}
    tab_dict_2 = {'legend': 'sspfm bias exp', 'form': 'c-', 'lw': 1}

    tabs_dict = [tab_dict_1, tab_dict_2]

    plot_graph(ax, x_tabs, y_tabs, plot_dict=plot_dict, tabs_dict=tabs_dict)

    return fig


def plt_amp(dict_meas, unit='a.u'):
    """
    Plot pfm amplitude signal measured, and SS PFM signal measured if the
    measure is done, for classic (sweep) mode SS PFM

    Parameters
    ----------
    dict_meas: dict
        Dict of all measurements in extracted file
    unit: str, optional
        Unit label for amplitude measurement:
        - 'a.u' if no calibration is performed
        - 'nm' in the other case

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = 'sspfm_bias_amplitude'
    ax2 = ax.twinx()
    plot_dict = {'title': 'SS PFM Signal and Amplitude', 'x lab': 'Time [s]',
                 'y lab': f'Amplitude [{unit}]', 'c y lab': 'b',
                 'y2 lab': 'SS PFM bias [V]', 'c y2 lab': 'g', 'y lw': 1,
                 'z lw': 1}
    tabs_dict = [{'form': 'b-'}, {'form': 'g-'}]
    plot_graph(ax, [dict_meas['times'], dict_meas['times_bias']],
               dict_meas['amp'], ax2=ax2, y2_tabs=dict_meas['tip_bias'],
               plot_dict=plot_dict, tabs_dict=tabs_dict)

    y_lim_plus = 1.1 * max(dict_meas['amp'])
    y_lim_minus = -y_lim_plus
    ax.set_ylim(bottom=y_lim_minus, top=y_lim_plus)

    return fig


def plt_signals(dict_meas, unit='a.u'):
    """
    Plot all the measurements in the same figure

    Parameters
    ----------
    dict_meas: dict
        Dict of all measurements in extracted file
    unit: str, optional
        Unit label for amplitude measurement:
        - 'a.u' if no calibration is performed
        - 'nm' in the other case

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    # Initialize figure
    figsize = get_setting("figsize")
    fig, axs = plt.subplots(4, 1, figsize=figsize, sharex='all')
    fig.sfn = "raw_signals"
    fig.suptitle('\nPhysical Signals in Time', fontsize=24, fontweight='heavy')
    plot_dict = {'x lab': '', 'lw': 1, 'fs': 15, 'edgew': 2, 'tickl': 3,
                 'gridw': 1}
    tab_dict = {}

    # Deflection sub image
    if len(dict_meas['deflection']) > 0:
        plot_dict.update({'y lab': 'Deflection [nm]', 'c y lab': 'm'})
        tab_dict.update({'form': 'm-'})
        plot_graph(axs[0], dict_meas['times'], dict_meas['deflection'],
                   plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=False)

    # Tip bias sub image
    try:
        plot_dict.update({'y lab': 'SS PFM bias [V]', 'c y lab': 'g'})
        tab_dict.update({'form': 'g-'})
        plot_graph(axs[1], dict_meas['times_bias'], dict_meas['tip_bias'],
                   plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=False)
    except KeyError:
        pass

    # Amplitude sub image
    plot_dict.update({'y lab': f'Amplitude [{unit}]', 'c y lab': 'b'})
    tab_dict.update({'form': 'b-'})
    plot_graph(axs[2], dict_meas['times'], dict_meas['amp'],
               plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=False)

    # Phase sub image
    plot_dict.update({'y lab': 'Phase [°]', 'x lab': 'Time [s]',
                      'c y lab': 'r'})
    tab_dict.update({'form': 'r-'})
    plot_graph(axs[3], dict_meas['times'], dict_meas['pha'],
               plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=False)

    return fig


def plt_seg_max(seg, unit='a.u'):
    """
    Plot a segment segment for max sweep analysis

    Parameters
    ----------
    seg: Segment class
        Segment class object
    unit: str, optional
        Unit label for amplitude measurement:
        - 'a.u' if no calibration is performed
        - 'nm' in the other case

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    # Initialize figure
    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = f'segment_{seg.segmentinfo.seg_infos["index"]}_max'
    ax2 = ax.twinx()

    # Plot amplitude and phase segment
    plot_dict = {'title': f'Segment n°{seg.segmentinfo.seg_infos["index"]}',
                 'y lab': f'Amplitude [{unit}]', 'y2 lab': 'Phase [°]',
                 'c y2 lab': 'r', 'c y lab': 'b', 'x lab': 'Frequency [kHz]'}
    tabs_dict = [{'form': 'b-', 'legend': 'amplitude'},
                 {'form': 'r-', 'legend': 'phase'}]
    plot_graph(ax, seg.freq_tab_init, seg.amp_tab_init, ax2=ax2,
               y2_tabs=seg.pha_tab_init, plot_dict=plot_dict,
               tabs_dict=tabs_dict, plot_leg=False)

    # Plot cut domain
    color = cm.Wistia(0.5)
    cut_range = [seg.freq_tab[0], seg.freq_tab[-1]]
    for i in range(2):
        ax.axvline(x=cut_range[i], lw=3, c=color, ls='-.')
    ax.axvspan(cut_range[0], cut_range[1], color=color, alpha=0.2)

    # Plot max amp and pha
    label = f'max: amp={seg.amp:.2f}{unit}, pha={seg.pha:.2f}°, \n' \
            f'          freq={seg.res_freq:.1f}kHz, Q={seg.q_fact:.1f}'
    ax.axvline(x=seg.res_freq, c='k', ls=':', lw=3, label=label)
    ax.plot(seg.res_freq, seg.amp, 'gs', ms=10, mec='k')
    ax2.plot(seg.res_freq, seg.pha, 'rh', ms=10, mec='k')

    # Annotate
    if seg.segmentinfo.seg_infos['type'] == 'read':
        label, col = 'Off field', 'w'
    else:
        label, col = 'On field', 'y'
    label = \
        f'{label}:\nwrite: {seg.segmentinfo.seg_infos["write volt"]:.2f}V,\n' \
        f'read: {seg.segmentinfo.seg_infos["read volt"]:.2f}V'
    fig.legend(fontsize=13, loc='upper right')
    fig.text(0.01, 0.90, label, color=col, fontsize=15, fontweight='heavy',
             backgroundcolor='black')

    return fig


def plt_seg_fit(seg, unit='a.u', fit_pha=False):
    """
    Plot a segment for fit sweep analysis

    Parameters
    ----------
    seg: Segment class
        Segment class object
    unit: str, optional
        Unit label for amplitude measurement:
        - 'a.u' if no calibration is performed
        - 'nm' in the other case
    fit_pha: bool, optional
        True if fit is performed on phase signal

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    # Initialize figure
    figsize = get_setting("figsize")
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex='all', sharey='all',
                                   figsize=figsize)
    fig.sfn = f'segment_{seg.segmentinfo.seg_infos["index"]}_fit'
    ax1b, ax2b = ax1.twinx(), ax2.twinx()

    # Plot amplitude and phase segment
    plot_dict = {'y lab': f'Amplitude [{unit}]', 'y2 lab': 'Phase [°]',
                 'c y2 lab': 'r', 'c y lab': 'b', 'x lab': 'Frequency [kHz]',
                 'fs': 13,
                 'edgew': 3, 'tickl': 5, 'gridw': 1}
    tab_dict_1 = {'form': 'b-', 'legend': 'amplitude'}
    tab_dict_2 = {'form': 'r-', 'legend': 'phase'}
    tabs_dict = [tab_dict_1, tab_dict_2]
    plot_graph(ax1, seg.freq_tab_init, seg.amp_tab_init, ax2=ax1b,
               y2_tabs=seg.pha_tab_init, plot_dict=plot_dict,
               tabs_dict=tabs_dict, plot_leg=False)
    plot_graph(ax2, seg.freq_tab, seg.amp_tab, ax2=ax2b, y2_tabs=seg.pha_tab,
               plot_dict=plot_dict, tabs_dict=tabs_dict, plot_leg=False)

    # Plot cut domain
    color = cm.Wistia(0.5)
    cut_range = [seg.freq_tab[0], seg.freq_tab[-1]]
    for ax in [ax1, ax2]:
        for i in range(2):
            ax.axvline(x=cut_range[i], lw=3, c=color, ls='-.')
        ax.axvspan(cut_range[0], cut_range[1], color=color, alpha=0.2)

    # Plot fit, max amp and pha
    if fit_pha:
        ax2b.plot(seg.freq_tab, seg.pha_best_fit, 'm--', lw=3,
                  label='phase fit')
    label = f'max: amp={seg.amp:.2f}{unit}, pha={seg.pha:.2f}°, ' \
            f'freq={seg.res_freq:.1f}kHz, Q={seg.q_fact:.1f}'
    ax2.axvline(x=seg.res_freq, color='k', ls=':', lw=3, label=label)
    if len(seg.best_fit) > 0:
        ax2.plot(seg.freq_tab, seg.best_fit, 'k--', lw=3, label='sho fit')
    ax2.plot(seg.res_freq, seg.amp + seg.bckgnd, 'gs', ms=10, mec='k')
    ax2b.plot(seg.res_freq, seg.pha, 'rh', ms=10, mec='k')

    # Annotate
    fig.legend(fontsize=13, loc='upper right')
    fig.suptitle(f'Segment n°{seg.segmentinfo.seg_infos["index"]}', fontsize=13)
    if seg.segmentinfo.seg_infos['type'] == 'read':
        label, col = 'Off field', 'w'
    else:
        label, col = 'On field', 'y'
    label = \
        f'{label}:\nwrite: {seg.segmentinfo.seg_infos["write volt"]:.2f}V,\n' \
        f'read: {seg.segmentinfo.seg_infos["read volt"]:.2f}V'
    fig.text(0.01, 0.90, label, color=col, fontsize=15, fontweight='heavy',
             backgroundcolor='black')

    return fig


def plt_seg_stable(seg, unit='a.u'):
    """
    Plot a segment for single frequency or DFRT analysis

    Parameters
    ----------
    seg: Segment class
        Segment class object
    unit: str, optional
        Unit label for amplitude measurement:
        - 'a.u' if no calibration is performed
        - 'nm' in the other case

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    # Initialize figure
    figsize = get_setting("figsize")
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex='all', figsize=figsize)
    fig.sfn = f'segment_{seg.segmentinfo.seg_infos["index"]}_cst'

    # Plot amplitude and phase segment
    plot_dict = {'y lab': f'Amplitude [{unit}]', 'x lab': '', 'fs': 13,
                 'edgew': 3, 'tickl': 5, 'gridw': 1}
    tab_dict = {'form': 'b-', 'legend': 'amplitude'}
    plot_graph(ax1, seg.time_tab_init, seg.amp_tab_init, plot_dict=plot_dict,
               tabs_dict=tab_dict)
    plot_dict['x lab'], plot_dict['y lab'] = 'Time [s]', 'Phase [°]'
    tab_dict = {'form': 'r-', 'legend': 'phase'}
    plot_graph(ax2, seg.time_tab_init, seg.pha_tab_init, plot_dict=plot_dict,
               tabs_dict=tab_dict)

    # Plot cut domain
    color = cm.Wistia(0.5)
    cut_range = [seg.time_tab[0], seg.time_tab[-1]]
    for ax in [ax1, ax2]:
        for i in range(2):
            ax.axvline(x=cut_range[i], lw=3, c=color, ls='-.')
        ax.axvspan(cut_range[0], cut_range[1], color=color, alpha=0.2)
    for elem in [-1, 1]:
        ax1.axhline(y=seg.amp + elem * seg.inc_amp, lw=1, c='c', ls='--')
        ax2.axhline(y=seg.pha + elem * seg.inc_pha, lw=1, c='m', ls='--')

    # Plot amp and pha variation
    label = f'mean amplitude = {seg.amp:.2E}{unit}, ' \
            f'error = {seg.inc_amp:.2E}{unit}'
    ax1.axhline(y=seg.amp, lw=3, c='c', ls='--', label=label)
    ax1.axhspan(seg.amp - seg.inc_amp, seg.amp + seg.inc_amp, alpha=0.2,
                color='cyan')
    label = f'mean phase = {seg.pha:.2f}°, error = {seg.inc_pha:.2f}°'
    ax2.axhline(y=seg.pha, lw=3, c='m', ls='--', label=label)
    ax2.axhline(y=seg.pha + seg.inc_pha, lw=1, c='m', ls='--')
    ax2.axhspan(seg.pha - seg.inc_pha, seg.pha + seg.inc_pha, alpha=0.2,
                color='magenta')

    # Annotate
    fig.legend(fontsize=13, loc='upper right')
    fig.suptitle(f'Segment n°{seg.segmentinfo.seg_infos["index"]}', fontsize=13)
    start = seg.segmentinfo.seg_infos['start time']
    end = seg.segmentinfo.seg_infos['end time']
    ax.set_xticks(np.linspace(seg.time_tab_init[0], seg.time_tab_init[-1], 5))
    ax.set_xticklabels([f'{elem:.2f}' for elem in np.linspace(start, end, 5)])
    if seg.segmentinfo.seg_infos['type'] == 'read':
        label, col = 'Off field', 'w'
    else:
        label, col = 'On field', 'y'
    label = \
        f'{label}:\nwrite: {seg.segmentinfo.seg_infos["write volt"]:.2f}V,\n' \
        f'read: {seg.segmentinfo.seg_infos["read volt"]:.2f}V'
    fig.text(0.01, 0.90, label, color=col, fontsize=15, fontweight='heavy',
             backgroundcolor='black')

    return fig


def plt_seg(dict_meas, hold_dict, index, sign_pars):
    """
    Plot measurement with segment subdivision

    Parameters
    ----------
    dict_meas: dict
        All measurement in extracted file
    hold_dict: dict
        Containing hold segment parameters
    index: dict
        All segment index
    sign_pars: dict
        sspfm bias signal parameters

    Returns
    -------
    fig: plt.figure
        The generated figure
    """
    # Initialize figure
    figsize = get_setting("figsize")
    fig, (ax_1, ax_2) = plt.subplots(2, 1, figsize=figsize)
    fig.suptitle('Cut function analysis', fontsize=24, fontweight='heavy')

    # Plot index nb with time
    ax_1.plot(range(len(dict_meas['times'])), dict_meas['times'], 'g.-')
    ax_1.axvline(0, c='k', ls=':')
    ax_1.axvline(hold_dict['index']['start'][1], c='k', ls=':')
    ax_1.axvspan(0, hold_dict['index']['start'][1], color='grey', alpha=0.5)
    ax_1.axvline(hold_dict['index']['end'][0], c='k', ls=':')
    ax_1.axvline(len(dict_meas['times']) - 1, c='k', ls=':')
    ax_1.axvspan(hold_dict['index']['end'][0], len(dict_meas['times']) - 1,
                 color='grey', alpha=0.5, label='hold segment')
    ax_1.axvspan(hold_dict['index']['start'][1] + 1,
                 hold_dict['index']['end'][0] - 1, color='green',
                 alpha=0.5, label='measurement')

    # Amplitude and phase measure with time cut in segment
    ax_2b = ax_2.twinx()
    ax_2.plot(dict_meas['times'], dict_meas['amp'], 'b.-', label='Amplitude')
    ax_2b.plot(dict_meas['times'], dict_meas['pha'], 'r.-', label='Phase [°]')
    ax_2.axvline(dict_meas['times'][0], c='black', ls=':')
    ax_2.axvline(dict_meas['times'][hold_dict['index']['start'][1]], c='k',
                 ls=':')
    ax_2.axvspan(dict_meas['times'][0],
                 dict_meas['times'][hold_dict['index']['start'][1]],
                 color='grey', alpha=0.5)
    ax_2.axvline(dict_meas['times'][hold_dict['index']['end'][0]], c='k',
                 ls=':')
    ax_2.axvline(dict_meas['times'][len(dict_meas['times']) - 1],
                 c='k', ls=':')
    ax_2.axvspan(dict_meas['times'][hold_dict['index']['end'][0]],
                 dict_meas['times'][len(dict_meas['times']) - 1],
                 color='grey', alpha=0.5)
    ax_2.axvspan(0, 0, color='m', alpha=0.5, label='on field segment')
    ax_2.axvspan(0, 0, color='c', alpha=0.5, label='off field segment')

    for elem in index['on f']:
        ax_2.axvline(dict_meas['times'][elem], c='magenta', ls=':')
        ax_2.axvline(dict_meas['times'][elem + sign_pars['Seg sample (W)']],
                     color='m', ls=':')
        ax_2.axvspan(dict_meas['times'][elem],
                     dict_meas['times'][elem + sign_pars['Seg sample (W)']],
                     color='m', alpha=0.5)

    for elem in index['off f']:
        ax_2.axvline(dict_meas['times'][elem], c='cyan', ls=':')
        ax_2.axvline(dict_meas['times'][elem + sign_pars['Seg sample (R)']],
                     c='c', ls=':')
        ax_2.axvspan(dict_meas['times'][elem],
                     dict_meas['times'][elem + sign_pars['Seg sample (R)']],
                     color='c', alpha=0.5)

    # Legend of the figure
    fig.legend(fontsize=12, loc='upper left')

    return fig
