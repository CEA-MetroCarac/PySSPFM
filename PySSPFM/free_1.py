"""
Free script for data analysis:
Select nanoloop file and plot some of the properties
"""

import os
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting
from PySSPFM.data_processing.nanoloop_to_hyst_s2 import \
    single_script, parameters
from PySSPFM.utils.nanoloop_to_hyst.electrostatic import differential_analysis
from PySSPFM.utils.nanoloop_to_hyst.file import print_parameters
from PySSPFM.utils.core.figure import plot_graph, print_plots


def plot_diff_loops(dict_diff_loops, legends):

    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = 'plot_diff_loops'

    plot_dict = {'x lab': 'Write voltage [V]',
                 'y lab': 'Piezoresponse [a.u]',
                 'fs': 15, 'edgew': 1, 'tickl': 2, 'gridw': 1}

    tabs_dict = []
    cmap = plt.get_cmap('turbo')
    for cont, legend in enumerate(legends):
        tabs_dict.append(
            {"form": "o-",
             "color": cmap(cont/len(dict_diff_loops['piezorep'])),
             "legend": legend})

    plot_graph(ax, dict_diff_loops['write'], dict_diff_loops['piezorep'],
               plot_dict=plot_dict, tabs_dict=tabs_dict, plot_leg=True)

    return fig


def plot_best_loops(tab_best_loops, modes, legends):

    best_loops_write = {}
    best_loops_piezorep = {}
    figs_best_loops = []
    for mode in modes:
        best_loops_write[mode] = []
        best_loops_piezorep[mode] = []
        for cont, best_loops in enumerate(tab_best_loops):
            best_loops_write[mode].append(best_loops[mode].piezorep.write_volt)
            best_loops_piezorep[mode].append(best_loops[mode].piezorep.y_meas)

        figsize = get_setting("figsize")
        fig, ax = plt.subplots(figsize=figsize)
        fig.sfn = f'plot_piezorep_loops_{mode}'

        plot_dict = {'x lab': 'Write voltage [V]',
                     'y lab': 'Piezoresponse [a.u]',
                     'fs': 15, 'edgew': 1, 'tickl': 2, 'gridw': 1}

        tabs_dict = []
        cmap = plt.get_cmap('turbo')
        for cont, legend in enumerate(legends):
            tabs_dict.append(
                {"form": "o-",
                 "color": cmap(cont/len(best_loops_piezorep[mode])),
                 "legend": legend})

        plot_graph(ax, best_loops_write[mode], best_loops_piezorep[mode],
                   plot_dict=plot_dict, tabs_dict=tabs_dict, plot_leg=True)

        figs_best_loops += [fig]

    return figs_best_loops


def plot_lists_in_dict(dictionary, x_axis):

    figsize = get_setting("figsize")
    fig, ax = plt.subplots(figsize=figsize)
    fig.sfn = 'plot_properties'

    plot_dict = {'x lab': list(x_axis.keys())[0],
                 'y lab': 'Properties axis', 'fs': 15,
                 'edgew': 1, 'tickl': 2, 'gridw': 1}

    tabs_dict = []
    for key, _ in dictionary.items():
        tabs_dict.append({"form": "o", "legend": key})

    plot_graph(ax, list(x_axis.values())[0], list(dictionary.values()),
               plot_dict=plot_dict, tabs_dict=tabs_dict, plot_leg=True)

    return fig


def get_files_by_modification_date(dir_path):
    all_files = os.listdir(dir_path)
    file_modification_times = [
        (file, os.path.getmtime(os.path.join(dir_path, file))) for file in
        all_files]
    sorted_files = sorted(file_modification_times, key=lambda x: x[1])
    sorted_file_names = [file[0] for file in sorted_files]

    return sorted_file_names


def get_files_sorted_alphabetically(dir_path):
    sorted_files = sorted(os.listdir(dir_path))
    return sorted_files


def single_script_free(file_name, dir_path_in, user_pars, meas_pars, sign_pars,
                       modes, cont, limit, verbose):

    tab_path_in = []
    for mode in modes:
        file_path = os.path.join(dir_path_in, f"{mode}_f_" + file_name)
        tab_path_in.append(file_path)

    best_loops, properties, _, _ = \
        single_script(tab_path_in, user_pars, meas_pars, sign_pars,
                      cont=cont + 1, limit=limit, test_dicts=None,
                      make_plots=False, verbose=verbose)

    mean_voltage, diff_piezorep_mean = None, None
    if len(modes) == 2:
        mean_voltage, diff_piezorep_mean, _, _ = differential_analysis(
            best_loops['on'], best_loops['off'],
            offset_off=properties["off"]['fit pars: offset'],
            bias_min=limit['min'], bias_max=limit['max'], dict_str=None,
            make_plots=False)

    return best_loops, properties, mean_voltage, diff_piezorep_mean


def main_free(dir_path_in, user_pars, modes, key_properties,
              file_names=None, x_axis=None, sorted_by="modification time",
              verbose=False):
    assert sorted_by in ["alphabetically", "modification time"]

    # Get file names
    if file_names is None:
        if sorted_by == "alphabetically":
            all_files = get_files_sorted_alphabetically(dir_path_in)
        elif sorted_by == "modification time":
            all_files = get_files_by_modification_date(dir_path_in)
        file_names = []
        for file in all_files:
            file_name = os.path.split(file)[1]
            file_name = file_name.replace("off_f_", "").replace("on_f_", "")
            file_names.append(file_name)
        file_names = list(set(file_names))
        file_names = file_names[::10]
    # Extract parameters from parameters.txt
    file_path_out_txt_save = os.path.join(os.path.split(dir_path_in)[0],
                                          "parameters.txt")
    meas_pars, sign_pars, _, _, _ = print_parameters(
        file_path_out_txt_save, verbose=verbose)
    limit = user_pars['diff domain']

    properties_extracted = {}
    tab_best_loops = []
    dict_diff_loops = {'write': [], 'piezorep': []}
    for key_property in key_properties:
        properties_extracted[f"{key_property[0]}: {key_property[1]}"] = []

    # Multi processing mode
    multiproc = get_setting("multi_processing")
    if multiproc:
        from PySSPFM.utils.core.multi_proc import run_multi_proc_free
        common_args = {
            "dir_path_in": dir_path_in,
            "user_pars": user_pars,
            "meas_pars": meas_pars,
            "sign_pars": sign_pars,
            "modes": modes,
            "cont": 1,
            "limit": limit,
            "verbose": verbose
        }
        tab_best_loops, tab_properties, tab_mean_voltage, \
            tab_diff_piezorep_mean = \
            run_multi_proc_free(file_names, common_args, processes=16)

        for properties, mean_voltage, diff_piezorep_mean in \
                zip(tab_properties, tab_mean_voltage, tab_diff_piezorep_mean):
            for key_property in key_properties:
                properties_extracted[
                    f"{key_property[0]}: {key_property[1]}"].append(
                    properties[key_property[0]][key_property[1]])
            dict_diff_loops['write'].append(mean_voltage)
            dict_diff_loops['piezorep'].append(diff_piezorep_mean)
    else:
        # Run single script of 2nd step analysis
        for cont, file_name in enumerate(file_names):

            best_loops, properties, mean_voltage, diff_piezorep_mean = \
                single_script_free(file_name, dir_path_in, user_pars, meas_pars,
                                   sign_pars, modes, cont, limit, verbose)

            tab_best_loops.append(best_loops)
            for key_property in key_properties:
                properties_extracted[
                    f"{key_property[0]}: {key_property[1]}"].append(
                    properties[key_property[0]][key_property[1]])
            dict_diff_loops['write'].append(mean_voltage)
            dict_diff_loops['piezorep'].append(diff_piezorep_mean)

    if x_axis is not None:
        legends = [f"{list(x_axis.keys())[0]}: {value}"
                   for value in list(x_axis.values())[0]]
    else:
        legends = file_names
    x_axis = {"File index": [i for i in range(1, len(file_names) + 1)]} \
        if x_axis is None else x_axis
    fig_props = plot_lists_in_dict(properties_extracted, x_axis=x_axis)
    fig_piezorep_loops = plot_best_loops(tab_best_loops, modes, legends)
    if len(modes) == 2:
        fig_diff_loops = plot_diff_loops(dict_diff_loops, legends)
    else:
        fig_diff_loops = []

    figs_analysis = [fig_props, fig_piezorep_loops, fig_diff_loops]

    return figs_analysis


if __name__ == '__main__':

    DIR_PATH_IN = r"S:\510-Technologies_Silicium\510.41-Stockage_Rayons_X\0-Dossiers Individuels a chacun\Hugo\AFM\PZT\Papier_SSPFM_DFRT\Mapping_1\SSPFM_DFRT_map_2024-03-15-13h18m_out_dfrt\nanoloops"
    MODES = ["off", "on"]
    VERBOSE = True
    SORTED_BY = "alphabetically"
    KEY_PROPERTIES = [["coupled", "a"],
                      ["off", 'fit pars: ampli_0'],
                      ["off", 'fit pars: offset']]
    FILE_NAMES = None
    # FILE_NAMES = \
    #      ['PIT_SSPFM_DFRT_T10ms_sample_center.0_00000.txt',
    #       'PIT_SSPFM_DFRT_T10ms_sample_edge1.0_00000.txt',
    #       'PIT_SSPFM_DFRT_T10ms_sample_edge2.0_00001.txt',
    #       'PIT_SSPFM_DFRT_T10ms_sample_edge3.0_00002.txt',
    #       'PIT_SSPFM_DFRT_T10ms_sample_edge4.0_00003.txt',
    #       'PIT_SSPFM_DFRT_T10ms_sample_edge5.0_00004.txt']
    X_AXIS = None
    # X_AXIS = {"Res": [500e3, 10e6, 500e3, 10e6, 500e3, 500e3]}
    # Extract user pars for second step analysis
    USER_PARS, _, _, _, _, _ = parameters()

    figs = main_free(DIR_PATH_IN, USER_PARS, MODES, KEY_PROPERTIES,
                     file_names=FILE_NAMES, x_axis=X_AXIS, sorted_by=SORTED_BY,
                     verbose=VERBOSE)
    print_plots(figs, show_plots=True, save_plots=False, dirname=None,
                transparent=False)
