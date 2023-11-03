"""
Module used to generate sspfm maps
    - Map annotation
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from PySSPFM.utils.map.interpolate import interp_2d_treated
from PySSPFM.utils.map.matrix_processing import formatting_measure

from PySSPFM.settings import \
    (COLOR_SSPFM_MAP_PIXEL, COLOR_SSPFM_MAP, COLOR_SSPFM_MAP_HIGHLIGHTED_PIXEL,
     FIGSIZE)


def plot_and_save_maps(property_arr, dim_pix, dim_mic=None, dict_interp=None,
                       dict_map=None, save=False, dir_path_out=None, mask=None,
                       revert_mask=False, prop_str='', ref=None, dict_ref=None,
                       color=COLOR_SSPFM_MAP, cbar_lab=None,
                       highlight_pix=None):
    """
    Plot the figure of the hysteresis nanoloop characteristic properties
    (all maps)

    Parameters
    ----------
    property_arr: numpy.ndarray
        Array of values for the considered property.
    dim_pix: dict
        Dictionary of map dimensions for 'x' and 'y' axes (in pixels).
    dim_mic: dict, optional
        Dictionary of map dimensions for 'x' and 'y' axes (in microns).
    dict_interp: dict, optional
        Dictionary of map interpolation parameters.
    dict_map: dict, optional
        Dictionary used for map annotation.
    save: bool, optional
        If True, save the property matrix in a txt file.
    dir_path_out: str, optional
        Path of the property matrix txt directory.
    mask: list or numpy.ndarray, optional
        List of index corresponding to the mask.
    revert_mask: bool, optional
        This parameter specifies if the mask should be reverted or not.
    prop_str: str, optional
        Title of the figure: i.e. name of the measured parameter.
    ref: numpy.ndarray, optional
        Array of values for the reference property.
    dict_ref: dict, optional
        Dictionary on ref property condition to generate the mask.
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

    applied_mask = [index for index in range(len(property_arr)) if
                    index not in mask] if revert_mask else mask

    property_arr = np.array(property_arr, dtype='f')

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
    plt.suptitle(prop_str, size=24, weight='heavy')
    main_ax.set_xlabel(f'width ({unit})', size=20, weight='heavy')
    main_ax.set_ylabel(f'height ({unit})', size=20, weight='heavy')
    main_ax.axis('off')

    if ref is not None:
        # Measure processing on the ref array to plot the maps
        (raw_ext, raw_dim_fact, matrix_step1, _, matrix_step2, interp_ext,
         _, _, matrix_step3b, index_blank, tab_all_index, tab_plotted_index,
         directions) = formatting_measure(
            ref, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp,
            mask=applied_mask)

        # Step 1 of ref: raw ref map (no selection criterion)
        title_ax1 = f'{dict_map["mask mode"]}: step 1 (init)' \
            if dict_map else 'step 1 (init)'
        intermediate_map(
            fig, axs[0], matrix_step1, dim_pix, ext=raw_ext,
            dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
            tab_plotted_index=tab_plotted_index, directions=directions,
            plot_ind=True, ax_title=title_ax1, color=color, cbar_lab=cbar_lab,
            highlight_pix=highlight_pix)

        # Step 2 or 4 (final) of ref: plot different images based on conditions
        if dict_interp is None:
            title_ax2 = f'{dict_map["mask mode"]}: step 2' \
                if dict_map else 'step 2'
            intermediate_map(
                fig, axs[1], matrix_step2, dim_pix, ext=raw_ext,
                dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                tab_plotted_index=tab_plotted_index, directions=directions,
                plot_ind=True, ax_title=title_ax2, color=color,
                cbar_lab=cbar_lab, highlight_pix=highlight_pix)
        else:
            title_ax2 = f'{dict_map["mask mode"]}: step 4 (final)' \
                if dict_map else 'step 4 (final)'
            final_map(
                fig, axs[1], matrix_step3b, dim_pix, ext=interp_ext,
                dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
                tab_plotted_index=tab_plotted_index, directions=directions,
                index_blank=index_blank, ax_title=title_ax2, color=color,
                cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Measure processing on the property array to plot the maps
    (raw_ext, raw_dim_fact, matrix_step1, _, matrix_step2, interp_ext, _,
     matrix_step3, matrix_step3b, index_blank, tab_all_index,
     tab_plotted_index, directions) = formatting_measure(
        property_arr, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp,
        mask=applied_mask)

    # Step 1 of measure: raw map (no selection criterion)
    title_ax3 = 'Step 1: Raw data'
    intermediate_map(
        fig, axs[2], matrix_step1, dim_pix, ext=raw_ext, dim_fact=raw_dim_fact,
        tab_all_index=tab_all_index, tab_plotted_index=tab_plotted_index,
        directions=directions, plot_ind=True, ax_title=title_ax3, color=color,
        cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Step 1bis: interpolation of step 1
    if dict_interp is not None:
        title_ax4 = 'Step 1bis: Interpolation of 1'
        _, matrix_step1b = interp_2d_treated(matrix_step1,
                                             dict_interp=dict_interp)
        intermediate_map(
            fig, axs[3], matrix_step1b, dim_pix, ext=interp_ext,
            dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
            tab_plotted_index=tab_plotted_index, directions=directions,
            plot_ind=False, ax_title=title_ax4, color=color, cbar_lab=cbar_lab,
            highlight_pix=highlight_pix)

    # Step 2: add the criterion selection: some pixel are removed
    title_ax5 = 'Step 2: Suppress value errors'
    intermediate_map(
        fig, axs[4], matrix_step2, dim_pix, ext=raw_ext, dim_fact=raw_dim_fact,
        tab_all_index=tab_all_index, tab_plotted_index=tab_plotted_index,
        directions=directions, plot_ind=True, ax_title=title_ax5, color=color,
        cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Step 3: interpolate removed pixel values (without increasing resolution)
    # to go back to normal values
    title_ax6 = 'Step 3: Interpolate value errors'
    intermediate_map(
        fig, axs[5], matrix_step3, dim_pix, ext=raw_ext, dim_fact=raw_dim_fact,
        tab_all_index=tab_all_index, tab_plotted_index=tab_plotted_index,
        directions=directions, plot_ind=True, ax_title=title_ax6, color=color,
        cbar_lab=cbar_lab, highlight_pix=highlight_pix)

    # Step 3bis: interpolation of step 3
    if dict_interp is not None:
        title_ax7 = 'Step 3bis: Interpolation of 3'
        intermediate_map(
            fig, axs[6], matrix_step3b, dim_pix, ext=interp_ext,
            dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
            tab_plotted_index=tab_plotted_index, directions=directions,
            plot_ind=False, ax_title=title_ax7, cbar_lab=cbar_lab, color=color,
            highlight_pix=highlight_pix)

    # Step 4: final result: interpolation of step 3 + remove the area
    # corresponding to the removed pixels on the map
    if dict_interp is not None:
        title_ax8 = 'Step 4: Final result, interpolation'
        final_map(
            fig, axs[7], matrix_step3b, dim_pix, ext=interp_ext,
            dim_fact=raw_dim_fact, tab_all_index=tab_all_index,
            tab_plotted_index=tab_plotted_index, directions=directions,
            index_blank=index_blank, ax_title=title_ax8, cbar_lab=cbar_lab,
            color=color, highlight_pix=highlight_pix)

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

    if len(applied_mask) < 15:
        # Add mask information
        fig.text(0.01, 0.04, f'mask, pixel removed: {str(applied_mask)}',
                 size=12, weight='heavy')

    if dict_ref:
        # Add pixel selection criterion information
        fig.text(0.01, 0.02,
                 f'pixel selection criterion: {dict_ref["crit sel lab"]}, '
                 f'revert mode is {revert_mask}',
                 size=12, weight='heavy')

    # Save .txt image data
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
        X = np.column_stack((pixels_index, x_coordinate, y_coordinate,
                             property_arr))

        # Save the data to a .txt file
        file_name_out = f'{prop_str}.txt'
        header = f'pixel index\t\tX coordinate (microns)\t\t' \
                 f'Y coordinate (microns)\t\t{prop_str}'
        file_path_out = os.path.join(dir_path_out, file_name_out)
        np.savetxt(file_path_out, X, fmt='%i\t\t%.2f\t\t%.2f\t\t%.2f',
                   header=header)

    return fig


def intermediate_map(fig, ax, matrix, dim_pix, ext=None, dim_fact=None,
                     tab_all_index=None, tab_plotted_index=None,
                     directions=None, plot_ind=True, ax_title='',
                     color=COLOR_SSPFM_MAP, cbar_lab=None, highlight_pix=None):
    """
    Plot intermediate map on the figure

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


def final_map(fig, ax, matrix, dim_pix, ext=None, dim_fact=None,
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


def annotate(ax, dim_pix, dim_fact=None, tab_all_index=None,
             tab_plotted_index=None, directions=None, plot_ind=True,
             highlight_pix=None):
    """
    Plot pixel position, label, and tip travel direction on the map

    Parameters
    ----------
    ax: matplotlib.axes
        Ax of the matplotlib figure
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_fact: dict('x': ,'y':) of float, optional
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
    highlight_pix: list(v) of int, optional
        List of pixel index to highlight for map plotting

    Returns
    -------
    None
    """
    dim_fact = dim_fact or {'x': 1, 'y': 1}

    if tab_all_index is not None and tab_plotted_index is not None:
        for i, index in enumerate(tab_all_index):
            color = COLOR_SSPFM_MAP_PIXEL
            if highlight_pix is not None and index in highlight_pix:
                color = COLOR_SSPFM_MAP_HIGHLIGHTED_PIXEL
            if index in tab_plotted_index and plot_ind:
                # Plot pixel index
                ax.annotate(str(int(index)),
                            ((i % dim_pix['x']) * dim_fact['x'],
                             (i // dim_pix['x']) * dim_fact['y']),
                            c=color, size=7)
                # Plot tip travel direction
                if directions:
                    index_directions = tab_plotted_index.index(index)
                    ax.plot((i % dim_pix['x']) * dim_fact['x'],
                            (i // dim_pix['x']) * dim_fact['y'],
                            marker=directions[index_directions], mfc=color,
                            mec=color, ms=4, mew=0.5)
            elif index != -1:
                # Plot pixel position
                ax.plot((i % dim_pix['x']) * dim_fact['x'],
                        (i // dim_pix['x']) * dim_fact['y'],
                        marker='+', mfc=color, mec=color, ms=3, mew=0.5)


def txt_image(mode='off', read_mode='Low to High'):
    """
    Generate label and color for map plotting

    Parameters
    ----------
    mode: str, optional
        Mode of measurement: 'off', 'on' or 'coupled'
    read_mode: str, optional
        Application order of read voltage:
        - 'Low to High'
        - 'High to Low'
        - 'Single Read Step'

    Returns
    -------
    dict_str: dict
        Dict used to annotate map
    """
    assert mode in ['off', 'on', 'coupled']

    if mode == 'off' and read_mode == 'Single Read Step':
        label, col = 'Off field: mean loop analysis', 'w'
    elif mode == 'off':
        label, col = 'Off field: multi loop analysis', 'w'
    elif mode == 'on':
        label, col = 'On field: mean loop analysis', 'y'
    else:
        label, col = 'Coupled analysis', 'r'

    return {'label': label, 'col': col}


def disable_ax(ax):
    """
    Disable plotting edges of ax

    Parameters
    ----------
    ax: plt.axes

    Returns
    -------
    None
    """
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top=False, bottom=False, left=False,
                   right=False)
