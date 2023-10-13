"""
Example of raw_extraction methods
"""
import os

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.seg_to_loop.plot import plt_signals
from PySSPFM.utils.raw_extraction import data_extraction, csv_meas_sheet_extract

from settings import EXAMPLE_ROOT_PATH_IN


def ex_data_extraction(ext, make_plots=False, verbose=False):
    """
    Example of data_extraction functions

    Parameters
    ----------
    ext: str
        File extension ['spm', 'txt', 'csv', 'xlsx']
    make_plots: bool, optional
        If True, plots the extracted data
    verbose: bool, optional
        If True, prints the script dictionary

    Returns
    -------
    dict_meas: dict
        All measurements in the extracted file
    script_dict: dict
        All parameters for the measurement script
    """
    assert ext in ['spm', 'txt', 'csv', 'xlsx']

    # File paths and settings
    dir_name = "KNN500n_reduced"
    if ext != 'spm':
        dir_name += f'_datacube_{ext}'
    file_name = 'KNN500n_SSPFM.0_00056' + f'.{ext}'
    mode_dfrt = True

    f_path = os.path.join(EXAMPLE_ROOT_PATH_IN, dir_name, file_name)

    # ex data_extraction
    dict_meas, script_dict = data_extraction(f_path, mode_dfrt=mode_dfrt,
                                             verbose=verbose)

    if verbose:
        print(f"{ext} file: {script_dict}")

    # Plotting
    if make_plots:
        fig = plt_signals(dict_meas, unit='')
        fig.sfn += f"_{ext}"
        return [fig]
    else:
        return dict_meas, script_dict


def ex_csv_meas_sheet_extract(verbose=False):
    """
    Example of csv_meas_sheet_extract functions

    Parameters
    ----------
    verbose: bool, optional
        If True, prints the script dictionary

    Returns
    -------
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        SSPFM bias signal parameters
    """

    dir_name = "KNN500n_reduced"
    csv_dir_path = os.path.join(EXAMPLE_ROOT_PATH_IN, dir_name)

    # ex csv_meas_sheet_extract
    meas_pars, sign_pars = csv_meas_sheet_extract(csv_dir_path)

    if verbose:
        print(f'measurement parameters: {meas_pars}')
        print(f'signal bias parameters: {sign_pars}')

    return meas_pars, sign_pars


if __name__ == "__main__":
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "raw_extraction", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_data_extraction('spm', make_plots=True, verbose=True)
    figs += ex_data_extraction('txt', make_plots=True, verbose=True)
    figs += ex_data_extraction('csv', make_plots=True, verbose=True)
    figs += ex_data_extraction('xlsx', make_plots=True, verbose=True)
    ex_csv_meas_sheet_extract(verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
