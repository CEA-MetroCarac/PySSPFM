"""
Module used for the scripts of sspfm 2d step data analysis
(convert nanoloop to hyst)
- plot functions
"""

import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.core.basic_func import linear
from PySSPFM.utils.core.figure import plot_graph, ax_formating
from PySSPFM.utils.nanoloop.plot import add_txt

from PySSPFM.settings import FIGSIZE


def plot_btfly_analysis(write, amp, mini, imprint, dict_str=None):
    """
    Generate figure for butterfly analysis (electrostatic)

    Parameters
    ----------
    write: dict
        Write voltage values for left and right segment (in V)
    amp: dict
        Amplitude values for left and right segment (in a.u or nm)
    mini: dict
        Minimum point on butterfly nanoloop
    imprint: float
        Imprint of butterfly nanoloop (in V)
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    fig: plt.figure
        Figure of butterfly analysis
    """
    unit = dict_str["unit"] if dict_str is not None else ""

    fig, ax = plt.subplots(figsize=FIGSIZE)
    add = dict_str["label"].lower().replace(' ', '_')
    fig.sfn = f'btfly_analysis_{add}'

    plot_dict = {'title': 'imprint: butterfly analysis',
                 'x lab': 'Write voltage [V]',
                 'y lab': f'Amplitude [{unit}]'}
    tab_dict_1 = {'legend': 'amplitude data (left)', 'form': 'r.-'}
    tab_dict_2 = {'legend': 'amplitude data (right)', 'form': 'b.-'}
    plot_graph(ax, [write['left'], write['right']],
               [amp['left'], amp['right']], plot_dict=plot_dict,
               tabs_dict=[tab_dict_1, tab_dict_2], plot_leg=False)

    for x_val, y_val, col, lab in zip(
            [mini['left'], mini['right'], imprint],
            [min(amp['left']), min(amp['right']), 0], ['r', 'b', 'g'],
            ['min left seg', 'min right seg', 'imprint']):
        ax.axvline(x=x_val, c=col, ls=':')
        ax.plot(x_val, y_val, marker='h', ls=':', c=col, ms=7, mew=1.0,
                mec='k', label=f'{lab} = {x_val:.2f}V')

    text = '(Valid only for On Field measurement)\n' \
           '(imprint = CPD for dominant electrostatic contribution)'
    fig.text(0.01, 0.95, text, size=15)
    if dict_str:
        add_txt(fig, dict_str)
    fig.legend(fontsize=13, loc='upper right')

    return fig


def plot_sat_analysis(write, amp, piezorep, a_elec, y_0, x_0, r_square, sat,
                      ind_sat_right, ind_sat_left, y_fit, elec_fit,
                      dict_str=None):
    """
    Generate figures for saturation analysis (electrostatic)

    Parameters
    ----------
    write: dict
        Dict of write voltage values for left and right segment (in V)
    amp: dict
        Dict of amplitude values for left and right segment (in a.u or nm)
    piezorep: dict
        Dict of piezoresponse values for left and right segment (in a.u or nm)
    a_elec: float
        Slope of affine electrostatic component: y_elec = a_elec*U+y_0
    y_0: float
        Offset of affine electrostatic component: y_elec = a_elec*U+y_0
    x_0: float
        y_elec(x_0)=0: can correspond to CPD
    r_square: float
        R² of saturation line regression
    sat: dict
        Dict of left and right results of linear regression for saturation of
        the nanoloop
    ind_sat_right: int
        Index corresponding to the right saturation of the nanoloop
    ind_sat_left: int
        Index corresponding to the left saturation of the nanoloop
    y_fit: dict
        Dict corresponding to the fit of left, right and mean containing the
        list of point of the fit
    elec_fit: dict
        Dict of left and right mean results of linear regression for
        saturation of the nanoloop
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    figs_sat: list(2) of plt.figure
        - fig: plt.figure
            1st figure (saturation analysis on butterfly ->
            1st step of the treatment)
        - fig2: plt.figure
            2nd figure (saturation analysis on hysteresis ->
            2nd step of the treatment)
    """
    unit = dict_str["unit"] if dict_str is not None else ""

    # Init figure
    fig, axs = plt.subplots(1, 2, figsize=FIGSIZE, sharex='all', sharey='all')
    add = dict_str["label"].lower().replace(' ', '_')
    fig.sfn = f'sat_analysis_fig1_{add}'

    # Plot butterfly
    plot_dict = {'x lab': 'Write voltage [V]',
                 'y lab': f'Amplitude [{unit}]',
                 'edgew': 3, 'tickl': 5, 'gridw': 1}
    tab_dict_1 = {'legend': 'amplitude data (left)', 'form': 'r.',
                  'mec': 'r', 'ms': 2}
    tab_dict_2 = {'legend': 'amplitude data (right)', 'form': 'b.',
                  'mec': 'b', 'ms': 2}
    plot_graph(axs[0], [write['left'], write['right']],
               [amp['left'], amp['right']], plot_dict=plot_dict,
               tabs_dict=[tab_dict_1, tab_dict_2], plot_leg=False)

    # Plot piezorep nanoloop
    plot_dict['y lab'] = f'Piezoresponse [{unit}]'
    tab_dict_1 = {'legend': 'piezorep data (left)', 'form': 'r+',
                  'mec': 'r', 'ms': 5}
    tab_dict_2 = {'legend': 'piezorep data (right)', 'form': 'b+',
                  'mec': 'b', 'ms': 5}
    plot_graph(axs[1], [write['left'], write['right']],
               [piezorep['left'], piezorep['right']], plot_dict=plot_dict,
               tabs_dict=[tab_dict_1, tab_dict_2], plot_leg=False)

    # Plot linear regression on butterfly and piezorep nanoloop
    for key, form in zip(['left', 'right'], ['m-', 'c-']):
        axs[0].plot(sat[key]['x fit'], sat[key]['y fit'], form, lw=3)
    axs[0].axvspan(write['right'][0], write['right'][ind_sat_right],
                   color='c',
                   alpha=0.3, ls='-.', lw=1, label='right sat domain')
    axs[0].axvspan(write['left'][0], write['left'][ind_sat_left], color='m',
                   alpha=0.3, ls='-.', lw=1, label='left sat domain')
    axs[1].axvspan(write['right'][0], write['right'][ind_sat_right],
                   color='c',
                   alpha=0.3, ls='-.', lw=1)
    axs[1].axvspan(write['left'][0], write['left'][ind_sat_left], color='m',
                   alpha=0.3, ls='-.', lw=1)
    for key, form, label in zip(['left', 'right'], ['m-', 'c-'],
                                ['left linereg', 'right linereg']):
        axs[1].plot(write[key], y_fit[key], form, lw=3, label=label)
    axs[1].plot(elec_fit['x fit'], elec_fit['y fit'], 'g--', lw=3,
                label='electrostatic fit')

    # Annotate
    title = 'Electrostatic component: saturation domain analysis'
    fig.suptitle(title, size=15)
    fig.text(0.01, 0.95, '(Valid only for On Field measurement)',
             size=15)
    if dict_str:
        add_txt(fig, dict_str)
    fig.legend(fontsize=13, loc='upper right')

    # Init figure
    fig2, ax = plt.subplots(figsize=FIGSIZE)
    add = dict_str["label"].lower().replace(' ', '_')
    fig2.sfn = f'sat_analysis_fig2_{add}'

    # Plot piezoresponse nanoloop with saturation analysis
    plot_dict = {'title': title, 'x lab': 'Write voltage [V]',
                 'y lab': f'Piezoresponse [{unit}]'}
    tab_dict_1 = {'legend': 'piezorep data (left)', 'form': 'r.-'}
    tab_dict_2 = {'legend': 'piezorep data (right)', 'form': 'b.-'}
    tab_dict_3 = {'legend': 'linereg sat (left)', 'form': 'm:'}
    tab_dict_4 = {'legend': 'linereg sat (right)', 'form': 'c:'}
    lab = f'fit : ({a_elec:.2e})*x+({y_0:.2e})\nR² = {r_square:.5f}'
    tab_dict_5 = {'legend': lab, 'form': 'g--'}
    x_tabs = [write['left'], write['right'], write['left'], write['right'],
              elec_fit['x fit']]
    y_tabs = [piezorep['left'], piezorep['right'], y_fit['left'],
              y_fit['right'], elec_fit['y fit']]
    tabs_dict = [tab_dict_1, tab_dict_2, tab_dict_3, tab_dict_4, tab_dict_5]
    plot_graph(ax, x_tabs, y_tabs, plot_dict=plot_dict,
               tabs_dict=tabs_dict, plot_leg=False)

    # Plot x_0 info
    ax.axhline(y=0, ls=':', c='k')
    ax.plot(x_0, 0, marker='h', c='g', ms=7, mew=1.0, mec='k', ls=':',
            label=f'x_0 = {x_0:.2f} V')
    ax.axvline(x=x_0, c='g', ls=':')

    # Annotate
    if dict_str:
        add_txt(fig2, dict_str)
    fig2.text(0.01, 0.95, '(Valid only for On Field measurement)', size=15)
    fig2.legend(fontsize=13, loc='upper right')

    return [fig, fig2]


def plot_offset_analysis(a_elec, y_0, x_0, r_square, read_volt, elec_fit,
                         offset, dict_str=None):
    """
    Generate figure for offset analysis (electrostatic)

    Parameters
    ----------
    a_elec: float
        Slope of affine electrostatic component: y_elec = a_elec*U+y_0
    y_0: float
        Offset of affine electrostatic component: y_elec = a_elec*U+y_0
    x_0: float
        y_elec(x_0)=0: can correspond to CPD
    r_square: float
        R² of saturation line regression
    read_volt: list(n) or numpy.array(n) of float
        Array of read voltage value (in V)
    elec_fit: dict
        Results of linear regression for electrostatic component
    offset: list(n) or numpy.array(n) of float
        Array of hysteresis offset value (in a.u or nm)
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    fig: plt.figure
        Figure of offset analysis
    """
    unit = dict_str["unit"] if dict_str is not None else ""

    fig, ax = plt.subplots(figsize=FIGSIZE)
    add = dict_str["label"].lower().replace(' ', '_')
    fig.sfn = f'offset_analysis_{add}'

    title = 'Electrostatic component: offset analysis'
    plot_dict = {'title': title, 'x lab': 'Read voltage [V]',
                 'y lab': f'Hyst offset [{unit}]'}
    lab = f'fit : ({a_elec:.2e})*x+({y_0:.2e})\nR² = {r_square:.5f}'
    tab_dict_1 = {'legend': 'data', 'form': 'm-o'}
    tab_dict_2 = {'legend': lab, 'form': 'g--'}
    plot_graph(ax, [read_volt, elec_fit['x fit']], [offset, elec_fit['y fit']],
               plot_dict=plot_dict, tabs_dict=[tab_dict_1, tab_dict_2],
               plot_leg=False)

    ax.axhline(y=0, c='k', ls=':', lw=2)
    ax.axvline(x=x_0, c='g', ls=':', lw=2)
    ax.plot(x_0, 0, 'gh:', ms=7, mew=1.0, mec='k', lw=2,
            label=f'x_0 = {x_0:.2f} V')

    fig.legend(fontsize=13, loc='upper right')
    text = '(multiple Off Field measurement with different read voltage)'
    fig.text(0.01, 0.95, text, size=15)
    if dict_str:
        add_txt(fig, dict_str)

    return fig


def plot_differential_analysis(write_volt_left, write_volt_right, diff_fit,
                               diff_piezorep_left, diff_piezorep_right,
                               diff_piezorep_mean, diff_piezorep_grad, a_diff,
                               y_0_diff, r_square, bias_min=-5., bias_max=5.,
                               dict_str=None):
    """
    Generate figure for differential analysis

    Parameters
    ----------
    write_volt_left: list(n) or numpy.array(n) of float
        Array of write voltage values for left segment (in V)
    write_volt_right: list(n) or numpy.array(n) of float
        Array of write voltage values for right segment (in V)
    diff_fit: dict
        Dict of results of linear regression for mean (left and right)
        piezoresponse(write voltage)
    diff_piezorep_left: list(n) or numpy.array(n) of float
        Array of diff piezoresponse values for left segment (in a.u or nm)
    diff_piezorep_right: list(n) or numpy.array(n) of float
        Array of diff piezoresponse values for right segment (in a.u or nm)
    diff_piezorep_mean: list(n) or numpy.array(n/2) of float
        Array of mean (left and right) diff piezoresponse values (in a.u or nm)
    diff_piezorep_grad: list(n) or numpy.array(n) of float
        Array of mean (left and right) differential piezoresponse values
        derivative (in a.u or nm)
    a_diff: float
        Slope of differential analysis: y_diff = a_diff*x+y_0_diff:
        should be equal to a_elec (slope of electrostatic component:
        y_elec = a_elec*U+y_0)
    y_0_diff: float
        Offset of differential analysis: y_diff = a_diff*x+y_0_diff:
        should be equal to 0
    r_square: float
        R² of differential line regression
    bias_min: float, optional
        Initial minimum value of write voltage axis range for the differential
        analysis (in V)
    bias_max: float, optional
        Initial maximum value of write voltage axis range for the differential
        analysis (in V)
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    fig: plt.figure
        Figure of differential analysis
    """
    unit = dict_str["unit"] if dict_str is not None else ""

    # Create the figure and axes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGSIZE, sharex='all')
    fig.sfn = 'differential_analysis'

    # Plot differential analysis
    title = 'Electrostatic component: differential analysis'
    plot_dict = {'title': title, 'x lab': '',
                 'y lab': f'Piezo Response [{unit}]',
                 'edgew': 3, 'tickl': 5, 'gridw': 1}

    # Tab dictionaries for plotting
    tab_dict_1 = {'legend': 'piezoresponse data (left)', 'form': 'r-.',
                  'lw': 1}
    tab_dict_2 = {'legend': 'piezoresponse data (right)', 'form': 'b-.',
                  'lw': 1}
    tab_dict_3 = {'legend': 'mean piezoresponse', 'form': 'm.-'}
    lab = f'fit : ({a_diff:.2e})*x+({y_0_diff:.2e})\nR² = {r_square:.5f}'
    tab_dict_4 = {'legend': lab, 'form': 'g--'}

    # Data for plotting
    x_tabs = [write_volt_left, write_volt_right, write_volt_right,
              diff_fit['x fit']]
    y_tabs = [diff_piezorep_left, diff_piezorep_right, diff_piezorep_mean,
              diff_fit['y fit']]
    tabs_dict = [tab_dict_1, tab_dict_2, tab_dict_3, tab_dict_4]

    # Plot the graph
    plot_graph(ax1, x_tabs, y_tabs, plot_dict=plot_dict,
               tabs_dict=tabs_dict, plot_leg=False)
    ax1.axvline(x=bias_min, c='g', ls=':', lw=2,
                label='linear domain for \ndifferential analysis')
    ax1.axvline(x=bias_max, c='g', ls=':', lw=2)

    # Plot derivative piezoresponse
    plot_dict = {'x lab': 'Write voltage [V]',
                 'y lab': f'Gradient piezoresponse [{unit}]',
                 'form': 'g.-', 'legend': 'gradient piezoresponse',
                 'edgew': 3, 'tickl': 5, 'gridw': 1}

    plot_graph(ax2, write_volt_right, diff_piezorep_grad, plot_dict=plot_dict,
               plot_leg=False)
    ax2.axvline(x=bias_min, c='g', ls=':', lw=2)
    ax2.axvline(x=bias_max, c='g', ls=':', lw=2)

    # Annotate the figure
    fig.legend(fontsize=13, loc='upper right')
    if dict_str:
        add_txt(fig, {"index": dict_str["index"]})

    return fig


def plot_nanoloop_on_off(loop_on, loop_off, dict_str=None):
    """
    Plot on and off field amplitude and piezoresponse nanoloop

    Parameters
    ----------
    loop_on: MeanLoop or MultiLoop class
        MeanLoop or MultiLoop class object, On Field loop
    loop_off: MeanLoop or MultiLoop class
        MeanLoop or MultiLoop class object, Off Field loop
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    fig: plt.figure
        Figure of on and off field amplitude and piezoresponse loop
    """
    # Extract unit and index from dict_str if available, otherwise set them
    # to default values
    unit = dict_str["unit"] if dict_str else ""
    index = dict_str["index"] if dict_str else 0

    # Create the figure and axes
    fig, axs = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.sfn = 'on_off_field'

    # Plot butterfly loop
    plot_dict = {'x lab': 'Write voltage [V]', 'edgew': 3, 'tickl': 5,
                 'gridw': 1}
    tab_dict_1 = {'form': 'k-o', 'ms': 2, 'mec': 'k', 'lw': 1}
    tab_dict_2 = {'form': 'r-o', 'ms': 2, 'mec': 'r', 'lw': 1}
    x_tabs = [loop_off.write_volt, loop_on.write_volt]
    y_tabs = [loop_off.amp, loop_on.amp]
    tabs_dict = [tab_dict_1, tab_dict_2]
    plot_graph(axs[0], x_tabs, y_tabs, plot_dict=plot_dict, tabs_dict=tabs_dict,
               plot_leg=False)

    # Plot piezoresponse hysteresis loop
    plot_dict['y lab'] = f'Piezo Response [{unit}]'
    tab_dict_1 = {'form': 'k-s', 'ms': 2, 'mec': 'k', 'lw': 1}
    tab_dict_2 = {'form': 'r-s', 'ms': 2, 'mec': 'r', 'lw': 1}
    y_tabs = [loop_off.piezorep, loop_on.piezorep]
    plot_graph(axs[1], x_tabs, y_tabs, plot_dict=plot_dict,
               tabs_dict=[tab_dict_1, tab_dict_2], plot_leg=False)

    # Add annotations
    fig.suptitle('On and Off Field analysis', size=15)
    axs[0].plot([], [], 'k-', lw=2, label='Off field')
    axs[0].plot([], [], 'r-', lw=2, label='On field')
    fig.legend(fontsize=13, loc='upper right')
    if dict_str:
        fig.text(0.01, 0.80, f'file n°{index}', size=15, weight='heavy')

    return fig


def plot_hysteresis(best_hyst, x_hyst, y_hyst, bckgnd=None, infl_threshold=10,
                    sat_threshold=90, dict_str=None):
    """
    Generate hysteresis analysis figure (fit + properties + data)

    Parameters
    ----------
    best_hyst: Hysteresis object
        Hysteresis object associated to the best hysteresis (minimum of
        electrostatic component or mean of all hysteresis depending on analysis)
    x_hyst: list(2*n) of float
        List of left and right array of hysteresis data corresponding to write
        voltage for best_hyst (V)
    y_hyst: list(2*n) of float
        List of left and right array of hysteresis corresponding to
        piezoresponse for best_hyst (a.u or nm)
    bckgnd: str, optional
        Keyword to take into account baseline in the hysteresis model among
        ('linear', 'offset', None)
    infl_threshold: float, optional
        Threshold (in %) of derivative amplitude of hysteresis fit function
        (sigmoid, arctan ...) used for nucleation bias analysis
    sat_threshold: float, optional
        Threshold related amplitude of hysteresis to consider for the 'x'
        axis saturation domain determination (in %)
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    fig: plt.figure
        Figure of hysteresis analysis (fit and properties hysteresis plotting)
    """
    # Extract unit from dict_str if available, otherwise set it to an empty
    # string
    unit = dict_str["unit"] if dict_str else ""

    # Create the figure and axes
    fig, [ax0, ax1] = plt.subplots(1, 2, figsize=FIGSIZE)
    add = dict_str["label"].lower().replace(' ', '_')
    fig.sfn = f'hysteresis_fit_{add}'

    # Plot loop data and fit characteristics (with background)
    best_hyst.plot(x_hyst, y=y_hyst, ax=ax0,
                   labels=['branch1 (fit)', 'branch2 (fit)'])
    best_hyst.properties(infl_threshold=infl_threshold,
                         sat_threshold=sat_threshold, bckgnd=bckgnd)
    best_hyst.plot_properties(x_hyst, ax=ax0, plot_dict={'fs': 8},
                              plot_hyst=False, bckgnd=bckgnd)
    ax_formating(ax0, edge=True, grid=True, plt_leg=True, edgew=3., fntsz=8.,
                 tickl=6., gridw=1.,
                 title='Hysteresis with background', xlab='Write Voltage [V]',
                 ylab=f'Piezoresponse [{unit}]')

    # Plot loop data and fit characteristics (without background)
    best_hyst.plot(x_hyst, y=y_hyst, ax=ax1,
                   labels=['branch1 (fit)', 'branch2 (fit)'])
    best_hyst.properties(infl_threshold=infl_threshold,
                         sat_threshold=sat_threshold)
    ax1.plot(x_hyst[0], linear(np.array(x_hyst[0]),
                               slope=best_hyst.params['slope'].value,
                               offset=best_hyst.params['offset'].value),
             'g--', label='bckgnd')
    best_hyst.plot_properties(x_hyst, ax=ax1, plot_dict={'fs': 8})
    ax_formating(ax1, edge=True, grid=True, plt_leg=True, edgew=3., fntsz=8.,
                 tickl=6., gridw=1.,
                 title='Hysteresis without background',
                 xlab='Write Voltage [V]', ylab=f'Piezoresponse [{unit}]')

    if dict_str:
        add_txt(fig, dict_str)

    return fig
