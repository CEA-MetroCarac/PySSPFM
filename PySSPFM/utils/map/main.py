"""
Module used to generate sspfm maps
    - Main map generation functions
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from PySSPFM.utils.core.iterable import arg_cond
from PySSPFM.utils.map.matrix_processing import \
    formatting_measure, sub_formatting_measure, cleared_measure
from PySSPFM.utils.map.interpolate import interp_2d_treated
from PySSPFM.utils.map.plot import annotate

from PySSPFM.settings import COLOR_SSPFM_MAP, FIGSIZE


def main_mapping(measurements, dim_pix, dim_mic=None, dict_interp=None,
                 colors=None, cbar_lab=None, dict_map=None, ref=None,
                 dict_ref=None, mask=None, verbose=False, show_plots=False,
                 save_plots=False, dir_path_out=None):
    """
    Main function to construct the maps

    Parameters
    ----------
    measurements: dict
        Measurements of sspfm maps
    dim_pix: dict
        Map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict, optional
        Map dimension for 'x' and 'y' axis (in microns)
    dict_interp: dict, optional
        Map interpolation parameters
    colors : dict, optional
        Colors for each measurement
    cbar_lab : dict, optional
        Colorbar labels for each measurement
    dict_map: dict, optional
        Dict used for map annotation
    ref: numpy.array, optional
        Array of values for the ref measurement (used to generate mask)
    dict_ref: dict, optional
        Ref measurement condition to generate the mask of the map
    mask: list or numpy.array, optional
        Index corresponding to the mask
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
        min_val, max_val, mask = mask_ref(
            ref, dim_pix, dim_mic=dim_mic, min_val=dict_ref["min val"],
            max_val=dict_ref["max val"], mode_man=dict_ref["interactive"],
            ref_str=dict_ref["meas"], dict_map=dict_map)
        if dict_ref is not None:
            dict_ref["min val"], dict_ref["max val"] = min_val, max_val
            string = {}
            for val, ind in zip([dict_ref["min val"], dict_ref["max val"]],
                                ['min', 'max']):
                string[ind] = f'{val:.5f}' if val is not None else '_'
            lab = f'{dict_ref["meas"]} in [{string["min"]};{string["max"]}]'
            dict_ref['crit sel lab'] = lab
    else:
        # Manual mask
        if dict_map:
            dict_map["mask mode"] = 'man mask'

    for key, measure in measurements.items():
        # try:
        _ = np.sum(measure)
        try:
            color = colors[key]
        except TypeError:
            color = COLOR_SSPFM_MAP
        try:
            cbar_lab = cbar_lab[key]
        except TypeError:
            cbar_lab = None

        fig = plot_and_save_image(
            measure, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp,
            dict_map=dict_map, measure_str=key, mask=mask, ref=ref,
            dict_ref=dict_ref, color=color, cbar_lab=cbar_lab)
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


def mask_ref(ref, dim_pix, dim_mic=None, min_val=None, max_val=None,
             mode_man=False, ref_str='', dict_map=None):
    """
    Generate mask from ref measurement and condition on its values

    Parameters
    ----------
    ref: numpy.array
        Array of values for the ref measurement
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
        Name of the ref measurement
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
            dict_map["mask mode"] = 'ref meas: man'
        min_val, max_val, mask = select_pixel(
            ref, dim_pix, dim_mic=dim_mic, dict_map=dict_map,
            measure_str=ref_str)
    else:
        # Automatic mode: mask created from pre-set condition on ref
        if dict_map:
            dict_map["mask mode"] = 'ref meas: auto'
        mask = np.ravel(arg_cond(np.array(ref), min_val=min_val,
                                 max_val=max_val, reverse=True))

    return min_val, max_val, mask


def plot_and_save_image(measure, dim_pix, dim_mic=None, dict_interp=None,
                        dict_map=None, save=False, dir_path_out=None, mask=None,
                        measure_str='', ref=None, dict_ref=None,
                        color=COLOR_SSPFM_MAP, cbar_lab=None,
                        highlight_pix=None):
    """
    Plot the figure of the hysteresis loop characteristic measurements

    Parameters
    ----------
    measure: numpy.ndarray
        Array of values for the considered measure.
    dim_pix: dict
        Dictionary of map dimensions for 'x' and 'y' axes (in pixels).
    dim_mic: dict, optional
        Dictionary of map dimensions for 'x' and 'y' axes (in microns).
    dict_interp: dict, optional
        Dictionary of map interpolation parameters.
    dict_map: dict, optional
        Dictionary used for map annotation.
    save: bool, optional
        If True, save the measurement matrix in a txt file.
    dir_path_out: str, optional
        Path of the measurement matrix txt directory.
    mask: list or numpy.ndarray, optional
        List of index corresponding to the mask.
    measure_str: str, optional
        Title of the figure: i.e. name of the measured parameter.
    ref: numpy.ndarray, optional
        Array of values for the reference measurement.
    dict_ref: dict, optional
        Dictionary on ref measurement condition to generate the mask.
    color: str, optional
        Color for the plot.
    cbar_lab: str, optional
        Label for the color bar.
    highlight_pix: list of int, optional
        List of pixel index to highlight for map plotting.

    Returns
    -------
    fig: plt.figure
    """
    measure = np.array(measure, dtype='f')

    # Initialize the figure
    fig = plt.figure(figsize=FIGSIZE)
    fig.sfn = 'map_image'
    main_ax = fig.add_subplot(111)
    axs = []
    for i in range(8):
        ax = fig.add_subplot(2, 4, i + 1)
        axs.append(ax)

    # Label and title
    unit = 'pixels' if dim_mic is None else 'microns'
    plt.suptitle(measure_str, size=24, weight='heavy')
    main_ax.set_xlabel(f'width ({unit})', size=20, weight='heavy')
    main_ax.set_ylabel(f'height ({unit})', size=20, weight='heavy')
    main_ax.axis('off')

    if ref is not None:
        # Measure processing on the ref array to plot the maps
        (raw_ext, raw_dim_fact, matrix_step1, _, matrix_step2, interp_ext,
         _, _, matrix_step3b, index_blank, tab_all_index, tab_plotted_index,
         directions) = formatting_measure(ref, dim_pix, dim_mic=dim_mic,
                                          dict_interp=dict_interp, mask=mask)

        # Step 1 of ref: raw ref map (no selection criterion)
        title_ax1 = f'{dict_map["mask mode"]}: step 1 (init)' \
            if dict_map else 'step 1 (init)'
        sub_image(fig, axs[0], matrix_step1, dim_pix, ext=raw_ext,
                  dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                  tab_plotted_index=tab_plotted_index,
                  directions=directions, plot_ind=True, ax_title=title_ax1,
                  color=color, cbar_lab=cbar_lab, highlight_pix=highlight_pix)

        # Step 2 or 4 (final) of ref: plot different images based on conditions
        if dict_interp is None:
            title_ax2 = f'{dict_map["mask mode"]}: step 2' \
                if dict_map else 'step 2'
            sub_image(fig, axs[1], matrix_step2, dim_pix, ext=raw_ext,
                      dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                      tab_plotted_index=tab_plotted_index,
                      directions=directions, plot_ind=True, ax_title=title_ax2,
                      color=color, cbar_lab=cbar_lab,
                      highlight_pix=highlight_pix)
        else:
            title_ax2 = f'{dict_map["mask mode"]}: step 4 (final)' \
                if dict_map else 'step 4 (final)'
            final_image(fig, axs[1], matrix_step3b, dim_pix, ext=interp_ext,
                        dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                        tab_plotted_index=tab_plotted_index,
                        directions=directions, index_blank=index_blank,
                        ax_title=title_ax2, color=color,
                        cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Measure processing on the measure array to plot the maps
    (raw_ext, raw_dim_fact, matrix_step1, _, matrix_step2, interp_ext, _,
     matrix_step3, matrix_step3b, index_blank, tab_all_index,
     tab_plotted_index, directions) = formatting_measure(
        measure, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp, mask=mask)

    # Step 1 of measure: raw measure map (no selection criterion)
    title_ax3 = 'Step 1: Raw datas'
    sub_image(fig, axs[2], matrix_step1, dim_pix, ext=raw_ext,
              dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
              tab_plotted_index=tab_plotted_index, directions=directions,
              plot_ind=True, ax_title=title_ax3, color=color,
              cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Step 1bis: interpolation of step 1
    if dict_interp is not None:
        title_ax4 = 'Step 1bis: Interpolation of 1'
        _, matrix_step1b = interp_2d_treated(matrix_step1,
                                             dict_interp=dict_interp)
        sub_image(fig, axs[3], matrix_step1b, dim_pix, ext=interp_ext,
                  dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                  tab_plotted_index=tab_plotted_index,
                  directions=directions, plot_ind=False, ax_title=title_ax4,
                  color=color, cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Step 2: add the criterion selection: some pixel are removed
    title_ax5 = 'Step 2: Suppress value errors'
    sub_image(fig, axs[4], matrix_step2, dim_pix, ext=raw_ext,
              dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
              tab_plotted_index=tab_plotted_index,
              directions=directions, plot_ind=True, ax_title=title_ax5,
              color=color, cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Step 3: interpolate removed pixel values (without increasing resolution)
    # to go back to normal values
    title_ax6 = 'Step 3: Interpolate value errors'
    sub_image(fig, axs[5], matrix_step3, dim_pix, ext=raw_ext,
              dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
              tab_plotted_index=tab_plotted_index, directions=directions,
              plot_ind=True, ax_title=title_ax6, color=color,
              cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Step 3bis: interpolation of step 3
    if dict_interp is not None:
        title_ax7 = 'Step 3bis: Interpolation of 3'
        sub_image(fig, axs[6], matrix_step3b, dim_pix, ext=interp_ext,
                  dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                  tab_plotted_index=tab_plotted_index,
                  directions=directions, plot_ind=False, ax_title=title_ax7,
                  cbar_lab=cbar_lab, color=color, highlight_pix=highlight_pix)

    # Step 4: final result: interpolation of step 3 + remove the area
    # corresponding to the removed pixels on the map
    if dict_interp is not None:
        title_ax8 = 'Step 4: Final result, interpolation'
        final_image(fig, axs[7], matrix_step3b, dim_pix, ext=interp_ext,
                    dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                    tab_plotted_index=tab_plotted_index, directions=directions,
                    index_blank=index_blank, ax_title=title_ax8,
                    cbar_lab=cbar_lab, color=color, highlight_pix=highlight_pix)

    # Annotate
    bbox_props_fast = {"boxstyle": 'darrow,pad=0.3', "fc": 'grey',
                       "ec": 'k', "lw": 2}
    bbox_props_slow = {"boxstyle": 'rarrow,pad=0.3', "fc": 'grey',
                       "ec": 'k', "lw": 2}

    if dict_map:
        # Add label for the map
        fig.text(0.01, 0.95, dict_map["label"], c=dict_map["col"], size=15,
                 weight='heavy', backgroundcolor='k')
        fig.text(0.01, 0.06, f'mask mode: {dict_map["mask mode"]}', size=12,
                 weight='heavy')

        if "limit" in dict_map.keys():
            # Add voltage range for differential analysis
            fig.text(0.65, 0.93,
                     f'voltage range for differential analysis: '
                     f'{str(dict_map["limit"])} V', size=12, weight='heavy')

    fig.text(0.01, 0.90, "Fast scan axis", rotation=0, size=10,
             bbox=bbox_props_fast)
    fig.text(0.03, 0.77, "Slow scan axis", rotation=270, size=10,
             bbox=bbox_props_slow)

    if len(mask) < 15:
        # Add mask information
        fig.text(0.01, 0.04, f'mask, pixel removed: {str(mask)}', size=12,
                 weight='heavy')

    if dict_ref:
        # Add pixel selection criterion information
        fig.text(0.01, 0.02,
                 f'pixel selection criterion: {dict_ref["crit sel lab"]}',
                 size=12, weight='heavy')

    # Save .txt image datas
    if save:
        # Generate pixel coordinates and indices
        pixels_index = np.arange(1, dim_pix['x'] * dim_pix['y'] + 1)
        vector_width_microns = np.linspace(0, dim_mic['x'], dim_pix['x'])
        vector_height_microns = np.linspace(0, dim_mic['y'], dim_pix['y'])
        x_coordinate, y_coordinate = np.meshgrid(vector_width_microns,
                                                 vector_height_microns)
        x_coordinate = x_coordinate.flatten()
        y_coordinate = y_coordinate.flatten()

        # Create the data matrix
        X = np.column_stack((pixels_index, x_coordinate, y_coordinate, measure))

        # Save the data to a .txt file
        file_name_out = f'{measure_str}.txt'
        header = f'pixel index\t\tX coordinate (microns)\t\t' \
                 f'Y coordinate (microns)\t\t{measure_str}'
        file_path_out = os.path.join(dir_path_out, file_name_out)
        np.savetxt(file_path_out, X, fmt='%i\t\t%.2f\t\t%.2f\t\t%.2f',
                   header=header)

    return fig


def select_pixel(ref, dim_pix, dim_mic=None, dict_map=None, measure_str=''):
    """
    From the array ref (R² most of the time), the user can choose a pixel
    selection criterion on ref value interval for which the pixel will be
    rejected (mask creation). The map is plotted at each new iteration
    and the user can choose to stop when the selection criterion is satisfying

    Parameters
    ----------
    ref: numpy.array(p) of float
        Array of values for the ref measurement
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)
    dict_map: dict, optional
        Dict used for map annotation
    measure_str: str, optional
        Name of the measure

    Returns
    -------
    min_val: float
        Min value condition on measure to construct mask (if None, no condition
        on the value)
    max_val: float
        Min value condition on measure to construct mask (if None, no condition
        on the value)
    mask: list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask (q<p)
    """
    # Initialize parameters
    min_val, max_val, mask = None, None, []

    # Initialize measure: sorted, cleared, and sized 2D matrix
    out = sub_formatting_measure(ref, dim_pix, dim_mic=dim_mic)
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
        sub_image(fig, ax, cleared_matrix, dim_pix, ext=raw_ext,
                  dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                  tab_plotted_index=tab_plotted_index, directions=directions,
                  plot_ind=True, ax_title='')

        # Annotate
        bbox_props_fast = {"boxstyle": 'darrow,pad=0.3', "fc": 'grey',
                           "ec": 'k', "lw": 2}
        bbox_props_slow = {"boxstyle": 'rarrow,pad=0.3', "fc": 'grey',
                           "ec": 'k', "lw": 2}

        unit = 'pixels' if dim_mic is None else 'microns'
        ax.set_title(measure_str, size=24, weight='heavy')
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
        input_str = str(input(f'If the criterion on {measure_str} is ok, press '
                              f'"Enter", else press another key:  '))

        if input_str != '':
            # User chooses a minimum measure value as the selection criterion
            try:
                min_val = float(input(f'Enter {measure_str} min value:  '))
                max_val = float(input(f'Enter {measure_str} max value:  '))
            except ValueError:
                print('Invalid input: please retry')
                min_val, max_val = None, None
        else:
            break

    return min_val, max_val, mask


def sub_image(fig, ax, matrix, dim_pix, ext=None, dim_fact=None,
              tab_all_index=None, tab_plotted_index=None, directions=None,
              plot_ind=True, ax_title='', color=COLOR_SSPFM_MAP, cbar_lab=None,
              highlight_pix=None):
    """
    Plot sub image i.e one map on the figure

    Parameters
    ----------
    fig: matplotlib.figure
        Matplotlib figure
    ax: matplotlib.axes
        Ax of the matplotlib figure
    matrix: numpy.array(m*n) of float
        2D array of values (m*n=p)
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    ext: list(4) of float, optional
        Axis (x and y) range of the maps for the plotting (in microns)
    dim_fact: dict('x': ,'y':) of float
        Dict of conv factor map dimension for x and y axis
    tab_all_index: list(r) or numpy.array(r) of int, optional
        2D array of index sorted and shaped in agreement scan size
    tab_plotted_index: list(s) or numpy.array(s) of int, optional
        Array of index with label plotted on the final image (an index is
        plotted when there is a change of tip travel direction i.e position
        in the limit of the scan) (s<p)
    directions: list(t) or numpy.array(t) of int, optional
        Array of symbol direction plotted on the final image (a symbol is
        plotted when there is a change of tip travel direction i.e position
        in the limit of the scan) (t<p)
    plot_ind: bool, optional
        If True, index in tab_plotted_index are plotted on the sub image
    ax_title: str, optional
        Title of the sub image
    color: str, optional
        Color for the plot.
    cbar_lab: str, optional
        Label for the color bar.
    highlight_pix: list(v) of int, optional
        List of pixel index to highlight for map plotting

    Returns
    -------
    None
    """
    dim_fact = dim_fact or {
        'x': (matrix.shape[0] - 1) / (dim_pix['x'] - 1),
        'y': (matrix.shape[1] - 1) / (dim_pix['y'] - 1)
    }

    # Set the title
    ax.set_title(ax_title)

    # Plot the image (cmap: jet or coolwarm)
    colo = ax.imshow(matrix, cmap=color, origin='lower', extent=ext)

    # from matplotlib.colors import LogNorm
    # colo = ax.imshow(matrix, cmap=color, origin='lower', extent=ext,
    #                  norm=LogNorm(vmin=0.9, vmax=1))

    # Plot pixel position, label, and tip direction on the map
    annotate(ax, dim_pix, dim_fact=dim_fact, tab_all_index=tab_all_index,
             tab_plotted_index=tab_plotted_index, directions=directions,
             plot_ind=plot_ind, highlight_pix=highlight_pix)

    # Add colorbar
    try:
        cbar = fig.colorbar(colo, ax=ax, ticks=cbar_lab[1])
    except TypeError:
        cbar = fig.colorbar(colo, ax=ax)
    if cbar_lab is not None:
        cbar.ax.set_yticklabels(cbar_lab[0])


def final_image(fig, ax, matrix, dim_pix, ext=None, dim_fact=None,
                tab_all_index=None, tab_plotted_index=None, directions=None,
                index_blank=None, ax_title='', color=COLOR_SSPFM_MAP,
                cbar_lab=None, highlight_pix=None):
    """
    Plot the final sub image i.e last map on the figure

    Parameters
    ----------
    fig: matplotlib.figure
        Matplotlib figure
    ax: matplotlib.axes
        Ax of the matplotlib figure
    matrix: numpy.array(m*n) of float
        2D array of values (m*n=p)
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    ext: list(4) of float, optional
        Axis (x and y) range of the maps for the plotting (in microns)
    dim_fact: dict('x': ,'y':) of float
        Dict of conv factor map dimension for x and y axis
    tab_all_index: list(r) or numpy.array(r) of int, optional
        2D array of index sorted and shaped in agreement scan size
    tab_plotted_index: list(s) or numpy.array(s) of int, optional
        Array of index with label plotted on the final image (an index is
        plotted when there is a change of tip travel direction i.e position
        in the limit of the scan) (s<p)
    directions: list(t) or numpy.array(t) of int, optional
        Array of symbol direction plotted on the final image (a symbol is
        plotted when there is a change of tip travel direction i.e position
        in the limit of the scan) (t<p)
    index_blank: numpy.array(u) of int, optional
        Array of value error index to add white square on the map (u<p)
    ax_title: str, optional
        Title of the sub image
    color: str, optional
        Color for the plot.
    cbar_lab: str, optional
        Label for the color bar.
    highlight_pix: list(v) of int, optional
        List of pixel index to highlight for map plotting

    Returns
    -------
    None
    """
    dim_fact = dim_fact or {
        'x': (matrix.shape[0] - 1) / (dim_pix['x'] - 1),
        'y': (matrix.shape[1] - 1) / (dim_pix['y'] - 1)
    }

    # Set the title
    ax.set_title(ax_title)

    # Plot the image with the specified color map
    colo = ax.imshow(matrix, cmap=color, origin='lower', extent=ext)

    if ext is not None:
        # Set the x and y limits of the plot
        ax.set_xlim(ext[0], ext[1])
        ax.set_ylim(ext[2], ext[3])

    # Add colorbar
    try:
        cbar = fig.colorbar(colo, ax=ax, ticks=cbar_lab[1])
    except TypeError:
        cbar = fig.colorbar(colo, ax=ax)
    if cbar_lab is not None:
        cbar.ax.set_yticklabels(cbar_lab[0])

    if index_blank is not None:
        # Add white squares at the error coordinates
        index_blank_xy_pix = [[elem // dim_pix['x'], elem % dim_pix['x']]
                              for elem in index_blank]
        index_blank_xy = [[(-0.5 + line[0]) * dim_fact['x'],
                           (-0.5 + line[1]) * dim_fact['y']]
                          for line in index_blank_xy_pix]
        for index in index_blank_xy:
            ax.add_patch(Rectangle(
                (index[1], index[0]), dim_fact['x'], dim_fact['y'],
                ec='w', fc='w', fill=True))

    # Plot pixel position, label, and tip direction on the map
    if dim_fact is not None:
        annotate(ax, dim_pix, dim_fact=dim_fact, tab_all_index=tab_all_index,
                 tab_plotted_index=tab_plotted_index, directions=directions,
                 plot_ind=False, highlight_pix=highlight_pix)


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
        the considered measurement parameter will be plotted)
    """
    # If measure is empty, the test is failed
    if len(measure) == 0:
        res = False
    else:
        # If all measurements are equal, the test is failed
        res = not all(elem == measure[0] for elem in measure)

        if res:
            # If all measurements are nan values, the test is failed
            res = not all(np.isnan(elem) for elem in measure)

    return res
