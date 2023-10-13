"""
module dedicated to hysteresis
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root
from lmfit import Model, Parameters, minimize, report_fit
from sklearn.metrics import r2_score

from PySSPFM.utils.core.basic_func import \
    linear, sigmoid, arctan # pylint:disable=W0611


class Hysteresis:
    """
    Class dedicated to hysteresis made of n branches (n>=1)

    Attributes
    ----------
    nbranches: int
        Number of branches (sigmoids, arctans) to consider in the hysteresis
    asymmetric: bool, optional
        Activation keyword to deal with asymmetric hysteresis
    model_name: str, optional
        Model name associated to the branch: 'sigmoid' or 'arctan'
    model: lmfit.CompositeModel
        Hysteresis composite model that consists in linear + (sigmoid or arctan)
        functions
    params: lmfit.Parameters
        Dictionary of parameters associated to the model where keys are:
        ('offset', 'slope','ampli_0', 'ampli_1', ... 'ampli_{nbranches-1}',
        'coef_0', 'coef_1', ... 'coef_{nbranches-1}', 'x0_0', 'x0_1', ...
         'x0_{nbranches-1}')
    props: dict
        Properties associated to the centered fitted hysteresis

    Parameters
    ----------
    nbranches: int, optional
        Number of branches (sigmoids, arctans) to consider in the hysteresis
    asymmetric: bool, optional
        Activation keyword to deal with asymmetric hysteresis
    model: str, optional
        Model name associated to the branch: 'sigmoid' or 'arctan'
    offset, slope: floats, optional
        Parameters associated to the linear model.
        Default values are 0.
    ampli: float or iterable of nbranches-floats, optional
        Parameter associated to the sigmoid or arctan model.
        Default value is (1,)*nbranches.
    coef: float or iterable of nbranches-floats, optional
        Parameter associated to the sigmoid or arctan model.
        Default value is (1,)*nbranches.
    x0: float or iterable of nbranches-floats, optional
        Parameter associated to the sigmoid or arctan model.
        Defaut value is (0,)*nbranches.
    """

    def __init__(self, nbranches=2, asymmetric=False, model='sigmoid',
                 offset=None, slope=None, ampli=None, coef=None, x0=None):

        model_valid = ['sigmoid', 'arctan']
        assert model in model_valid, f"'model' should be in {model_valid}"

        self.nbranches = nbranches
        self.asymmetric = asymmetric
        self.model_name = model
        self.model = Model(linear, independent_vars=['x', 'der'])
        self.model += Model(eval(model), independent_vars=['x', 'der'])
        self.params = None
        self.props = None

        self.init_params(offset=offset, slope=slope,
                         ampli=ampli, coef=coef, x0=x0)

    def init_params(self, offset=None, slope=None,
                    ampli=None, coef=None, x0=None):
        """ Initialize 'params' """

        ampli = ampli or 1.
        coef = coef or 1.
        x0 = x0 or 0.
        if isinstance(ampli, float):
            ampli = (ampli,) * self.nbranches
        if isinstance(coef, float):
            coef = (coef,) * self.nbranches
        if isinstance(x0, float):
            x0 = (x0,) * self.nbranches

        msg = "size of '{}' " + f"should be {self.nbranches}"
        assert len(ampli) == self.nbranches, msg.format('ampli')
        assert len(coef) == self.nbranches, msg.format('coef')
        assert len(x0) == self.nbranches, msg.format('x0')

        self.params = Parameters()
        self.params.add("offset", value=offset or 0.)
        self.params.add("slope", value=slope or 0.)

        def add_param(label, values, min=None, max=None, expr=None):
            for i, value in enumerate(values):
                self.params.add(f"{label}_{i}", value=value, vary=True,
                                min=min, max=max, expr=None if i == 0 else expr)

        add_param("ampli", ampli, expr="ampli_0")
        add_param("coef", coef, min=0,
                  expr=None if self.asymmetric else "coef_0")
        add_param("x0", x0)

    def eval(self, x, params=None, i=0, der=0):
        """
        Return hysteresis ith-branch evaluation on support 'x'

        Parameters
        ----------
        x: numpy.array(n) or list of numpy.array(n)
            x-support for the hysteresis evaluation
        params: lmfit.Parameters
            Dictionary of parameters associated to the model ('offset', 'slope',
            'ampli', 'coef', 'x0_0', 'x0_1', ... 'x0_{nbranches-1}')
        i: int, optional
            index associated to the hysteresis branch to handle
        der: int, optional
            Degree associated to the hysteresis derivatives evaluation

        Returns
        -------
        numpy.array(n)
            Results of the hysteresis evaluation on the x-support
        """
        params = params or self.params
        return self.model.eval(x=np.array(x).ravel(),
                               offset=params['offset'].value,
                               slope=params['slope'].value,
                               ampli=params[f'ampli_{i}'].value,
                               coef=params[f'coef_{i}'].value,
                               x0=params[f'x0_{i}'].value,
                               der=der)

    def residue(self, params, x, y):
        """
        Return the residue between model evaluation and y

        Parameters
        ----------
        params: lmfit.Parameters
            Dictionary of parameters associated to the model ('offset', 'slope',
            'ampli', 'coef', 'x0_0', 'x0_1', ... 'x0_{nbranches-1}')
        x, y = list of np.ndarrays
            List of (x, y) coordinates associated to the n-branches of the
            hysteresis

        Returns
        -------
        res_tot: numpy.array(p)
            Residue (flattened) issued from the n-branches evaluation
        """
        res_tot = []
        for i, (x_i, y_i) in enumerate(zip(x, y)):
            res_tot.append(self.eval(x_i, params, i) - y_i)
        return np.concatenate(res_tot)

    def fit(self, x, y, verbosity=True, **kwargs):
        """
        Fit the hysteresis and update the 'params' attribute

        Parameters
        ----------
        x, y: list of np.ndarrays
            List of (x, y) coordinates associated to the n-branches of the
            hysteresis
        verbosity: bool, optional
            Activation key for verbosity displaying
        kwargs:
            Extra parameters associated to lmfit.minimize()
        """
        result = minimize(self.residue, self.params, args=(x, y), **kwargs)
        self.params = result.params
        if verbosity:
            report_fit(result)

    def plot(self, x, y=None, ax=None, labels=None):
        """
        Plot the hysteresis

        Parameters
        ----------
        x: list of n np.ndarrays
            List of x-coordinates associated to the n-branches of the hysteresis
            to plot
        y: list of n np.ndarrays, optional
            y-data associated to the x-coordinates used, for instance, in fit
        ax: matplotlib.Axes, optional
            Axis associated to the plot displaying
        labels: list of n strings
            Labels associated to each hysteresis branch representation

        Returns
        -------
        fig, ax: matplotlib.Figure and matplotib.Axes
        """
        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None

        labels = labels or [None] * len(x)
        if y is not None:
            for i, (x_i, y_i) in enumerate(zip(x, y)):
                ax.plot(x_i, y_i, 'ko', ms=2)
        if self.params is not None:
            ax.set_prop_cycle(None)
            for i, x_i in enumerate(x):
                y_eval = self.eval(x_i, self.params, i=i)
                ax.plot(x_i, y_eval, label=labels[i])
        ax.legend()

        return fig, ax

    def plot_properties(self, x, ax=None, plot_dict=None, bckgnd=None,
                        plot_hyst=True):
        """
        Plot the hysteresis properties (markers) from centered hysteresis

        Parameters
        ----------
        x: list of n np.ndarrays
            List of x-coordinates associated to the n-branches of the hysteresis
            to plot
        ax: matplotlib.Axes, optional
            Axis associated to the plot displaying
        plot_dict: dict, optional
            Dict of annotation for plot
        bckgnd: str, optional
            Keyword to take into account baseline in the hysteresis model among
            ('linear', 'offset', None)
        plot_hyst: bool, optional
            Key to activate hysteresis plotting

        Returns
        -------
        fig, ax: matplotlib.Figure and matplotib.Axes
        """
        assert self.props is not None, 'properties have to calculated before'
        assert bckgnd in ['linear', 'offset', None]

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = None

        # Background (baseline) parameters
        if bckgnd is None:
            self.params['offset'].value = 0.
            self.params['slope'].value = 0.
        elif bckgnd == 'offset':
            self.params['slope'].value = 0.

        # Hysteresis plotting
        if plot_hyst:
            ax.set_prop_cycle(None)
            for i, x_i in enumerate(x):
                y_eval = self.eval(x_i, self.params, i=i)
                ax.plot(x_i, y_eval, '--', label=f'prop branch{i + 1} (fit)')

        # Init plot_dict
        plot_dict = plot_dict or {}
        for key, val in zip(['c', 'ms', 'fs', 'mec', 'add str'],
                            ['lime', 10, 15, 'k', '']):
            if key not in plot_dict.keys():
                plot_dict[key] = val

        ax.axhline(self.props['y sat l'], ls='--', c=plot_dict['c'],
                   label=f'saturation {plot_dict["add str"]}')
        ax.axhline(self.props['y sat r'], ls='--', c=plot_dict['c'])
        ax.axvline(self.props['x sat l'], ls='--', c=plot_dict['c'])
        ax.axvline(self.props['x sat r'], ls='--', c=plot_dict['c'])
        ax.plot([self.props['x infl r'], self.props['x infl l']],
                [self.props['y infl r'], self.props['y infl l']], '*',
                mfc=plot_dict['c'], ms=plot_dict['ms'],
                mec=plot_dict['mec'],
                label=f'inflection {plot_dict["add str"]}')
        ax.plot([self.props['x0 r'], self.props['x0 l']],
                [self.props['y shift'], self.props['y shift']], 'X',
                mfc=plot_dict['c'], ms=plot_dict['ms'],
                mec=plot_dict['mec'], label=f'x0 {plot_dict["add str"]}')
        ax.plot([self.props['x shift'], self.props['x shift']],
                [self.props['y0 r'], self.props['y0 l']], 'P',
                mfc=plot_dict['c'], ms=plot_dict['ms'], mec=plot_dict['mec'],
                label=f'y0 {plot_dict["add str"]}')
        ax.plot([0, 0], [self.props['y inter l'], self.props['y inter r']], 'o',
                mfc=plot_dict['c'], ms=plot_dict['ms'], mec=plot_dict['mec'],
                label=f'y intersection {plot_dict["add str"]}')
        ax.plot([self.props['x inter l'], self.props['x inter r']], [0, 0], 'p',
                mfc=plot_dict['c'], ms=plot_dict['ms'], mec=plot_dict['mec'],
                label=f'x intersection {plot_dict["add str"]}')
        ax.axhline(self.props['y shift'], ls='-.', c=plot_dict['c'],
                   label=f'y, x shift {plot_dict["add str"]}')
        ax.axvline(self.props['x shift'], ls='-.', c=plot_dict['c'])
        ax.axhline(0, ls=':', c='k', label=f'x, y =0 {plot_dict["add str"]}')
        ax.axvline(0, ls=':', c='k')

        ax.legend(fontsize=plot_dict['fs'], loc='best')

        return fig, ax

    def properties(self, infl_threshold=10., sat_threshold=90., bckgnd=None):
        """
        Calculate the main properties of the hysteresis (stored in 'props'
        attribute)

        Parameters
        ----------
        infl_threshold: float, optional
            Threshold related to the maximum deflection value (at x0) to
            consider for the inflection points determination (in %)
        sat_threshold: float, optional
            Threshold related amplitude of hysteresis to consider for the 'x'
            axis saturation domain determination (in %)
        bckgnd: str, optional
            Keyword to take into account baseline in the hysteresis model among
            ('linear', 'offset', None)

        Returns
        -------
        """
        assert self.params is not None
        assert 0 <= infl_threshold <= 100
        assert 0 <= sat_threshold <= 100
        assert bckgnd in ['linear', 'offset', None]

        # Background (baseline) parameters
        offset = self.params['offset'].value
        slope = self.params['slope'].value
        if bckgnd is None:
            offset, slope = 0., 0.
        elif bckgnd == 'offset':
            slope = 0.

        # Find left and right branches whatever hysteresis orientation
        x0 = []
        for i in range(self.nbranches):
            x0.append(self.params[f'x0_{i}'].value)
        x0_l, ind_l = min(x0), np.argmin(x0)
        x0_r, ind_r = max(x0), np.argmax(x0)

        ampli_r = self.params[f'ampli_{ind_r}'].value
        coef_r = self.params[f'coef_{ind_r}'].value
        ampli_l = self.params[f'ampli_{ind_l}'].value
        coef_l = self.params[f'coef_{ind_l}'].value

        # Hysteresis branches definition
        sigmo_r = Hysteresis(nbranches=1, model=self.model_name,
                             offset=offset, slope=slope,
                             ampli=ampli_r, coef=coef_r, x0=x0_r)

        sigmo_l = Hysteresis(nbranches=1, model=self.model_name,
                             offset=offset, slope=slope,
                             ampli=ampli_l, coef=coef_l, x0=x0_l)

        # Hysteresis properties calculation
        x_shift = (x0_r + x0_l) / 2
        x0_wid = x0_r - x0_l
        y0_r = float(sigmo_r.eval(x_shift))
        y0_l = float(sigmo_l.eval(x_shift))
        area = 0.5 * (ampli_r + ampli_l) * (x0_r - x0_l)
        diff_coef = (coef_r - coef_l) / coef_r

        # Intersections points calculation
        x_inters_r = root(sigmo_r.eval, x0=x0_r).x[0]
        x_inters_l = root(sigmo_l.eval, x0=x0_l).x[0]
        x_window = x_inters_r - x_inters_l
        y_inters_r = float(sigmo_r.eval(0.))
        y_inters_l = float(sigmo_l.eval(0.))
        y_window = y_inters_l - y_inters_r

        # Inflection points calculation
        x_infl0_r = inflection(offset, slope, ampli_r, coef_r,
                               model=self.model_name, threshold=infl_threshold)
        x_infl0_l = inflection(offset, slope, ampli_l, coef_l,
                               model=self.model_name, threshold=infl_threshold)
        x_infl_r = x0_r - x_infl0_r
        x_infl_l = x0_l + x_infl0_l
        y_infl_r = float(sigmo_r.eval(x_infl_r))
        y_infl_l = float(sigmo_l.eval(x_infl_l))

        # Saturation domain calculation
        x_sat0_r = saturation(ampli_r, coef_r, model=self.model_name,
                              threshold=sat_threshold)
        x_sat0_l = saturation(ampli_l, coef_l, model=self.model_name,
                              threshold=sat_threshold)
        x_sat_r = x0_r - x_sat0_r
        x_sat_l = x0_l + x_sat0_l

        self.props = {'x sat l': x_sat_l,
                      'x sat r': x_sat_r,
                      'y sat l': ampli_l / 2 + offset,
                      'y sat r': -ampli_r / 2 + offset,
                      'x infl l': x_infl_l,
                      'x infl r': x_infl_r,
                      'y infl l': y_infl_l,
                      'y infl r': y_infl_r,
                      'x0 l': x0_l,
                      'x0 r': x0_r,
                      'x0 wid': x0_wid,
                      'x shift': x_shift,
                      'y shift': offset,
                      'y0 l': y0_l,
                      'y0 r': y0_r,
                      'x inter l': x_inters_l,
                      'x inter r': x_inters_r,
                      'x wdw': x_window,
                      'y inter l': y_inters_l,
                      'y inter r': y_inters_r,
                      'y wdw': y_window,
                      'area': area,
                      'diff coef': diff_coef}

    def r_square(self, x, y):
        """
        Calculate the R-squared value for the hysteresis.

        Parameters
        ----------
        x: list of n np.ndarrays
            List of x-coordinates associated to the n-branches of the hysteresis
        y: list of n np.ndarrays, optional
            List of y-coordinates associated to the n-branches of the hysteresis
        """
        r_squared = []
        for i, (x_i, y_i) in enumerate(zip(x, y)):
            y_eval = self.eval(x_i, self.params, i=i)
            r_squared.append(r2_score(y_i, y_eval))

        self.props.update({'R² hyst': np.mean(r_squared)})


def inflection(offset, slope, ampli, coef, model='sigmoid', threshold=10.):
    """
    Inflection x-axis coordinate determination

    Parameters
    ----------
    offset: float
        Offset parameter associated to the linear model
    slope: float
        Slope parameter associated to the linear model
    ampli: float
        Amplitude parameter associated to the model
    coef: float
        Coef of dilatation parameter associated to the model.
    model: str, optional
        Model name associated to the branch: 'sigmoid' or 'arctan'
    threshold: float, optional
        Threshold related to the maximum deflection value (at x0) to
        consider for the inflection points determination (in %)

    Returns
    -------
    x_infl0: float
        Inflection x-axis coordinate
    """
    sigmo_0 = Hysteresis(nbranches=1, model=model, offset=offset,
                         slope=slope, ampli=ampli, coef=coef, x0=0.)
    infl_rax = sigmo_0.eval(0., der=1)

    def infl_fun(x):
        return sigmo_0.eval(x, der=1) - infl_rax * threshold / 100

    x_infl0 = root(infl_fun, x0=ampli / (2 * infl_rax)).x[0]

    return x_infl0


def saturation(ampli, coef, model='sigmoid', threshold=90.):
    """
    Saturation x-axis coordinate determination

    Parameters
    ----------
    ampli: float
        Amplitude parameter associated to the model
    coef: float
        Coef of dilatation parameter associated to the model.
    model: str, optional
        Model name associated to the branch: 'sigmoid' or 'arctan'
    threshold: float, optional
        Threshold related amplitude of hysteresis to consider for the 'x'
        axis saturation domain determination (in %)

    Returns
    -------
    x_sat0: float
        Saturation x-axis coordinate
    """
    pure_sigmo_0 = Model(eval(model))
    params_sigmo_0 = pure_sigmo_0.make_params(ampli=ampli, coef=coef, x0=0.)

    def sat_fun(x):
        return pure_sigmo_0.eval(params_sigmo_0, x=x) + \
               (ampli / 2 * threshold / 100)

    x_sat0 = root(sat_fun, x0=np.array([0])).x[0]

    return x_sat0
