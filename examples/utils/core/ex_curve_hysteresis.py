"""
Examples with Hysteresis
"""
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.core import noise
from PySSPFM.utils.core.basic_func import linear, sigmoid
from PySSPFM.utils.core.curve_hysteresis import Hysteresis


def ex_hysteresis(asymmetric=False, verbose=False, make_plots=False):
    """ Example of symmetric/asymmetric hysteresis fitting """
    np.random.seed(0)

    # Hysteresis parameters
    offset, slope = 1, -0.1
    ampli, x0 = 10, [-1.5, 4.5]
    coef = [1, 3] if asymmetric else [3, 3]
    noise_ampli = 2

    # First branch creation
    x1 = np.linspace(-10, 10, 201)
    y1_target = linear(x1, offset, slope) + sigmoid(x1, ampli, coef[0], x0[0])
    y1 = noise.normal(y1_target, noise_ampli)

    # Second branch creation
    x2 = np.linspace(-10, 10, 101)
    y2_target = linear(x2, offset, slope) + sigmoid(x2, ampli, coef[1], x0[1])
    y2 = noise.normal(y2_target, noise_ampli)

    x, y = [x1, x2], [y1, y2]

    # Hysteresis fitting
    hyster_fit = Hysteresis(nbranches=2, asymmetric=asymmetric, model='sigmoid')
    hyster_fit.params['ampli_0'].set(min=0)
    hyster_fit.fit(x, y, verbosity=False)
    hyster_fit.properties(infl_threshold=10, sat_threshold=90)
    hyster_fit.r_square(x, y)

    if verbose:
        print("Fitting results :", hyster_fit.params)

    if make_plots:
        fig, ax = plt.subplots()
        add_sfn = "asymmetric" if asymmetric else ""
        fig.sfn = f"ex_hysteresis_{add_sfn}"

        plt.plot(x1, y1_target, '.-', label='branch1 (target)')
        plt.plot(x2, y2_target, '.-', label='branch2 (target)')

        labels = ['branch1 (fit)', 'branch2 (fit)']
        hyster_fit.plot(x, y, ax=ax, labels=labels)
        hyster_fit.plot_properties(x, ax=ax, plot_dict={'fs': 8})

        return [fig]
    else:
        return hyster_fit.params, hyster_fit.props


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "core_curve_hysteresis", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_hysteresis(verbose=True, make_plots=True)
    figs += ex_hysteresis(asymmetric=True, verbose=True, make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
