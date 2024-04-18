"""
Example of phase_offset_analyzer methods
"""

import os

from examples.utils.datacube_to_nanoloop.ex_gen_data import pars_segment

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.phase_offset_analyzer import main_phase_offset_analyzer


def example_phase_offset_analyzer(make_plots=False, verbose=False):
    """
    Example of main_phase_offset_analyzer functions.

    Parameters
    ----------
    make_plots: bool, optional
        Flag to indicate whether to generate plots or not (default is False)
    verbose: bool, optional
        Flag to activate verbosity (default is False)

    Returns
    -------
    figures: list of plt.figure
        If make_plots is True, returns a list containing the generated figures.
        If make_plots is False, returns phase offset table.
    """
    # Path management
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(example_root_path_in, "PZT100n")

    # Configuration parameters
    _, _, _, _, _, _, user_pars = pars_segment()

    # ex main_phase_offset_analyzer
    phase_offset_tab, map_dim, figures = \
        main_phase_offset_analyzer(user_pars, dir_path_in, range_file=None,
                                   extension="spm", verbose=verbose,
                                   make_plots=make_plots)

    if make_plots:
        return figures
    else:
        return phase_offset_tab, map_dim


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "phase_offset_analyzer.py", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_phase_offset_analyzer(make_plots=True, verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
