"""
Examples of iterable functions
"""

import numpy as np

from PySSPFM.utils.core.iterable import arg_cond, sort_2d_arr


def ex_iterable(verbose=False):
    """
    Example of iterable functions.

    Parameters
    ----------
    verbose: bool, optional
        If True, print the results.

    Returns
    -------
    ind_cond_1: numpy.array
        Array of indices satisfying the condition for arr.
    ind_cond_2: numpy.array
        Array of indices satisfying the condition for arr_2d.
    sort_tab_l0: list
        Sorted 2d list by line 0.
    sort_tab_c2: list
        Sorted 2d list by column 2 in descending order.
    """
    tab = [4, -12, -5, 8, 9, 14, -12, 6, 3, 14, 8]
    arr = np.array(tab)
    tab_2d = [[1, 8, 9], [-8, 6, 7], [10, 6, 11]]
    arr_2d = np.array(tab_2d)

    # ex arg_cond
    ind_cond_1 = arg_cond(arr, min_val=5, max_val=10)
    ind_cond_2 = arg_cond(arr_2d, min_val=5, max_val=10)

    # ex sort_2d_arr
    sort_tab_l0 = sort_2d_arr(np.array(tab_2d), mode='line', index=0)
    sort_tab_c2 = sort_2d_arr(np.array(tab_2d), mode='column', index=2,
                              reverse=True)

    if verbose:
        print('# ex arg_cond')
        print(ind_cond_1)
        print(ind_cond_2)
        print('\n')
        print('# ex sort_2d_arr')
        print(sort_tab_l0)
        print(sort_tab_c2)
        print('\n')

    return ind_cond_1, ind_cond_2, sort_tab_l0, sort_tab_c2


if __name__ == '__main__':
    ex_iterable(verbose=True)
