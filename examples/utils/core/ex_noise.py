"""
Examples of noise applications
"""
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import plot_graph, plot_hist, print_plots
from PySSPFM.utils.core.noise import noise, filter_mean, normal


def ex_gen_noise(make_plots=False):
    """
    Example of noise generation functions.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots. Default is False.

    Returns
    -------
    tuple or list
        Depending on the value of make_plots, returns either a tuple or a list
        containing the generated noise and pure noise components.
    """
    np.random.seed(0)

    x_val = np.linspace(0, 20 * np.pi, 1000)
    y_val = 5 * np.sin(x_val)

    noise_pars = [
        {'type': 'uniform', 'ampli': 10},
        {'type': 'normal', 'ampli': 10},
        {'type': 'laplace', 'ampli': 10}
    ]

    # ex noise
    y_noise = {}
    for elem in noise_pars:
        y_noise[elem['type']] = noise(y_val, elem)

    # Isolate noise and normal noise component
    pure_noise = {}
    for key, value in y_noise.items():
        pure_noise[key] = [elem_noise - elem_clear for
                           elem_noise, elem_clear in zip(value, y_val)]

    if make_plots:
        fig, ax = plt.subplots(2, 3, figsize=[18, 9], sharey='row')
        fig.sfn = "ex_gen_noise"
        plot_dict = {'title': 'Noised Signal', 'fs': 13, 'edgew': 3, 'tickl': 5,
                     'gridw': 1}
        tab_dict_1 = {'legend': 'noised sin', 'form': 'r-'}
        tab_dict_2 = {'legend': 'clear sin', 'form': 'b-'}
        plot_graph(ax[0, 0], x_val, [y_noise['uniform'], y_val],
                   plot_dict=plot_dict, tabs_dict=[tab_dict_1, tab_dict_2])
        plot_dict['title'] = 'Norm Noised Signal'
        plot_graph(ax[0, 1], x_val, [y_noise['normal'], y_val],
                   plot_dict=plot_dict, tabs_dict=[tab_dict_1, tab_dict_2])
        plot_dict['title'] = 'Laplace Noised Signal'
        plot_graph(ax[0, 2], x_val, [y_noise['laplace'], y_val],
                   plot_dict=plot_dict, tabs_dict=[tab_dict_1, tab_dict_2])
        plot_dict = {'x lab': 'Noise (a.u)',
                     'y lab': 'Noise repartition (count)', 'bins': 20, 'fs': 13,
                     'edgew': 3, 'tickl': 5, 'gridw': 1}
        plot_hist(ax[1, 0], pure_noise['uniform'], plot_dict)
        plot_hist(ax[1, 1], pure_noise['normal'], plot_dict)
        plot_hist(ax[1, 2], pure_noise['laplace'], plot_dict)

        return [fig]

    else:
        return (y_noise['uniform'], y_noise['normal'], y_noise['laplace'],
                pure_noise['uniform'], pure_noise['normal'],
                pure_noise['laplace'])


def ex_filter_mean(make_plots=False):
    """
    Example of the filter_mean function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots. Default is False.

    Returns
    -------
    y_filt: list
        List of y values after applying the filter.
    """
    np.random.seed(0)

    x_val = np.linspace(0, 20 * np.pi, 1000)
    y_val = 10 * np.sin(x_val) * np.exp(-0.05 * x_val)
    y_noise = normal(y_val, 10)

    # ex filter_mean
    y_filt = filter_mean(y_noise, window_size=10)

    if make_plots:
        fig, ax = plt.subplots(figsize=[18, 9])
        fig.sfn = "ex_filter_mean"
        plot_dict = {'title': 'Filter'}
        tab_dict_1 = {'legend': 'noised sin', 'form': 'r-'}
        tab_dict_2 = {'legend': 'filtered signal', 'form': 'b-'}
        plot_graph(ax, x_val, [y_noise, y_filt], plot_dict=plot_dict,
                   tabs_dict=[tab_dict_1, tab_dict_2])
        return [fig]
    else:
        return y_filt


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "core_noise", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_gen_noise(make_plots=True)
    figs += ex_filter_mean(make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
