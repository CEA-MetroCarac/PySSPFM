"""
Module used to generate sspfm maps
    - Map annotation
"""

from PySSPFM.settings import \
    COLOR_SSPFM_MAP_PIXEL, COLOR_SSPFM_MAP_HIGHLIGHTED_PIXEL


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


def extent(dim_pix, dim_mic=None, dict_interp=None):
    """
    Find the maps dimension for raw and interpolated map

    Parameters
    ----------
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)
    dict_interp: dict, optional
        Dict of map interpolation parameters

    Returns
    -------
    raw_ext: list(4) of float
        List for axis (x and y) range of the maps for the plotting (in microns)
    raw_dim_fact: dict('x': ,'y':) of float
        Dict of conv factor map dimension for 'x' and 'y' axis
    interp_ext: list(4) of float
        List axis (x and y) range of the interpolated maps for the plotting (in
        microns)
    interp_dim_fact: dict('x': ,'y':) of float
        Dict of conv factor interpolated map dimension for 'x' and 'y' axis
    """
    raw_ext, raw_dim_fact = ext_calc(dim_pix, dim_mic=dim_mic)

    if dict_interp:
        nb_nan = dict_interp['fact'] - 1
        interp_dim_pix = {'x': dim_pix['x'] * dict_interp['fact'] - nb_nan,
                          'y': dim_pix['y'] * dict_interp['fact'] - nb_nan}
        interp_ext, interp_dim_fact = ext_calc(interp_dim_pix, dim_mic=dim_mic)
    else:
        interp_ext, interp_dim_fact = None, None

    return raw_ext, raw_dim_fact, interp_ext, interp_dim_fact


def ext_calc(dim_pix, dim_mic=None):
    """
    Calculate pixel dimension of a map from its number of pixel

    Parameters
    ----------
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for 'x' and 'y' axis (in microns)

    Returns
    -------
    ext: list(4) of float
        List for axis (x and y) range of the maps for the plotting (in microns)
    dim_fact: dict('x': ,'y':) of float
        Dict of conv factor map dimension for 'x' and 'y' axis
    """
    ext = [-0.5, (dim_pix['x'] - 0.5), -0.5, (dim_pix['y'] - 0.5)]
    dim_fact = {}

    if dim_mic:
        dim_fact['x'] = dim_mic['x'] / (dim_pix['x'] - 1)
        dim_fact['y'] = dim_mic['y'] / (dim_pix['y'] - 1)
        ext = [elem * dim_fact['x'] if cont < 2 else elem * dim_fact['y'] for
               cont, elem in enumerate(ext)]

    dim_fact = dim_fact or None

    return ext, dim_fact


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
