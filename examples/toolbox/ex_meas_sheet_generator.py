"""
Example of meas_sheet_generator methods
"""

import os
import shutil

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.toolbox.meas_sheet_generator import main_meas_sheet_generator


def example_meas_sheet_generator(verbose=False):
    """
    Example of meas_sheet_generator main function

    Parameters
    ----------
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    indexs: list of str
        Indexes of the modified cells
    values: list
        Values of the modified cells
    """

    # Define paths
    dir_path_in = os.path.join(get_setting("example_root_path_in"),
                               'CSV measurement sheet')
    content_path_out = os.path.join(get_setting("example_root_path_in"),
                                    'PZT100n_reduced')
    # Find csv measurement sheet
    file_path_in = None
    csv_paths = os.listdir(dir_path_in)
    for csv_path in csv_paths:
        if "measurement sheet model SSPFM" in os.path.split(csv_path)[1]:
            file_path_in = os.path.join(dir_path_in, csv_path)
            break

    if verbose:
        dir_path_out_data = os.path.join(
            get_setting("example_root_path_out"), 'ex_meas_sheet_generator')
    else:
        dir_path_out_data = os.path.join(
            get_setting("default_data_path_out"), 'ex_meas_sheet_generator')

    # Remove existing output directory and create a new one
    shutil.rmtree(dir_path_out_data, ignore_errors=True)
    shutil.copytree(content_path_out, dir_path_out_data)

    if verbose:
        print('\nex meas_sheet_generator:')

    # ex main_meas_sheet_generator
    indexs, values = main_meas_sheet_generator(
        file_path_in, dir_path_out_data, extension=".spm",
        nb_hold_seg_start=2, nb_hold_seg_end=1, verbose=verbose)
    return indexs, values


if __name__ == "__main__":
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "meas_sheet_generator", save_example_exe=True, save_test_exe=False)
    figs = []
    example_meas_sheet_generator(verbose=True)
