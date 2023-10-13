"""
Tools for iterable
"""

import numpy as np


def arg_cond(arr, min_val=None, max_val=None, reverse=False):
    """
    Return index fill condition

    Parameters
    ----------
    arr: numpy.array(n*m*...)
        Initial array
    min_val: float, optional
        Minimum value for array values
    max_val: float, optional
        Maximum value for array values
    reverse: bool, optional
        Revert the initial condition

    Returns
    -------
    ind: numpy.array(p*q*...)
        Array of index of arr that fill the condition
    """
    mask = arr
    if min_val is not None:
        mask = np.where(mask >= min_val, mask, np.nan)
    if max_val is not None:
        mask = np.where(mask <= max_val, mask, np.nan)
    ind = np.argwhere(np.isnan(mask) == reverse)

    return ind


def sort_2d_arr(arr_2d, mode='line', index=0, reverse=False):
    """
    Sort 2D array values by taking a specific line or column as reference.

    Parameters
    ----------
    arr_2d: numpy.array(n*m) or list(n*m)
        2D array.
    mode: str, optional
        Sorting mode. 'line' or 'column' (default: 'line').
    index: int, optional
        Index of the considered line or column (default: 0).
    reverse: bool, optional
        If True, the 2D array is sorted in descending order (default: False).

    Returns
    -------
    sorted_arr_2d: list(n*m)
        Sorted 2D list.
    """
    if mode == 'line':
        # Sort by line
        ref = list(arr_2d[index])
        indexs = sorted(range(len(ref)), key=ref.__getitem__, reverse=reverse)
        sorted_arr_2d = zip(*[[val[elem] for val in arr_2d] for elem in indexs])
        sorted_arr_2d = [list(elem) for elem in sorted_arr_2d]
    elif mode == 'column':
        # Sort by column
        ref = [val[index] for val in arr_2d]
        indexs = sorted(range(len(ref)), key=ref.__getitem__, reverse=reverse)
        sorted_arr_2d = arr_2d[indexs]
    else:
        raise IOError('mode in [\'line\',\'column\']')

    return sorted_arr_2d
