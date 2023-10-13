"""
Functions and class in order to perform fitting
"""

import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model, Parameters, minimize, report_fit
from PySSPFM.utils.core.basic_func import \
    linear, gaussian, sho, sho_phase, sho_phase_switch
from PySSPFM.utils.core.peak import width_peak

from PySSPFM.settings import FIT_METHOD


class CurveFit:
    """ CurveFit object """

    def __init__(self, model):
        """ Main function of the class """
        self.model = Model(linear, independent_vars=['x', 'der']) + model
        self.params = None
        self.result = None

    def init_parameters(self, x_val, y_val):
        """
        Initialize fit parameters with initial guesses.

        Parameters
        ----------
        x_val : array-like
            x-values of the data.
        y_val : array-like
            y-values of the data.

        Returns
        -------
        None
        """
        raise NotImplementedError("Subclasses must implement init_parameters.")

    def fit(self, x_val, y_val, init_pars=None):
        """
        Perform curve fitting using the defined model.

        Parameters
        ----------
        x_val : array-like
            The x-values of the data.
        y_val : array-like
            The y-values of the data.
        init_pars: dict of dict, optional
            Initial guesses for the fit parameters

        Returns
        -------
        None
        """
        if init_pars is None:
            self.init_parameters(x_val, y_val)
        else:
            self.params = Parameters()
            for param_name, param_settings in init_pars.items():
                self.params.add(param_name, **param_settings)

        def objective(params):
            return y_val - self.model.eval(params, x=x_val)

        # Perform the minimization
        self.result = minimize(
            objective, self.params, args=(), method=FIT_METHOD)

    def eval(self, x_val):
        """
        Evaluate the fitted peak at given x-values.

        Parameters
        ----------
        x_val : array-like
            x-values at which to evaluate the peak.

        Returns
        -------
        y_fit_val : array-like
            y-values of the fitted peak at the specified x-values.
        """
        if self.result is None:
            raise ValueError("Fit has not been performed. Call fit() first.")

        return self.model.eval(self.result.params, x=x_val)

    def report_fit_results(self, verbose=False):
        """
        Print and return the fit results.

        Returns
        -------
        result_params: lmfit.Parameters
            The parameters of the fit result.
        """
        if self.result is None:
            raise ValueError("Fit has not been performed. Call fit() first.")
        if verbose:
            report_fit(self.result,)
        return self.result.params

    def plot(self, x_val, y_val, ax=None):
        """
        Plot the original data and the fitted curve.

        Parameters
        ----------
        x_val : array-like
            The x-values of the data.
        y_val : array-like
            The y-values of the data.
        ax: matplotlib.Axes, optional
            Axis associated with the plot display
        """
        if self.result is None:
            raise ValueError("Fit has not been performed. Call fit() first.")

        model = self.model
        result = self.result

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None

        ax.scatter(x_val, y_val, label='Original Data', color='blue', alpha=0.5)
        y_fit = model.eval(result.params, x=x_val)
        plt.plot(x_val, y_fit, label='Fitted Curve', color='red')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()

        return fig


class GaussianPeakFit(CurveFit):
    """ GaussianPeakFit object """

    def __init__(self):
        model = Model(gaussian, independent_vars=['x', 'der'])
        super().__init__(model)

    def init_parameters(self, x_val, y_val):
        # Implementation specific to Gaussian peak fitting
        # Guess and define parameters
        guess_width = width_peak(x_val, y_val, np.argmax(y_val),
                                 (max(y_val) - min(y_val) / 2) + min(y_val))
        self.params = Parameters()
        self.params.add(
            "ampli", value=max(y_val) - min(y_val), vary=True,
            min=0, max=2 * (max(y_val) - min(y_val)))
        self.params.add(
            "fwhm", value=guess_width['width'], vary=True,
            min=0, max=max(x_val) - min(x_val))
        self.params.add(
            "x0", value=x_val[np.argmax(y_val)], vary=True,
            min=min(x_val), max=max(x_val))
        self.params.add(
            "offset", value=min(y_val), vary=True, min=0, max=max(y_val))
        self.params.add("slope", value=0.0, vary=False, min=None, max=None)


class ShoPeakFit(CurveFit):
    """ ShoPeakFit object """

    def __init__(self):
        model = Model(sho, independent_vars=['x', 'der'])
        super().__init__(model)

    def init_parameters(self, x_val, y_val):
        # Implementation specific to Sho peak fitting
        # Guess and define parameters
        guess_width = width_peak(
            x_val, y_val, np.argmax(y_val),
            (max(y_val) - min(y_val)) / np.sqrt(2) + min(y_val))
        q_fact = x_val[np.argmax(y_val)] / guess_width['width']
        self.params = Parameters()
        self.params.add(
            "ampli", value=(max(y_val) - min(y_val)) / q_fact, vary=True,
            min=0, max=2 * (max(y_val) - min(y_val)) / q_fact)
        self.params.add(
            "coef", q_fact, vary=True,
            min=min(x_val) / (max(x_val) - min(x_val)), max=None)
        self.params.add(
            "x0", value=x_val[np.argmax(y_val)], vary=True,
            min=min(x_val), max=max(x_val))
        self.params.add(
            "offset", value=min(y_val), vary=True, min=0, max=max(y_val))
        self.params.add("slope", value=0.0, vary=False, min=None, max=None)


class ShoPhaseFit(CurveFit):
    """ ShoPhaseFit object """

    def __init__(self, switch=False):
        if switch:
            model = Model(sho_phase_switch, independent_vars=['x', 'der'])
        else:
            model = Model(sho_phase, independent_vars=['x', 'der'])
        super().__init__(model)
        self.switch = switch

    def init_parameters(self, x_val, y_val):
        # Implementation specific to ShoPhase fitting
        self.params = Parameters()
        self.params.add(
            "ampli", value=(max(y_val) - min(y_val)) / np.pi, vary=True,
            min=0, max=2 * (max(y_val) - min(y_val)) / np.pi)
        self.params.add(
            "coef",
            value=4 * np.mean([max(x_val), min(x_val)])/(max(x_val)-min(x_val)),
            vary=True,
            min=min(x_val) / (max(x_val) - min(x_val)), max=None)
        guess_x0 = x_val[np.argmax(y_val)] \
            if self.switch else (max(x_val) - min(x_val)) / 2
        self.params.add(
            "x0", value=guess_x0, vary=True, min=min(x_val), max=max(x_val))
        guess_offset = np.mean(y_val) if self.switch else min(y_val)
        self.params.add(
            "offset", value=guess_offset, vary=True,
            min=min(y_val), max=max(y_val))
        self.params.add("slope", value=0.0, vary=False, min=None, max=None)
