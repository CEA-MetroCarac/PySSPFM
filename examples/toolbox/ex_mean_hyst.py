"""
Example of mean_hyst methods
"""
import os
import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.mean_hyst import main_mean_hyst

from PySSPFM import EXAMPLE_ROOT_PATH_IN


def example_mean_hyst(phase='1', mode='off', verbose=False, make_plots=False):
    """
    Example of mean_hyst functions.

    Parameters
    ----------
    phase: str, optional
        Phase value ('1' or '2') (default is '1').
    mode: str, optional
        Mode value ('off', 'on', 'coupled') (default is 'off').
    verbose: bool, optional
        Verbosity flag (default is False).
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    figures: list or None
        List of figures when make_plots is True, None otherwise.
    mean_best_loop: array or None
        Array of mean best nanoloops if mode is 'on' or 'off', None otherwise.
    best_hysts: dict or None
        Dictionary of the best hysteresis if mode is 'on' or 'off',
        None otherwise.
    mean_diff_piezorep: array or None
        Array of mean differential piezoresponse if mode is 'coupled',
        None otherwise.
    fit_res: dict or None
        Dictionary of fit results if mode is 'coupled', None otherwise.
    """
    assert phase in ['1', '2']
    assert mode in ['off', 'on', 'coupled']

    user_pars = {'mode': mode,
                 'mask': {'man mask': None,
                          'ref': {'prop': 'fit pars: ampli_0',
                                  'mode': mode,
                                  'min val': None,
                                  'max val': None,
                                  'fmt': '.2f',
                                  'interactive': False}},
                 'func': 'sigmoid',
                 'method': 'least_square',
                 'asymmetric': False,
                 'inf thresh': 10,
                 'sat thresh': 90,
                 'del 1st loop': True,
                 'pha corr': 'offset',
                 'pha fwd': 0,
                 'pha rev': 180,
                 'pha func': np.cos,
                 'main elec': True,
                 'locked elec slope': None,
                 'diff domain': {'min': -5., 'max': 5.},
                 'sat mode': 'set',
                 'sat domain': {'min': -9., 'max': 9.},
                 'interp fact': 4,
                 'interp func': 'linear'}

    if mode == 'coupled':
        user_pars['mask']['ref']['prop'] = 'a'
        # Select ferro phase 1 or 2 measurement or not depending on mode
        if phase == '1':
            user_pars['mask']['ref']['max val'] = -0.0001
            user_pars['mask']['ref']['min val'] = -0.00025
        else:
            user_pars['mask']['ref']['max val'] = -0.00025
    elif mode == 'off':
        # Select ferro phase 1 or 2 measurement or not depending on mode
        if phase == '1':
            user_pars['mask']['ref']['min val'] = 0.001
        else:
            user_pars['mask']['ref']['min val'] = 0.0002
            user_pars['mask']['ref']['max val'] = 0.001
    elif mode == 'on':
        # Select ferro phase 1 or 2 measurement or not depending on mode
        if phase == '1':
            user_pars['mask']['ref']['min val'] = -0.0025
        else:
            user_pars['mask']['ref']['max val'] = -0.0025
    else:
        raise IOError("mode should be in 'off', 'on', 'coupled'")
    # file management
    dir_path_in = os.path.join(
        EXAMPLE_ROOT_PATH_IN, "KNN500n_2023-10-05-17h23m_out_dfrt")
    dir_path_in_props = os.path.join(dir_path_in, "properties")
    dir_path_in_loop = os.path.join(dir_path_in, "nanoloops")
    file_path_in_pars = os.path.join(dir_path_in, "parameters.txt")
    user_pars['dir path in prop'] = dir_path_in_props
    user_pars['dir path in loop'] = dir_path_in_loop
    user_pars['file path in pars'] = file_path_in_pars

    # ex main_mean_hyst
    if make_plots:
        figures = main_mean_hyst(
            user_pars, verbose=verbose, make_plots=make_plots)
        for fig in figures:
            fig.sfn += f"_{phase}_{mode}"
        return figures
    elif mode in ['on', 'off']:
        mean_best_loop, best_hysts = main_mean_hyst(
            user_pars, verbose=verbose, make_plots=make_plots)
        return mean_best_loop, best_hysts
    else:
        mean_diff_piezorep, fit_res = main_mean_hyst(
            user_pars, verbose=verbose, make_plots=make_plots)
        return mean_diff_piezorep, fit_res


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "mean_hyst", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_mean_hyst(phase='1', mode='on', verbose=True,
                              make_plots=True)
    figs += example_mean_hyst(phase='1', mode='off', verbose=True,
                              make_plots=True)
    figs += example_mean_hyst(phase='1', mode='coupled', verbose=True,
                              make_plots=True)
    figs += example_mean_hyst(phase='2', mode='on', verbose=True,
                              make_plots=True)
    figs += example_mean_hyst(phase='2', mode='off', verbose=True,
                              make_plots=True)
    figs += example_mean_hyst(phase='2', mode='coupled', verbose=True,
                              make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
