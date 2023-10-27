"""
Example of file methods
"""
import os
import shutil
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from examples.utils.hyst_to_map.ex_analysis import ex_sort_meas
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.nanoloop_to_hyst.file import \
    (generate_file_paths, read_plot_parameters, complete_txt_file,
     save_measurement, extract_measures)

from PySSPFM import \
    EXAMPLE_ROOT_PATH_IN, EXAMPLE_ROOT_PATH_OUT, DEFAULT_DATA_PATH_OUT
from PySSPFM.settings import FIGSIZE


def example_file(make_plots=False, verbose=False):
    """
    Example of file methods.

    Parameters
    ----------
    make_plots: bool, optional
        Whether to generate plots, defaults to False.
    verbose: bool, optional
        Whether to print verbose output, defaults to False.

    Returns
    -------
    file_paths: list
        List of file paths.
    meas_pars: dict
        Measurement parameters.
    sign_pars: dict
        Signal parameters.
    dict_analysis_1: dict
        Analysis dictionary.
    nb_write_per_read: int
        Number of writes per read.
    write_segment: list
        Write segment data.
    measurements: list
        Ferroelectric measurements.
    dim_pix: dict
        Dimension in pixels.
    dim_mic: dict
        Dimension in micrometers.
    """
    # Define input and output file paths
    root_data = os.path.join(
        EXAMPLE_ROOT_PATH_IN, "KNN500n_2023-10-05-17h21m_out_dfrt")
    dir_path_in = os.path.join(root_data, "txt_loops")
    if make_plots:
        root_out = os.path.join(EXAMPLE_ROOT_PATH_OUT, "ex_hyst_to_map_file")
    else:
        root_out = os.path.join(DEFAULT_DATA_PATH_OUT, "test_hyst_to_map_file")

    # Remove existing output directory and copy the data
    if os.path.isdir(root_out):
        shutil.rmtree(root_out)
    shutil.copytree(root_data, root_out)

    user_pars = {'dir path in': dir_path_in,
                 'func': 'sigmoid',
                 'method': 'leastsq',
                 'asymmetric': False,
                 'inf thresh': 10,
                 'sat thresh': 90,
                 'del 1st loop': True,
                 'pha corr': 'offset',
                 'pha fwd': 0,
                 'pha rev': 180,
                 'pha func': np.cos,
                 'main elec': True,
                 'locked elec slope': None,
                 'diff mode': 'set',
                 'diff domain': {'min': -5., 'max': 5.},
                 'sat mode': 'set',
                 'sat domain': {'min': -9., 'max': 9.}}

    t0, date = time.time(), datetime.now()
    date = date.strftime('%Y-%m-%d %H;%M')

    # Generate file paths
    file_paths = generate_file_paths(dir_path_in)
    if verbose:
        print('\t- ex generate_file_paths')
        for cont, elem in enumerate(file_paths):
            print(f'\t\tpath n°{cont + 1}: {elem}')
        print('\n')

    # ex read_plot_parameters
    file_path_in_txt_save = os.path.join(
        root_data, 'results', 'saving_parameters.txt')
    out = read_plot_parameters(file_path_in_txt_save, verbose=verbose)
    (meas_pars, sign_pars, dict_analysis_1, nb_write_per_read,
     write_segment) = out
    if verbose:
        print('\n\t- ex read_plot_parameters')
        print(f'\t\tnb write per read: {nb_write_per_read}')

    # ex complete_txt_file
    file_path_out_txt_save = os.path.join(
        root_out, 'results', 'saving_parameters.txt')
    complete_txt_file(file_path_out_txt_save, user_pars, t0, date)

    fig = []
    if make_plots:
        fig, ax = plt.subplots(figsize=FIGSIZE)
        fig.sfn = 'example_file'
        plot_dict = {'title': 'Write segment',
                     'x lab': 'Index', 'y lab': 'Voltage [V]'}
        plot_graph(ax, range(len(np.array(write_segment))), write_segment,
                   plot_dict=plot_dict)

    dir_path_out_meas = os.path.join(
        root_out, "txt_ferro_meas")

    measurements = ex_sort_meas()
    dim_pix = {'x': 8,
               'y': 8}
    dim_mic = {'x': 3.5,
               'y': 3.5}

    # ex save_measurement
    save_measurement(measurements, dir_path_out_meas, dim_pix=dim_pix,
                     dim_mic=dim_mic)

    # ex extract_measures
    measurements, dim_pix, dim_mic = extract_measures(dir_path_out_meas)

    if verbose:
        print('\n\t- ex extract_measures')
        print(f'\t\tmeasurements: {measurements}')
        print(f'\t\tdim pix: {dim_pix}')
        print(f'\t\tdim mic: {dim_mic}')

    if make_plots:
        return [fig]
    else:
        return (file_paths, meas_pars, sign_pars, dict_analysis_1,
                nb_write_per_read, write_segment, measurements, dim_pix,
                dim_mic)


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "hyst_to_map_file", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_file(make_plots=True, verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
