"""
--> Executable Script
This module is used to generate sspfm maps by extracting data from ferro
measurements in text files.
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.map.main import main_mapping
from PySSPFM.utils.nanoloop_to_hyst.file import extract_measures
from PySSPFM.toolbox.map_correlation import cross_corr_sspfm
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def main_global_map_reader(
        user_pars, verbose=False, show_plots=False, save_plots=False,
        dir_path_in=None, dir_path_out=None, all_meas=None, dim_pix=None,
        dim_mic=None, index_lim=None):
    """
    Generate all sspfm maps from extraction of ferro measurements in txt files

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    verbose: bool, optional
        Activation key for verbosity
    show_plots: bool, optional
        Activation key for matplotlib figures generation
    save_plots: bool, optional
        Activation key for fig save
    dir_path_in: str, optional
        Path of ferro measurements txt directory (in)
    dir_path_out: str, optional
        Path of saving directory for sspfm maps (out)
    all_meas: dict, optional
        Dict of measurements of sspfm maps
    dim_pix: dict('x': ,'y':) of int, optional
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)
    index_lim: list(2) of int, optional
        Range index of map can be generated

    Returns
    -------
    mask: dict (for each mode) of list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask
    coef_corr_arr: dict
        All cross correlation coefficient arrays
    """
    assert dir_path_in is not None or all_meas is not None

    # Directory management
    if save_plots and dir_path_out is None and dir_path_in is not None:
        root, _ = os.path.split(dir_path_in)
        dir_path_out = os.path.join(root, 'results', 'figs_step_2')
        if not os.path.isdir(dir_path_out):
            os.makedirs(dir_path_out)

    dict_interp = {'fact': user_pars['interp fact'],
                   'func': user_pars['interp func']}
    lab_tab = [['on', 'off', 'coupled'], ['y', 'w', 'r'],
               ['On Field', 'Off Field', 'Coupled']]
    measures, mask = {}, {}

    # Extract all measurements
    if dir_path_in is not None:
        all_meas, dim_pix, dim_mic = extract_measures(dir_path_in)

    # Cross correlation analysis between maps
    coef_corr_arr, figs = cross_corr_sspfm(all_meas)
    print_plots(figs, show_plots=show_plots, save_plots=save_plots,
                dirname=dir_path_out)

    for mode in all_meas.keys():
        # Ref determination
        if user_pars['man mask'][mode] is None:
            ref = all_meas[mode][user_pars['ref'][mode]['meas']]
        else:
            user_pars['ref'][mode], ref = None, None

        indx = lab_tab[0].index(mode)
        dict_map = {'label': lab_tab[2][indx], 'col': lab_tab[1][indx]}
        measures[mode] = {}

        # Limit of nb of map plotted
        if index_lim is not None:
            for cont, key in enumerate(all_meas[mode].keys()):
                if cont < index_lim[0]:
                    continue
                if index_lim[0] <= cont < index_lim[1]:
                    measures[mode][key] = all_meas[mode][key]
                else:
                    break
        else:
            measures[mode] = all_meas[mode]

        # Generate map
        mask[mode] = main_mapping(
            measures[mode], dim_pix, dim_mic=dim_mic, dict_interp=dict_interp,
            dict_map=dict_map, ref=ref, dict_ref=user_pars['ref'][mode],
            mask=user_pars['man mask'][mode], verbose=verbose,
            show_plots=show_plots, save_plots=save_plots,
            dir_path_out=dir_path_out)

        if verbose:
            print(f'mask in {mode} mode: {mask[mode]}')

    return mask, coef_corr_arr


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - interp_fact: int
        Interpolation factor for sspfm maps interpolation.
        This parameter determines the level of interpolation to be applied to
        SSPFM maps.
    - interp_func: str
        Interpolation function
        This parameter specifies the interpolation function used for sspfm
        maps interpolation. It can take one of the following values:
        'linear', or 'cubic'.
    - man_mask: dict [for each mode] of list
        Manual mask for selecting specific files.
        This parameter is a list of pixel indices.
        It should be a dictionary with mode keys and lists of indices as values.
        - If the list of pixels is empty ( [] ), all files are selected.
        - If the list of pixels is None, the criterion of selection is made
        with the reference measurement.
        - If the list of pixels is [a, b, c ...], files of index a, b, c [...]
        are not selected.
    - ref: dict [for each mode] of dict
        --> construct a mask with a criterion selection on ref values
        (valid if man_mask is None)
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
    # global_map_reader_2023-10-02-16h38m
    verbose = True
    show_plots = True
    save = False
    user_pars = {'interp fact': 4,
                 'interp func': 'linear',
                 'man mask': {'on': [],
                              'off': [],
                              'coupled': []},
                 'ref': {'on': {'meas': 'charac tot fit: area',
                                'fmt': '.5f',
                                'min val': None,
                                'max val': 0.005,
                                'interactive': False},
                         'off': {'meas': 'charac tot fit: area',
                                 'fmt': '.5f',
                                 'min val': None,
                                 'max val': 0.005,
                                 'interactive': False},
                         'coupled': {'meas': 'r_2',
                                     'fmt': '.5f',
                                     'min val': 0.95,
                                     'max val': None,
                                     'interactive': False}}}
    return user_pars, dir_path_in, dir_path_out, verbose, show_plots, save


def main():
    """ Main function for data analysis. """
    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, verbose, show_plots, save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save, dirname="global_map_reader",
        lvl=1, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    main_global_map_reader(
        user_pars, verbose=verbose, show_plots=show_plots, save_plots=save,
        dir_path_in=dir_path_in, dir_path_out=dir_path_out)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()
