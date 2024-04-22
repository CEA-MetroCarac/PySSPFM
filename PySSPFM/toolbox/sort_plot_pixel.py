"""
--> Executable Script
Find extremum value of sspfm map of a reference property and plot hysteresis
of associated files
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting, copy_default_settings_if_not_exist
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.figure import print_plots, plot_hist, ax_formating
from PySSPFM.utils.core.basic_func import linear
from PySSPFM.utils.nanoloop.plot import plot_ckpfm
from PySSPFM.utils.nanoloop.phase import gen_dict_pha
from PySSPFM.utils.nanoloop.file import extract_nanoloop_data
from PySSPFM.utils.nanoloop.analysis import nanoloop_treatment, gen_ckpfm_meas
from PySSPFM.utils.map.main import plot_and_save_maps
from PySSPFM.utils.map.interpolate import remove_val
from PySSPFM.utils.nanoloop_to_hyst.file import \
    generate_file_nanoloop_paths, extract_properties, print_parameters
from PySSPFM.utils.nanoloop_to_hyst.gen_data import gen_data_dict
from PySSPFM.utils.nanoloop_to_hyst.electrostatic import differential_analysis
from PySSPFM.utils.nanoloop_to_hyst.analysis import \
    gen_analysis_mode, find_best_nanoloop, hyst_analysis
from PySSPFM.toolbox.mean_hyst import main_mean_hyst
from PySSPFM.toolbox.mean_hyst import single_script
from PySSPFM.toolbox.loop_file_reader import main_loop_file_reader
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars

DEFAULT_LIMIT = {'min': -8., 'max': 8.}


def add_txt(fig, dict_str):
    """
    Add annotation for figures

    Parameters
    ----------
    fig: plt.figure
        Figure object to add annotations to
    dict_str: dict
        Annotations for the plot

    Returns
    -------
    None
    """
    if 'label' in dict_str and 'col' in dict_str:
        fig.text(0.9, 0.95, dict_str["label"], c=dict_str["col"], size=20,
                 weight='heavy', backgroundcolor='black')

    if 'index' in dict_str:
        fig.text(0.9, 0.90, f'file n°{dict_str["index"]}', size=15,
                 weight='heavy')


def plot_comparative_hyst(mean_hyst, mean_loop, hyst, loop, bckgnd=None,
                          infl_threshold=10, sat_threshold=90, pixel_ind=1,
                          dict_str=None):
    """
    Generate hysteresis analysis figure (fit + properties + data)

    Parameters
    ----------
    mean_hyst: Hysteresis object
        Hysteresis object associated with all the analyzed files
    mean_loop: loop (MultiLoop or MeanLoop) object
        Loop object associated with all the analyzed files
    hyst: Hysteresis object
        Hysteresis associated with the specific file being analyzed
    loop: loop (MultiLoop or MeanLoop) object
        Loop object associated with the specific file being analyzed
    bckgnd: str, optional
        Keyword to take into account baseline in the hysteresis model among
        ('linear', 'offset', None)
    infl_threshold: float, optional
        Threshold (in %) of derivative amplitude of hysteresis
        fit function (sigmoid, arctan, etc.) used for nucleation bias analysis
    sat_threshold: float, optional
        Threshold related amplitude of hysteresis to consider for
        the x-axis saturation domain determination (in %)
    pixel_ind: int, optional
        Index of the pixel corresponding to the analyzed file
    dict_str: dict, optional
        Dict of annotations for the plot

    Returns
    -------
    fig: plt.figure
        Figure of hysteresis analysis (fit and properties hysteresis plotting)
    """
    unit = "" if dict_str is None else dict_str["unit"]
    figsize = get_setting("figsize")
    fig, axs = plt.subplots(2, 2, figsize=figsize, sharex='all', sharey='row')
    fig.sfn = f'hysteresis_fit_pixel_{pixel_ind}'

    # For mean // selected file
    for [ax, axb], hyster, loop_data, add_str in zip(
            [[axs[0][0], axs[1][0]], [axs[0][1], axs[1][1]]],
            [mean_hyst, hyst], [mean_loop, loop],
            ['mean', f'pixel {pixel_ind}']):
        x_hyst = [np.array(loop_data.piezorep.write_volt_right),
                  np.array(loop_data.piezorep.write_volt_left)]
        y_hyst = [np.array(loop_data.piezorep.y_meas_right),
                  np.array(loop_data.piezorep.y_meas_left)]

        # Plot loop data and fit characteristics -> total fit
        hyster.plot(x_hyst, y=y_hyst, ax=ax,
                    labels=['branch1 (fit)', 'branch2 (fit)'])
        hyster.properties(infl_threshold=infl_threshold,
                          sat_threshold=sat_threshold, bckgnd=bckgnd)
        hyster.plot_properties(x_hyst, ax=ax, plot_dict={'fs': 8},
                               plot_hyst=False, bckgnd=bckgnd)
        ax_formating(ax, edge=True, grid=True, plt_leg=True,
                     edgew=3., fntsz=8., tickl=6., gridw=1.,
                     title=f'Hysteresis with background: {add_str}')

        # Plot loop data and fit characteristics -> ferro and electrostatic fit
        hyster.properties(infl_threshold=infl_threshold,
                          sat_threshold=sat_threshold)
        axb.plot(x_hyst[0],
                 linear(np.array(x_hyst[0]), slope=hyster.params['slope'].value,
                        offset=hyster.params['offset'].value),
                 'g--', label='bckgnd')
        hyster.plot_properties(x_hyst, ax=axb, plot_dict={'fs': 8})
        ax_formating(axb, edge=True, grid=True, plt_leg=True,
                     edgew=3., fntsz=8., tickl=6., gridw=1.,
                     title=f'Hysteresis without background: {add_str}')

        plt.xlim(min([min(x_hyst[0]), min(x_hyst[1])]),
                 max([max(x_hyst[0]), max(x_hyst[1])]))

    # Annotation
    if dict_str:
        add_txt(fig, dict_str)

    fig.text(0.5, 0.05, 'Write voltage [V]', ha='center', fontsize=15)
    fig.text(0.05, 0.5, f'Piezo Response [{unit}]', ha='center', va='center',
             fontsize=15, rotation=90)

    return fig


def extract_params(file_path_in=None):
    """
    Generate all dict parameters from saving parameters measurement txt file

    Parameters
    ----------
    file_path_in: str, optional
        Path of saving parameters measurement txt file (in)

    Returns
    -------
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        sspfm bias signal parameters
    user_pars: dict
        All user parameters for the treatment
    """
    assert os.path.isfile(file_path_in)

    # Open and read each lines of the file
    with open(file_path_in, encoding='utf-8') as parameter_file:
        lines = parameter_file.readlines()

    # Init parameters
    meas_pars, sign_pars, hyst_pars, pha_pars, other_pars = {}, {}, {}, {}, {}
    indx_meas_pars, indx_sign_pars, indx_hyst_pars, indx_pha_pars, \
        indx_other_pars = 0, 0, 0, 0, 0

    # Find starting line
    for cont, line in enumerate(lines):
        if line.startswith('- Global parameters'):
            indx_meas_pars = cont
        if line.startswith('- SS PFM parameters'):
            indx_sign_pars = cont
        if line.startswith('- Hysteresis / loop treatment parameters'):
            indx_hyst_pars = cont
        if line.startswith('- Phase treatment parameters'):
            indx_pha_pars = cont
        if line.startswith('- Other parameters'):
            indx_other_pars = cont

    def get_keys(lines_pars, line_start=0, line_end=-1):
        """
        Extract keys from lines of parameters.

        Parameters
        ----------
        lines_pars: list of str
            List of lines containing parameters
        line_start: int, optional
            Starting line index (inclusive)
        line_end: int, optional
            Ending line index (exclusive)

        Returns
        -------
        keys_pars: list of str
            List of extracted keys
        """
        lines_pars = lines_pars[line_start:line_end]
        keys_pars = [line_pars.split(':')[0] for line_pars in lines_pars if
                     line_pars != '\n']
        return keys_pars

    # Key of all dict parameters
    keys_meas_pars = get_keys(lines, line_start=indx_meas_pars+1,
                              line_end=indx_sign_pars-1)
    keys_sign_pars = get_keys(lines, line_start=indx_sign_pars+1,
                              line_end=indx_hyst_pars-1)
    keys_hyst_pars = ['func', 'method', 'asymmetric', 'inf thresh',
                      'sat thresh', 'del 1st loop']
    keys_pha_pars = ['pha corr', 'pha fwd', 'pha rev', 'pha func', 'main elec',
                     'locked elec slope']
    keys_other_pars = ['diff domain', 'diff mode', 'sat domain', 'sat mode']

    # Lines of parameters in txt file
    lines_meas_pars = lines[indx_meas_pars + 1:
                            indx_meas_pars + (1 + len(keys_meas_pars))]
    lines_sign_pars = lines[indx_sign_pars + 1:
                            indx_sign_pars + (1 + len(keys_sign_pars))]
    lines_hyst_pars = lines[indx_hyst_pars + 1:
                            indx_hyst_pars + (1 + len(keys_hyst_pars))]
    lines_pha_pars = lines[indx_pha_pars + 1:
                           indx_pha_pars + (1 + len(keys_pha_pars))]
    lines_other_pars = lines[indx_other_pars + 1:
                             indx_other_pars + (1 + len(keys_other_pars))]

    # Fill dict parameters
    keys_all_pars = [keys_meas_pars, keys_sign_pars, keys_hyst_pars,
                     keys_pha_pars, keys_other_pars]
    line_all_pars = [lines_meas_pars, lines_sign_pars, lines_hyst_pars,
                     lines_pha_pars, lines_other_pars]
    all_pars = [meas_pars, sign_pars, hyst_pars, pha_pars, other_pars]
    for keys, line, dico in zip(keys_all_pars, line_all_pars, all_pars):
        for key, txt in zip(keys, line):
            txt_split = txt.split(':', 1)
            if len(txt_split) > 1:
                lab = txt_split[0].strip()
                value_str = txt_split[1].strip()
                if lab == 'phase function':
                    value = np.cos if 'cos' in value_str else np.sin
                elif lab == 'differential domain between on/off ' \
                            'field loops, mode ?':
                    value = value_str
                elif lab == 'saturation domain for electrostatic ' \
                            'decoupling procedure, mode ?':
                    value = value_str
                else:
                    try:
                        value = eval(value_str)
                    except (NameError, SyntaxError):
                        value = value_str
                dico[key] = value

    user_pars = {**hyst_pars, **pha_pars, **other_pars}

    return meas_pars, sign_pars, user_pars


def single_analysis(file_path_in, user_pars, meas_pars, sign_pars, dict_pha,
                    analysis_mode='on_f_loop', cont=1, test_dict=None,
                    make_plots=False):
    """
    Data analysis of a measurement file (i.e. a pixel), extract loop data in txt
    file, find the best hysteresis loop depending on the analysis mode, fit and
    extract properties from it and analyse electrostatic component

    Parameters
    ----------
    file_path_in: str
        Path of the txt loop file (in)
    user_pars: dict
        All user parameters for the treatment
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        sspfm bias signal parameters
    dict_pha: dict
        Used for phase treatment
    analysis_mode: str, optional
        Operating mode for the reader: three possible modes:
        - 'on_f_loop' for on field measurement
        - 'mean_loop' for off field measurement with a constant value of read
        voltage
        - 'multi_loop' for off field measurement with different value of read
        voltage
    cont: int, optional
        Index of the corresponding file
    test_dict: dict, optional
        Dict of test parameters (used for test of the module)
    make_plots: bool, optional
        Activation key for figures generation

    Returns
    -------
    best_hyst: Hysteresis object
        Best hysteresis depending on analysis mode of the pixel
    best_loop: loop (MultiLoop or MeanLoop) object
        Best loop depending on analysis mode of the pixel
    """
    assert analysis_mode in ['multi_loop', 'mean_loop', 'on_f_loop']

    # Init pars
    figs = []

    # Data extraction
    if test_dict is None:
        data_dict, dict_str, _ = extract_nanoloop_data(file_path_in)
    else:
        pha_val = {"fwd": user_pars["pha fwd"], "rev": user_pars["pha rev"]}
        data_dict, dict_str = gen_data_dict(
            test_dict, meas_pars['Q factor'], mode=test_dict['mode'],
            pha_val=pha_val)
    dict_str['index'] = cont

    # List of MultiLoop object
    res = nanoloop_treatment(
        data_dict, sign_pars, dict_pha=dict_pha, dict_str=dict_str,
        q_fact_scalar=meas_pars['Q factor'])
    (loop_tab, _, _) = res

    # cKPFM analysis if multiloop
    if analysis_mode == 'multi_loop':
        ckpfm_dict = gen_ckpfm_meas(loop_tab)
        if make_plots:
            fig = plot_ckpfm(ckpfm_dict, dict_str=dict_str)
            figs.append(fig)

    # Find best loop depending on analysis mode
    res = find_best_nanoloop(
        loop_tab, dict_pha['counterclockwise'], dict_pha['grounded tip'],
        analysis_mode=analysis_mode, del_1st_loop=user_pars['del 1st loop'],
        model=user_pars['func'], asymmetric=user_pars['asymmetric'],
        method=user_pars['method'])
    (x_hyst, y_hyst, best_loop, _, _) = res

    # Perform hysteresis fit and extract properties
    res = hyst_analysis(
        x_hyst, y_hyst, best_loop, dict_pha['counterclockwise'],
        dict_pha['grounded tip'], dict_str=dict_str,
        infl_threshold=user_pars['inf thresh'],
        sat_threshold=user_pars['sat thresh'], model=user_pars['func'],
        asymmetric=user_pars['asymmetric'], method=user_pars['method'],
        analysis_mode=analysis_mode, make_plots=make_plots)
    (best_hyst, _, _, figs_hyst) = res
    figs += figs_hyst

    if make_plots:
        return figs
    else:
        return best_hyst, best_loop


def main_sort_plot_pixel(user_pars, dir_path_in, verbose=False,
                         show_plots=False, save_plots=False, dirname=None):
    """
    Main function used to find extremum value of sspfm map of a reference
    property and plot hysteresis of associated files

    Parameters
    ----------
    user_pars: dict
        Dict of all user parameters for the treatment
    dir_path_in: str
        Spm measurement files directory (in)
    verbose: bool, optional
        Activation key for verbosity
    show_plots: bool, optional
        Activation key to plot figures
    save_plots: bool, optional
        If True, the plots are saved in the dirname with a user-defined name
    dirname: str, optional
        If None, the directory where saved plots go is the temporary directory

    Returns
    -------
    files: list of str
        List of all file sorted with measurement parameter of reference
    """
    # Path generation / management
    assert os.path.isdir(dir_path_in)

    # Extract and init parameters
    make_plots = bool(show_plots or save_plots)
    meas_pars, sign_pars, treat_pars = extract_params(
        user_pars['file path in pars'])
    treat_pars.update({
        'mode': user_pars['prop key']['mode'],
        'dir path in prop': user_pars['dir path in prop'],
        'dir path in loop': user_pars['dir path in loop'],
        'file path in pars': user_pars['file path in pars'],
        'mask': {'man mask': [],
                 'revert mask': False}
    })
    dict_pha = gen_dict_pha(meas_pars, treat_pars['pha corr'],
                            pha_fwd=treat_pars['pha fwd'],
                            pha_rev=treat_pars['pha rev'],
                            func=treat_pars['pha func'],
                            main_elec=treat_pars['main elec'],
                            locked_elec_slope=treat_pars['locked elec slope'])

    # Extract file paths
    tab_path_raw = dir_path_in.split('_')[:-3]
    dir_path_raw = '_'.join(tab_path_raw)
    file_paths_raw = [elem[0]
                      for elem in generate_file_nanoloop_paths(dir_path_raw)]
    dict_file = {file: cont for cont, file in enumerate(file_paths_raw)}

    # Extract property value
    properties, dim_pix, dim_mic = extract_properties(
        user_pars['dir path in prop'])
    sel_property = properties[
        user_pars['prop key']['mode']][user_pars['prop key']['prop']]

    # Associate file with corresponding value and sort it in ascending order
    dictio = {}
    for elem_file, elem_val in zip(file_paths_raw, sel_property):
        dictio[elem_file] = elem_val
    dictio = dict(sorted(dictio.items(), key=lambda item: item[1]))
    sorted_files = list(dictio.keys())
    if not user_pars['reverse']:
        sorted_files.reverse()

    # Define pixel file to analyze
    if user_pars['list pixels'] is None:
        files = sorted_files
    elif len(user_pars['list pixels']) == 0:
        files = [list(dict_file.keys())[pix] for pix in
                 range(len(sorted_files))]
    else:
        files = [list(dict_file.keys())[pix] for pix in
                 user_pars['list pixels']]

    # Mean sel_property value
    if verbose:
        if user_pars["list pixels"] is None:
            mask_for_mean = user_pars["list pixels"]
        elif len(user_pars["list pixels"]) > 0:
            mask_for_mean = user_pars["list pixels"]
        else:
            mask_for_mean = None
        mean = np.mean(remove_val(sel_property, mask=mask_for_mean,
                                  reverse=True))
        print(f'mean value: {mean}')

    # For each sorted file
    for cont, file in enumerate(files):
        # Print info on file
        if verbose:
            rank = len(files) - cont if user_pars['reverse'] else cont + 1
            print(f'\t - {os.path.split(file)[1]}: {rank}/{len(files)}, value='
                  f'{dictio[file]}, pixel_index={dict_file[file]}')
        if make_plots:
            # On // off mode
            if user_pars['prop key']['mode'] in ['off', 'on']:
                # Mean hysteresis measurement
                res = main_mean_hyst(treat_pars, verbose=False,
                                     make_plots=False)
                (mean_loop, mean_hyst) = res
                loop_file_name = os.path.split(file)[1][:-4] + '.txt'
                loop_file_path = os.path.join(user_pars['dir path in loop'],
                                              loop_file_name)
                _, dict_str, _ = extract_nanoloop_data(loop_file_path)
                analysis_mode = gen_analysis_mode(
                    mode=user_pars['prop key']['mode'],
                    read_mode=sign_pars['Mode (R)'])
                tab = ['mean_loop', 'multi_loop']
                bckgnd = 'offset' if analysis_mode in tab else 'linear'
                figs_nanoloop = main_loop_file_reader(
                    loop_file_path, dict_pha=dict_pha,
                    del_1st_loop=user_pars['del 1st loop'],
                    verbose=False, make_plots=make_plots)
                for fig in figs_nanoloop:
                    fig.sfn += f"_pixel_{dict_file[file]}"
                best_hyst, best_loop = single_analysis(
                    loop_file_path, treat_pars, meas_pars, sign_pars, dict_pha,
                    analysis_mode=analysis_mode, cont=dict_file[file])
                fig_hyst = plot_comparative_hyst(
                    mean_hyst, mean_loop, best_hyst, best_loop, bckgnd=bckgnd,
                    infl_threshold=treat_pars['inf thresh'],
                    sat_threshold=treat_pars['sat thresh'], dict_str=dict_str,
                    pixel_ind=dict_file[file])
                figs = figs_nanoloop + [fig_hyst]
            # Other mode
            elif user_pars['prop key']['mode'] == 'other':
                loop_file_name = os.path.split(file)[1][:-4] + '.txt'
                loop_file_path = os.path.join(user_pars['dir path in loop'],
                                              loop_file_name)
                _, dict_str, _ = extract_nanoloop_data(loop_file_path)
                figs = []
            # Coupled mode
            elif user_pars['prop key']['mode'] == 'coupled':
                best_loop, figs_nanoloop = {}, {}
                res = print_parameters(treat_pars['file path in pars'])
                meas_pars, sign_pars, _, _, _ = res
                for mode in ['off', 'on']:
                    loop_file_name = mode + '_f_' + \
                                     os.path.split(file)[1][:-4] + '.txt'
                    loop_file_path = os.path.join(user_pars['dir path in loop'],
                                                  loop_file_name)
                    analysis_mode = gen_analysis_mode(
                        mode=mode, read_mode=sign_pars['Mode (R)'])
                    best_loop[mode], _ = single_script(
                        loop_file_path, treat_pars, meas_pars,
                        sign_pars, analysis_mode=analysis_mode)
                    figs_nanoloop[mode] = main_loop_file_reader(
                        loop_file_path, dict_pha=dict_pha,
                        del_1st_loop=user_pars['del 1st loop'],
                        verbose=False, make_plots=make_plots)
                multi_figures = main_mean_hyst(treat_pars, verbose=False,
                                               make_plots=True)
                offsets_off = properties['off']['charac tot fit: y shift']
                elec_offset = get_setting('electrostatic_offset')
                offset_off = offsets_off[dict_file[file]] if elec_offset else 0
                _, _, _, single_fig = differential_analysis(
                    best_loop['on'], best_loop['off'], offset_off=offset_off,
                    bias_min=DEFAULT_LIMIT['min'],
                    bias_max=DEFAULT_LIMIT['max'], dict_str=None,
                    make_plots=make_plots)
                dict_str = {'label': 'Coupled', 'col': 'r'}
                figs = figs_nanoloop['off'] + figs_nanoloop['on']
                figs += multi_figures + [single_fig]
            else:
                raise IOError("'user_pars['prop key']['mode']' should be "
                              "'on' or 'off' or 'coupled' or 'other'")

            dict_interp = {'fact': user_pars['interp fact'],
                           'func': user_pars['interp func']}
            fig_map = plot_and_save_maps(
                sel_property, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp,
                mask=[], prop_str=user_pars['prop key']['prop'],
                highlight_pix=[dict_file[file]])
            fig_map.sfn += f'_pixel_{dict_file[file]}'
            add_txt(fig_map, dict_str)
            figsize = get_setting("figsize")
            histo, ax = plt.subplots(figsize=figsize)
            histo.sfn = f'histo_pixel_{dict_file[file]}'
            plot_dict = {'title': f'histo: pixel {dict_file[file]}',
                         'x lab': f'{user_pars["prop key"]["prop"]}',
                         'bins': 20, 'fs': 15, 'edgew': 5, 'tickl': 5,
                         'gridw': 2}
            plot_hist(ax, list(dictio.values()), plot_dict=plot_dict)
            add_txt(histo, dict_str)
            ax.axvline(x=dictio[file], c='r', ls=':', lw=5)
            figs += [fig_map] + [histo]
            print_plots(figs, show_plots=show_plots, save_plots=save_plots,
                        dirname=dirname, transparent=False)

    return files


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - prop key: dict
        --> property key to ordered pixel
        - mode: str --> Mode of prop key ('on', 'off', 'coupled')
        - prop: str --> Name of prop key
    - list_pix: list[int]
        List of pixel indices to analyze.
        This parameter is used to specify a list of pixel indices for analysis.
        Value:
        - A list of integers: If the list_pix is [a, b, c ...],
        files of index a, b, c [...] are analyzed.
        - If list_pix is None, all pixels are analyzed in ascending order in
        terms of the value of the property.
        - If list_pix is an empty list (list_pix=[]), all pixels are analyzed
        in ascending order in terms of the index.
    - reverse: bool
        Reverse the order of pixels to analyze.
        This parameter allows you to control the order in which pixels are
        analyzed. When set to True, it reverses the order of pixels that
        are analyzed.
    - del_1st_loop: bool
        Delete First Loop
        If this parameter is set to True, it deletes the first loop of the
        analysis, which is typically used for calculating the mean hysteresis.
        This can be useful when the first write voltage values are equal to
        zero, indicating that the material is in a pristine state, and the
        loop shape would be different from the polarized state.
        Deleting the first loop helps to avoid artifacts in the analysis.
        This parameter has influence only on figure.
    - interp_fact: int
        Interpolation factor for sspfm maps interpolation.
        This parameter determines the level of interpolation to be applied to
        SSPFM maps.
    - interp_func: str
        Interpolation function
        This parameter specifies the interpolation function used for sspfm
        maps interpolation. It can take one of the following values:
        'linear', or 'cubic'.

    - dir_path_in: str
        Results of analysis directory.
        This parameter specifies the directory containing the results of
        analysis generated after the 1st and 2nd step of the analysis.
        Default: 'title_meas_out_mode'
    - dir_path_in_prop: str
        Properties files directory
        This parameter specifies the directory containing the ferroelectric
         properties text files generated after the 2nd step of the analysis.
        Optional, Default: 'properties'
    - dir_path_in_loop: str
        Txt loop files directory.
        This parameter specifies the directory containing the loop text files
        generated after the 1st step of the analysis.
        Optional, Default: 'nanoloops'
    - file_path_in_pars: str
        Measurement and analysis parameters txt file.
        This parameter specifies the file containing measurement and analysis
        parameters generated after the 2nd step of the analysis.
        Optional, Default: 'parameters.txt'
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
        file_path = os.path.realpath(__file__)
        file_path_user_params = copy_default_settings_if_not_exist(file_path)

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
        # dir_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # plot_pix_extrem_2023-10-02-16h38m
        verbose = True
        show_plots = True
        save = False
        user_pars = {'prop key': {'mode': 'off',
                                  'prop': 'charac tot fit: area'},
                     'list pixels': None,
                     'reverse': False,
                     'del 1st loop': True,
                     'interp fact': 4,
                     'interp func': 'linear'}
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    properties_folder_name = get_setting('default_properties_folder_name')
    dir_path_in_prop = os.path.join(dir_path_in, properties_folder_name)
    # dir_path_in_prop = r'...\KNN500n_15h18m02-10-2023_out_dfrt\properties
    nanoloops_folder_name = get_setting('default_nanoloops_folder_name')
    dir_path_in_loop = os.path.join(dir_path_in, nanoloops_folder_name)
    # dir_path_in_loop = r'...\KNN500n_15h18m02-10-2023_out_dfrt\nanoloops
    parameters_file_name = get_setting('default_parameters_file_name')
    file_path_in_pars = os.path.join(dir_path_in, parameters_file_name)
    # file_path_in_pars = r'...\KNN500n_15h18m02-10-2023_out_dfrt\parameters.txt
    user_pars['dir path in prop'] = dir_path_in_prop
    user_pars['dir path in loop'] = dir_path_in_loop
    user_pars['file path in pars'] = file_path_in_pars

    return user_pars, dir_path_in, dir_path_out, verbose, show_plots, save


def main():
    """ Main function for data analysis. """
    # Extract parameters
    out = parameters()
    (user_pars, dir_path_in, dir_path_out, verbose, show_plots, save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        dir_path_in, dir_path_out, save=save, dirname="plot_pix_extremum",
        lvl=0, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    main_sort_plot_pixel(
        user_pars, dir_path_in, verbose=verbose, show_plots=show_plots,
        save_plots=save, dirname=dir_path_out)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=True)


if __name__ == '__main__':
    main()
