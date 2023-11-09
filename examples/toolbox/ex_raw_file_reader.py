"""
Example of raw_file_reader methods
"""

import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.raw_file_reader import main_raw_file_reader


def example_raw_file_reader(ext, verbose=False):
    """
    Example of raw_file_reader main function

    Parameters
    ----------
    ext: str
        File extension ['spm', 'txt', 'csv', 'xlsx']
    verbose: bool, optional
        If True, prints verbose information

    Returns
    -------
    fig: matplotlib.figure.Figure
        The generated matplotlib figure
    """
    assert ext in ['spm', 'txt', 'csv', 'xlsx']

    # File paths and settings
    dir_name = "KNN500n_reduced"
    if ext != 'spm':
        dir_name += f'_datacube_{ext}'
    file_name = 'KNN500n_SSPFM.0_00056' + f'.{ext}'
    mode = 'dfrt'
    example_root_path_in = get_setting("example_root_path_in")
    f_path = os.path.join(example_root_path_in, dir_name, file_name)

    # ex main_raw_file_reader
    fig = main_raw_file_reader(f_path, mode, verbose=verbose)
    for elem in fig:
        elem.sfn += f"_{ext}"

    return fig


if __name__ == "__main__":
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "raw_file_reader", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_raw_file_reader('spm', verbose=True)
    figs += example_raw_file_reader('txt', verbose=True)
    figs += example_raw_file_reader('csv', verbose=True)
    figs += example_raw_file_reader('xlsx', verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
