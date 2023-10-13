"""
Module used to generate sspfm maps
    - Map interpolation
"""

import numpy as np
from scipy import interpolate, spatial


def remove_val(tab, mask=None, reverse=False):
    """
    Remove values from tab corresponding to indices specified in the mask list

    Parameters
    ----------
    tab: list
        Initial list of values
    mask: list of int, optional
        List of indices to delete from the tab
    reverse: bool, optional
        If True, reverse the mask values

    Returns
    -------
    tab: list
        Final list with values corresponding to the mask indices removed
    """
    tab_out = list(tab)

    if mask is not None:
        if reverse:
            mask = [i for i in range(len(list(tab))) if i not in mask]
        for index in reversed(mask):
            del tab_out[index]

    return tab_out


def interp_2d_treated(matrix, dict_interp=None):
    """
    Interpolate the matrix to fill value errors and increase resolution

    Parameters
    ----------
    matrix: np.array
        2D array of values
    dict_interp: dict, optional
        Dict of map interpolation parameters

    Returns
    -------
    filled_matrix: np.array
        2D array with filled value errors
    resol_matrix: np.array
        2D array with increased resolution
    """
    if dict_interp is None:
        dict_interp = {
            'x fact': 1,
            'y fact': 1,
            'fact': 1,
            'func': 'linear'
        }
    else:
        dict_interp['x fact'] = dict_interp['fact']
        dict_interp['y fact'] = dict_interp['fact']

    # 2D interpolation of the matrix
    filled_matrix, resol_matrix = interp_2d(matrix, dict_interp=dict_interp)

    # Remove value errors of the interpolation located at the sup extremities
    # of 'x' and 'y' axis
    resol_matrix = resol_matrix[
                   :-(dict_interp['fact'] - 1), :-(dict_interp['fact'] - 1)]
    # # dimension of interpolated matrix (in pixel)
    # interp_dim_pix = dict()
    # interp_dim_pix['x'] = (dim_pix['x'] - 1) * dim_fact['x'] + 1
    # interp_dim_pix['y'] = (dim_pix['y'] - 1) * dim_fact['y'] + 1
    # # conversion factor of interpolated matrix (in microns/pixel)
    # interp_fact = dict()
    # interp_fact['x'] = dim_mic['x'] / interp_dim_pix['x']
    # interp_fact['y'] = dim_mic['y'] / interp_dim_pix['y']

    return filled_matrix, resol_matrix


def interp_2d(matrix, dict_interp=None):
    """
    Interpolate the matrix to fill value errors and increase resolution

    Parameters
    ----------
    matrix: np.array
        2D array of values
    dict_interp: dict, optional
        Dict of map interpolation parameters

    Returns
    -------
    filled_matrix: np.array
        2D array with filled value errors
    resol_matrix: np.array
        2D array with increased resolution
    """
    dict_interp = dict_interp or {
        'x fact': 1,
        'y fact': 1,
        'func': 'linear'
    }

    filled_matrix = grid_interp(matrix, interp_func=dict_interp['func'])

    resol_nan_matrix = np.empty(
        (int(np.shape(filled_matrix)[0] * dict_interp['x fact']),
         int(np.shape(filled_matrix)[1] * dict_interp['y fact'])))
    resol_nan_matrix.fill(np.nan)

    for x_coor, line in enumerate(filled_matrix):
        x_coor = int(x_coor * dict_interp['x fact'])
        for y_cont, elem in enumerate(line):
            y_coor = int(y_cont * dict_interp['y fact'])
            resol_nan_matrix[x_coor][y_coor] = elem

    resol_matrix = grid_interp(resol_nan_matrix,
                               interp_func=dict_interp['func'])

    return filled_matrix, resol_matrix


def grid_interp(matrix, interp_func='linear'):
    """
    Perform 2D interpolation

    Parameters
    ----------
    matrix: np.array
        2D array of values
    interp_func: str, optional
        Interpolation function: 'linear' or 'cubic'

    Returns
    -------
    interp_matrix: np.array
        2D array of interpolated values
    """
    assert interp_func in ['linear', 'cubic']

    array = np.ma.masked_invalid(matrix)
    x_axis = np.arange(0, np.shape(matrix)[1])
    y_axis = np.arange(0, np.shape(matrix)[0])
    x_grid, y_grid = np.meshgrid(x_axis, y_axis)
    x1, y1 = x_grid[~array.mask], y_grid[~array.mask]
    new_array = array[~array.mask]
    try:
        interp_matrix = interpolate.griddata(
            (x1, y1), new_array.ravel(), (x_grid, y_grid), method=interp_func)
    except (spatial.qhull.QhullError, ValueError) as err:
        print(f"Error: {err}")
        interp_matrix = np.zeros_like(x_grid)

    return interp_matrix
