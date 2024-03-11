"""
Example of file methods
"""
import os
import shutil
import time
from datetime import datetime

from examples.utils.datacube_to_nanoloop.ex_gen_data import pars_segment
from PySSPFM.settings import get_setting
from PySSPFM.utils.raw_extraction import csv_meas_sheet_extract
from PySSPFM.utils.datacube_to_nanoloop.file import \
    print_params, save_parameters, get_acquisition_time, get_file_names


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
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        SSPFM bias signal parameters
    dir_path_out: str
        Directory path of the output files
    """
    # In and out file management
    dir_path_in = os.path.join(get_setting("example_root_path_in"), "KNN500n")
    if verbose:
        dir_path_out = os.path.join(
            get_setting("example_root_path_out"), "ex_seg_to_loop_file")
    else:
        dir_path_out = os.path.join(
            get_setting("default_data_path_out"), "test_seg_to_loop_file")

    # Remove output directory if it already exists
    if os.path.isdir(dir_path_out):
        shutil.rmtree(dir_path_out)

    t0, date = time.time(), datetime.now()
    date = date.strftime('%Y-%m-%d %H;%M')

    # Get parameters
    _, _, _, _, _, _, user_pars = pars_segment()
    user_pars['f path'] = dir_path_in
    meas_pars, sign_pars = csv_meas_sheet_extract(user_pars['f path'])

    # ex get_file_names
    file_names_ordered = get_file_names(dir_path_in, file_format=".txt")

    # ex print_params
    if verbose:
        print('- ex print_params:')
    print_params(meas_pars, sign_pars, user_pars, verbose=verbose)

    # ex get_acquisition_time
    exp_meas_time = get_acquisition_time(dir_path_in, file_format='.txt')
    if verbose:
        print('\n- ex get_acquisition_time:')
        print(f'experimental acquisition time [s]: {exp_meas_time}')

    # ex save_parameters
    save_parameters(dir_path_out, t0, date, exp_meas_time, user_pars, meas_pars,
                    sign_pars, 0)

    return exp_meas_time, file_names_ordered


if __name__ == '__main__':
    example_file(verbose=True)
