"""
Examples of fitting functions and class
"""
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.core import noise
from PySSPFM.utils.core.basic_func import \
    linear, gaussian, sho, sho_phase, sho_phase_switch
from PySSPFM.utils.core.fitting import GaussianPeakFit, ShoPeakFit, ShoPhaseFit


def ex_gaussian_peak_fit(verbose=False, make_plots=False):
    """ Example of gaussian peak fitting """
    np.random.seed(0)

    # Gaussian parameters
    offset, slope = 2, 0
    ampli, fwhm, x0,  = 10, 4, 0
    noise_ampli = 2

    # Noised gaussian creation
    x = np.linspace(-10, 10, 201)
    y_target = linear(x, offset, slope) + gaussian(x, ampli, fwhm, x0)
    y = noise.normal(y_target, noise_ampli)

    # Gaussian fitting
    gaussian_peak = GaussianPeakFit()
    gaussian_peak.fit(x, y, init_params=None)
    gaussian_pars = gaussian_peak.report_fit_results()

    if verbose:
        print("Fitting results :", gaussian_pars)

    if make_plots:
        fig = gaussian_peak.plot(x, y)
        fig.sfn = "ex_gaussian_peak_fit"
        return [fig]
    else:
        return gaussian_pars


def ex_sho_peak_fit(verbose=False, make_plots=False):
    """ Example of sho peak fitting """
    np.random.seed(0)

    # Sho parameters
    offset, slope = 2, 0
    ampli, coef, x0 = 1, 10, 10
    noise_ampli = 2

    # Noised sho creation
    x = np.linspace(0, 20, 201)
    y_target = linear(x, offset, slope) + sho(x, ampli, coef, x0)
    y = noise.normal(y_target, noise_ampli)

    # Sho fitting
    sho_peak = ShoPeakFit()
    sho_peak.fit(x, y, init_params=None)
    sho_pars = sho_peak.report_fit_results()

    if verbose:
        print("Fitting results :", sho_pars)

    if make_plots:
        fig = sho_peak.plot(x, y)
        fig.sfn = "ex_sho_peak_fit"
        return [fig]
    else:
        return sho_pars


def ex_sho_phase_fit(verbose=False, make_plots=False):
    """ Example of sho phase fitting """
    np.random.seed(0)

    # Sho phase parameters
    offset, slope = 1, 0
    ampli, coef, x0 = 1, 10, 10
    noise_ampli = 0.5

    # Noised sho phase creation
    x = np.linspace(0, 20, 201)
    y_target = linear(x, offset, slope) + sho_phase(x, ampli, coef, x0)
    y = noise.normal(y_target, noise_ampli)

    # Sho phase fitting
    sho_phase_obj = ShoPhaseFit()
    sho_phase_obj.fit(x, y, init_params=None)
    sho_phase_pars = sho_phase_obj.report_fit_results()

    if verbose:
        print("Fitting results :", sho_phase_pars)

    if make_plots:
        fig = sho_phase_obj.plot(x, y)
        fig.sfn = "ex_sho_phase_fit"
        return [fig]
    else:
        return sho_phase_pars


def ex_sho_phase_switch_fit(verbose=False, make_plots=False):
    """ Example of sho phase switch fitting """
    np.random.seed(0)

    # Sho phase switch parameters
    offset, slope = 1, 0
    ampli, coef, x0 = 1, 2, 10
    noise_ampli = 0.5

    # Noised sho phase switch creation
    x = np.linspace(0, 20, 201)
    y_target = linear(x, offset, slope) + sho_phase_switch(x, ampli, coef, x0)
    y = noise.normal(y_target, noise_ampli)

    # Sho phase switch fitting
    sho_phase_switch_obj = ShoPhaseFit(switch=True)
    sho_phase_switch_obj.fit(x, y, init_params=None)
    sho_phase_switch_pars = sho_phase_switch_obj.report_fit_results()

    if verbose:
        print("Fitting results :", sho_phase_switch_pars)

    if make_plots:
        fig = sho_phase_switch_obj.plot(x, y)
        fig.sfn = "ex_sho_phase_switch_fit"
        return [fig]
    else:
        return sho_phase_switch_pars


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "core_fitting", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_gaussian_peak_fit(verbose=True, make_plots=True)
    figs += ex_sho_peak_fit(verbose=True, make_plots=True)
    figs += ex_sho_phase_fit(verbose=True, make_plots=True)
    figs += ex_sho_phase_switch_fit(verbose=True, make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
