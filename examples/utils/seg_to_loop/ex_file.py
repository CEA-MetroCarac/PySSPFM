"""
Example of file methods
"""
import os
import shutil
import time
from datetime import datetime

from examples.utils.seg_to_loop.ex_gen_datas import pars_segment
from PySSPFM.utils.raw_extraction import csv_meas_sheet_extract
from PySSPFM.utils.seg_to_loop.file import print_pars, save_txt_file

from settings import \
    EXAMPLE_ROOT_PATH_IN, EXAMPLE_ROOT_PATH_OUT, DEFAULT_DATA_PATH_OUT


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
    dir_path_in = os.path.join(EXAMPLE_ROOT_PATH_IN, "KNN500n")
    if verbose:
        dir_path_out = os.path.join(
            EXAMPLE_ROOT_PATH_OUT, "ex_seg_to_loop_file")
    else:
        dir_path_out = os.path.join(
            DEFAULT_DATA_PATH_OUT, "test_seg_to_loop_file")

    # Remove output directory if it already exists
    if os.path.isdir(dir_path_out):
        shutil.rmtree(dir_path_out)

    t0, date = time.time(), datetime.now()
    date = date.strftime('%Y-%m-%d %H;%M')

    # Get parameters
    _, _, _, _, _, _, user_pars = pars_segment()
    user_pars['f path'] = dir_path_in
    meas_pars, sign_pars = csv_meas_sheet_extract(user_pars['f path'])

    # ex print_pars
    if verbose:
        print('- ex print_pars:')
    print_pars(meas_pars, sign_pars, user_pars, verbose=verbose)

    # ex save_txt_file
    save_txt_file(dir_path_out, t0, date, user_pars, meas_pars, sign_pars, 0)


if __name__ == '__main__':
    example_file(verbose=True)
