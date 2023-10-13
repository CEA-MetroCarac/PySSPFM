"""
--> Executable Script
Cross correlation coefficient analysis for sspfm maps
"""

import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.core.figure import print_plots, plot_map
from PySSPFM.utils.hyst_to_map.file import extract_measures
from PySSPFM.utils.map.interpolate import remove_val
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars

from PySSPFM.settings import FIGSIZE


def cross_corr_table(arr, map_label=None, add_txt=''):
    """
    Construct a table of cross correlation coefficient for a list of maps

    Parameters
    ----------
    arr: np.array(n*n) of float
        Array of cross correlation coefficients between n maps
    map_label: list(n) of str, optional
        List of map name
    add_txt: str, optional
        Add str to table title

    Returns
    -------
    fig: matplotlib.pyplot.figure
        Figure object containing the cross correlation table
    """
    fig, axs = plt.subplots(1, 2, figsize=FIGSIZE)
    fig.sfn = f"cross correlation table {add_txt}"
    plot_dict = {'title': f'Cross correlation mapping: {add_txt}',
                 'origin': 'upper'}
    colorbar_dict = {'lab': 'intensity', 'col': 'bwr', 'vmin': -1, 'vmax': 1}

    # If arr is 1D add a None axis to plot table
    if len(arr.shape) == 1:
        add = np.array([np.nan] * arr.shape[0])
        arr = np.vstack((arr, add))
        axs[0].axes.get_yaxis().set_visible(False)

    plot_map(fig, axs[0], arr, plot_dict=plot_dict, colorbar_dict=colorbar_dict)

    # Add str value for table
    if (arr.shape[0] and arr.shape[1]) <= 20:
        for row_ind in range(arr.shape[0]):
            for col_ind in range(arr.shape[1]):
                if not np.isnan(arr[row_ind, col_ind]):
                    label = f"{arr[row_ind][col_ind]:.2f}"
                    axs[0].text(col_ind, row_ind, label, fontsize=8,
                                weight='heavy', ha="center", va="center")

    # Axis
    x_lab = np.arange(1, arr.shape[1] + 1, dtype=np.int16)
    y_lab = np.arange(1, arr.shape[0] + 1, dtype=np.int16)
    axs[0].set_xticks(x_lab - 1, labels=x_lab)
    axs[0].tick_params('x', top=True, labeltop=True, bottom=False,
                       labelbottom=False)
    axs[0].set_yticks(y_lab - 1, labels=y_lab)

    # Legend
    axs[1].axis('off')
    if map_label is not None:
        for cont, label in enumerate(map_label):
            axs[1].text(0, 1 - cont / len(map_label), f"{cont + 1} = {label}",
                        fontsize=8, weight='heavy')

    return [fig]


def cross_corr_arr(maps, mask=None):
    """
    Generate cross correlation coefficient array of a list of maps

    Parameters
    ----------
    maps: list(n)
        List of maps (i.e. arrays of same shape)
    mask: list of int, optional
        --> if mask is [a, b, c ...] pixels of index a, b, c [...] are
        masked for the analysis
        --> if mask is None: all pixels are analyzed in ascending order in
        terms of value of meas

    Returns
    -------
    coef_arr: array(n*n)
        Array of cross correlation coefficient
    """
    coef_arr = np.zeros((len(maps), len(maps)))
    for i, map1 in enumerate(maps):
        for j, map2 in enumerate(maps[i + 1:], start=i + 1):
            coef_arr[i][j] = np.corrcoef(remove_val(map1, mask=mask),
                                         y=remove_val(map2, mask=mask))[0][1]

    return coef_arr


def cross_corr_sspfm(measurements, mask=None):
    """
    Correlation analysis for sspfm measurements

    Parameters
    ----------
    measurements: dict
        Dict of measurements of sspfm maps
    mask: list of int, optional
        --> if mask is [a, b, c ...] pixels of index a, b, c [...] are
        masked for the analysis
        --> if mask is None: all pixels are analyzed in ascending order in
        terms of value of meas

    Returns
    -------
    coef_arr: dict
        Dict of all cross correlation coefficient arrays
    figures: list of matplotlib.pyplot.figure
        Associated table of cross correlation coefficient arrays
    """
    figures = []
    coef_arr = {}

    # Separated correlation analysis for all off field maps & on field maps
    for mode in ['on', 'off']:
        if mode in measurements:
            dict_map = measurements[mode]
            # Add coupled maps
            if 'coupled' in measurements:
                dict_map.update(measurements['coupled'])
            maps = list(dict_map.values())
            key_map = list(dict_map.keys())
            coef_arr[mode] = cross_corr_arr(maps, mask=mask)
            figures.extend(cross_corr_table(coef_arr[mode], key_map,
                                            add_txt=mode))

    # Correlation analysis between off and on field maps
    if 'on' in measurements and 'off' in measurements:
        keys_off = measurements['off'].keys()
        keys_on = measurements['on'].keys()
        keys = list(set(keys_off).intersection(keys_on))
        coef_arr['off on'] = np.array([
            np.corrcoef(remove_val(measurements['off'][key], mask=mask),
                        y=remove_val(measurements['on'][key], mask=mask))[0][1]
            for key in keys
        ])
        figures.extend(cross_corr_table(coef_arr['off on'], keys,
                                        add_txt='on off field'))

    return coef_arr, figures


def main_map_correlation(user_pars, dir_path_in):
    """
    Correlation analysis for sspfm measurements with the possibility to use a
    mask taken into account in the analysis

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    dir_path_in: str
        Spm measurement files directory (in)

    Returns
    -------
    coef_arr: dict
        Dict of all cross correlation coefficient arrays
    figures: list of matplotlib.pyplot.figure
        Associated table of cross correlation coefficient arrays
    """

    # Extract all measurements
    all_meas, _, _ = extract_measures(dir_path_in)

    if user_pars['ind maps'] is not None:
        # Select multi measurements of interest
        multi_meas = {f'{elem[1]} ({elem[0]})': all_meas[elem[0]][elem[1]]
                      for elem in user_pars['ind maps']}
        coef_arr = cross_corr_arr(list(multi_meas.values()),
                                  mask=user_pars['mask'])
        figures = cross_corr_table(coef_arr, multi_meas.keys())
        coef_arr = {'single': coef_arr}
    else:
        # Cross correlation analysis between all maps
        coef_arr, figures = cross_corr_sspfm(all_meas, mask=user_pars['mask'])

    return coef_arr, figures


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - ind_maps: list(n, 2) of str
        List of Measurement Modes and Names for Cross Correlation Analysis.
        This parameter is a list that specifies which measurement modes and
        their corresponding names should be used for cross-correlation analysis.
        - It contains pairs of measurement modes and associated names in the
        format [['mode', 'name']].
        - For example,
        [['off', 'charac tot fit: area'],
        ['off', 'fit pars: ampli_0'],
        ['on', 'charac tot fit: area'],
        ['on', 'fit pars: ampli_0']]
    - mask: list of int
        Manual mask for selecting specific files.
        This parameter is a list of pixel indices.
        - If list of pixels is None: no masked pixels.
        - If list of pixels is [a, b, c ...]: files of index a, b, c [...]
        are masked for the analysis.

    - dir_path_in: str
        Ferroelectric measurements files directory (default: txt_ferro_meas)
        This parameter specifies the directory containing the ferroelectric
        measurements text files generated after the 2nd step of the analysis.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
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
    # map_correlation_2023-10-02-16h38m
    show_plots = True
    save = False

    ind_maps = [['off', 'charac tot fit: area'],
                ['off', 'fit pars: ampli_0'],
                ['on', 'charac tot fit: area'],
                ['on', 'fit pars: ampli_0']]

    user_pars = {'ind maps': ind_maps,
                 'mask': None}

    return user_pars, dir_path_in, dir_path_out, show_plots, save


def main():
    """ Main function for data analysis. """
    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, show_plots, save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save,
        dirname="map_correlation", lvl=1, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    _, figs = main_map_correlation(user_pars, dir_path_in)
    # Plot figures
    print_plots(figs, show_plots=show_plots, save_plots=save,
                dirname=dir_path_out, transparent=False)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=True)


if __name__ == '__main__':
    main()
