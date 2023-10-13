"""
This module gather functions to deal with matplotlib plots
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import axes, legend
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable

from PySSPFM import DEFAULT_DATA_PATH_OUT


def print_plots(figs, save_plots=True, show_plots=True, dirname=None,
                close_plots=False, file_format='png', tight_layout=False,
                transparent=True, verbose=True,
                **kwargs):
    r"""
    Function that prints matplotlib figure on screen or disk.

    >>> fig = plt.figure(1)
    >>> fig.sfn = 'boar_on_the_beach'
    >>> line = plt.plot([1, 2, 3], [3, 6, 2])
    >>> print_plots([fig], save_plots=True, show_plots=False, dirname='.')
    Figure number 1 saved to .\boar_on_the_beach.png

    Parameters
    ----------
    figs : list
        List of matplotlib figures. Note that the user has to add the field
        "sfn" to the figure object. This field is the relative position of the
        file without extention
    save_plots : bool, optional
        If True, the plots are saved in the dirname with a user-defined name
    show_plots : bool, optional
        If True, the all the figures are displayed, even the ones that
        are not passed as arguments
    dirname: str, optional
        If None, the directory where saved plots go is the temporary directory
    close_plots : bool, optional
        If True, the figures specified by figs are closed at the end.
        If show_plots is True, then the command does not work and the user
        closes figures manually.
    file_format: str, optional
        File type of outputs. Can be anything accepted by matplotlib's savefig
    tight_layout: bool, optional
        Set to true if a tight layout around figures is preferred
    transparent: bool, optional
        Set to False if a solid white background is preferred.
    verbose: bool, optional
        To print figure saving message
    **kwargs : optional
        Parameters to be passed to save_fig function of matplotlib.
    """

    if save_plots:

        if dirname is None:
            dirname = DEFAULT_DATA_PATH_OUT

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        for fig in figs:
            if not hasattr(fig, 'sfn'):
                raise ValueError('figure objects must have a sfn attribute '
                                 'containing a string used as a file name')

            fn = os.path.join(dirname, fig.sfn + '.' + file_format)
            plt.figure(fig.number)
            if tight_layout:
                # Then get all the legends of the figure
                ax_list = [c for c in figs[0].get_children()
                           if isinstance(c, axes.Axes)]
                lgd = []
                for ax in ax_list:
                    lgd += [c for c in ax.get_children()
                            if isinstance(c, legend.Legend)]

                plt.savefig(fn, transparent=transparent,
                            bbox_extra_artists=lgd,
                            bbox_inches='tight', **kwargs)
            else:
                plt.savefig(fn, transparent=transparent, **kwargs)

            if verbose:
                print(f'Figure number {fig.number:d} saved to {fn}')

    if show_plots:
        plt.show()
    else:
        if close_plots:
            for fig in figs:
                plt.close(fig)


def init_y(init_y_tabs, ax):
    """
    Function used for plot_graph function:
    Init y values and in 2D array for loop plotting and create corresponding
    ax array

    Parameters
    ----------
    init_y_tabs: np.array
        Initial array of all y array values for ax.
    ax: plt.axes
        Axe of the figure

    Returns
    -------
    final_y_tabs: np.array
        2D array of all y array values for ax
    final_axs_tabs: np.array
        Array of ax corresponding to final_y_tabs
    """
    final_y_tabs, final_axs_tabs = [], []

    test = isinstance(init_y_tabs[0], (list, np.ndarray)) \
        if len(init_y_tabs) > 0 else False
    y_values = init_y_tabs if test else [init_y_tabs]
    for elem in y_values:
        final_y_tabs.append(elem)
        final_axs_tabs.append(ax)

    return final_y_tabs, final_axs_tabs


def ax_formating(ax, edge=None, grid=None, plt_leg=None, edgew=5., fntsz=15.,
                 tickl=10., gridw=2., fntsz_titles=15., title='', xlab='',
                 ylab='', cylab='k', ax2=None, y2lab='', cy2lab='k'):
    """
    Init ax with edge, ticks and grid plotting

    Parameters
    ----------
    ax: plt.axes
        First axe of the figure
    edge: bool, optional
        If True plot edges on ax
    grid: bool, optional
        If True plot a grid on ax
    plt_leg: bool, optional
        Plot legend if True and if there is a label legend
    edgew: float, optional
        Width of ax edges
    fntsz: float, optional
        Size of labels
    tickl: float, optional
        Length of ticks
    gridw: float, optional
        Width of grid
    fntsz_titles: float, optional
        Size of titles (figure and axis) labels
    title: str, optional
        Title of the ax
    xlab: str, optional
        Title for 'x' axis of ax
    ylab: str, optional
        Title for 'y' axis of ax
    cylab: str, optional
        Color of 'y' axis title of ax
    ax2: plt.axes, optional
        Second axe of the figure
    y2lab: str, optional
        Title for 'y' axis of ax2
    cy2lab: str, optional
        Color of 'y' axis title of ax2

    Returns
    ----------
    None
    """
    # Borders, graduations and grid
    if edge:
        ax_right = not bool(ax2)
        tick_params = {'length': tickl, 'width': edgew, 'right': ax_right,
                       'top': False, 'labelsize': fntsz}
        ax.tick_params(**tick_params, grid_linewidth=gridw, grid_linestyle=':')
        ax.spines['left'].set_linewidth(edgew)
        ax.spines['bottom'].set_linewidth(edgew)
        if ax2:
            ax2.tick_params(**tick_params)
            ax2.spines['right'].set_linewidth(edgew)
        else:
            ax.spines['right'].set_linewidth(edgew)
        ax.spines['top'].set_linewidth(edgew)
    if grid:
        ax.grid(True)
    # Annotations
    if title:
        ax.set_title(title, size=fntsz_titles)
    ax.set_xlabel(xlab, size=fntsz_titles)
    ax.set_ylabel(ylab, size=fntsz_titles, c=cylab)
    if ax2:
        ax2.set_ylabel(y2lab, size=fntsz_titles, c=cy2lab)
    if plt_leg:
        ax.legend(fontsize=fntsz, loc='upper left')
        if ax2:
            ax2.legend(fontsize=fntsz, loc='lower right')


def plot_graph(ax, x_tabs, y_tabs, ax2=None, y2_tabs=None, plot_dict=None,
               tabs_dict=None, plot_leg=True):
    """
    Plot a graph.

    Parameters
    ----------
    ax: plt.axes
        First axe of the figure.
    x_tabs: numpy.array or list(n) or (m*n) of float
        Array of x values.
    y_tabs: numpy.array or list(n) or (m*n) of float
        Array of all y array values for ax.
    ax2: plt.axes, optional
        Second axe of the figure.
    y2_tabs: numpy.array or list(n) or (m*n) of float, optional
        Array of all y array values for ax2.
    plot_dict: dict, optional
        Dict for annotation of the figure.
    tabs_dict: numpy.array or list(n) or dict, optional
        Array of dict for plotting parameters of all y array values.
    plot_leg: bool, optional
        Plot legend if True and if there is a label legend

    Returns
    ----------
    None
    """
    # Initialize y values and axs
    y_values, y_axs = init_y(y_tabs, ax)
    if y2_tabs is not None and ax2 is not None:
        y2_tabs, y2_axs = init_y(y2_tabs, ax2)
        y_values.extend(y2_tabs)
        y_axs.extend(y2_axs)

    # Initialize plot_dict
    plot_dict = plot_dict or {}
    plot_dict.setdefault('title', '')
    plot_dict.setdefault('x lab', 'x axis')
    plot_dict.setdefault('y lab', 'y axis')
    plot_dict.setdefault('y2 lab', 'y2 axis')
    plot_dict.setdefault('fs', 15)
    plot_dict.setdefault('edgew', 5.0)
    plot_dict.setdefault('tickl', 10)
    plot_dict.setdefault('gridw', 2)
    plot_dict.setdefault('c y lab', 'k')
    plot_dict.setdefault('c y2 lab', 'k')

    # Initialize tabs_dict
    tabs_dict = tabs_dict or []
    if isinstance(tabs_dict, dict):
        tabs_dict = [tabs_dict]
    if plot_leg:
        plt_leg = any('legend' in tab_dict for tab_dict in tabs_dict)
    else:
        plt_leg = False
    tabs_dict = [{} for _ in
                 range(len(y_values))] if not tabs_dict else tabs_dict
    for tab_dict in tabs_dict:
        tab_dict.setdefault('legend', '')
        tab_dict.setdefault('ms', 5)
        tab_dict.setdefault('mec', 'k')
        tab_dict.setdefault('lw', 2)

    # init x values
    test = isinstance(x_tabs[0], (list, np.ndarray)) if len(
        x_tabs) > 0 else False
    x_values = x_tabs if test else [x_tabs for _ in range(len(y_values))]

    # plot function
    for x_val, y_val, dictio, axs in zip(x_values, y_values, tabs_dict, y_axs):
        form = dictio.get('form')
        if form is None:
            axs.plot(x_val, y_val, label=dictio['legend'],
                     ms=dictio['ms'], mec=dictio['mec'], lw=dictio['lw'])
        else:
            axs.plot(x_val, y_val, form, label=dictio['legend'],
                     ms=dictio['ms'], mec=dictio['mec'], lw=dictio['lw'])

    # Format ax
    ax_formating(ax, edge=True, grid=True, plt_leg=plt_leg,
                 edgew=plot_dict['edgew'], fntsz=plot_dict['fs'],
                 tickl=plot_dict['tickl'], gridw=plot_dict['gridw'],
                 fntsz_titles=plot_dict['fs'], title=plot_dict['title'],
                 xlab=plot_dict['x lab'], ylab=plot_dict['y lab'],
                 cylab=plot_dict['c y lab'], ax2=ax2,
                 y2lab=plot_dict['y2 lab'], cy2lab=plot_dict['c y2 lab'])


def plot_hist(ax, y_value, plot_dict=None):
    """
    Plot histogram in a graph.

    Parameters
    ----------
    ax: plt.axes
        Axes of the figure.
    y_value: list(n) or numpy.array(n) of float
        Array of y values.
    plot_dict: dict, optional
        Dictionary for annotations of the figure.

    Returns
    ----------
    None
    """
    # Initialize plot_dict
    plot_dict = plot_dict or {}
    plot_dict.setdefault('title', '')
    plot_dict.setdefault('x lab', 'value')
    plot_dict.setdefault('y lab', 'cont')
    plot_dict.setdefault('legend', '')
    plot_dict.setdefault('fs', 15)
    plot_dict.setdefault('edgew', 5.0)
    plot_dict.setdefault('tickl', 10)
    plot_dict.setdefault('gridw', 2)

    # Plot function
    bins = plot_dict.get('bins')
    ax.hist(y_value, bins=bins, label=plot_dict['legend'], ec='k')

    # Format ax
    ax_formating(ax, edge=True, grid=True, plt_leg=bool(plot_dict['legend']),
                 edgew=plot_dict['edgew'], fntsz=plot_dict['fs'],
                 tickl=plot_dict['tickl'], gridw=plot_dict['gridw'],
                 fntsz_titles=plot_dict['fs'], title=plot_dict['title'],
                 xlab=plot_dict['x lab'], ylab=plot_dict['y lab'])

    # Set axis limits and scale if needed
    # ax.set_xlim([np.min(x_value), np.max(x_value)])
    # ax.set_ylim([np.min(y_value), np.max(y_value)])
    # ax.loglog()
    # ax.semilogx()
    # ax.semilogy()


def plot_map(fig, ax, matrix, extent=None, plot_dict=None, colorbar_dict=None):
    """
    Plot image of 2D data (without generate_ticks_vector function).

    Parameters
    ----------
    fig: plt.figure
        Figure object.
    ax: plt.axes
        Axes of the figure.
    matrix: numpy.array(m*n) of float
        2D array of values.
    extent: list(4) or tuple(4), optional
        List of 'x' and 'y' axis limit values.
    plot_dict: dict, optional
        Dictionary for annotations of the figure.
    colorbar_dict: dict, optional
        Dictionary for annotations of the colorbar.

    Returns
    ----------
    None
    """
    # Initialize plot_dict
    plot_dict = plot_dict or {}
    plot_dict.setdefault('title', '')
    plot_dict.setdefault('x lab', '')
    plot_dict.setdefault('y lab', '')
    plot_dict.setdefault('fs', 15)
    plot_dict.setdefault('aspect', 'auto')
    plot_dict.setdefault('origin', 'lower')

    # Initialize colorbar_dict
    colorbar_dict = colorbar_dict or {}
    colorbar_dict.setdefault('col', 'jet')
    colorbar_dict.setdefault('lab', '')
    colorbar_dict.setdefault('log', False)
    colorbar_dict.setdefault('size', 2)
    colorbar_dict.setdefault('pad', 0.05)
    colorbar_dict.setdefault('vmin', None)
    colorbar_dict.setdefault('vmax', None)

    norm_func = LogNorm() if colorbar_dict['log'] else None
    colo = ax.imshow(matrix, cmap=colorbar_dict['col'],
                     origin=plot_dict['origin'], extent=extent, norm=norm_func,
                     aspect=plot_dict['aspect'], vmin=colorbar_dict['vmin'],
                     vmax=colorbar_dict['vmax'])

    # Colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size=f"{colorbar_dict['size']}%",
                              pad=colorbar_dict['pad'])
    cbar = fig.colorbar(colo, cax=cax)
    cbar.set_label(colorbar_dict['lab'], size=plot_dict['fs'], va='baseline',
                   rotation=270)

    # Annotate
    ax.set_title(plot_dict['title'], size=plot_dict['fs'])
    ax.set_xlabel(plot_dict['x lab'], size=plot_dict['fs'])
    ax.set_ylabel(plot_dict['y lab'], size=plot_dict['fs'])


if __name__ == '__main__':
    import doctest  # pylint: disable=wrong-import-position

    doctest.testmod()
