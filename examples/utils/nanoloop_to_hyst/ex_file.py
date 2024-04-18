"""
Example of file methods
"""
import os
import shutil
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from examples.utils.nanoloop_to_hyst.ex_analysis import ex_sort_prop
from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.nanoloop_to_hyst.file import \
    (generate_file_nanoloop_paths, print_parameters, complete_parameters,
     save_properties, extract_properties)


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
    file_paths_from_nanoloops: list
        File paths generated from nanoloops file.
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
    properties: list
        Sample properties.
    dim_pix: dict
        Dimension in pixels.
    dim_mic: dict
        Dimension in micrometers.
    """
    # Define input and output file paths
    root_data = os.path.join(get_setting("example_root_path_in"),
                             "KNN500n_2023-11-20-16h18m_out_dfrt")
    dir_path_in = os.path.join(root_data, "nanoloops")
    if make_plots:
        root_out = os.path.join(
            get_setting("example_root_path_out"), "ex_nanoloop_to_hyst_file")
    else:
        root_out = os.path.join(
            get_setting("default_data_path_out"), "test_nanoloop_to_hyst_file")

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

    # Generate file paths from nanoloops and raw measurement files
    file_paths_from_nanoloops = generate_file_nanoloop_paths(dir_path_in)
    if verbose:
        print('\t- ex generate_file_nanoloop_paths')
        for cont, elem in enumerate(file_paths_from_nanoloops):
            print(f'\t\tpath n°{cont + 1}: {elem}')
        print('\n')

    # ex print_parameters
    file_path_in_txt_save = os.path.join(root_data, 'parameters.txt')
    out = print_parameters(file_path_in_txt_save, verbose=verbose)
    (meas_pars, sign_pars, dict_analysis_1, nb_write_per_read,
     write_segment) = out
    if verbose:
        print('\n\t- ex print_parameters')
        print(f'\t\tnb write per read: {nb_write_per_read}')

    # ex complete_parameters
    file_path_out_txt_save = os.path.join(root_data, 'parameters.txt')
    complete_parameters(file_path_out_txt_save, user_pars, t0, date)

    fig = []
    if make_plots:
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(figsize=figsize)
        fig.sfn = 'example_file'
        plot_dict = {'title': 'Write segment',
                     'x lab': 'Index', 'y lab': 'Voltage [V]'}
        plot_graph(ax, range(len(np.array(write_segment))), write_segment,
                   plot_dict=plot_dict)

    dir_path_out_prop = os.path.join(root_out, "properties")

    properties = ex_sort_prop()
    dim_pix = {'x': 8,
               'y': 8}
    dim_mic = {'x': 3.5,
               'y': 3.5}

    # ex save_properties
    save_properties(properties, dir_path_out_prop, dim_pix=dim_pix,
                    dim_mic=dim_mic)

    # ex extract_properties
    properties, dim_pix, dim_mic = extract_properties(dir_path_out_prop)

    if verbose:
        print('\n\t- ex extract_properties')
        print(f'\t\tproperties: {properties}')
        print(f'\t\tdim pix: {dim_pix}')
        print(f'\t\tdim mic: {dim_mic}')

    if make_plots:
        return [fig]
    else:
        return (file_paths_from_nanoloops, meas_pars, sign_pars,
                dict_analysis_1, nb_write_per_read, write_segment,
                properties, dim_pix, dim_mic)


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_to_hyst_file", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_file(make_plots=True, verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
