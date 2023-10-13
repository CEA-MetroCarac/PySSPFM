"""
Examples of theory methods
"""
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop.theory import main


def example_theory():
    """
    Example of theory main function.

    Returns
    -------
    figs_theory: list
        List of figures.
    """
    # Physical parameters
    write_pars = {'range': [-10, 10],
                  'nb': 201,
                  'mode': 'Zero, up'}
    read_pars = {'value': 0}
    elec_pars = {'cpd': 0.3,
                 'slope': -3}
    ferro_pars = {'amp': 5,
                  'coer l': -4,
                  'coer r': 3,
                  'sw slope': 1,
                  'offset': 1}

    user_pars = {'write': write_pars,
                 'read': read_pars,
                 'elec': elec_pars,
                 'ferro': ferro_pars}

    pha_val = {"fwd": 0, "rev": 180}

    # ex main
    figs_theory = main(user_pars, pha_val=pha_val)

    return figs_theory


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_theory", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_theory()
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
