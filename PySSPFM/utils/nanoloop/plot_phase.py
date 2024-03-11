"""
Module used for phase analysis: - plot functions
"""

import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.figure import plot_graph


def histo_init(filtered_phase, dict_str=None, make_plots=False):
    """
    Initialize the histogram figure and data

    Parameters
    ----------
    filtered_phase: numpy.array(m=n-nb_err) or list(m=n-nb_-nb_err) of float
        Array of phase values with deleted errors (None values) (in °)
    dict_str: dict, optional
        Dict used for figure annotation
    make_plots: bool, optional
        Activation key for matplotlib figures generation

    Returns
    -------
    fig: plt.figure
        Figure of the histogram (generated when make_plots=True)
    ax: plt.axes
        Axes of the figure
    hist_vect: numpy.array(int(m/4)) or list(int(m/4)) of float
        Array of x values for histogram (in °)
    hist: numpy.array(int(m/4)) or list(int(m/4)) of int
        Array of y values for histogram: count
    """
    mode = dict_str["label"] if dict_str else 'Off field'

    discret = int(len(filtered_phase) / 4)
    hist_vect = np.linspace(min(filtered_phase), max(filtered_phase),
                            discret + 1)
    hist, _ = np.histogram(filtered_phase, bins=hist_vect)

    fig, ax = [], []
    if make_plots:
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(figsize=figsize)
        add = mode.lower().replace(' ', '_')
        fig.sfn = f'histo_phase_{add}'
        plot_dict = {'title': 'Histogram phase', 'x lab': 'Phase (°)',
                     'y lab': 'Count', 'lw': 1}
        tabs_dict = {'form': 'c.-', 'legend': 'phase repartition'}
        plot_graph(ax, hist_vect[:-1], hist, plot_dict=plot_dict,
                   tabs_dict=tabs_dict, plot_leg=True)
        if dict_str:
            add_txt(fig, dict_str)

    return fig, ax, hist_vect[:-1], hist


def refocused_phase_histo(ax_hist, hist_vect, hist, phase_offset_val,
                          make_plots=False):
    """
    Refocused and plot phase histogram

    Parameters
    ----------
    ax_hist: plt.Axes
        Histogram axes
    hist_vect: list
        Phase values
    hist: list
        Histogram values
    phase_offset_val: float
        Phase offset value
    make_plots: bool, optional
        Flag to indicate whether to make plots (default is False)

    Returns
    -------
    None
    """
    slided_vector = [[], []]
    static_vector = [[], []]
    key = 0
    for val_x, val_y in zip(hist_vect, hist):
        if val_x - phase_offset_val < -180:
            slided_vector[0].append(val_x + 360)
            slided_vector[1].append(val_y)
            key = 1
        elif val_x - phase_offset_val > 180:
            slided_vector[0].append(val_x - 360)
            slided_vector[1].append(val_y)
            key = 2
        else:
            static_vector[0].append(val_x)
            static_vector[1].append(val_y)

    if key == 1:
        new_histo = \
            [np.concatenate([static_vector[0], slided_vector[0]]),
             np.concatenate([static_vector[1], slided_vector[1]])]
    elif key == 2:
        new_histo = \
            [np.concatenate([slided_vector[0], static_vector[0]]),
             np.concatenate([slided_vector[1], static_vector[1]])]
    else:
        new_histo = [static_vector[0], static_vector[1]]

    if new_histo is not None and make_plots:
        ax_hist.plot(new_histo[0], new_histo[1], '.-', label="refocused histo",
                     color='orange')
        ax_hist.legend()


def annotate_histo(fig_hist, ax_hist, dict_pha, bias_pha_meas, bias_pola_target,
                   hist, nb_peaks, reverted, diff_phase_max=None,
                   diff_phase_fit=None):
    """
    Annotate phase histogram with result of analysis

    Parameters
    ----------
    fig_hist: plt.figure
        Figure of phase histogram
    ax_hist: plt.axes
        Axes of the phase histogram
    dict_pha: dict
        Used for phase calibration
    bias_pha_meas: dict
        Dictionary containing bias and phase value measured
    bias_pola_target: dict
        Dictionary containing bias and polarisation target
    hist: numpy.array
        Histogram data
    nb_peaks: int
        Number of peaks in phase histogram
    reverted: float
        Reverted phase value
    diff_phase_max: float, optional
        Phase difference determined with peak maximum (default is None)
    diff_phase_fit: float, optional
        Phase difference determined with peak fit (default is None)

    Returns
    -------
    None
    """
    if dict_pha["grounded tip"]:
        pola_pha_meas = {"down": bias_pha_meas["low"],
                         "up": bias_pha_meas["high"]}
    else:
        pola_pha_meas = {"up": bias_pha_meas["low"],
                         "down": bias_pha_meas["high"]}

    pola_bias_target = {value: key for key, value in
                        bias_pola_target.items()}
    if nb_peaks >= 2:
        for annot, value in pola_pha_meas.items():
            txt = str(annot) + f" pola\n{pola_bias_target[annot]} bias"
            ax_hist.text(value, np.mean(hist), txt, c='r', size=15,
                         weight='heavy', ha='center', va='top')
    diff_phase_target = abs(dict_pha["pha rev"] - dict_pha["pha fwd"])
    try:
        txt = f'diff phase with fit = {diff_phase_fit:.1f} ' \
              f'(expected = {diff_phase_target:.1f})'
        fig_hist.text(0.65, 0.95, txt, c='g', size=15, weight='heavy')
    except (ValueError, TypeError):
        pass
    try:
        txt = f'diff phase without fit = {diff_phase_max:.1f} ' \
              f'(expected = {diff_phase_target:.1f})'
        fig_hist.text(0.65, 0.98, txt, c='g', size=15, weight='heavy')
    except (ValueError, TypeError):
        pass
    fig_hist.text(0.72, 0.02, f'Reverted phase value: {reverted}',
                  c='c', size=15, weight='heavy')


def plot_phase_bias_grad(reduced_write_voltage, mean_pha, grad_mean_pha,
                         positive_pha_grad, mode, bias_pola_target=None,
                         bias_pha_target=None, dict_str=None):
    """
    Plot phase bias gradient.

    Parameters
    ----------
    reduced_write_voltage: array-like
        Reduced write voltage
    mean_pha: array-like
        Mean phase values
    grad_mean_pha: array-like
        Gradient of mean phase values
    positive_pha_grad: bool
        Flag indicating positive phase gradient
    mode: str
        Measurement mode: 'On field' or 'Off field'
    bias_pola_target: dict, optional
        Dictionary containing bias and polarisation target (default is None)
    bias_pha_target: dict, optional
        Dictionary containing bias and phase target (default is None)
    dict_str: dict, optional
        Dictionary of annotations for the plot (default is None)

    Returns
    -------
    fig: plt.figure
    """
    figsize = get_setting("figsize")
    fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize=figsize)
    add = mode.lower().replace(' ', '_')
    fig.sfn = f'phase_analysis_{add}'
    fig.suptitle('Phase up & down analysis', size=24, weight='heavy')
    plot_dict = {'form': 'r+-', 'fs': 13, 'edgew': 3, 'tickl': 5,
                 'gridw': 1, 'title': 'Phase repartition with voltage',
                 'y lab': 'Mean phase [°]', 'x lab': 'Write voltage [V]'}
    plot_graph(ax_1, reduced_write_voltage, mean_pha, plot_dict=plot_dict)

    if bias_pola_target is not None:
        # Arrow for polarisation and phase target
        x_rel = 0.5
        delta_x_rel = 0.4
        y_rel = 0.5
        arrowstyle = '->, head_length=1.5, head_width=1.5'
        arrow_props = {"edgecolor": 'red', "arrowstyle": arrowstyle,
                       "linewidth": 10, "relpos": (0.5, 0.5)}
        len_x = ax_1.get_xlim()[1] - ax_1.get_xlim()[0]
        len_y = ax_1.get_ylim()[1] - ax_1.get_ylim()[0]
        x_text = ax_1.get_xlim()[0] + x_rel * len_x
        y_text = ax_1.get_ylim()[0] + y_rel * len_y
        delta_x = delta_x_rel * len_x
        x_arrow = x_text
        y_arrow = y_text
        txt = f"Polarization {bias_pola_target['low']}"
        if bias_pha_target is not None:
            txt += f"\n({bias_pha_target['low']} °)"
        ax_1.annotate(txt, xy=(x_text - delta_x, y_text),
                      xytext=(x_arrow - delta_x, y_arrow),
                      xycoords='data', textcoords='data', va='center',
                      ha='left', fontsize=12, fontweight='heavy',
                      arrowprops=arrow_props)
        txt = f"Polarization {bias_pola_target['high']}"
        if bias_pha_target is not None:
            txt += f"\n({bias_pha_target['high']} °)"
        ax_1.annotate(txt, xy=(x_text + delta_x, y_text),
                      xytext=(x_arrow + delta_x, y_arrow),
                      xycoords='data', textcoords='data', va='center',
                      ha='right', fontsize=12, fontweight='heavy',
                      arrowprops=arrow_props)

    # Plot phase gradient
    plot_dict.update({'form': 'm*-',
                      'title': 'Phase variation with voltage',
                      'y lab': 'Phase gradient'})
    plot_graph(ax_2, reduced_write_voltage, grad_mean_pha,
               plot_dict=plot_dict)
    ax_2.axhline(y=0, ls='--', c='lime', label='gradient=0')
    ax_2.axhline(y=np.mean(grad_mean_pha), ls='--', c='c',
                 label='mean gradient')
    ax_2.legend(fontsize=plot_dict['fs'], loc='best')
    # Annotate
    annot = "positive" if positive_pha_grad else "negative"
    fig.text(0.72, 0.02, f'Phase gradient: {annot}', c='c', size=15,
             weight='heavy')
    if dict_str:
        add_txt(fig, dict_str)

    return fig


def add_txt(fig, dict_str):
    """
    Add annotations to figures

    Parameters
    ----------
    fig: plt.figure
        Figure object to annotate
    dict_str: dict
        Dictionary of annotations for the plot

    Returns
    -------
    None
    """
    if 'label' in dict_str and 'col' in dict_str:
        # Add label annotation with color
        fig.text(0.01, 0.85, dict_str["label"], c=dict_str["col"],
                 size=20, weight='heavy', backgroundcolor='black')

    if 'index' in dict_str:
        # Add file index annotation
        fig.text(0.01, 0.80, f'file n°{dict_str["index"]}', size=15,
                 weight='heavy')
