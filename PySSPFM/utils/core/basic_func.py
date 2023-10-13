"""
Module containing different basic functions (sigmoids, sinusoids, ...)
"""

import numpy as np


def linear(x, offset, slope, der=0):
    r"""
    Return Linear function defined as: :math:`offset + slope * x`
    or related derivatives (der=0, 1, 2,..)
    """
    if der == 0:
        return offset + slope * x
    elif der == 1:
        return slope * np.ones_like(x)
    else:
        return np.zeros_like(x)


def sigmoid(x, ampli, coef, x0, is_centered=True, der=0):
    r"""
    Return Sigmoid function defined as:
    :math:`\frac{ampli}{1 + e^{-coef * (x - x0)}} - 0.5 * ampli` (if centered)
    or related derivatives (der=0, 1, 2)
    """

    exp = np.exp(-coef * (x - x0))
    if der == 0:
        return ampli / (1. + exp) - 0.5 * ampli * is_centered
    elif der == 1:
        # from https://www.wolframalpha.com/:input?i=d%2Fdx+a+%2F+%281+%2B
        # +exp%28-b%28x-c%29%29%29+-a+*+0.5
        return ampli * coef * exp / (1. + exp) ** 2
    elif der == 2:
        # from https://www.wolframalpha.com/ :
        # input?i=d2%2Fdx+a+%2F+%281+%2B+exp%28-b%28x-c%29%29%29+-a+*+0.5
        return 2. * ampli * (coef * exp) ** 2 / (1. + exp) ** 3 - \
               ampli * coef ** 2 * exp / (1. + exp) ** 2
    else:
        raise NotImplementedError("'der' should be in [0, 1, 2]")


def arctan(x, ampli, coef, x0, der=0):
    r"""
    Return Arctan function defined as: :math:`ampli * atan(-coef * (x-x0))`
    or related derivatives (der=0, 1, 2)
    """
    if der == 0:
        return ampli * np.arctan(coef * (x - x0))
    elif der == 1:
        return ampli * coef / (1 + coef ** 2 * (x - x0) ** 2)
    elif der == 2:
        return -2 * ampli * coef ** 3 * (x - x0) / \
               (1 + coef ** 2 * (x - x0) ** 2) ** 2
    else:
        raise NotImplementedError("'der' should be in [0, 1, 2]")


def gaussian(x, ampli, fwhm, x0, der=0):
    r"""
    Return Gaussian function defined as:
    :math:`ampli * e^{-(x-x0)^2/(2*\sigma^2)}`
    with :math:`\sigma = fwhm / (2*\sqrt{2*log(2)})`
    or related derivatives (der=0, 1, 2)
    https://www.wolframalpha.com/input?i=d%2Fdx2+a*exp%28-c+*+%28x-x0%29**2%29
    """
    sigma = fwhm / (2. * np.sqrt(2. * np.log(2.)))
    coef = 1. / (2 * sigma ** 2)
    exp = np.exp(-coef * (x - x0) ** 2)
    if der == 0:
        return ampli * exp
    elif der == 1:
        return - 2 * ampli * coef * (x - x0) * exp
    elif der == 2:
        return 2 * ampli * coef * (2 * coef * (x - x0) ** 2 - 1) * exp
    else:
        raise NotImplementedError("'der' should be in [0, 1, 2]")


def lorentzian(x, ampli, fwhm, x0, der=0):
    r"""
    Return Lorentzian function defined as:
    :math:`ampli * \frac{fwhm^2}{4 * ((x - x0)^2 + fwhm^2 / 4)}`
    or related derivatives (der=0, 1, 2)
    der from https://www.derivative-calculator.net/
    """
    num = fwhm ** 2
    denom = 4 * ((x - x0) ** 2 + fwhm ** 2 / 4)
    if der == 0:
        return ampli * num / denom
    elif der == 1:
        return - 8 * lorentzian(x, ampli, fwhm, x0) * (x - x0) / denom
    elif der == 2:
        lorentz_1 = lorentzian(x, ampli, fwhm, x0, der=1)
        return -16 * lorentz_1 * (x - x0) / denom + lorentz_1 / (x - x0)
    else:
        raise NotImplementedError("'der' should be in [0, 1, 2]")


def pseudovoigt(x, ampli, fwhm, x0, alpha=0.5, der=0):
    r"""
    Return Pseudovoigt function defined as:
    :math:`alpha * Gaussian + (1 - alpha) * Lorentzian`
    or related derivatives (der=0, 1, 2)
    """
    return alpha * gaussian(x, ampli, fwhm, x0, der=der) + \
        (1 - alpha) * lorentzian(x, ampli, fwhm, x0, der=der)


def sho(x, ampli, coef, x0, der=0):
    r"""
    Return Simple Harmonic Oscillator peak resonance function defined as:
    :math:`ampli * \frac{x0^2}{\sqrt{(x0^2 - x^2)^2 + ((x * x0 / coef)^2)}}`
    or related derivatives (der=0, 1, 2)
    from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8291420/
    der from https://www.derivative-calculator.net/
    """
    num = x0 ** 2
    denom = (x0 ** 2 - x ** 2) ** 2 + ((x * x0 / coef) ** 2)
    if der == 0:
        return ampli * num / np.sqrt(denom)
    elif der == 1:
        num_1 = 2 * x0 ** 2 * x / (coef ** 2) - 4 * x * (x0 ** 2 - x ** 2)
        return - ampli * num * num_1 / (2 * denom ** (3 / 2))
    elif der == 2:
        num_1 = 2 * x0 ** 2 / (coef ** 2) - 4 * x * (x0 ** 2 - x ** 2)
        num_2 = 2 * x0 ** 2 * x / (coef ** 2) - 4 * (x0 ** 2 - x ** 2)
        num_2 += 8 * x ** 2
        term_1 = 3 * ampli * num * num_1 ** 2 / (4 * denom ** (5 / 2))
        term_2 = - ampli * num * num_2 / (2 * denom ** (3 / 2))
        return term_1 + term_2
    else:
        raise NotImplementedError("'der' should be in [0, 1, 2]")


def sho_phase(x, ampli, coef, x0, der=0):
    r"""
    Return Simple Harmonic Oscillator phase resonance function
    defined with non-standard atan (:code:`numpy.arctan2`) as:
    :math:`ampli * arctan2(\frac{x * x0}{coef * (x0^2 - x^2)})`
    or related derivatives (der=0, 1, 2)
    from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8291420/
    der from https://www.derivative-calculator.net/
    """
    num = x * x0
    denom = coef * (x0 ** 2 - x ** 2)
    denom_1 = coef ** 2 * (x ** 4 + x0 ** 4) + \
        (1 - 2 * coef ** 2) * (x * x0) ** 2
    if der == 0:
        return ampli * np.arctan2(num, denom)
    elif der == 1:
        num_1 = coef * x0 * (x ** 2 + x0 ** 2)
        return ampli * num_1 / denom_1
    elif der == 2:
        num_2 = - 2 * coef * x0 * x * (coef ** 2 * x ** 4 +
                                       2 * (coef * x * x0) ** 2 +
                                       (1 - 3 * coef ** 2) * x0 ** 4)
        return ampli * num_2 / denom_1 ** 2
    else:
        raise NotImplementedError("'der' should be in [0, 1, 2]")


def sho_phase_switch(x, ampli, coef, x0, der=0):
    r"""
    Return Simple Harmonic Oscillator phase (with switch) resonance function
    defined as: :math:`ampli * atan(\frac{x * x0}{coef * (x0^2 - x^2)})`
    or related derivatives (der=0, 1, 2)
    from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8291420/
    der from https://www.derivative-calculator.net/
    """
    num = x * x0
    denom = coef * (x0 ** 2 - x ** 2)
    if der == 0:
        return ampli * np.arctan(num / denom)
    elif der == 1:
        return sho_phase(x, ampli, coef, x0, der=1)
    elif der == 2:
        return sho_phase(x, ampli, coef, x0, der=2)
    else:
        raise NotImplementedError("'der' should be in [0, 1, 2]")


def sho_complex(x, x0, coef_q, y0, z0):
    """
    Return Simple Harmonic Oscillator complex (with switch) resonance func
    or related derivatives (der=0, 1, 2)
    """
    num_y = - y0 * x0 ** 2 * np.exp(z0 * 1j)
    denom_y = x ** 2 - (x * x0 * 1j / coef_q) - x0 ** 2

    return num_y / denom_y
