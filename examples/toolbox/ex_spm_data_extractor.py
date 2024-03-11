"""
Example of spm_data_extractor methods
"""

import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.spm_data_extractor import main_spm_data_extractor


def example_spm_data_extractor(verbose=False, make_plots=False):
    """
    Example of spm_data_extractor main function

    Parameters
    ----------
    verbose: bool, optional
        If True, prints verbose information
    make_plots: bool, optional
        Activation key for figures generation

    Returns
    -------
    out: figure or dictionaries
        Result of data extraction
    """

    # File paths and settings
    dir_name = "PZT100n_reduced"
    file_name = 'PIT_SSPFM_DFRT_T2ms_map.0_00000.spm'
    example_root_path_in = get_setting("example_root_path_in")
    f_path = os.path.join(example_root_path_in, dir_name, file_name)

    # ex main_spm_data_extractor
    out = main_spm_data_extractor(
        f_path, nb_hold_seg_start=2, nb_hold_seg_end=1, verbose=verbose,
        make_plots=make_plots)

    return out


if __name__ == "__main__":
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "spm_data_extractor", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_spm_data_extractor(verbose=True, make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
