"""
--> Executable Script
Module used to generate sspfm maps of selected sample properties
    - Generate multi sspfm maps from extraction of property in txt files
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, copy_default_settings_if_not_exist
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.nanoloop.plot import subplots_dim
from PySSPFM.utils.nanoloop_to_hyst.file import extract_properties
from PySSPFM.utils.map.plot import disable_ax, final_map, intermediate_map
from PySSPFM.utils.map.main import gen_mask_ref
from PySSPFM.utils.map.matrix_processing import formatting_measure
from PySSPFM.toolbox.map_correlation import \
    gen_correlation_array, plot_correlation_table
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def main_list_map_reader(user_pars, dir_path_in, verbose=False):
    """
    Generate multi sspfm maps from extraction of properties in txt files

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    dir_path_in: str
        Path of properties txt directory (in)
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    figures: list of matplotlib.pyplot.figure
        List of figures
    """
    assert os.path.isdir(dir_path_in)

    # Extract all properties
    all_prop, dim_pix, dim_mic = extract_properties(dir_path_in)

    # Select multi properties of interest
    multi_prop = {f'{elem[1]} ({elem[0]})': all_prop[elem[0]][elem[1]]
                  for elem in user_pars['ind maps']}

    coef_corr_arr = gen_correlation_array(list(multi_prop.values()))
    corr_table = plot_correlation_table(coef_corr_arr, multi_prop.keys())

    # Define ref
    if user_pars['man mask'] is None:
        ref = all_prop[user_pars['ref']['mode']][user_pars['ref']['prop']]
    else:
        user_pars['ref'], ref = None, None

    # Init dict parameters
    dict_interp = {
        'fact': user_pars['interp fact'],
        'func': user_pars['interp func']} if \
        user_pars['interp fact'] > 1 else None
    dict_map = {'label': '', 'col': 'k'}
    dict_ref = user_pars['ref']

    # Mask with condition on ref
    if user_pars['man mask'] is None:
        res = gen_mask_ref(
            ref, dim_pix, dim_mic=dim_mic, min_val=dict_ref["min val"],
            max_val=dict_ref["max val"], mode_man=dict_ref["interactive"],
            ref_str=dict_ref["prop"], dict_map=dict_map)
        (min_val, max_val, mask) = res
        if dict_ref is not None:
            dict_ref["min val"], dict_ref["max val"] = min_val, max_val
            string = {
                'min': f'{dict_ref["min val"]:.5f}'
                if dict_ref["min val"] is not None else '_',
                'max': f'{dict_ref["max val"]:.5f}' if
                dict_ref["max val"] is not None else '_'
            }
            lab = f'{dict_ref["prop"]} in [{string["min"]};{string["max"]}]'
            dict_ref['crit sel lab'] = lab
    # Manual mask
    else:
        mask, dict_map["mask mode"] = user_pars['man mask'], 'man mask'

    applied_mask = [index for index in range(int(dim_pix['x']*dim_pix['y']))
                    if index not in mask] \
        if user_pars['revert mask'] else mask

    maps = []
    figsize = get_setting("figsize")
    # Plot ref
    if ref:
        if verbose:
            print('# reference property')
        fig_ref = plt.figure(figsize=figsize)
        fig_ref.sfn = "list_map_reader_ref"
        axs_ref = formatting_fig_maps(
            fig_ref, [1, 1], applied_mask, nb_map=1, dict_map=None,
            dict_ref=None, dim_mic=None)
        ref_str = f'ref prop: {user_pars["ref"]["prop"]}' \
                  f' ({user_pars["ref"]["mode"]})'
        treatment_plot_map(
            fig_ref, axs_ref[0], ref, dim_pix, dim_mic=dim_mic,
            dict_interp=dict_interp, mask=applied_mask, prop_str=ref_str,
            plot_ind=True)
        fig_ref.tight_layout()
        maps += [fig_ref]

    # Plot multi_prop map
    if verbose:
        print('# multi mapping')
    nb_map = len(list(multi_prop.keys()))
    fig_maps_dim = subplots_dim(nb_map)
    fig_maps = plt.figure(figsize=figsize)
    fig_maps.sfn = "list_map_reader_maps"
    axs_maps = formatting_fig_maps(
        fig_maps, fig_maps_dim, applied_mask,  nb_map=nb_map, dict_map=None,
        dict_ref=None, dim_mic=None)
    # Plot multi_prop graph
    fig_graphs = plt.figure(figsize=figsize)
    fig_graphs.sfn = "list_map_reader_graphs"
    axs_graphs = formatting_fig_graphs(fig_graphs, fig_maps_dim,
                                       nb_graph=nb_map)

    # Generate a map and graph for each property
    plot_ind = len(axs_maps) <= 10
    for i, (lab_prop, prop) in enumerate(multi_prop.items()):
        if verbose:
            print(f'\t- {lab_prop}')
        # Treat and plot map: property
        treatment_plot_map(
            fig_maps, axs_maps[i], prop, dim_pix, dim_mic=dim_mic,
            dict_interp=dict_interp, mask=applied_mask, prop_str=lab_prop,
            plot_ind=plot_ind)

        # Treat and plot graph: property
        treatment_plot_graph(axs_graphs[i], prop, nb_line=dim_pix['y'],
                             mask=applied_mask, prop_str=lab_prop,
                             meas_time=user_pars["meas time"])

    fig_maps.tight_layout()
    fig_graphs.tight_layout()
    maps += [fig_maps]
    maps += [fig_graphs]
    figures = corr_table + maps

    return figures


def treatment_plot_graph(ax_graph, prop, nb_line, mask=None, prop_str=None,
                         meas_time=None):
    """
    Plot graph for treatment

    Parameters
    ----------
    ax_graph: plt.Axes
        Axis for plotting
    prop: list
        Property values
    nb_line: int
        Number of lines of the map
    mask: list, optional
        List of indexes to mask
    prop_str: str, optional
        Property string
    meas_time: float, optional
        Total measurement time

    Returns
    -------
    None
    """
    prop_str = "" if prop_str is None else prop_str
    mask = [] if mask is None else mask
    line_indexs = np.linspace(0, nb_line, len(prop))
    if meas_time is not None:
        time_tab = np.linspace(0, meas_time, len(prop))
        time_tab = [value for index, value in enumerate(time_tab)
                    if index not in mask]
    line_indexs = [value for index, value in enumerate(line_indexs)
                   if index not in mask]
    prop = [value for index, value in enumerate(prop) if index not in mask]
    plot_dict = {'x lab': 'Line index', 'y lab': f'{prop_str}', 'fs': 15,
                 'edgew': 1, 'tickl': 2, 'gridw': 1}
    tab_dict = {'form': 'g-'}
    plot_graph(ax_graph, line_indexs, prop, plot_dict=plot_dict,
               tabs_dict=tab_dict, plot_leg=False)
    if meas_time is not None:
        ax2 = ax_graph.twiny()
        ax2.set_xlabel('Time (h)', fontsize=plot_dict['fs'])
        ax2.plot(time_tab, prop, alpha=0)
        ax2.tick_params(axis='both', which='major', length=plot_dict['tickl'],
                        labelsize=plot_dict['fs'])


def treatment_plot_map(fig, ax, propertie, dim_pix, dim_mic=None,
                       dict_interp=None, mask=None, prop_str=None,
                       plot_ind=False):
    """
    Treat property map (interpolation, mask ...) and plot it

    Parameters
    ----------
    fig: plt.figure
        Figure object
    ax: plt.axes
        Axes object of the figure
    propertie: numpy.array(p) of float
        Array of values for the considered property
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)
    dict_interp: dict, optional
        Dict of map interpolation parameters
    mask: list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask (q<p)
    prop_str: str, optional
        Title of ax: i.e. name of the property parameter
    plot_ind: bool, optional
        If True, index in tab_plotted_index are plotted on the sub image

    Returns
    -------
    None
    """
    # Treatment (interpolation, mask ...)
    (raw_ext, raw_dim_fact, _, _, matrix_step2, interp_ext,
     _, _, matrix_step3b, index_blank, tab_all_index, tab_plotted_index,
     directions) = formatting_measure(
        np.array(propertie, dtype='f'), dim_pix, dim_mic=dim_mic,
        dict_interp=dict_interp, mask=mask)

    # Plot map
    if dict_interp is None:
        intermediate_map(
            fig, ax, matrix_step2, dim_pix, ext=raw_ext, dim_fact=raw_dim_fact,
            tab_all_index=tab_all_index, tab_plotted_index=tab_plotted_index,
            directions=directions, plot_ind=plot_ind, ax_title=prop_str,
            highlight_pix=None)
    else:
        final_map(
            fig, ax, matrix_step3b, dim_pix, ext=interp_ext,
            dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
            tab_plotted_index=tab_plotted_index, directions=directions,
            index_blank=index_blank, ax_title=prop_str, highlight_pix=None)


def formatting_fig_maps(fig, fig_dim, mask, nb_map=None, dict_map=None,
                        dict_ref=None, dim_mic=None):
    """
    Formatting map figure

    Parameters
    ----------
    fig: plt.figure
        Figure object
    fig_dim: list(2) of int
        List of figure dimension [nb of line, mb of column]
    mask: list(q) or numpy.array(q) of int
        List of index corresponding to the mask (q<p)
    nb_map: int, optional
        Number of plotted map
    dict_map: dict, optional
        Dict used for map annotation
    dict_ref: dict, optional
        Dict on ref property condition to generate the mask
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)

    Returns
    -------
    axs: list(nb_map) of plt.axes
        Axes of the figure
    """
    # Ax management
    main_ax = fig.add_subplot(111)
    axs = [main_ax] if int(fig_dim[0] * fig_dim[1]) == 1 else []
    if int(fig_dim[0] * fig_dim[1]) > 1:
        disable_ax(main_ax)
        axs = [fig.add_subplot(fig_dim[0], fig_dim[1], i + 1) for i in
               range(int(fig_dim[0] * fig_dim[1])) if i < nb_map]

    # Label
    unit = 'pixels' if dim_mic is None else 'microns'
    main_ax.set_xlabel(f'width ({unit})', size=20, weight='heavy')
    fig.text(0.02, 0.5, f'height ({unit})', size=20, weight='heavy',
             va='center', rotation=90)

    # Scan direction
    bbox_props_fast = {"boxstyle": "darrow,pad=0.3", "fc": "grey", "ec": "k",
                       "lw": 2}
    bbox_props_slow = {"boxstyle": "rarrow,pad=0.3", "fc": "grey", "ec": "k",
                       "lw": 2}

    # Other annotations
    if dict_map:
        fig.text(0.01, 0.95, dict_map["label"], c=dict_map["col"], size=15,
                 weight='heavy', backgroundcolor='k')
        fig.text(0.01, 0.06, f'mask mode: {dict_map["mask mode"]}', size=12,
                 weight='heavy')
        if "limit" in dict_map:
            fig.text(0.65, 0.93,
                     f'voltage range for differential analysis: '
                     f'{str(dict_map["limit"])} V',
                     size=12, weight='heavy')
    fig.text(0.01, 0.90, "Fast scan axis", rotation=0, size=10,
             bbox=bbox_props_fast)
    fig.text(0.03, 0.77, "Slow scan axis", rotation=270, size=10,
             bbox=bbox_props_slow)
    if len(mask) < 15:
        fig.text(0.01, 0.04, f'mask, pixel removed: {str(mask)}', size=12,
                 weight='heavy')
    if dict_ref:
        fig.text(0.01, 0.02,
                 f'pixel selection criterion: {dict_ref["crit sel lab"]}',
                 size=12, weight='heavy')

    return axs


def formatting_fig_graphs(fig, fig_dim, nb_graph=None):
    """
    Formatting graph figure

    Parameters
    ----------
    fig: plt.figure
        Figure object
    fig_dim: list(2) of int
        List of figure dimension [nb of line, mb of column]
    nb_graph: int, optional
        Number of plotted graph

    Returns
    -------
    axs: list(nb_graph) of plt.axes
        Axes of the figure
    """
    # Ax management
    main_ax = fig.add_subplot(111)
    axs = [main_ax] if int(fig_dim[0] * fig_dim[1]) == 1 else []
    if int(fig_dim[0] * fig_dim[1]) > 1:
        disable_ax(main_ax)
        axs = [fig.add_subplot(fig_dim[0], fig_dim[1], i + 1)
               for i in range(int(fig_dim[0] * fig_dim[1])) if i < nb_graph]

    return axs


def parameters(fname_json=None):
    """
    To complete by user of the script: return parameters for analysis

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)

    - ind_maps: list(n, 2) of str
        List of Property Modes and Names for Plotting.
        It contains pairs of property modes and associated names in the
        format [['mode', 'name']].
        For example,
        [['off', 'charac tot fit: area'],
        ['off', 'fit pars: ampli_0'],
        ['on', 'charac tot fit: area'],
        ['on', 'fit pars: ampli_0']]
    - interp fact: int
        Interpolation factor for sspfm maps interpolation.
        This parameter determines the level of interpolation to be applied to
        SSPFM maps.
    - interp_func: str
        Interpolation function
        This parameter specifies the interpolation function used for sspfm
        maps interpolation. It can take one of the following values:
        'linear', or 'cubic'.
    - meas_time: float
        Real duration of the measurement in hours.
        This parameter represents the actual duration of the measurement in
        hours. It is used to generate a time axis for the property graphs
        corresponding to the measurements. If set to None, no time axis is
        generated, and only the line index is used as the x-axis values.
    - revert_mask: bool
        Revert option of the mask for selecting specific files.
        This parameter specifies if the mask should be reverted (True), or not
        (False)
    - man_mask: list
        Manual mask for selecting specific files.
        This parameter is a list of pixel indices.
        - If the list of pixels is empty ( [] ), all files are selected.
        - If the list of pixels is None, the criterion of selection is made
        with the reference property.
        - If the list of pixels is [a, b, c ...], files of index a, b, c [...]
        are not selected.
    - ref: dict
        --> construct a mask with a criterion selection on ref values
        (valid if man_mask is None)
        - mode: str --> mode of reference property chosen
        - prop: str --> reference property chosen
        - min val: float --> minimum value of ref required (if None no minimum
        value criterion) (valid if interactive is False)
        - max val: float --> maximum value of ref required (if None no maximum
        value criterion) (valid if interactive is False)
        - fmt: str --> format of printed value in the map
        - interactive: bool --> if True, user select interactively the criterion
        selection

    - dir_path_in: str
        Properties files directory (default: properties)
        This parameter specifies the directory containing the properties text
        files generated after the 2nd step of the analysis.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - verbose: bool
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.
    - show_plots: bool
        Activation key for generating matplotlib figures during analysis.
        This parameter serves as an activation key for generating
        matplotlib figures during the analysis process.
    - save: bool
        Activation key for saving results of analysis.
        This parameter serves as an activation key for saving results
        generated during the analysis process.
    """
    if get_setting("extract_parameters") in ['json', 'toml']:
        # if fname_json is provided, use it, else use the default one
        if fname_json is not None:
            file_path_user_params = fname_json
        else:
            file_path = os.path.realpath(__file__)
            file_path_user_params = \
                copy_default_settings_if_not_exist(file_path)

        # Load parameters from the specified configuration file
        print(f"user parameters from {os.path.split(file_path_user_params)[1]} "
              f"file")
        config_params = load_parameters_from_file(file_path_user_params)
        dir_path_in = config_params['dir_path_in']
        dir_path_out = config_params['dir_path_out']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = config_params['user_pars']
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt\properties
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # list_map_reader_2023-10-02-16h38m
        verbose = True
        show_plots = True
        save = False

        ind_maps = [['off', 'charac tot fit: area'],
                    ['off', 'fit pars: ampli_0'],
                    ['on', 'charac tot fit: area'],
                    ['on', 'fit pars: ampli_0']]

        user_pars = {'ind maps': ind_maps,
                     'interp fact': 3,
                     'interp func': 'linear',
                     'meas time': None,
                     'revert mask': False,
                     'man mask': [],
                     'ref': {'mode': 'off',
                             'prop': 'charac tot fit: R_2 hyst',
                             'fmt': '.5f',
                             'min val': 0.95,
                             'max val': None,
                             'interactive': False}}
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, dir_path_in, dir_path_out, verbose, show_plots, save


def main(fname_json=None):
    """
    Main function for data analysis.

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)
    """
    figs = []
    # Extract parameters
    res = parameters(fname_json=fname_json)
    (user_pars, dir_path_in, dir_path_out, verbose, show_plots, save) = res
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save, dirname="list_map_reader", lvl=1,
        create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    figs += main_list_map_reader(user_pars, dir_path_in, verbose=verbose)
    # Plot figures
    print_plots(figs, show_plots=show_plots, save_plots=save,
                dirname=dir_path_out, transparent=False)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()
