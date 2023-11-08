"""
Example of spm_converter methods
"""

import os
import shutil

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.raw_extraction import data_extraction
from PySSPFM.toolbox.raw_file_reader import main_raw_file_reader
from PySSPFM.toolbox.spm_converter import main_spm_converter

from PySSPFM.settings import \
    EXAMPLE_ROOT_PATH_IN, EXAMPLE_ROOT_PATH_OUT, DEFAULT_DATA_PATH_OUT


def example_spm_converter(ext, make_plots=False, verbose=False):
    """
    Example of spm_converter main function

    Parameters
    ----------
    ext: str
        Converted file extension ['txt', 'csv', 'xlsx']
    make_plots: bool, optional
        Indicates whether to generate plots
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    dict_meas, script_dict or figs_datas_file
        Dictionary of measurements and script information or list of figures
        and data files
    """
    assert ext in ['txt', 'csv', 'xlsx']

    # Define paths
    dir_path_in = os.path.join(EXAMPLE_ROOT_PATH_IN, 'KNN500n_reduced')
    if make_plots:
        dir_path_out_data = os.path.join(
            EXAMPLE_ROOT_PATH_OUT, f'KNN500n_reduced_datacube_{ext}')
    else:
        dir_path_out_data = os.path.join(
            DEFAULT_DATA_PATH_OUT, f'KNN500n_reduced_datacube_{ext}')

    # Remove existing output directory and create a new one

    shutil.rmtree(dir_path_out_data, ignore_errors=True)
    os.makedirs(dir_path_out_data)

    file_name = 'KNN500n_SSPFM.0_00056'
    mode = 'dfrt'

    # ex main_spm_converter
    main_spm_converter(
        dir_path_in, mode=mode, extension=ext, dir_path_out=dir_path_out_data,
        verbose=verbose)

    if make_plots:
        figs_datas_file = []
        fig1 = main_raw_file_reader(
            os.path.join(dir_path_in, file_name + '.spm'), mode)
        figs_datas_file += fig1
        fig2 = main_raw_file_reader(
            os.path.join(dir_path_out_data, file_name + f'.{ext}'), mode)
        figs_datas_file += fig2
        for fig in figs_datas_file:
            fig.sfn += f"_{ext}"
        return figs_datas_file
    else:
        out = data_extraction(os.path.join(dir_path_out_data,
                                           file_name + f'.{ext}'),
                              mode_dfrt=bool(mode.lower() == 'dfrt'),
                              verbose=verbose)
        dict_meas, script_dict = out
        return dict_meas, script_dict


if __name__ == "__main__":
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "spm_converter", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_spm_converter('txt', make_plots=True, verbose=True)
    figs += example_spm_converter('csv', make_plots=True, verbose=True)
    figs += example_spm_converter('xlsx', make_plots=True, verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
