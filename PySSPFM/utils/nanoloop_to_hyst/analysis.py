"""
Module used for the scripts of sspfm 2d step data analysis
(convert nanoloop to hyst)
    - Data analysis toolbox
"""

import numpy as np

from PySSPFM.utils.core.signal import interpolate
# pylint: disable=unused-import
from PySSPFM.utils.core.basic_func import linear, sigmoid, arctan
from PySSPFM.utils.core.curve_hysteresis import Hysteresis
from PySSPFM.utils.core.noise import filter_mean
from PySSPFM.utils.nanoloop.plot import plot_multiloop
from PySSPFM.utils.nanoloop.analysis import MeanLoop
from PySSPFM.utils.nanoloop_to_hyst.plot import plot_hysteresis
from PySSPFM.utils.nanoloop_to_hyst.electrostatic import \
    (btfly_analysis, sat_analysis, offset_analysis)


def gen_analysis_mode(mode='off', read_mode='Single Read Step'):
    """
    Generate analysis_mode

    Parameters
    ----------
    mode: str, optional
        'on' or 'off'
    read_mode: str, optional
        Read voltage mode application: 'Single Read Step', 'Low to High',
        'High to Low'

    Returns
    -------
    analysis_mode: str
        Operating mode for the reader: three possible mode:
        - 'on_f_loop' for on field measurement
        - 'mean_loop' for off field measurement with a constant value of read
        voltage
        - 'multi_loop' for off field measurement with different value of read
        voltage
    """
    if mode == 'on':
        analysis_mode = 'on_f_loop'
    elif mode == 'off':
        analysis_mode = 'mean_loop' if \
            read_mode == 'Single Read Step' else 'multi_loop'
    else:
        raise IOError('mode in [\'on\',\'off\']')
    return analysis_mode


def init_hysteresis_params(hyst, counterclockwise, grounded_tip,
                           analysis_mode='mean_loop', locked_elec_slope=None,
                           x_hyst=None, y_hyst=None):
    """
    Initiate hysteresis parameters and bckgnd function from analysis_mode for
    the hysteresis fit

    Parameters
    ----------
    hyst: Hysteresis object
        Hysteresis object
    counterclockwise: bool
        Specifies if the hysteresis is counterclockwise
    grounded_tip: bool
        Flag indicating whether the tip is grounded.
    analysis_mode: str, optional
        Operating mode for the reader: three possible mode:
        - 'on_f_loop' for on field measurement
        - 'mean_loop' for off field measurement with a constant value of read
        voltage
        - 'multi_loop' for off field measurement with different value of read
        voltage
    locked_elec_slope: str, optional
        Electrostatic slope sign is locked with this parameter
    x_hyst: list, optional
        x values for the hysteresis fit. Default is None.
    y_hyst: list, optional
        y values for the hysteresis fit. Default is None.

    Returns
    -------
    bckgnd: str
        Keyword to take into account baseline in the hysteresis model among
        ('linear', 'offset', None)
    """
    # Slope of switch is set to positive value
    hyst.params['coef_0'].set(min=0)
    hyst.params['coef_1'].set(min=0)

    # Amplitude of hysteresis is set to a negative value for counterclockwise
    # loop and vice versa (Neumayer et al. : doi: 10.1063/5.0011631)
    if counterclockwise:
        hyst.params['ampli_0'].set(min=0)
        hyst.params['ampli_1'].set(min=0)
        amp_fact = 1
    else:
        hyst.params['ampli_0'].set(max=0)
        hyst.params['ampli_1'].set(max=0)
        amp_fact = -1

    # Set x0_0 and x0_1 based on x_hyst min and max values
    if x_hyst is not None:
        x_hyst_flat = np.array(
            [item for sublist in x_hyst for item in sublist]).ravel()
        y_hyst_flat = np.array(
            [item for sublist in y_hyst for item in sublist]).ravel()

        if not all(isinstance(elem, (float, int)) for elem in x_hyst_flat):
            print("Type problem in x_hyst_flat :",
                  set(type(elem) for elem in x_hyst_flat))

        if not all(isinstance(elem, (float, int)) for elem in y_hyst_flat):
            print("Type problem in y_hyst_flat :",
                  set(type(elem) for elem in y_hyst_flat))

        # Min and max limits
        x_min = np.nanmin(x_hyst_flat)
        x_max = np.nanmax(x_hyst_flat)
        hyst.params['x0_0'].set(min=x_min, max=x_max)
        hyst.params['x0_1'].set(min=x_min, max=x_max)

    # Set offset based on y_hyst min and max values
    if y_hyst is not None:
        y_hyst_flat = np.array(
            [item for sublist in y_hyst for item in sublist]).ravel()

        if not all(isinstance(elem, (float, int)) for elem in y_hyst_flat):
            print("Type problem in y_hyst_flat :",
                  set(type(elem) for elem in y_hyst_flat))

        # Min and max limits
        y_min = np.nanmin(y_hyst_flat)
        y_max = np.nanmax(y_hyst_flat)
        hyst.params['offset'].set(min=y_min, max=y_max)

    # Perform operations when both x_hyst and y_hyst are not None and have
    # equal lengths
    if x_hyst is not None and y_hyst is not None and len(x_hyst) == len(y_hyst):
        # Interpolate and calculate difference for each branch of hysteresis:
        # Determination of differential hysteresis loop
        branch_1 = interpolate(x_hyst[0], y_hyst[0], 1, interp_type='linear')
        branch_2 = interpolate(x_hyst[1], y_hyst[1], 1, interp_type='linear')
        diff_hyst = np.abs(branch_1['y interp'] - branch_2['y interp'])
        diff_hyst = filter_mean(diff_hyst, window_size=5)

        # Set ampli_0: max of differential hysteresis loop
        guess_amp = max(diff_hyst)
        hyst.params['ampli_0'].set(value=amp_fact * guess_amp)

        # Set x0_0 and x0_1: max(abs(slopes)) of differential hysteresis loop
        slopes = np.diff(diff_hyst)
        guess_x0s = [branch_1['x interp'][np.argmax(slopes)],
                     branch_2['x interp'][np.argmin(slopes)]]
        x0_0_guess = np.min(guess_x0s)
        x0_1_guess = np.max(guess_x0s)
        hyst.params['x0_0'].set(value=x0_0_guess)
        hyst.params['x0_1'].set(value=x0_1_guess)

    # Set bckgnd and slope based on analysis_mode
    if analysis_mode in ['mean_loop', 'multi_loop']:
        bckgnd = 'offset'
        hyst.params['slope'].set(value=0, vary=False)
    elif analysis_mode == 'on_f_loop':
        bckgnd = 'linear'
        if locked_elec_slope is None:
            # Grounded tip -> negative slope of electrostatic component
            if grounded_tip:
                hyst.params['slope'].set(max=0)
                coef_slope = -1
            # Grounded bottom -> positive slope of electrostatic component
            else:
                hyst.params['slope'].set(min=0)
                coef_slope = 1
        elif locked_elec_slope == 'positive':
            hyst.params['slope'].set(min=0)
            coef_slope = 1
        elif locked_elec_slope == 'negative':
            hyst.params['slope'].set(max=0)
            coef_slope = -1
        else:
            raise NotImplementedError(
                "locked_elec_slope should be None or 'negative' or 'positive'")
        if x_hyst is not None and y_hyst is not None:
            num = np.max(y_hyst) - np.min(y_hyst)
            denom = np.max(x_hyst) - np.min(x_hyst)
            guess_slope = coef_slope * num / denom
            hyst.params['slope'].set(value=guess_slope)
    else:
        raise IOError('analysis_mode must be one of [\'mean_loop\', '
                      '\'multi_loop\', \'on_f_loop\']')

    return bckgnd


def find_best_nanoloop(loop_tab, counterclockwise, grounded_tip,
                       analysis_mode='mean_loop', del_1st_loop=False,
                       model='sigmoid', asymmetric=False, method='leastsq',
                       locked_elec_slope=None):
    """
    Function used to find the best piezoresponse nanoloop.

    Parameters
    ----------
    loop_tab: list(n) of loop (MultiLoop or MeanLoop) object
        List of all loops associated with SSPFM measurement
    counterclockwise: bool
        Specifies if the hysteresis is counterclockwise
    grounded_tip: bool
        Flag indicating whether the tip is grounded.
    analysis_mode: str, optional
        Operating mode for the reader: three possible modes:
        - 'on_f_loop' for on-field measurement
        - 'mean_loop' for off-field measurement with a constant value of read
        voltage
        - 'multi_loop' for off-field measurement with different values of
        read voltage
    del_1st_loop: bool, optional
        If True, remove the first loop for analysis
    model: str, optional
        Algebraic model of the branch: 'sigmoid' or 'arctan'
    asymmetric: bool, optional
        Activation keyword to deal with asymmetric hysteresis
    method: str, optional
        Name of the fitting method to use
    locked_elec_slope: str, optional
        Electrostatic slope sign is locked with this parameter

    Returns
    -------
    x_hyst: list(2) of numpy.array(m)
        Write voltage value associated with the left and right segments of
        the hysteresis (in V)
    y_hyst: list(2) of numpy.array(m)
        Piezoresponse value associated with the left and right segments of
        the hysteresis (in a.u or nm)
    best_loop: loop (MultiLoop or MeanLoop) object
        Best loop depending on the analysis mode
    read_volt: list(n) or numpy.array(n) of float
        Array of read voltage values (in V) (used for 'multi_loop' analysis)
    bckgnd_tab: list(n) or numpy.array(n) of float
        Array of hysteresis offset values (in a.u or nm) (used for
        'multi_loop' analysis)
    """
    read_volt, bckgnd_tab = None, None

    if analysis_mode == 'multi_loop':
        xy_hyst_tab, bckgnd_tab, read_volt = [], [], []
        for loop in loop_tab:
            x_hyst_i = [np.array(loop.write_volt_right),
                        np.array(loop.write_volt_left)]
            y_hyst_i = [np.array(loop.piezorep_right),
                        np.array(loop.piezorep_left)]
            xy_hyst_tab.append([x_hyst_i, y_hyst_i])
            hyst = Hysteresis(model=model, asymmetric=asymmetric)
            _ = init_hysteresis_params(
                hyst, counterclockwise, grounded_tip,
                analysis_mode=analysis_mode,
                locked_elec_slope=locked_elec_slope,
                x_hyst=x_hyst_i, y_hyst=y_hyst_i)
            hyst.fit(x_hyst_i, y_hyst_i, verbosity=False, method=method)
            bckgnd_tab.append(hyst.params['offset'].value)
            read_volt.append(loop.read_volt)
        best_idx = np.argmin([abs(value) for value in bckgnd_tab])
        best_loop = loop_tab[best_idx]
        x_hyst = xy_hyst_tab[best_idx][0]
        y_hyst = xy_hyst_tab[best_idx][1]

    elif analysis_mode in ['mean_loop', 'on_f_loop']:
        best_loop = MeanLoop(loop_tab, del_1st_loop=del_1st_loop)
        x_hyst = [np.array(best_loop.write_volt_right),
                  np.array(best_loop.write_volt_left)]
        y_hyst = [np.array(best_loop.piezorep_right),
                  np.array(best_loop.piezorep_left)]

    else:
        raise IOError(
            'analysis_mode in [\'mean_loop\',\'multi_loop\',\'on_f_loop\']')

    return x_hyst, y_hyst, best_loop, read_volt, bckgnd_tab


def hyst_analysis(x_hyst, y_hyst, best_loop, counterclockwise, grounded_tip,
                  dict_str=None, infl_threshold=10, sat_threshold=90,
                  model='sigmoid', asymmetric=False, method='leastsq',
                  analysis_mode='mean_loop', locked_elec_slope=None,
                  make_plots=False):
    """
    Generate hysteresis, perform fit and extract parameters + properties

    Parameters
    ----------
    x_hyst: list(2) of numpy.array(n)
        Write voltage value associated with the left and right segments of the
        hysteresis (in V)
    y_hyst: list(2) of numpy.array(n)
        Piezoresponse value associated with the left and right segments of the
        hysteresis (in a.u or nm)
    best_loop: loop (MultiLoop or MeanLoop) object
        Best loop depending on the analysis mode
    counterclockwise: bool
        Specifies if the hysteresis is counterclockwise
    grounded_tip: bool
        Flag indicating whether the tip is grounded.
    dict_str: dict, optional
        Dict used for figure annotation
    infl_threshold: float, optional
        Threshold (in %) of the derivative amplitude of the hysteresis fit
        function (sigmoid, arctan, etc.)
        used for nucleation bias analysis
    sat_threshold: float, optional
        Threshold related to the amplitude of the hysteresis to consider for
        the x-axis saturation domain determination (in %)
    model: str, optional
        Algebraic model of the branch: 'sigmoid' or 'arctan'
    asymmetric: bool, optional
        Activation keyword to deal with asymmetric hysteresis
    method: str, optional
        Name of the fitting method to use
    analysis_mode: str, optional
        Operating mode for the reader: three possible modes:
        - 'on_f_loop' for on-field measurement
        - 'mean_loop' for off-field measurement with a constant value
        of read voltage
        - 'multi_loop' for off-field measurement with different values
        of read voltage
    locked_elec_slope: str, optional
        Electrostatic slope sign is locked with this parameter
    make_plots: bool, optional
        Activation key for matplotlib figure generation

    Returns
    -------
    best_hyst: Hysteresis object
        Best hysteresis associated with best_loop
    props_tot: dict
        Hysteresis (with background) properties
    props_no_bckgnd: dict
        Hysteresis (without background) properties
    figs: list(m) of figure
        List of figure objects (multiloop + hysteresis with properties)
    """
    figs = []

    # Hysteresis object and fit
    best_hyst = Hysteresis(model=model, asymmetric=asymmetric)
    bckgnd = init_hysteresis_params(
        best_hyst, counterclockwise, grounded_tip, analysis_mode=analysis_mode,
        locked_elec_slope=locked_elec_slope, x_hyst=x_hyst, y_hyst=y_hyst)
    try:
        best_hyst.fit(x_hyst, y_hyst, verbosity=False, method=method)
    except ValueError:
        print("ValueError management with except: hysteresis fit is "
              "unsuccessful")

    # Plot multiloop
    if make_plots:
        fig = plot_multiloop(best_loop, dict_str=dict_str)
        figs.append(fig)

    # Extract hysteresis properties
    best_hyst.properties(infl_threshold=infl_threshold,
                         sat_threshold=sat_threshold, bckgnd=bckgnd)
    # Extract R² of hysteresis
    best_hyst.r_square(x_hyst, y_hyst)
    props_tot = best_hyst.props
    props_tot['area'] = abs(props_tot['area'])
    best_hyst.properties(infl_threshold=infl_threshold,
                         sat_threshold=sat_threshold, bckgnd=None)

    props_no_bckgnd = best_hyst.props
    props_no_bckgnd['area'] = abs(props_no_bckgnd['area'])

    # Plot hysteresis with properties
    if make_plots:
        fig = plot_hysteresis(best_hyst, x_hyst, y_hyst, bckgnd=bckgnd,
                              infl_threshold=infl_threshold,
                              sat_threshold=sat_threshold, dict_str=dict_str)
        figs.append(fig)

    return best_hyst, props_tot, props_no_bckgnd, figs


def electrostatic_analysis(best_loop, analysis_mode='mean_loop',
                           sat_domain=None, make_plots=False, dict_str=None,
                           read_volt=None, bckgnd_tab=None, func=None):
    """
    Perform electrostatic analysis on the best loop depending on the analysis
    mode

    Parameters
    ----------
    best_loop: loop (MultiLoop or MeanLoop) object
        Best loop depending on the analysis mode
    analysis_mode: str, optional
        Operating mode for the reader: three possible modes:
        - 'on_f_loop' for on-field measurement
        - 'mean_loop' for off-field measurement with a constant value of read
        voltage
        - 'multi_loop' for off-field measurement with different values of
        read voltage
    sat_domain: list(2), optional
        X-axis saturation domain (in V)
    make_plots: bool, optional
        Activation key for matplotlib figure generation
    dict_str: dict, optional
        Dict used for figure annotation
    read_volt: list(n) or numpy.array(n) of float, optional
        Array of read voltage values (in V) (used for 'multi_loop' analysis)
    bckgnd_tab: list(n) or numpy.array(n) of float, optional
        Array of hysteresis offset values (in a.u or nm) (used for
        'multi_loop' analysis)
    func: callable, optional
        Function to apply to the phase values to determine piezoresponse
        (default is np.cos)

    Returns
    -------
    electrostatic_dict: dict
        All electrostatic results of the analysis
    figs: list(m) of figure
        List of figure objects of electrostatic analysis
    """
    func = func or np.cos
    assert analysis_mode in ['multi_loop', 'mean_loop', 'on_f_loop']
    figs = []
    electrostatic_dict = {}

    if analysis_mode == 'on_f_loop':
        # On-field electrostatic analysis
        write_loop = {'left': best_loop.write_volt_left,
                      'right': best_loop.write_volt_right}
        amp_loop = {'left': best_loop.amp_left, 'right': best_loop.amp_right}
        pha_loop = {'left': best_loop.pha_left, 'right': best_loop.pha_right}
        piezorep_loop = {'left': best_loop.piezorep_left,
                         'right': best_loop.piezorep_right}

        # Butterfly analysis
        imprint_btfly, fig = btfly_analysis(write_loop, amp_loop,
                                            make_plots=make_plots,
                                            dict_str=dict_str)
        electrostatic_dict['butterfly analysis: imprint'] = imprint_btfly
        if make_plots:
            figs.append(fig)

        # Saturation analysis
        sat_res, figs_sat = sat_analysis(write_loop, amp_loop, pha_loop,
                                         piezorep_loop, sat_domain=sat_domain,
                                         make_plots=make_plots,
                                         dict_str=dict_str, func=func)
        for key, value in sat_res.items():
            electrostatic_dict[f'sat analysis: {key}'] = value
        if make_plots:
            figs += figs_sat

    elif analysis_mode == 'multi_loop':
        # Off-field (multi loop) electrostatic analysis
        offset_res, fig = offset_analysis(
            read_volt, bckgnd_tab, make_plots=make_plots, dict_str=dict_str)
        for key, value in offset_res.items():
            electrostatic_dict[f'offset analysis: {key}'] = value
        if make_plots:
            figs.append(fig)

    return electrostatic_dict, figs


def sort_prop(properties):
    """
    Transform property dict to be plotted in sspfm map

    Parameters
    ----------
    properties: dict
        Initial property --> property[mode][- file n°i][prop]

    Returns
    -------
    result_dict: dict
        Final property --> property[mode][prop] = [all file n°]
    """
    result_dict = {key: {
        sub_key: [] for sub_key in properties[key][' - file n°1'].keys()}
        for key in properties}
    for key, files in properties.items():
        for file in files.values():
            for sub_key, value in file.items():
                result_dict[key][sub_key].append(value)

    return result_dict
