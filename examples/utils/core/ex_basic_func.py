"""
Examples of basic func
"""
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.core.basic_func import \
    (linear, sigmoid, arctan, gaussian, lorentzian, pseudovoigt, sho, sho_phase,
     sho_phase_switch)


def ex_basic_func(model, make_plots=False):
    """
    Example of basic function

    Parameters
    ----------
    model: str
        Curve model name
    make_plots: bool, optional
        Activation key for plot generation

    Returns
    -------
    a list of Matplotlib.Figures or list of params related to the fitted model
    """
    x = np.linspace(-10, 10, 201)

    if model == 'linear':
        y = linear(x, offset=1., slope=0.1)

    elif model == 'sigmoid':
        y = sigmoid(x, ampli=1, coef=2, x0=2, is_centered=True)

    elif model == 'arctan':
        y = arctan(x, ampli=1, coef=2, x0=2)

    elif model == 'gaussian':
        y = gaussian(x, ampli=1, fwhm=2, x0=2)

    elif model == 'lorentzian':
        y = lorentzian(x, ampli=1, fwhm=2, x0=2)

    elif model == 'pseudovoigt':
        y = pseudovoigt(x, ampli=1, fwhm=2, x0=2, alpha=0.5)

    elif model == 'sho':
        x = np.linspace(200, 300, 1001)
        y = sho(x, ampli=1, coef=100, x0=250)

    elif model == 'sho_phase':
        x = np.linspace(200, 300, 1001)
        y = sho_phase(x, ampli=1, coef=100, x0=250)

    elif model == 'sho_phase_switch':
        x = np.linspace(200, 300, 1001)
        y = sho_phase_switch(x, ampli=1, coef=100, x0=250)

    else:
        raise IOError("model not defined")

    if make_plots:
        fig = plt.figure()
        fig.sfn = f"ex_{model}_basic_func"
        plt.grid()
        plt.plot(x, y)

        return [fig]
    else:
        return y


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "core_basic_func", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_basic_func('linear', make_plots=True)
    figs += ex_basic_func('sigmoid', make_plots=True)
    figs += ex_basic_func('arctan', make_plots=True)
    figs += ex_basic_func('gaussian', make_plots=True)
    figs += ex_basic_func('lorentzian', make_plots=True)
    figs += ex_basic_func('pseudovoigt', make_plots=True)
    figs += ex_basic_func('sho', make_plots=True)
    figs += ex_basic_func('sho_phase', make_plots=True)
    figs += ex_basic_func('sho_phase_switch', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
