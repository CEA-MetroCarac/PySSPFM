"""
--> Executable Script
Module used to generate sspfm maps of selected ferroelectric measurements
    - Generate multi sspfm maps from extraction of ferro measurements in txt
    files
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop.plot import subplots_dim
from PySSPFM.utils.hyst_to_map.file import extract_measures
from PySSPFM.utils.map.annotate import disable_ax
from PySSPFM.utils.map.main import mask_ref, final_image, sub_image
from PySSPFM.utils.map.matrix_formatting import formatting_measure
from PySSPFM.toolbox.map_correlation import cross_corr_arr, cross_corr_table
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars

from PySSPFM.settings import FIGSIZE


def main_list_map_reader(user_pars, dir_path_in, verbose=False):
    """
    Generate multi sspfm maps from extraction of ferro measurements in txt files

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    dir_path_in: str
        Path of ferro measurements txt directory (in)
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    figures: list of matplotlib.pyplot.figure
        List of figures
    """
    assert os.path.isdir(dir_path_in)

    # Extract all measurements
    all_meas, dim_pix, dim_mic = extract_measures(dir_path_in)

    # Select multi measurements of interest
    multi_meas = {f'{elem[1]} ({elem[0]})': all_meas[elem[0]][elem[1]]
                  for elem in user_pars['ind maps']}

    coef_corr_arr = cross_corr_arr(list(multi_meas.values()))
    corr_table = cross_corr_table(coef_corr_arr, multi_meas.keys())

    # Define ref
    if user_pars['man mask'] is None:
        ref = all_meas[user_pars['ref']['mode']][user_pars['ref']['meas']]
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
        res = mask_ref(ref, dim_pix, dim_mic=dim_mic,
                       min_val=dict_ref["min val"], max_val=dict_ref["max val"],
                       mode_man=dict_ref["interactive"],
                       ref_str=dict_ref["meas"], dict_map=dict_map)
        (min_val, max_val, mask) = res
        if dict_ref is not None:
            dict_ref["min val"], dict_ref["max val"] = min_val, max_val
            string = {
                'min': f'{dict_ref["min val"]:.5f}'
                if dict_ref["min val"] is not None else '_',
                'max': f'{dict_ref["max val"]:.5f}' if
                dict_ref["max val"] is not None else '_'
            }
            lab = f'{dict_ref["meas"]} in [{string["min"]};{string["max"]}]'
            dict_ref['crit sel lab'] = lab
    # Manual mask
    else:
        mask, dict_map["mask mode"] = user_pars['man mask'], 'man mask'

    maps = []

    # Plot ref
    if ref:
        if verbose:
            print('# reference meas')
        fig_ref = plt.figure(figsize=FIGSIZE)
        fig_ref.sfn = "list_map_reader_ref"
        axs_ref = formatting_fig(fig_ref, [1, 1], mask, nb_map=1,
                                 dict_map=None, dict_ref=None, dim_mic=None)
        ref_str = f'ref meas: {user_pars["ref"]["meas"]}' \
                  f' ({user_pars["ref"]["mode"]})'
        treat_and_plot(fig_ref, axs_ref[0], ref, dim_pix, dim_mic=dim_mic,
                       dict_interp=dict_interp, mask=mask, measure_str=ref_str,
                       plot_ind=True)
        fig_ref.tight_layout()
        maps += [fig_ref]

    # Plot multi_meas
    if verbose:
        print('# multi mapping')
    nb_map = len(list(multi_meas.keys()))
    fig_maps_dim = subplots_dim(nb_map)
    fig_maps = plt.figure(figsize=FIGSIZE)
    fig_maps.sfn = "list_map_reader_maps"
    axs_maps = formatting_fig(fig_maps, fig_maps_dim, mask, nb_map=nb_map,
                              dict_map=None, dict_ref=None, dim_mic=None)
    # Generate a map for each ferro measurement
    plot_ind = len(axs_maps) <= 10
    for i, (lab_meas, meas) in enumerate(multi_meas.items()):
        if verbose:
            print(f'\t- {lab_meas}')
        # Treat and plot map: measure
        treat_and_plot(fig_maps, axs_maps[i], meas, dim_pix, dim_mic=dim_mic,
                       dict_interp=dict_interp, mask=mask, measure_str=lab_meas,
                       plot_ind=plot_ind)
    fig_maps.tight_layout()
    maps += [fig_maps]
    figures = corr_table + maps

    return figures


def treat_and_plot(fig, ax, measure, dim_pix, dim_mic=None, dict_interp=None,
                   mask=None, measure_str=None, plot_ind=False):
    """
    Treat measure map (interpolation, mask ...) and plot it

    Parameters
    ----------
    fig: plt.figure
        Figure object
    ax: plt.axes
        Axes object of the figure
    measure: numpy.array(p) of float
        Array of values for the considered measure
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)
    dict_interp: dict, optional
        Dict of map interpolation parameters
    mask: list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask (q<p)
    measure_str: str, optional
        Title of ax: i.e. name of the measured parameter
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
        np.array(measure, dtype='f'), dim_pix, dim_mic=dim_mic,
        dict_interp=dict_interp, mask=mask)

    # Plot map
    if dict_interp is None:
        sub_image(fig, ax, matrix_step2, dim_pix, ext=raw_ext,
                  dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                  tab_plotted_index=tab_plotted_index,
                  directions=directions, plot_ind=plot_ind,
                  ax_title=measure_str, highlight_pix=None)
    else:
        final_image(fig, ax, matrix_step3b, dim_pix, ext=interp_ext,
                    dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                    tab_plotted_index=tab_plotted_index,
                    directions=directions, index_blank=index_blank,
                    ax_title=measure_str, highlight_pix=None)


def formatting_fig(fig, fig_dim, mask, nb_map=None, dict_map=None,
                   dict_ref=None, dim_mic=None):
    """
    Formatting figure

    Parameters
    ----------
    fig: plt.figure
        Figure object
    fig_dim: list(2) of int
        List of figure dimension [nb of line, mb of column]
    mask: list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask (q<p)
    nb_map: int, optional
        Number of plotted map
    dict_map: dict, optional
        Dict used for map annotation
    dict_ref: dict, optional
        Dict on ref measurement condition to generate the mask
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


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - ind_maps: list(n, 2) of str
        List of Measurement Modes and Names for Plotting.
        It contains pairs of measurement modes and associated names in the
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
    - man_mask: list
        Manual mask for selecting specific files.
        This parameter is a list of pixel indices.
        - If the list of pixels is empty ( [] ), all files are selected.
        - If the list of pixels is None, the criterion of selection is made
        with the reference measurement.
        - If the list of pixels is [a, b, c ...], files of index a, b, c [...]
        are not selected.
    - ref: dict
        --> construct a mask with a criterion selection on ref values
        (valid if man_mask is None)
        - mode: str --> mode of reference measurement chosen
        - meas: str --> reference measurement chosen
        - min val: float --> minimum value of ref required (if None no minimum
        value criterion) (valid if interactive is False)
        - max val: float --> maximum value of ref required (if None no maximum
        value criterion) (valid if interactive is False)
        - fmt: str --> format of printed value in the map
        - interactive: bool --> if True, user select interactively the criterion
        selection

    - dir_path_in: str
        Ferroelectric measurements files directory (default: txt_ferro_meas)
        This parameter specifies the directory containing the ferroelectric
        measurements text files generated after the 2nd step of the analysis.
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
    dir_path_in = tkf.askdirectory()
    # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt\txt_ferro_meas
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
                 'man mask': [],
                 'ref': {'mode': 'off',
                         'meas': 'charac tot fit: R_2 hyst',
                         'fmt': '.5f',
                         'min val': 0.95,
                         'max val': None,
                         'interactive': False}}

    return user_pars, dir_path_in, dir_path_out, verbose, show_plots, save


def main():
    """ Main function for data analysis. """
    figs = []
    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, verbose, show_plots, save) = out
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
