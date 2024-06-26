"""
Peak treatment module
"""

import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import simpson
from scipy.stats import linregress

from PySSPFM.utils.core.iterable import sort_2d_arr


def detect_peak(x, y, sens_coef=1.5):
    """
    Perform a peak detection on set of y values

    Parameters
    ----------
    x: list(n) or numpy.array(n) of float
        Array of x values
    y: list(n) or numpy.array(n) of float
        Array of y values
    sens_coef: float, optional
        Sensitivity of the peak detection (>1)

    Returns
    -------
    test: bool
        True if a peak is detected, False if not.
    """
    # Find peak in the histogram
    dist_min = int(len(x) / 5)
    width_min = int(len(x) / 100)
    res = find_main_peaks(x, y, nb_peak=1, dist_min=dist_min,
                          width_min=width_min)

    if len(res['peaks']) < 1:
        return False
    else:
        # Background determination
        bckgnd = guess_bckgnd(y)

        # Variance condition
        total_inc = np.sqrt(np.var(y))
        test_var = bool(y[res['peaks']][0] - bckgnd > 2 * total_inc)

        # Mean condition
        threshold = sens_coef * (np.mean(y) - bckgnd) * sens_coef
        test_mean = bool(y[res['peaks']][0] - bckgnd > threshold)

        test = bool(test_var is True and test_mean is True)

        return test


def find_main_peaks(x, y, nb_peak=2, dist_min=None, width_min=None,
                    make_plots=False, ax=None):
    """
    Find and calculate two main histogram peaks parameters

    Parameters
    ----------
    x: list(n) or numpy.array(n) of float
        Array of x values for histogram (in °)
    y: list(n) or numpy.array(n) of float
        Array of y values for histogram: count
    nb_peak: int, optional
        Number of main peaks returned
    dist_min: int, optional
        Minimum domain in 'x' axis for peak detection (in number of point)
    width_min: int, optional
        Minimum width of peak in 'x' axis for peak detection
        (in number of point)
    make_plots: bool, optional
        Activation key for matplotlib figures generation
    ax: plt.axes, optional
        Axes of the figure

    Returns
    -------
    res: dict
        Dict of two main histogram peaks parameters
    """
    assert nb_peak > 0

    # Find peaks in the histogram
    peaks, _ = find_peaks(y, height=np.mean(y), distance=dist_min,
                          width=width_min)

    # Compute the considered part of the peak (threshold = phase mean)
    wid_left, wid_right, left_limit, right_limit = [], [], [], []
    for peak in peaks:
        width_res = width_peak(x, y, peak, float(np.mean(y)))
        left_limit.append(width_res['ind left'])
        wid_left.append(x[peak - width_res['ind left']])
        right_limit.append(width_res['ind right'])
        wid_right.append(x[width_res['ind right'] - peak])

    # Suppress peaks in the same area
    iteration, error = len(peaks) - 1, 0
    for i in range(iteration):
        if right_limit[i - error] == right_limit[i + 1 - error]:
            if left_limit[i - error] == left_limit[i + 1 - error]:
                add_ite = 0
                if y[peaks[i - error]] >= y[peaks[i + 1 - error]]:
                    add_ite = 1
                peaks = np.delete(peaks, i + add_ite - error)
                for elem in [left_limit, right_limit, wid_left, wid_right]:
                    elem.pop(i + add_ite - error)
                error += 1

    # Suppress peaks with too close area
    iteration, error = len(peaks) - 1, 0
    for i in range(iteration):
        if right_limit[i - error] > left_limit[i + 1 - error]:
            add_ite = 0
            if y[peaks[i - error]] >= y[peaks[i + 1 - error]]:
                add_ite = 1
            peaks = np.delete(peaks, i + add_ite - error)
            for elem in [left_limit, right_limit, wid_left, wid_right]:
                elem.pop(i + add_ite - error)
            error += 1

    # Compute the peak integrals
    integs = []
    for peak, elem_left, elem_right in zip(peaks, left_limit, right_limit):
        integ = simpson(y[elem_left:elem_right], x=x[elem_left:elem_right])
        integs.append(integ)
        if make_plots:
            ax.plot(x[peak], y[peak], 'rx', ms=10)
            ax.axvline(x=x[elem_left], c='r', ls='--')
            ax.axvline(x=x[elem_right], c='r', ls='--')

    # The two peaks with the largest integral are considered
    arr_2d = np.array([integs, range(len(integs))])
    sorted_arr_2d = sort_2d_arr(arr_2d, 'line', 0, reverse=True)
    main_index = [int(elem) for elem in sorted_arr_2d[1][:nb_peak]]
    main_peaks = [peaks[index] for index in main_index]
    x_offset, y_offset = (max(x) - min(x)) / 10, max(y) / 10

    return {'peaks': peaks,
            'main': main_index,
            'main peaks': main_peaks,
            'lim': [left_limit, right_limit],
            'offset': [x_offset, y_offset]}


def plot_main_peaks(ax, x, y, res):
    """
    Plot main peaks on a given axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to plot on.
    x : array-like
        X-axis data.
    y : array-like
        Y-axis data.
    res : dict
        Result dictionary containing peak information.

    Returns
    -------
    None
    """
    for index, peak in zip(res['main'], res['main peaks']):
        ax.plot(x[peak], y[peak], 'go', ms=10)
        ax.axvline(x=x[res["lim"][0][index]], c='g', ls='--')
        ax.axvline(x=x[res["lim"][1][index]], c='g', ls='--')
        ax.annotate(f'{x[peak]:.1f}',
                    xy=(x[peak], y[peak]),
                    xytext=(x[peak] + res["offset"][0],
                            y[peak] - res["offset"][1]),
                    c='g', size=15,
                    arrowprops={'facecolor': 'green'}, weight='heavy')
    ax.axhline(y=float(np.mean(y)), c='k', ls=':',
               label='amplitude mean : threshold of peak detection')


def width_peak(x_val, y_val, index_cent, threshold):
    """
    Guess width of a peak

    Parameters
    ----------
    x_val: list(n) or numpy.array(n) of float
        Array of x-axis values
    y_val: list(n) or numpy.array(n) of float
        Array of y-axis values
    index_cent: int
        Index of the peak center
    threshold: float
        Threshold for width determination

    Returns
    -------
    res_width: dict
        Dict of width and right and left x corresponding coordinates
    """
    assert index_cent >= 0
    assert index_cent < len(x_val)

    def condition(y, val):
        return y <= val

    # Calculate the left index where the condition is satisfied
    bool_arr = condition(y_val[:index_cent], threshold)
    try:
        index_left = np.where(bool_arr)[0][-1]
    except IndexError:
        index_left = 0

    # Calculate the right index where the condition is satisfied
    bool_arr = condition(y_val[index_cent:], threshold)
    try:
        index_right = index_cent + np.where(bool_arr)[0][0]
    except IndexError:
        index_right = len(x_val) - 1

    width = x_val[index_right] - x_val[index_left]

    return {'width': width,
            'ind right': index_right,
            'ind left': index_left}


def guess_bckgnd(y_val, x_bckgnd=10):
    """
    Guess constant background component of a peak

    Parameters
    ----------
    y_val: list(n) or numpy.array(n) of float
        Array of y-axis values
    x_bckgnd: int, optional
        First and last x-axis percent used to guess the background

    Returns
    -------
    bckgnd: float
        Constant background value guessed
    """
    assert 0 <= x_bckgnd <= 100
    coef = int(x_bckgnd / 100 * len(y_val))
    y_val_bckgnd = np.concatenate([y_val[:coef], y_val[-coef:]])
    bckgnd = \
        np.mean(np.concatenate([y_val_bckgnd[:coef], y_val_bckgnd[-coef:]]))

    return bckgnd


def guess_affine(x_val, y_val, x_bckgnd=10):
    """
    Guess affine background component of a peak

    Parameters
    ----------
    x_val: list(n) or numpy.array(n) of float
        Array of x-axis values
    y_val: list(n) or numpy.array(n) of float
        Array of y-axis values
    x_bckgnd: int, optional
        First and last x-axis percent used to guess the background

    Returns
    -------
    a: float
        Coefficient a (order 1) of affine background component: y=ax+b.
    b: float
        Coefficient b (order 0) of affine background component: y=ax+b.
    """
    assert 0 <= x_bckgnd <= 100
    coef = int(x_bckgnd / 100 * len(x_val))
    x_val_bckgnd = np.concatenate([x_val[:coef], x_val[-coef:]])
    y_val_bckgnd = np.concatenate([y_val[:coef], y_val[-coef:]])
    bckgnd_res = linregress(x_val_bckgnd, y_val_bckgnd)

    return bckgnd_res[0], bckgnd_res[1]
