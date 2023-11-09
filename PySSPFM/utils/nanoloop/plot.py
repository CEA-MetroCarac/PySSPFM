"""
Module used for nanoloop: - plot functions
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.figure import plot_graph
from PySSPFM.utils.nanoloop.analysis import MeanLoop


def plot_ckpfm(loop_dict, dict_str=None):
    """
    Create a figure of ckpfm measure: piezorep = f(read volt) for each write
    volt values. Valid for multi read voltage values off-field measurements.

    Parameters
    ----------
    loop_dict: dict
        Dictionary of loop data sorted in terms of ckpfm measure.
    dict_str: dict, optional
        Dictionary of annotations for the plot.

    Returns
    -------
    fig: plt.figure
        Figure object for the plot.
    """
    unit = "" if dict_str is None else dict_str["unit"]

    # Plotting initialization
    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = 'plot_ckpfm'
    ax.tick_params(length=10, width=5, right=True, top=False,
                   grid_linewidth=2, grid_linestyle=':', labelsize=15)
    for direction in ['top', 'bottom', 'left', 'right']:
        ax.spines[direction].set_linewidth(5.0)
    ax.grid(True)
    ax.set_title('cKPFM analysis', size=24, va='bottom', weight='heavy')
    ax.set_xlabel('Read Voltage [V]', size=20, weight='heavy')
    ax.set_ylabel(f'Piezo Response [{unit}]', size=20, weight='heavy')

    # Plot each cKPFM line with a color defined in the colorbar
    for cont, elem in enumerate(loop_dict['write volt']):
        fraction = (elem - min(loop_dict['write volt'])) / \
                   (max(loop_dict['write volt']) - min(loop_dict['write volt']))
        color = cm.jet(fraction)
        ax.plot(loop_dict['read volt'], loop_dict['piezorep'][cont], marker='o',
                mec='k', ls='-', c=color)

    # Plot the colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='3%', pad=0.4)
    cmap = plt.get_cmap('jet')
    norm = mpl.colors.Normalize(vmin=min(loop_dict['write volt']),
                                vmax=max(loop_dict['write volt']))
    s_m = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    s_m.set_array(np.array([]))
    c_b = fig.colorbar(s_m, cax=cax)
    c_b.set_label(label='Write Voltage [V]', size=20, weight='heavy',
                  rotation=270, labelpad=20)
    len_tick = len(loop_dict['write volt'])
    while len_tick > 11:
        len_tick = len_tick // 2
    c_b.set_ticks(ticks=np.linspace(min(loop_dict['write volt']),
                                    max(loop_dict['write volt']), len_tick))
    c_b.ax.tick_params(labelsize=20)

    # Annotations: legend...
    if dict_str:
        add_txt(fig, dict_str)

    return fig


def plot_multiloop(mean_loop, dict_str=None):
    """
    Create a figure of single multi loop with amplitude, phase, and
    piezoresponse.

    Parameters
    ----------
    mean_loop: MeanLoop class
        MeanLoop or MultiLoop class object.
    dict_str: dict, optional
        Dictionary of annotations for the plot.

    Returns
    -------
    fig: plt.figure
        Figure object for the plot.
    """
    if dict_str is None:
        unit, mode = "", 'Off Field'
    else:
        unit, mode = dict_str["unit"], dict_str["label"]

    figsize = get_setting("figsize")
    fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize=figsize)
    add = mode.lower().replace(' ', '_')
    fig.sfn = f'plot_multiloop_{add}'

    # Amplitude and phase loops
    add_ax_1 = ax_1.twinx()
    plot_dict = {'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1,
                 'x lab': 'Write voltage [V]',
                 'y lab': f'Amplitude [{unit}]',
                 'y2 lab': 'Phase [°]', 'title': 'Amplitude & Phase'}
    tab_dict_1 = {'legend': 'amplitude (left)', 'form': 'r+-'}
    tab_dict_2 = {'legend': 'amplitude (right)', 'form': 'b+-'}
    tab_dict_3 = {'legend': 'phase (left)', 'form': 'm:x', 'mec': 'm'}
    tab_dict_4 = {'legend': 'phase (right)', 'form': 'c:x', 'mec': 'c'}
    x_tabs = [mean_loop.write_volt_left, mean_loop.write_volt_right,
              mean_loop.write_volt_left, mean_loop.write_volt_right]
    y_tabs = [mean_loop.amp_left, mean_loop.amp_right]
    y2_tabs = [mean_loop.pha_left, mean_loop.pha_right]
    tabs_dict = [tab_dict_1, tab_dict_2, tab_dict_3, tab_dict_4]
    plot_graph(ax_1, x_tabs, y_tabs, ax2=add_ax_1, y2_tabs=y2_tabs,
               plot_dict=plot_dict, tabs_dict=tabs_dict)

    # Piezoresponse loop
    plot_dict['title'] = 'Piezo Response'
    plot_dict['y lab'] = f'Piezo Response [{unit}]'
    tab_dict_1 = {'legend': 'piezoresponse (left)', 'form': 'r.-'}
    tab_dict_2 = {'legend': 'piezoresponse (right)', 'form': 'b.-'}
    x_tabs = [mean_loop.write_volt_left, mean_loop.write_volt_right]
    y_tabs = [mean_loop.piezorep_left, mean_loop.piezorep_right]
    tabs_dict = [tab_dict_1, tab_dict_2]
    plot_graph(ax_2, x_tabs, y_tabs, plot_dict=plot_dict, tabs_dict=tabs_dict)

    ax_2.yaxis.tick_right()
    ax_2.yaxis.set_label_position("right")

    # Annotations: axis, legend...
    if dict_str:
        add_txt(fig, dict_str)

    # Segment markers
    for cont, (elem_x, elem_y1, elem_y2, elem_y3) in enumerate(zip(
            mean_loop.write_marker, mean_loop.amp_marker, mean_loop.pha_marker,
            mean_loop.piezorep_marker), start=1):
        ax_1.plot(elem_x, elem_y1, '*', c='g', ms=8, mec='k', mew=0.5)
        ax_1.text(elem_x, elem_y1, str(cont), c='g', size=13, weight='heavy')
        add_ax_1.plot(elem_x, elem_y2, '*', c='g', ms=8, mec='k', mew=0.5)
        add_ax_1.text(elem_x, elem_y2, str(cont), c='g', size=13,
                      weight='heavy')
        ax_2.plot(elem_x, elem_y3, '*', c='g', ms=8, mec='k', mew=0.5)
        ax_2.text(elem_x, elem_y3, str(cont), c='g', size=13, weight='heavy')

    y_offset = 0.02
    for j in range(len(mean_loop.write_marker) - 1):
        fig.text(0.01, 0.98 - y_offset * j,
                 f'segment {j + 1}: point {j + 1} to {j + 2} '
                 f'({mean_loop.write_marker[j]:.2f} to '
                 f'{mean_loop.write_marker[j + 1]:.2f})',
                 c='g', size=15, weight='heavy')

    return fig


def plot_sspfm_loops(loops_tab, pha_calib, dict_str=None, del_1st_loop=False):
    """
    Figure of multiple multi and mean loops with amplitude, phase and
    piezoresponse

    Parameters
    ----------
    loops_tab: numpy.array(n) or list(n) of Multiloop
        Array of MultiLoop class object
    pha_calib: dict
        Phase calibration parameters
    dict_str: dict, optional
        Annotation for plot
    del_1st_loop: bool, optional
        If True, remove first loop for analysis

    Returns
    -------
    figs: list(6) of figure
        List of figure object
    """
    figs = plot_all_loop(loops_tab, pha_calib, dict_str=dict_str)
    figs += plot_meanloop(loops_tab, pha_calib, dict_str=dict_str,
                          del_1st_loop=del_1st_loop)
    return figs


def plot_all_loop(loops_tab, pha_calib, dict_str=None):
    """
    Figure of separated multiple multi loops with amplitude, phase and
    piezoresponse.

    Parameters
    ----------
    loops_tab: numpy.array(n) or list(n) of Multiloop
        Array of MultiLoop class objects.
    pha_calib: dict
        Phase calibration parameters
    dict_str: dict, optional
        Annotations for the plot.

    Returns
    -------
    figs: list(3) of figure
        List of figure objects.
    """
    if dict_str is None:
        unit, mode = "", 'Off Field'
    else:
        unit, mode = dict_str["unit"], dict_str["label"]

    # Compute the figure dimension
    fig_dim = subplots_dim(len(loops_tab))

    read_voltage = [loop.read_volt for loop in loops_tab]

    titles = ['Amplitude Loops', 'Phase Loops', 'Piezorep Loops']
    label_x = 'Write voltage [V]'
    labels_y = [f'Amplitude [{unit}]', 'Phase [°]', f'Piezo Response [{unit}]']
    figs = []

    for title, label_y in zip(titles, labels_y):

        # Init figure (label ...)
        figsize = get_setting("figsize")
        fig, axs = plt.subplots(fig_dim[0], fig_dim[1], sharex='all',
                                sharey='all', figsize=figsize)
        add = mode.lower().replace(' ', '_')
        fig.sfn = f'plot_meanloop_{add}_{title.replace(" ", "_").lower()}'
        str_dict = {'title': title, 'x label': label_x, 'y label': label_y}
        set_figure(fig, str_dict, pha_calib, loops_tab[0].write_marker,
                   dict_str=dict_str)

        for i, loop in enumerate(loops_tab):
            if mode == 'Off Field':
                if min(read_voltage) == max(read_voltage):
                    color = cm.jet(0.55)
                else:
                    fraction = (loop.read_volt - min(read_voltage)) / (
                            max(read_voltage) - min(read_voltage))
                    fraction = fraction * 0.7 + 0.2
                    color = cm.jet(fraction)
                label_tit = f'loop n°{i}, read = {loop.read_volt:.2f} V'
            else:
                color = cm.jet(0.55)
                label_tit = f'loop n°{i}, baseline = {loop.read_volt:.2f} V'
            index_line, index_column = divmod(i, fig_dim[1])
            ax = axs if fig_dim[0] == fig_dim[1] == 1 else axs[
                index_line, index_column]
            ax.set_title(label_tit, c=color, weight='heavy',
                         backgroundcolor='k')
            ax.grid(True, ls=':')
            if 'Phase' in label_y and pha_calib['corr'] != 'raw':
                ax.plot(loop.write_volt_left, loop.pha_left, 'mx:', ms=5)
                ax.plot(loop.write_volt_right, loop.pha_right, 'cx:', ms=5)
            if 'Amplitude' in title:
                measure_left = loop.amp_left
                measure_right = loop.amp_right
                measure_marker = loop.amp_marker
            elif 'Phase' in title:
                measure_left = loop.treat_pha_left
                measure_right = loop.treat_pha_right
                measure_marker = loop.treat_pha_marker
            else:
                measure_left = loop.piezorep_left
                measure_right = loop.piezorep_right
                measure_marker = loop.piezorep_marker
            ax.plot(loop.write_volt_left, measure_left, 'r.-', ms=5, mec='k')
            ax.plot(loop.write_volt_right, measure_right, 'b.-', ms=5, mec='k')
            for elem_wr, elem_meas in zip(loop.write_marker, measure_marker):
                ax.plot(elem_wr, elem_meas, 'wo', ms=5, mec='g')
        figs.append(fig)

    return figs


def plot_meanloop(loops_tab, pha_calib, dict_str=None, del_1st_loop=False):
    """
    Figure of superposed multiple multi loops and mean loop with
    amplitude, phase, and piezoresponse.

    Parameters
    ----------
    loops_tab: numpy.array(n) or list(n) of Multiloop
        Array of MultiLoop class objects.
    pha_calib: dict
        Phase calibration parameters
    dict_str: dict, optional
        Annotations for the plot.
    del_1st_loop: bool, optional
        If True, remove the first loop for analysis.

    Returns
    -------
    figs: list(3) of figure
        List of figure objects.
    """
    if dict_str is None:
        unit, mode = "", 'Off Field'
    else:
        unit, mode = dict_str["unit"], dict_str["label"]

    mean_loop = MeanLoop(
        loops_tab, pha_calib=pha_calib, del_1st_loop=del_1st_loop)
    if del_1st_loop:
        loops_tab = loops_tab[1:]

    titles = ['Amplitude Loops', 'Phase Loops', 'Piezorep Loops']
    label_x = 'Write voltage [V]'
    labels_y = [f'Amplitude [{unit}]', 'Phase [°]', f'Piezo Response [{unit}]']

    figs = []

    for title, label_y in zip(titles, labels_y):

        if 'Amplitude' in title:
            measure_left = [loop.amp_left for loop in loops_tab]
            measure_right = [loop.amp_right for loop in loops_tab]
            mean_measure_left = mean_loop.amp_left
            mean_measure_right = mean_loop.amp_right
            mean_measure_marker = mean_loop.amp_marker
        elif 'Phase' in title:
            measure_left = [loop.treat_pha_left for loop in loops_tab]
            measure_right = [loop.treat_pha_right for loop in loops_tab]
            mean_measure_left = mean_loop.pha_left
            mean_measure_right = mean_loop.pha_right
            mean_measure_marker = mean_loop.pha_marker
        else:
            measure_left = [loop.piezorep_left for loop in loops_tab]
            measure_right = [loop.piezorep_right for loop in loops_tab]
            mean_measure_left = mean_loop.piezorep_left
            mean_measure_right = mean_loop.piezorep_right
            mean_measure_marker = mean_loop.piezorep_marker

        figsize = get_setting("figsize")
        fig, (ax_1, ax_2) = plt.subplots(1, 2, sharey='all', figsize=figsize)
        add = mode.lower().replace(' ', '_')
        fig.sfn = f'plot_all_loop_{add}_{title.replace(" ", "_").lower()}'
        fig.suptitle(title, size=24, weight='heavy')

        plot_dict = {'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1,
                     'x lab': label_x, 'y lab': label_y,
                     'title': 'superposed loops'}

        plot_graph(ax_1, [], [], plot_dict=plot_dict)
        cmap = cm.get_cmap('jet')

        for cont, (elem_left, elem_right) in enumerate(zip(measure_left,
                                                           measure_right)):
            ax_1.plot(loops_tab[0].write_volt_left, elem_left, ls='-', lw=1,
                      c=cmap(cont / len(measure_left)))
            ax_1.plot(loops_tab[0].write_volt_right, elem_right, ls='-',
                      lw=1, c=cmap(cont / len(measure_left)))

        plot_dict['title'] = 'mean loop'
        tab_dict_1 = {'form': 'r.-', 'ms': 10}
        tab_dict_2 = {'form': 'b.-', 'ms': 10}
        x_tabs = [mean_loop.write_volt_left, mean_loop.write_volt_right]
        y_tabs = [mean_measure_left, mean_measure_right]
        tabs_dict = [tab_dict_1, tab_dict_2]
        plot_graph(ax_2, x_tabs, y_tabs, plot_dict=plot_dict,
                   tabs_dict=tabs_dict)

        if dict_str:
            add_txt(fig, dict_str)

        for i, (elem_x, elem_y) in enumerate(zip(
                mean_loop.write_marker, mean_measure_marker), start=1):
            ax_2.plot(elem_x, elem_y, '*', c='g', ms=10, mec='k', mew=0.5)
            ax_2.text(elem_x, elem_y, str(i), c='g', size=13, weight='heavy')

        y_offset = 0.02
        for j in range(len(mean_loop.write_marker) - 1):
            fig.text(0.01, 0.98 - y_offset * j,
                     f'segment {j + 1}: point {j + 1} to {j + 2} '
                     f'({mean_loop.write_marker[j]:.2f} to '
                     f'{mean_loop.write_marker[j + 1]:.2f})',
                     c='g', size=15, weight='heavy')

        figs.append(fig)

    return figs


def subplots_dim(nb_subplot):
    """
    Compute subplots dimensions from the number of subplots.

    Parameters
    ----------
    nb_subplot: int
        Number of subplots to plot in the main figure.

    Returns
    -------
    fig_dim: list(2) of int
        List of figure dimensions [number of lines, number of columns].
    """
    assert nb_subplot > 0

    # Compute the square value for the number of subplots
    square = nb_subplot
    sqrt_square = np.sqrt(square)
    while sqrt_square != int(sqrt_square):
        square += 1
        sqrt_square = np.sqrt(square)

    nb_column = int(sqrt_square)
    cont = 0
    i = 0
    while cont < nb_subplot:
        cont = cont + nb_column
        i += 1

    nb_line = i

    return [nb_line, nb_column]


def set_figure(fig, str_dict, pha_calib, write_markers, dict_str=None):
    """
    Add annotation and segment markers for meanloop and all_loop figures

    Parameters
    ----------
    fig: plt.figure
        Figure object to modify
    str_dict: dict
        Dictionary containing figure and axis titles
    pha_calib: dict
        Phase calibration parameters
    write_markers: numpy.array(3 or 4) or list(3 or 4)
        Array of segment write markers
    dict_str: dict, optional
        Figure annotations

    Returns
    -------
    None
    """
    # Set figure title and axis labels
    fig.suptitle(str_dict['title'], size=24, weight='heavy')
    fig.text(0.5, 0.04, str_dict['x label'], ha='center', va='center', size=24,
             weight='heavy')
    fig.text(0.04, 0.5, str_dict['y label'], ha='center', va='center',
             rotation='vertical', size=24, weight='heavy')

    # Add annotation for plot
    if dict_str:
        fig.text(0.90, 0.95, dict_str["label"], c=dict_str["col"], size=20,
                 weight='heavy', backgroundcolor='black')

    # Add phase correction mode and reverted phase value for phase plots
    if 'Phase' in str_dict['y label'] and pha_calib['corr'] != 'raw':
        fig.text(0.72, 0.04,
                 f'Phase correction mode: {pha_calib["corr"]}',
                 c='orange', size=15, weight='heavy')
        fig.text(0.72, 0.02,
                 f'Reverted phase value: {pha_calib["reverse"]}',
                 c='c', size=15, weight='heavy')

    # Add segment markers
    y_offset = 0.02
    for k, marker in enumerate(write_markers[:-1]):
        fig.text(0.01, 0.98 - y_offset * k,
                 f'segment {k + 1}: point {k + 1} to {k + 2} ({marker:.2f} to '
                 f'{write_markers[k + 1]:.2f})',
                 c='g', size=15, weight='heavy')


def add_txt(fig, dict_str):
    """
    Add annotation for figures

    Parameters
    ----------
    fig: plt.figure
        Figure object
    dict_str: dict
        Dictionary of annotations for plot

    Returns
    -------
    None
    """
    if 'label' in dict_str and 'col' in dict_str:
        fig.text(0.01, 0.85, dict_str["label"], c=dict_str["col"],
                 size=20, weight='heavy', backgroundcolor='black')
    if 'index' in dict_str:
        fig.text(0.01, 0.80, f'file n°{dict_str["index"]}',
                 size=15, weight='heavy')
