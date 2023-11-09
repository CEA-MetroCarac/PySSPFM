"""
Example of signal_bias functions
"""
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.signal_bias import \
    (sspfm_generator, sspfm_time, dynamic_generator, ckpfm_generator,
     extract_sspfm_bias_pars)


def example_sspfm_bias(open_mode=False, verbose=False, make_plots=False):
    """
    Example of sspfm_bias functions

    Parameters
    ----------
    open_mode: bool, optional
        Flag indicating open mode
    verbose: bool, optional
        If True, prints the script dictionary
    make_plots: bool, optional
        Flag indicating whether to create plots

    Returns
    -------
    output: tuple or list
        When make_plots is True, returns a list containing the figure object.
        Otherwise, returns a tuple containing sspfm_bias, real_sspfm_time, and
        real_sspfm_bias, extracted_bias_pars.
    """
    sspfm_pars = {
        'Min volt (R) [V]': 0,
        'Max volt (R) [V]': 0,
        'Nb volt (R)': 10,
        'Mode (R)': 'Low to High',
        'Seg durat (R) [ms]': 500,
        'Seg sample (R)': 100,
        'Min volt (W) [V]': -10,
        'Max volt (W) [V]': 10,
        'Nb volt (W)': 9,
        'Mode (W)': 'Zero, up',
        'Seg durat (W) [ms]': 500,
        'Seg sample (W)': 100
    }
    start_hold_time = 1

    # ex sspfm_generator
    sspfm_bias = sspfm_generator(sspfm_pars, open_mode=open_mode)

    # ex extract_sspfm_bias_pars
    extracted_bias_pars = {}
    if open_mode is False:
        extracted_bias_pars = extract_sspfm_bias_pars(sspfm_bias)
        if verbose:
            print(f"initial sspfm pars: {sspfm_pars}")
            print(f"extracted sspfm pars: {extracted_bias_pars}")

    # ex sspfm_time
    out = sspfm_time(sspfm_bias, sspfm_pars, start_hold_time=start_hold_time)
    (real_sspfm_time, real_sspfm_bias) = out
    if make_plots:
        # Create plot
        plot_dict = {'x lab': 'time (s)', 'y lab': 'sspfm bias (V)'}
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(figsize=figsize)
        add_str = "_open" if open_mode else ""
        fig.sfn = f"example_sspfm_bias{add_str}"
        plot_graph(ax, real_sspfm_time, real_sspfm_bias, plot_dict=plot_dict)

        return [fig]
    else:
        return sspfm_bias, real_sspfm_time, real_sspfm_bias, extracted_bias_pars


def example_dynamic_bias(make_plots=False):
    """
    Example of dynamic_generator functions

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to create plots

    Returns
    -------
    output: tuple or list
        When make_plots is True, returns a list containing the figure object.
        Otherwise, returns a tuple containing dynamic_time and dynamic_bias.
    """
    dynamic_pars = {
        'Time (read)': 5,
        'Bias (read)': 0,
        'Time (set)': 10,
        'Bias (set)': -5,
        'Min bias (switch)': 2,
        'Max bias (switch)': 6,
        'Nb bias (switch)': 5,
        'Min time (switch)': 1,
        'Max time (switch)': 1000,
        'Nb time (switch)': 10,
        'Freq ech': 10
    }

    # ex dynamic_generator
    dynamic_bias, dynamic_time = dynamic_generator(dynamic_pars)

    if make_plots:
        # Create plot
        plot_dict = {'x lab': 'time (s)', 'y lab': 'dynamic bias (V)'}
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(figsize=figsize)
        fig.sfn = "example_dynamic_bias"
        plot_graph(ax, dynamic_time, dynamic_bias, plot_dict=plot_dict)

        return [fig]
    else:
        return dynamic_time, dynamic_bias


def example_ckpfm_bias(mode='Sweep', make_plots=False):
    """
    Example of ckpfm_bias functions

    Parameters
    ----------
    mode: str, optional
        Mode parameter for ckpfm_generator function
    make_plots: bool, optional
        Flag indicating whether to create plots

    Returns
    -------
    output: tuple or list
        When make_plots is True, returns a list containing the figure object.
        Otherwise, returns a tuple containing ckfpm_time and ckfpm_bias.
    """
    ckpfm_pars = {
        'Min volt (R) [V]': -4,
        'Max volt (R) [V]': 4,
        'Mode (R)': mode,
        'Order (R)': 'Up',
        'Seg durat (R) [ms]': 500,
        'Seg sample (R)': 500,
        'Min volt (W) [V]': -10,
        'Max volt (W) [V]': 10,
        'Nb volt (W)': 41,
        'Mode (W)': 'Zero, up',
        'Seg durat (W) [ms]': 500,
        'Seg sample (W)': 100,
        'Freq ech': 10
    }

    # ex ckpfm_generator
    ckfpm_bias, ckfpm_time = ckpfm_generator(ckpfm_pars)

    if make_plots:
        # Create plot
        plot_dict = {'x lab': 'time (s)', 'y lab': 'ckpfm bias (V)'}
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(figsize=figsize)
        fig.sfn = f"example_ckpfm_{mode}_bias"
        plot_graph(ax, ckfpm_time, ckfpm_bias, plot_dict=plot_dict)

        return [fig]
    else:
        return ckfpm_time, ckfpm_bias


if __name__ == "__main__":
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "signal_bias", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_sspfm_bias(open_mode=False, verbose=True, make_plots=True)
    figs += example_sspfm_bias(open_mode=True, verbose=True, make_plots=True)
    figs += example_dynamic_bias(make_plots=True)
    figs += example_ckpfm_bias(mode='Sequence_11', make_plots=True)
    figs += example_ckpfm_bias(mode='Sweep', make_plots=True)
    figs += example_ckpfm_bias(mode='Dual_sweep', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
