"""
Examples of peak applications
"""
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.core.noise import noise
from PySSPFM.utils.core.basic_func import gaussian, linear
from PySSPFM.utils.core.peak import \
    detect_peak, find_main_peaks, width_peak, guess_bckgnd, guess_affine


def ex_find_main_peaks(make_plots=False):
    """
    Example of find_main_peaks function.

    Parameters
    ----------
    make_plots: bool, optional
        Activation key for matplotlib figures generation.

    Returns
    -------
    list or tuple
        When make_plots is True, returns a list containing the figure object.
        When make_plots is False, returns a tuple containing the peaks, main,
        and lim values.
    """
    np.random.seed(0)
    x = np.linspace(0, 10, 1001)
    y = np.zeros(1201)
    amp = np.random.random(3) * 10
    position_inc = 2.5
    for i in range(1, 4):
        y_gauss = gaussian(x, ampli=amp[i - 1], fwhm=1.5, x0=i * position_inc)
        y = [elem_y + elem_peak for elem_y, elem_peak in zip(y, y_gauss)]
    noise_pars = {'type': 'normal', 'ampli': 4}
    y = noise(y, noise_pars)
    dist_min, width_min = int(len(x) / 10), int(len(x) / 100)

    # ex find_main_peaks
    res = find_main_peaks(x, y, nb_peak=3, dist_min=dist_min,
                          width_min=width_min)

    if make_plots:
        fig, ax = plt.subplots(figsize=[18, 9])
        fig.sfn = "ex_find_main_peaks"
        plot_dict = {'title': 'peak detection'}
        tab_dict = {'form': 'g-'}
        plot_graph(ax, x, y, plot_dict=plot_dict, tabs_dict=tab_dict)
        for peak in res['peaks']:
            ax.plot(x[peak], y[peak], 'rx', ms=10)
        return [fig]
    else:
        return res['peaks'], res['main'], res['lim']


def ex_detect_peak(verbose=False):
    """
    Example of detect_peak function.

    Parameters
    ----------
    verbose: bool, optional
        Activation key for verbose mode.

    Returns
    -------
    list or tuple
        If verbose is True, returns an empty list.
        If verbose is False, returns a tuple containing the test_peak and
        test_bckgnd values.
    """
    np.random.seed(0)
    x = np.linspace(0, 10, 101)
    y_peak = gaussian(x, ampli=2, fwhm=1, x0=5)
    pars_bckgnd = {'slope': 0.2, 'bckgnd': 2}
    noise_pars = {'type': 'normal', 'ampli': 1}
    bckgnd = linear(x, pars_bckgnd['bckgnd'], pars_bckgnd['slope'])
    y = noise(y_peak + bckgnd, noise_pars)
    backnd_seg = noise(bckgnd, noise_pars)

    # ex detect peak for peak segment
    test_peak = detect_peak(x, y)

    # ex detect peak for no segment
    test_bckgnd = detect_peak(x, backnd_seg)

    if verbose:
        print('# ex_detect_peak:')
        print(f'\t- peak signal: peak detected ?: {test_peak}')
        print(f'\t- bckgnd signal: peak detected ?: {test_bckgnd}')
        return []
    else:
        return test_peak, test_bckgnd


def ex_width_peak(make_plots=False):
    """
    Example of width_peak function.

    Parameters
    ----------
    make_plots: bool, optional
        Activation key for generating plots.

    Returns
    -------
    dict or list
        When make_plots is True, returns a list containing the figure object.
        When make_plots is False, returns a dictionary containing the width
        information.
    """
    np.random.seed(0)
    x = np.linspace(0, 10, 101)
    y_peak = gaussian(x, ampli=2, fwhm=2, x0=5)
    y_bckgnd = linear(x, 2, 0)
    noise_pars = {'type': 'normal', 'ampli': 0.5}
    y = noise(y_peak + y_bckgnd, noise_pars)
    threshold = (max(y) - min(y)) / 2 + min(y)

    # ex width_peak
    width = width_peak(x, y, np.argmax(y), threshold)

    if make_plots:
        fig, ax = plt.subplots(figsize=[18, 9])
        fig.sfn = "ex_width_peak"
        plot_dict = {'title': 'width peak determination'}
        tab_dict = {'form': 'g-', 'legend': 'data'}
        plot_graph(ax, x, y, plot_dict=plot_dict, tabs_dict=tab_dict)
        plt.axvline(x[width['ind left']], ls=':', c='k', lw=2, label='width')
        plt.axvline(x[width['ind right']], ls=':', c='k', lw=2)
        plt.axhline(threshold, ls='--', c='k', lw=2, label='threshold')
        plt.legend()
        return [fig]
    else:
        return width


def ex_guess_affine(make_plots=False):
    """
    Example of guess_affine function.

    Parameters
    ----------
    make_plots: bool, optional
        Activation key for generating plots.

    Returns
    -------
    float or list
        When make_plots is True, returns a list containing the figure object.
        When make_plots is False, returns the slope and background values.
    """
    np.random.seed(0)
    x = np.linspace(0, 10, 101)
    y_peak = gaussian(x, ampli=2, fwhm=2, x0=5)
    y_bckgnd = linear(x, 2, 0.2)
    noise_pars = {'type': 'normal', 'ampli': 0.2}
    y = noise(y_peak + y_bckgnd, noise_pars)

    # ex guess_affine
    slope, bckgnd = guess_affine(x, y, x_bckgnd=20)

    if make_plots:
        fig, ax = plt.subplots(figsize=[18, 9])
        fig.sfn = "ex_guess_affine"
        plot_dict = {'title': 'guess affine component'}
        tab_dict_1 = {'form': 'g-', 'legend': 'data'}
        tab_dict_2 = {'form': 'k-', 'legend': 'guess affine'}
        tab_dict_3 = {'form': 'r-', 'legend': 'target'}
        plot_graph(ax, x, [y, linear(x, bckgnd, slope), y_bckgnd],
                   plot_dict=plot_dict,
                   tabs_dict=[tab_dict_1, tab_dict_2, tab_dict_3])
        return [fig]
    else:
        return slope, bckgnd


def ex_guess_bckgnd(make_plots=False):
    """
    Example of guess_bckgnd function.

    Parameters
    ----------
    make_plots: bool, optional
        Activation key for generating plots.

    Returns
    -------
    float or list
        When make_plots is True, returns a list containing the figure object.
        When make_plots is False, returns the background value.
    """
    np.random.seed(0)
    x = np.linspace(0, 10, 101)
    y_peak = gaussian(x, ampli=2, fwhm=2, x0=5)
    y_bckgnd = linear(x, 2, 0)
    noise_pars = {'type': 'normal', 'ampli': 0.2}
    y = noise(y_peak + y_bckgnd, noise_pars)

    # ex guess_bckgnd
    bckgnd = guess_bckgnd(y, x_bckgnd=20)

    if make_plots:
        fig, ax = plt.subplots(figsize=[18, 9])
        fig.sfn = "ex_guess_bckgnd"
        plot_dict = {'title': 'guess bckgnd component'}
        tab_dict_1 = {'form': 'g-', 'legend': 'data'}
        tab_dict_2 = {'form': 'k-', 'legend': 'guess bckgnd'}
        tab_dict_3 = {'form': 'r-', 'legend': 'target'}
        plot_graph(ax, x, [y, linear(x, bckgnd, 0), y_bckgnd],
                   plot_dict=plot_dict,
                   tabs_dict=[tab_dict_1, tab_dict_2, tab_dict_3])
        return [fig]
    else:
        return bckgnd


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "core_peak", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_find_main_peaks(make_plots=True)
    figs += ex_detect_peak(verbose=True)
    figs += ex_width_peak(make_plots=True)
    figs += ex_guess_affine(make_plots=True)
    figs += ex_guess_bckgnd(make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
