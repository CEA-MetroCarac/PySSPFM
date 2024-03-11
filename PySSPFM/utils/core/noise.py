"""
Utilities methods for noise generation and filtering
"""
import numpy as np
from scipy.special import erf
from scipy.optimize import root
from scipy.signal import butter, lfilter


def noise(y, noise_pars, relative=False):
    """
    Add noise to an initial set of data.

    Parameters
    ----------
    y: np.array
        Array of y-axis values.
    noise_pars: dict
        Noise parameters. It should contain the following keys:
        - 'type': Type of noise distribution. Allowed values are
        'uniform', 'normal', and 'laplace'.
        - 'args': Additional arguments required for the chosen noise
        distribution.
    relative: bool, optional
        If True, the noise amplitude is relative to the signal range (in %).

    Returns
    -------
    y_noise: np.array
        Array of y-axis values with noise added.
    """
    list_pars = list(noise_pars.values())
    assert list_pars[0] in ['uniform', 'normal', 'laplace']
    if relative:
        y_range = max(y) - min(y)
        list_pars[1] = y_range * list_pars[1] / 100
    y_noise = eval(list_pars[0])(y, *list_pars[1:])

    return y_noise


def uniform(y, ampli):
    """
    This function add uniform noise to an initial set of data

    Parameters
    ----------
    y: np.array
        Array of y-axis values
    ampli: float
        Amplitude of noise for data

    Returns
    -------
    y_noise: np.array
        Array of y-axis values with noise
    """
    return y + np.array(np.random.uniform(-0.5, 0.5, len(y)) * ampli)


def normal_pdf(x, sigma=1., mu=0.):
    """ Normal probability distribution function """
    e_f = -1 / 2 * ((x - mu) / sigma) ** 2
    coef = 1 / (sigma * np.sqrt(2 * np.pi))
    return coef * np.exp(e_f)


def normal_cdf(x, sigma=1., mu=0.):
    """ Normal cumulative distribution function """
    return 1 / 2 * (1 + erf((x - mu) / (sigma * np.sqrt(2))))


def normal(y, ampli, sigma=1, cdf=0.99):
    """
    Add normal noise to an initial set of data.

    Parameters
    ----------
    y: np.array
        Array of y-axis values.
    ampli: int
        Level of noise for data (in %).
    sigma: float, optional
        Standard deviation (spread or "width") of the distribution.
        Default is 1.
    cdf: float, optional
        Proportion of density of probability function in ampli range.
        Default is 0.99.

    Returns
    -------
    y_noise: np.array
        Array of y-axis values with noise.
    """
    assert 0 < cdf < 1

    # Function to find root of
    def fun(x):
        return normal_cdf(x, sigma=sigma) - cdf

    # Find the root of the function using optimization
    root_val = root(fun, x0=np.array([0])).x

    # Adjust the ampli based on the root value
    ampli /= 2 * root_val[0]

    # Generate the normal noise based on the adjusted ampli
    y_variation = np.random.normal(0, sigma, len(y)) * ampli

    # Add the noise to the original data
    y_noise = y + np.array(y_variation)

    return y_noise


def laplace_pdf(x, lbda=1., mu=0.):
    """ Laplace's probability distribution function """
    return lbda / 2 * np.exp(-lbda * abs(x - mu))


def laplace_cdf(x, lbda=1., mu=0.):
    """ Laplace cumulative distribution function """
    return 1 / 2 + 1 / 2 * np.sign(x - mu) * (1 - np.exp(-lbda * (abs(x - mu))))


def laplace(y, ampli, lbda=1, cdf=0.99):
    """
    Add Laplace noise to an initial set of data.

    Parameters
    ----------
    y: np.array
        Array of y-axis values.
    ampli: int
        Level of noise for data (in %).
    lbda: float, optional
        Spread of the distribution. Default is 1.
    cdf: float, optional
        Proportion of density of probability function in ampli range.
        Default is 0.99.

    Returns
    -------
    y_noise: np.array
        Array of y-axis values with noise.
    """
    assert 0 < cdf < 1

    # Function to find root of
    def fun(x):
        return laplace_cdf(x, lbda=lbda) - cdf

    # Find the root of the function using optimization
    root_val = root(fun, x0=np.array([0])).x

    # Adjust the ampli based on the root value
    ampli /= 2 * root_val[0]

    # Generate the Laplace noise based on the adjusted ampli
    y_variation = np.random.laplace(0, lbda, len(y)) * ampli

    # Add the noise to the original data
    y_noise = y + np.array(y_variation)

    return y_noise


def filter_mean(signal, window_size):
    """
    Apply a mean filter to a signal.

    Parameters
    ----------
    signal : np.ndarray
        Input signal.
    window_size : int
        Size of the moving window for the mean filter.

    Returns
    -------
    filtered_signal : np.ndarray
        Filtered signal.
    """
    window = np.ones(window_size) / window_size
    filtered_signal = np.convolve(signal, window, mode='same')

    return filtered_signal


def butter_filter(signal, sampling_frequency, cutoff_frequency,
                  filter_type="low", filter_order=1):
    """
    Apply a Butterworth filter to the input signal.

    Parameters
    ----------
    signal : np.ndarray
        Input signal.
    sampling_frequency : float
        Sampling frequency of the input signal.
    cutoff_frequency : float or tuple
        Cutoff frequency or frequencies of the filter.
    filter_type : str
        Type of the filter ('low', 'high', 'bandpass', or 'bandstop').
        Default is "low".
    filter_order : int, optional
        Order of the filter. Default is 1.

    Returns
    -------
    filtered_signal : array-like
        Filtered signal.
    """
    # Frequency normalization
    nyquist = 0.5 * sampling_frequency

    # Calcul of filter coefficients
    if filter_type in ('low', 'high'):
        normal_cutoff = cutoff_frequency / nyquist
        coef_b, coef_a = butter(filter_order, normal_cutoff,
                                btype=filter_type, analog=False)[:2]
    elif filter_type in ('bandpass', 'bandstop'):
        normal_cutoff = np.array(cutoff_frequency) / nyquist
        coef_b, coef_a = butter(filter_order, normal_cutoff,
                                btype=filter_type, analog=False)[:2]
    else:
        raise ValueError("Invalid filter type. Use 'low', 'high', "
                         "'bandpass', or 'bandstop'.")

    # Applying the filter to the signal
    filtered_signal = lfilter(coef_b, coef_a, signal)

    return filtered_signal
