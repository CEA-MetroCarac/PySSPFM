"""
Example of file methods
"""
import os
import shutil

from examples.utils.datacube_to_nanoloop.ex_gen_data import pars_segment
from PySSPFM.settings import get_setting
from PySSPFM.utils.raw_extraction import csv_meas_sheet_extract
from PySSPFM.utils.datacube_to_nanoloop.file import \
    get_phase_tab_offset, print_params


def example_file(verbose=False):
    """
    Example of file functions

    Parameters
    ----------
    verbose: bool, optional
        Verbosity flag, controls whether to print additional information
        (default is False)

    Returns
    -------
    phase_tab : array-like
        Phase offset table extracted from a text file.
    """
    # In and out file management
    dir_path_in = os.path.join(get_setting("example_root_path_in"), "KNN500n")
    file_path_in_offset = \
        os.path.join(get_setting("example_root_path_in"), "KNN500n_toolbox",
                     "phase_offset_analyzer_2024-05-21-18h18m",
                     "phase_offset.txt")
    if verbose:
        dir_path_out = os.path.join(
            get_setting("example_root_path_out"), "ex_seg_to_loop_file")
    else:
        dir_path_out = os.path.join(
            get_setting("default_data_path_out"), "test_seg_to_loop_file")

    # Remove output directory if it already exists
    if os.path.isdir(dir_path_out):
        shutil.rmtree(dir_path_out)

    # Get parameters
    _, _, _, _, _, _, user_pars = pars_segment()
    user_pars['f path'] = dir_path_in
    meas_pars, sign_pars = csv_meas_sheet_extract(user_pars['f path'])

    # ex print_params
    if verbose:
        print('- ex print_params:')
    print_params(meas_pars, sign_pars, user_pars, verbose=verbose)

    # ex get_phase_tab_offset
    phase_tab = get_phase_tab_offset(file_path_in_offset)

    return phase_tab


if __name__ == '__main__':
    example_file(verbose=True)
