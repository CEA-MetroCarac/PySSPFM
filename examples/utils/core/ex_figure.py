"""
Examples of figure
"""
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.noise import noise
from PySSPFM.utils.core.figure import \
    plot_graph, plot_hist, plot_map, print_plots


def ex_plot_graph():
    """
    Example of plot_graph function.

    Returns
    -------
    list
        Returns a list containing the figure object.
    """
    # 1st graph function
    x_val_1 = np.linspace(0, 20 * np.pi, 1000)
    y_val_1 = 5 * np.sin(x_val_1)

    # 2nd graph functions
    x_val_2 = np.linspace(0, 1, 50)
    y_value_1 = [elem ** (1 / 3) for elem in x_val_2]
    y_value_2 = [elem ** (1 / 2) for elem in x_val_2]
    y_value_3 = x_val_2
    y_value_4 = [elem ** 2 for elem in x_val_2]
    y_value_5 = [elem ** 3 for elem in x_val_2]
    y_val_2 = [y_value_1, y_value_2, y_value_3, y_value_4, y_value_5]

    # 3rd graph functions
    x_val_3 = np.linspace(-1, 1, 100)
    y_val_3 = [np.exp(elem) for elem in x_val_3]
    y2_val_3 = [-np.exp(5 * elem) for elem in x_val_3]

    # 4th graph functions
    x_val_4 = np.linspace(-1, 1, 500)
    y_value_1 = [np.sin(np.pi * elem) for elem in x_val_4]
    y_value_2 = [np.cos(np.pi * elem) for elem in x_val_4]
    y_val_4 = [y_value_1, y_value_2]
    y2_value_1 = [np.arcsin(elem) for elem in x_val_4]
    y2_value_2 = [np.arccos(elem) for elem in x_val_4]
    y2_val_4 = [y2_value_1, y2_value_2]

    # Plot
    fig, ax = plt.subplots(2, 2, figsize=[18, 9])
    fig.sfn = "ex_plot_graph"

    # Set plot parameters
    plot_dict_1 = {'title': '', 'x lab': 'x', 'y lab': 'y', 'fs': 13,
                   'edgew': 3, 'tickl': 5, 'gridw': 1}
    plot_dict_2 = {'title': '', 'x lab': 'x', 'y lab': 'y', 'fs': 13,
                   'edgew': 3, 'tickl': 5, 'gridw': 1}
    plot_dict_3 = {'title': '', 'x lab': 'x', 'y lab': '', 'y2 lab': '',
                   'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1}
    plot_dict_4 = {'title': '', 'x lab': 'x', 'y lab': '', 'y2 lab': '',
                   'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1}

    # Plot graph 1: single function / single 'y' axis
    tab_dict_1 = {'legend': 'sin', 'form': 'rs-', 'ms': 3, 'mec': 'k', 'lw': 1}
    plot_graph(ax[0, 0], x_val_1, y_val_1, plot_dict=plot_dict_1,
               tabs_dict=tab_dict_1)

    # Plot graph 2: multi functions / single 'y' axis
    tab_dict_2 = {'legend': '**(1/3)', 'form': 'rs-', 'ms': 3, 'mec': 'k',
                  'lw': 1}
    tab_dict_3 = {'legend': '**(1/2)', 'form': 'gh--', 'ms': 3, 'mec': 'k',
                  'lw': 1}
    tab_dict_4 = {'legend': '**1', 'form': 'bo-.', 'ms': 3, 'mec': 'k', 'lw': 1}
    tab_dict_5 = {'legend': '**2', 'form': 'kx:', 'ms': 3, 'mec': 'k', 'lw': 1}
    tab_dict_6 = {'legend': '**3', 'form': 'c^-', 'ms': 3, 'mec': 'k', 'lw': 1}
    tabs_dict = [tab_dict_2, tab_dict_3, tab_dict_4, tab_dict_5, tab_dict_6]
    plot_graph(ax[0, 1], x_val_2, y_val_2, plot_dict=plot_dict_2,
               tabs_dict=tabs_dict)

    # Plot graph 3: two functions / two 'y' axis
    tab_dict_7 = {'legend': 'f(x)=exp(x)', 'form': 'bs-', 'ms': 3, 'mec': 'k',
                  'lw': 1}
    tab_dict_8 = {'legend': 'f(x)=-exp(5x)', 'form': 'gs-', 'ms': 3, 'mec': 'k',
                  'lw': 1}
    tabs_dict_2 = [tab_dict_7, tab_dict_8]
    ax2 = ax[1, 0].twinx()
    plot_graph(ax[1, 0], x_val_3, y_val_3, ax2=ax2, y2_tabs=y2_val_3,
               plot_dict=plot_dict_3, tabs_dict=tabs_dict_2)

    # Plot graph 4: multi functions / two 'y' axis
    tab_dict_9 = {'legend': 'sin', 'form': 'r-', 'ms': 3, 'mec': 'k', 'lw': 1}
    tab_dict_10 = {'legend': 'cos', 'form': 'b-', 'ms': 3, 'mec': 'k', 'lw': 1}
    tab_dict_11 = {'legend': 'arcsin', 'form': 'm-', 'ms': 3, 'mec': 'k',
                   'lw': 1}
    tab_dict_12 = {'legend': 'arccos', 'form': 'c-', 'ms': 3, 'mec': 'k',
                   'lw': 1}
    tabs_dict_3 = [tab_dict_9, tab_dict_10, tab_dict_11, tab_dict_12]
    ax3 = ax[1, 1].twinx()
    plot_graph(ax[1, 1], x_val_4, y_val_4, ax2=ax3, y2_tabs=y2_val_4,
               plot_dict=plot_dict_4, tabs_dict=tabs_dict_3)

    return [fig]


def ex_plot_hist():
    """
    Example of plot_hist function.

    Returns
    -------
    list
        Returns a list containing the figure object.
    """
    # Generate values: noise
    noise_pars = {'type': 'normal', 'ampli': 10}
    signal = np.linspace(-1, 1, 500)
    tot = noise(signal, noise_pars)
    norm_noise = tot - signal

    # Plot
    fig, ax = plt.subplots(figsize=[18, 9])
    fig.sfn = "ex_plot_hist"

    # Set plot parameters
    plot_dict = {'title': 'histogram', 'x lab': 'normal noise', 'bins': 20,
                 'fs': 15, 'edgew': 5, 'tickl': 5, 'gridw': 2}

    # ex plot_hist
    plot_hist(ax, norm_noise, plot_dict)

    return [fig]


def ex_plot_map():
    """
    Example of plot_map function.

    Returns
    -------
    list
        Returns a list containing the figure object.
    """
    # Generate 2D matrix
    x_tab = [i * 0.1 for i in range(324)]
    y_tab = [i * 0.5 for i in range(245)]
    matrix = np.reshape(
        np.array([elem + j for j in range(len(y_tab)) for elem in x_tab]),
        (len(y_tab), -1))

    # Plot
    fig, ax = plt.subplots(figsize=[18, 9])
    fig.sfn = "ex_plot_map"

    # ex plot_map
    plot_dict = {'title': 'intensity map'}
    colorbar_dict = {'lab': 'intensity'}
    extent = [min(x_tab), max(x_tab), min(y_tab), max(y_tab)]
    plot_map(fig, ax, matrix, extent=extent, plot_dict=plot_dict,
             colorbar_dict=colorbar_dict)

    return [fig]


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "core_figure", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_plot_graph()
    figs += ex_plot_hist()
    figs += ex_plot_map()
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
