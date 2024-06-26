"""
Module used to generate sspfm maps
    - Formatting of matrix measurement to be plot in sspfm maps
"""

import numpy as np

from PySSPFM.utils.map.interpolate import interp_2d_treated


def formatting_measure(measure, dim_pix, dim_mic=None, dict_interp=None,
                       mask=None):
    """
    Measure formatting to plot the maps

    Parameters
    ----------
    measure: np.array(p) of float
        Array of values for the considered measure
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    dim_mic: dict('x': ,'y':) of float, optional
        Dict of map dimension for x and y axis (in microns)
    dict_interp: dict, optional
        Dict of map interpolation parameters
    mask: list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask (q<p)

    Returns
    -------
    raw_ext: list(4) of float
        List for axis (x and y) range of the maps for the plotting (in microns)
    raw_dim_fact: dict('x': ,'y':) of float
        Dict of conv factor map dimension for x and y axis
    sorted_matrix: numpy.array(m*n) of float
        2D array of measure sorted and shaped in agreement scan size (m*n=p)
    nb_bug: int
        Number of missing pixel in the scan
    interp_ext: list(4) of float
        List axis (x and y) range of the interpolated maps for the plotting (in
        microns)
    interp_dim_fact: dict('x': ,'y':) of float
        Dict of conv factor interpolated map dimension for x and y axis
    cleared_matrix: numpy.array(m*n) of float
        2D array of measure sized and sorted in agreement with scan and
        cleared with missing pixel (nb_bug) or pixed removed with selection
        criterion (mask) (m*n=p)
    filled_matrix: np.array(m*n) of float
        2D array of values with removed value errors with interpolated values
        (m*n=p)
    resol_matrix: np.array(n*i, m*i) of float
        2D array of interpolated values with increased resolution
        (i fact = interp_factor)
    tab_all_index: list(r) or numpy.array(r) of int
        2D array of index sorted and shaped in agreement scan size
    tab_plotted_index: list(s) or numpy.array(s) of int, optional
        Array of index with label plotted on the final image (an index is
        plotted when there is a change of tip travel direction i.e position
        in the limit of the scan) (s<p)
    directions: list(t) or numpy.array(t) of int, optional
        Array of symbol direction plotted on the final image (a symbol is
        plotted when there is a change of tip travel direction i.e position
        in the limit of the scan) (t<p)
    index_blank: numpy.array(u) of int
        Array of value error index to add white square on the map (u<p)
    """
    # Initiate measure: sorted, cleared, and sized 2D matrix in agreement with
    # the scan and plotted element
    (_, _, nb_bug, sorted_matrix, tab_all_index, tab_plotted_index,
     directions) = init_formatting_measure(measure, dim_pix, dim_mic=dim_mic)

    # Dimensions of the maps in pixels
    (raw_ext, raw_dim_fact, interp_ext, interp_dim_fact) = extent(
        dim_pix, dim_mic=dim_mic, dict_interp=dict_interp)

    # Remove the pixels in agreement with the selection criterion and nb_bug
    cleared_matrix = cleared_measure(measure, dim_pix, nb_bug=nb_bug, mask=mask)

    # Index of cleared pixels (missing (nb_bug) or removed (mask)
    # pixels i.e. value errors)
    index_bug_step_2 = [int(tab[0] * dim_pix['x'] + tab[1])
                        for tab in np.argwhere(np.isnan(cleared_matrix))]

    # Interpolate the matrix to fill value errors with interpolated values
    (filled_matrix, resol_matrix) = interp_2d_treated(cleared_matrix,
                                                      dict_interp=dict_interp)

    # Value errors in the filled matrix
    index_bug_step_3 = [int(tab[0] * dim_pix['x'] + tab[1])
                        for tab in np.argwhere(np.isnan(filled_matrix))]

    # Index blank removed in the final image i.e. all error index - error index
    # of filled matrix
    index_blank = list(set(index_bug_step_2) - set(index_bug_step_3))

    return (raw_ext, raw_dim_fact, sorted_matrix, nb_bug, cleared_matrix,
            interp_ext, interp_dim_fact, filled_matrix, resol_matrix,
            index_blank, tab_all_index, tab_plotted_index, directions)


def init_formatting_measure(measure, dim_pix, dim_mic=None):
    """
    Initialize measure formatting for plotting maps.

    Parameters
    ----------
    measure : np.array(p) of float
        Array of values for the considered measure.
    dim_pix : dict('x': int, 'y': int)
        Dict of map dimensions for 'x' and 'y' axes (in pixels).
    dim_mic : dict('x': float, 'y': float), optional
        Dict of map dimensions for 'x' and 'y' axes (in microns).

    Returns
    -------
    raw_ext : list(2) of float
        List for axis (x and y) range of the maps for plotting (in microns).
    raw_dim_fact : dict('x': float, 'y': float)
        Dict of conversion factor for map dimensions for 'x' and 'y' axes.
    nb_bug : int
        Number of missing pixels in the scan.
    sorted_matrix : np.array(m*n) of float
        2D array of measures sorted and shaped in agreement with scan size
        (m*n=p).
    tab_all_index : np.array(r) of int
        2D array of indices sorted and shaped in agreement with scan size.
    tab_plotted_index : np.array(s) of int, optional
        Array of indices with labels plotted on the final image (an index is
        plotted when there is a change of tip travel direction, i.e., position
        in the limit of the scan) (s < p).
    directions : np.array(t) of str, optional
        Array of symbol directions plotted on the final image (a symbol is
        plotted when there is a change of tip travel direction, i.e., position
        in the limit of the scan) (t < p).
    """
    # Calculate the map dimensions in microns
    raw_ext, raw_dim_fact = ext_calc(dim_pix, dim_mic=dim_mic)

    # Find the number of missing pixels in the image
    nb_bug = dim_pix['x'] * dim_pix['y'] - len(measure)

    # Organize the measure in a 2D matrix, sorted and shaped in agreement
    # with the scan size
    sorted_matrix = np.resize(measure, new_shape=(dim_pix['x'], dim_pix['y']))
    try:
        sorted_matrix[-1, -(1 + np.arange(nb_bug))] = np.nan
    except IndexError:
        pass
    sorted_matrix = rearrange_matrix(sorted_matrix)

    # Organize the indices in a 2D matrix, sorted and shaped in agreement with
    # the scan size
    index_matrix = np.resize(np.arange(len(measure)),
                             new_shape=(dim_pix['y'], dim_pix['x']))
    try:
        index_matrix[-1, -(1 + np.arange(nb_bug))] = -1
    except IndexError:
        pass
    rearranged_index_matrix = rearrange_matrix(index_matrix)
    tab_all_index = [elem for sublist in rearranged_index_matrix
                     for elem in sublist]

    # List of plotted indices and directions on the maps
    tab_plotted_index, directions = [], []
    cont = 0
    dir_lr = ['>', '<']
    for i in range(dim_pix['x'] * dim_pix['y']):
        if i % dim_pix['x'] == 0:
            if i > 0:
                tab_plotted_index.append(i - 1)
                directions.append('v')
            ind = cont % 2
            tab_plotted_index.append(i)
            directions.append(dir_lr[ind])
            cont += 1

    tab_plotted_index.append(np.max(tab_all_index))
    directions.append('s')

    return (raw_ext, raw_dim_fact, nb_bug, sorted_matrix, tab_all_index,
            tab_plotted_index, directions)


def rearrange_matrix(matrix):
    """
    Sort the matrix of measurement according to the tip travel on the surface
    sample

    Parameters
    ----------
    matrix: np.array(m*n) of float
        2D array of values (m*n=p)

    Returns
    -------
    rearranged_matrix: np.array(m*n) of float
        2D array of values sorted according to the scan (m*n=p)
    """
    # Flip odd-numbered lines
    mixed_matrix = [line if cont % 2 == 0 else np.flip(line)
                    for cont, line in enumerate(matrix)]

    # Flip the entire matrix along the y-axis
    rearranged_matrix = mixed_matrix[::-1]

    return rearranged_matrix


def cleared_measure(measure, dim_pix, nb_bug=0, mask=None):
    """
    Find 2D array of measure sized and sorted in agreement with scan and
    cleared with missing pixel (nb_bug) or pixels removed with selection
    criterion (mask)

    Parameters
    ----------
    measure: np.array(p) of float
        Array of values for the considered measure
    dim_pix: dict('x': ,'y':) of int
        Dict of map dimension for 'x' and 'y' axis (in pixel)
    nb_bug: int, optional
        Number of missing pixels in the scan (default: 0)
    mask: list(q) or numpy.array(q) of int, optional
        List of index corresponding to the mask (default: None)

    Returns
    -------
    cleared_matrix: np.array(m*n) of float
        2D array of measure sized and sorted in agreement with scan and
        cleared with missing pixel (nb_bug) or pixels removed with selection
        criterion (mask) (m*n=p)
    """
    # Init clear measure array : clear_measure = measure
    clear_measure = measure.copy()

    # Clear the removed pixel in the matrix (mask)
    if mask is not None and len(mask) > 0:
        for cont, _ in enumerate(measure):
            if cont in mask:
                clear_measure[cont] = np.nan

    # Organize the measurements in a 2D matrix
    cleared_matrix = np.resize(clear_measure, new_shape=(dim_pix['y'],
                                                         dim_pix['x']))

    # Clear the missing pixel at the end of the matrix (nb_bug)
    for i in range(nb_bug):
        cleared_matrix[-1][-(1 + i)] = np.nan

    # Organize and sort the matrix in agreement with scan
    cleared_matrix = rearrange_matrix(cleared_matrix)

    return cleared_matrix


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
