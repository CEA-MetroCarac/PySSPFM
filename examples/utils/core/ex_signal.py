"""
Examples with signal functions
"""
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.core.noise import noise
from PySSPFM.utils.core.signal import interpolate, line_reg


def sinc_exp(x, coef_a, coef_b, coef_c, coef_d, coef_e):
    """ Function model """

    sin_c = coef_a * np.sin(coef_b * np.array(x)) / x
    exp = coef_c * np.exp(coef_d * x)

    return sin_c + exp + coef_e


def ex_line_reg(verbose=False, make_plots=False):
    """
    Example of linear regression.

    Parameters
    ----------
    verbose: bool, optional
        Flag to enable verbose printing. Defaults to False.
    make_plots: bool, optional
        Flag to enable plot generation. Defaults to False.

    Returns
    -------
    dict or list
        If make_plots is True, returns a list containing the generated figure.
        Otherwise, returns a dictionary with regression results.
    """
    np.random.seed(0)
    noise_pars = {'type': 'normal', 'ampli': 20}
    x_val = np.linspace(0, 10, 200)
    y_func = [5 * elem + 2 for elem in x_val]
    y_val = noise(y_func, noise_pars)

    # Fit performing: ex line_reg
    results = line_reg(x_val, y_val, n_sample=50)

    # Print
    if verbose:
        print("Linear regression:\n"
              f"- slope (95%): {results['coefs'][0]:.6f} "
              f"+/- {results['unc a']:.6f}\n"
              f"- intercept: {results['coefs'][1]:.6f}\n"
              f"- R²: {results['r**2']:.6f}\n")

    # Plot
    if make_plots:
        fig, ax = plt.subplots()
        fig.sfn = "ex_lin_reg"
        plot_dict = {'title': 'Linear regression', 'fs': 13, 'edgew': 3,
                     'tickl': 5, 'gridw': 1, 'x lab': 'x axis'}
        tab_dict_1 = {'legend': 'data', 'form': 'r.'}
        tab_dict_2 = {'legend': 'target', 'form': 'k--'}
        tab_dict_3 = {'legend': 'fit', 'form': 'b-'}
        tabs_dict = [tab_dict_1, tab_dict_2, tab_dict_3]
        x_tabs = [x_val, x_val, results['x fit']]
        y_tabs = [y_val, y_func, results['y fit']]
        plot_graph(ax, x_tabs, y_tabs, plot_dict=plot_dict, tabs_dict=tabs_dict)

        return [fig]

    else:
        return results


def ex_interpolate(make_plots=False):
    """
    Example of interpolate function.

    Parameters
    ----------
    make_plots: bool, optional
        If True, generate a plot.

    Returns
    -------
    results: dict
        Dictionary containing interpolated x and y values, and interpolation
        function.
    """
    np.random.seed(0)
    noise_pars = {'type': 'normal', 'ampli': .5}
    x_val = np.linspace(-5 * np.pi, 5 * np.pi, 200)
    y_val = noise([sinc_exp(elem, 2, 2, 1, 0.1, -1) for elem in x_val],
                  noise_pars)

    # ex interpolate
    results = interpolate(x_val, y_val, 10)

    if make_plots:
        plot_dict = {'title': 'Interpolation'}
        tab_dict_1 = {'legend': 'data', 'form': 'ro'}
        tab_dict_2 = {'legend': 'interpolation', 'form': 'b-'}
        tabs_dict = [tab_dict_1, tab_dict_2]
        fig, ax = plt.subplots(figsize=[18, 9])
        fig.sfn = "ex_interpolate"
        plot_graph(ax, [x_val, results['x interp']],
                   [y_val, results['y interp']], plot_dict=plot_dict,
                   tabs_dict=tabs_dict)
        return [fig]
    else:
        return results['x interp'], results['y interp']


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "core_signal", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_line_reg(verbose=True, make_plots=True)
    figs += ex_interpolate(make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
