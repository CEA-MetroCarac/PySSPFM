"""
Generic module with functions used for signal treatment and measurement
"""

import numpy as np
from scipy.stats import t, linregress
from scipy.interpolate import InterpolatedUnivariateSpline, interp1d


def line_reg(x_meas, y_meas, n_sample=10):
    """
    Perform a linear regression on a set of data

    Parameters
    ----------
    x_meas: list(n) or numpy.array(n) of float
        Array of x value
    y_meas: list(n) or numpy.array(n) of float
        Array of y value
    n_sample: int, optional
        Discretization for fit result

    Returns
    -------
    results: dict
        Dict of result(fit coefs, uncertainty, R², x and y fit tab)
    """
    assert len(list(x_meas)) == len(list(y_meas))
    # Line regression
    res = linregress(x_meas, y_meas)
    coefs = [res[0], res[1]]
    r_2 = np.square(res[2])
    # Fit function
    x_fit = np.linspace(min(x_meas), max(x_meas), n_sample)
    y_fit = np.polyval(coefs, x_fit)
    # Uncertainty of the slope value
    int_conf = 0.05
    t_inv = abs(t.ppf(int_conf / 2, len(x_meas) - 2))
    unc_a = t_inv * res[4]
    return {'coefs': coefs,
            'unc a': unc_a,
            'r**2': r_2,
            'x fit': x_fit,
            'y fit': y_fit}


def interpolate(x_meas, y_meas, discret, interp_type='default'):
    """
    Perform interpolation.

    Parameters
    ----------
    x_meas: list(n) or numpy.array(n)
        Array of x values.
    y_meas: list(n) or numpy.array(n)
        Array of y values.
    discret: int
        Discretization factor for interpolation.
    interp_type: str, optional
        Type of interpolation:
        - 'default'
        - 'linear'
        - 'quadratic'
        - 'cubic' (default: 'default').

    Returns
    -------
    result: dict
        Dictionary containing the interpolated x and y values, and the
        interpolation function.
    """
    assert len(x_meas) == len(
        y_meas), "Length of x_meas and y_meas must be equal."

    # x interpolation array
    x_interp = np.linspace(min(x_meas), max(x_meas), len(x_meas) * discret)

    # Interpolation
    if interp_type == 'default':
        interp_func = InterpolatedUnivariateSpline(x_meas, y_meas)
    elif interp_type in ['linear', 'quadratic', 'cubic']:
        interp_func = interp1d(x_meas, y_meas, kind=interp_type)
    else:
        raise ValueError(
            'Invalid interp_type. It should be one of: \'default\', '
            '\'linear\', \'quadratic\', \'cubic\'.')

    # y interpolated values
    y_interp = interp_func(x_interp)

    return {'x interp': x_interp,
            'y interp': y_interp,
            'interp func': interp_func}
