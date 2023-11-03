"""
Module used to generate sspfm maps
    - Main map generation functions
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.core.iterable import arg_cond
from PySSPFM.utils.map.matrix_processing import \
    init_formatting_measure, cleared_measure
from PySSPFM.utils.map.plot import plot_and_save_maps, intermediate_map

from PySSPFM.settings import COLOR_SSPFM_MAP, FIGSIZE


def main_mapping(properties, dim_pix, dim_mic=None, dict_interp=None,
                 colors=None, cbar_lab=None, dict_map=None, ref=None,
                 dict_ref=None, mask=None, revert_mask=False, verbose=False,
                 show_plots=False, save_plots=False, dir_path_out=None):
    """
    Main function to construct the maps

    Parameters
    ----------
    properties: dict
        Sample properties to plot in sspfm maps
    dim_pix: dict
        Map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict, optional
        Map dimension for 'x' and 'y' axis (in microns)
    dict_interp: dict, optional
        Map interpolation parameters
    colors : dict, optional
        Colors for each property
    cbar_lab : dict, optional
        Colorbar labels for each property
    dict_map: dict, optional
        Dict used for map annotation
    ref: numpy.array, optional
        Array of values for the ref property (used to generate mask)
    dict_ref: dict, optional
        Ref property condition to generate the mask of the map
    mask: list or numpy.array, optional
        Index corresponding to the mask
    revert_mask: bool, optional
        This parameter specifies if the mask should be reverted or not
    verbose: bool, optional
        Activation key for verbosity
    show_plots: bool, optional
        Activation key for matplotlib figure visualization
    save_plots: bool, optional
        Activation key for fig save
    dir_path_out: str, optional
        Path of saving directory for sspfm maps (out)

    Returns
    -------
    mask: list or numpy.array, optional
        List of index corresponding to the mask
    """
    if mask is None:
        # Mask with condition on ref
        min_val, max_val, mask = gen_mask_ref(
            ref, dim_pix, dim_mic=dim_mic, min_val=dict_ref["min val"],
            max_val=dict_ref["max val"], mode_man=dict_ref["interactive"],
            ref_str=dict_ref["prop"], dict_map=dict_map)
        if dict_ref is not None:
            dict_ref["min val"], dict_ref["max val"] = min_val, max_val
            string = {}
            for val, ind in zip([dict_ref["min val"], dict_ref["max val"]],
                                ['min', 'max']):
                string[ind] = f'{val:.5f}' if val is not None else '_'
            lab = f'{dict_ref["prop"]} in [{string["min"]};{string["max"]}]'
            dict_ref['crit sel lab'] = lab
    else:
        # Manual mask
        if dict_map:
            dict_map["mask mode"] = 'man mask'

    for key, prop in properties.items():
        # try:
        _ = np.sum(prop)
        try:
            color = colors[key]
        except TypeError:
            color = COLOR_SSPFM_MAP
        try:
            cbar_lab = cbar_lab[key]
        except TypeError:
            cbar_lab = None

        fig = plot_and_save_maps(
            prop, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp,
            dict_map=dict_map, prop_str=key, mask=mask,
            revert_mask=revert_mask, ref=ref, dict_ref=dict_ref, color=color,
            cbar_lab=cbar_lab)
        if show_plots:
            plt.show()
        if save_plots:
            fig_name = key + ' ' + (dict_map['label'] if dict_map else '')
            fig_name = fig_name.lower().replace(' ', '_').replace(':', '')
            if verbose:
                print(fig_name)
            if dir_path_out:
                if not os.path.exists(dir_path_out):
                    os.mkdir(dir_path_out)
                fig.savefig(os.path.join(dir_path_out, fig_name))
        plt.close(fig=fig)
        # except (TypeError, ValueError):
        #     continue

    return mask


def gen_mask_ref(ref, dim_pix, dim_mic=None, min_val=None, max_val=None,
                 mode_man=False, ref_str='', dict_map=None):
    """
    Generate mask from ref property and condition on its values

    Parameters
    ----------
    ref: numpy.array
        Array of values for the ref property
    dim_pix: dict
        Map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict, optional
        Map dimension for 'x' and 'y' axis (in microns)
    min_val: float, optional
        Min value condition on ref to construct mask (if None, no condition on
        the value)
    max_val: float, optional
        Max value condition on ref to construct mask (if None, no condition on
        the value)
    mode_man: bool, optional
        If True, user can chose manually ref condition to generate the mask
    ref_str: str, optional
        Name of the ref property
    dict_map: dict, optional
        Dict used for map annotation

    Returns
    -------
    min_val: float
        Min value condition on ref to construct mask (if None, no condition on
        the value)
    max_val: float
        Max value condition on ref to construct mask (if None, no condition on
        the value)
    mask: list or numpy.array
        List of index corresponding to the mask
    """
    if mode_man:
        # Manual mode: mask created from manual set condition
        if dict_map:
            dict_map["mask mode"] = 'ref prop: man'
        min_val, max_val, mask = interactive_range_ref(
            ref, dim_pix, dim_mic=dim_mic, dict_map=dict_map,
            prop_str=ref_str)
    else:
        # Automatic mode: mask created from pre-set condition on ref
        if dict_map:
            dict_map["mask mode"] = 'ref prop: auto'
        mask = np.ravel(arg_cond(np.array(ref), min_val=min_val,
                                 max_val=max_val, reverse=True))

    return min_val, max_val, mask


def interactive_range_ref(ref, dim_pix, dim_mic=None, dict_map=None,
                          prop_str=''):
    """
    From the array ref (R² most of the time), the user can choose a pixel
    selection criterion on ref value interval for which the pixel will be
    rejected (mask creation). The map is plotted at each new iteration
    and the user can choose to stop when the selection criterion is satisfying

    Parameters
    ----------
    ref: numpy.array(p) of float
        Array of values for the ref property
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)
    dict_map: dict, optional
        Dict used for map annotation
    prop_str: str, optional
        Name of the property

    Returns
    -------
    min_val: float
        Min value condition on property to construct mask (if None, no condition
        on the value)
    max_val: float
        Min value condition on property to construct mask (if None, no condition
        on the value)
    mask: list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask (q<p)
    """
    # Initialize parameters
    min_val, max_val, mask = None, None, []

    # Initialize matrix: sorted, cleared, and sized 2D matrix
    out = init_formatting_measure(ref, dim_pix, dim_mic=dim_mic)
    (raw_ext, raw_dim_fact, nb_bug, cleared_matrix, tab_all_index,
     tab_plotted_index, directions) = out

    while True:
        # Pixel removed by the selection criterion
        ind = arg_cond(np.array(ref), min_val=min_val, max_val=max_val,
                       reverse=True)
        mask = np.ravel(ind)
        print('Index of pixel removed:')
        print(*mask, sep=", ")

        # Remove corresponding pixels in the matrix
        cleared_matrix = cleared_measure(ref, dim_pix, nb_bug=nb_bug,
                                         mask=mask)

        # Initialize image
        fig = plt.figure(figsize=FIGSIZE)
        ax = fig.add_subplot(111)

        # Colormap and colorbar
        intermediate_map(
            fig, ax, cleared_matrix, dim_pix, ext=raw_ext,
            dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
            tab_plotted_index=tab_plotted_index, directions=directions,
            plot_ind=True, ax_title='')

        # Annotate
        bbox_props_fast = {"boxstyle": 'darrow,pad=0.3', "fc": 'grey',
                           "ec": 'k', "lw": 2}
        bbox_props_slow = {"boxstyle": 'rarrow,pad=0.3', "fc": 'grey',
                           "ec": 'k', "lw": 2}

        unit = 'pixels' if dim_mic is None else 'microns'
        ax.set_title(prop_str, size=24, weight='heavy')
        ax.set_xlabel(f'width ({unit})', size=20, weight='heavy')
        ax.set_ylabel(f'height ({unit})', size=20, weight='heavy')
        fig.text(0.01, 0.90, "Fast scan axis", rotation=0, size=10,
                 bbox=bbox_props_fast)
        fig.text(0.03, 0.77, "Slow scan axis", rotation=270, size=10,
                 bbox=bbox_props_slow)

        if dict_map:
            fig.text(0.01, 0.95, dict_map["label"], color=dict_map["col"],
                     size=15, weight='heavy', backgroundcolor='k')

        plt.show()

        # User can choose to stop or continue the process
        input_str = str(input(f'If the criterion on {prop_str} is ok, press '
                              f'"Enter", else press another key:  '))

        if input_str != '':
            # User chooses a minimum property value as the selection criterion
            try:
                min_val = float(input(f'Enter {prop_str} min value:  '))
                max_val = float(input(f'Enter {prop_str} max value:  '))
            except ValueError:
                print('Invalid input: please retry')
                min_val, max_val = None, None
        else:
            break

    return min_val, max_val, mask


def check_list(measure):
    """
    Test performing to decide to plot (test successful) or not (test
    unsuccessful) the scan map of the measured considered parameter

    Parameters
    ----------
    measure: numpy.array(m*n) of float
        Array of values for the considered measure (m*n=p)

    Returns
    -------
    res: bool
        Result of the test: if True the test is success (i.e: the scan of
        the considered property parameter will be plotted)
    """
    # If measure is empty, the test is failed
    if len(measure) == 0:
        res = False
    else:
        # If all sample properties are equal, the test is failed
        res = not all(elem == measure[0] for elem in measure)

        if res:
            # If all sample properties are nan values, the test is failed
            res = not all(np.isnan(elem) for elem in measure)

    return res
