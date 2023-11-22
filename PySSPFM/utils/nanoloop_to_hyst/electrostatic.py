"""
Module used for the scripts of sspfm 2d step data analysis
(convert nanoloop to hyst)
    - Electrostatic analysis toolbox
"""

import numpy as np

from PySSPFM.utils.core.signal import line_reg
from PySSPFM.utils.nanoloop_to_hyst.plot import \
    (plot_btfly_analysis, plot_sat_analysis, plot_offset_analysis,
     plot_differential_analysis)


def btfly_analysis(write, amp, make_plots=False, dict_str=None):
    """
    Find imprint value with butterfly analysis method (imprint = CPD for
    dominant electrostatic contribution and on field measure)

    Parameters
    ----------
    write: dict
        Write voltage values for left and right segment (in V)
    amp: dict
        Amplitude values for left and right segment (in a.u or nm)
    make_plots: bool, optional
        Activation key for matplotlib figures generation
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    imprint: float
        Imprint of butterfly nanoloop (in V)
    fig: plt.figure
        Figure of butterfly analysis
    """
    mini = {'left': write['left'][np.argmin(amp['left'])],
            'right': write['right'][np.argmin(amp['right'])]}
    imprint = np.mean(list(mini.values()))

    fig = plot_btfly_analysis(
        write, amp, mini, imprint, dict_str=dict_str) if make_plots else []

    return imprint, fig


def sat_analysis(write, amp, pha, piezorep, sat_domain=None, make_plots=False,
                 dict_str=None, func=None):
    """
    Find affine electrostatic component y_elec = a_elec*U+y_0 (x_0=CPD only
    valid if On Field saturated measurement + the only origin of offset for off
    field measurement is electrostatic)
    S. Jesse et Al. : « Quantitative Mapping of Switching Behavior in
    Piezoresponse Force Microscopy ». Review of Scientific Instruments 77, nᵒ 7
    2006. https://doi.org/10.1063/1.2214699.

    Parameters
    ----------
    write: dict
        Write voltage values for left and right segment (in V)
    amp: dict
        Amplitude values for left and right segment (in a.u or nm)
    pha: dict
        Phase values for left and right segment (in °)
    piezorep: dict
        Piezoresponse values for left and right segment (in a.u or nm)
    sat_domain: list(2), optional
        X axis saturation domain (in V)
    make_plots: bool, optional
        Activation key for matplotlib figures generation
    dict_str: dict, optional
        Dict used for figure annotation
    func: callable, optional
        Function to apply to the phase values to determine piezoresponse
        (default is np.cos)

    Returns
    -------
    sat_res: dict
        Dict containing all saturation analysis results:
        - a_elec: float
            Slope of affine electrostatic component: y_elec = a_elec*U+y_0
        - y_0: float
            Offset of affine electrostatic component: y_elec = a_elec*U+y_0
        - x_0: float
            y_elec(x_0)=0: can correspond to CPD
        - r_square: float
            R² of saturation line regression
    figs_sat: list(2) of plt.figure
        - fig: plt.figure
             1st figure (saturation analysis on butterfly ->
             1st step of the treatment)
        - fig2: plt.figure
             2nd figure (saturation analysis on hysteresis ->
             2nd step of the treatment)
    """
    func = func or np.cos

    # Linear regression of saturation domain for amp left and right segment
    sat, ind_sat = {}, {}

    # Sat domain determination
    if sat_domain is None:
        # Saturation domain, in percent of write voltage axis
        sat_prcnt = 10
        ind_sat = {seg: int(sat_prcnt / 100 * len(write[seg])) for seg in
                   ['right', 'left']}
        sat = {seg: line_reg(write[seg][:ind_sat[seg] + 1],
                             amp[seg][:ind_sat[seg] + 1]) for seg in
               ['right', 'left']}
    else:
        for elem_sat, seg in zip(np.sort(sat_domain), ['right', 'left']):
            coef = -1 if seg == 'left' else 1
            ind_sat[seg] = next((cont for cont, elem in enumerate(write[seg]) if
                                 coef * elem >= coef * elem_sat), None)
            sat[seg] = line_reg(write[seg][:ind_sat[seg] + 1],
                                amp[seg][:ind_sat[seg] + 1])

    # Find electrostatic component
    coef_left = func(np.deg2rad(pha['right'][np.argmin(write['right'])]))
    coef_right = func(np.deg2rad(pha['left'][np.argmax(write['left'])]))
    y_fit = {key: coef * np.polyval(sat[key]['coefs'], write[key]) for key, coef
             in zip(['left', 'right'], [coef_right, coef_left])}
    y_fit['mean'] = [(np.flip(y_fit['left'])[i] + y_fit['right'][i]) / 2 for i
                     in range(len(y_fit['left']))]
    elec_fit = line_reg(write['right'], y_fit['mean'])
    a_elec = elec_fit['coefs'][0]
    y_0 = elec_fit['coefs'][1]
    x_0 = -y_0 / a_elec if a_elec != 0 else np.NaN
    r_square = np.mean([sat['right']['r**2'], sat['left']['r**2']])

    figs_sat = plot_sat_analysis(write, amp, piezorep, a_elec, y_0, x_0,
                                 r_square, sat, ind_sat['right'],
                                 ind_sat['left'], y_fit, elec_fit,
                                 dict_str=dict_str) if make_plots else []

    sat_res = {'a_elec': a_elec, 'y_0': y_0, 'x_0': x_0, 'r_square': r_square}

    return sat_res, figs_sat


def offset_analysis(read_volt, offset, make_plots=False, dict_str=None):
    """
    Find affine electrostatic component y_elec = a_elec*U+y_0 (multi off field
    measurement are performed with different read voltage, line regression is
    performed to find electrostatic component) (x_0=CPD valid if the only
    origin of offset for off field measurement is electrostatic)

    Parameters
    ----------
    read_volt: list(n) or numpy.array(n) of float
        Array of read voltage value (in V)
    offset: list(n) or numpy.array(n) of float
        Array of hysteresis offset value (in a.u or nm)
    make_plots: bool, optional
        Activation key for matplotlib figures generation
    dict_str: dict, optional
        Dict used for figure annotation

    Returns
    -------
    offset_res: dict
        Dict containing all offset analysis results:
        - a_elec: float
            Slope of affine electrostatic component: y_elec = a_elec*U+y_0
        - y_0: float
            Offset of affine electrostatic component: y_elec = a_elec*U+y_0
        - x_0: float
            y_elec(x_0)=0: can correspond to CPD
        - r_square: float
            R² of saturation line regression
    fig: plt.figure
        Figure of offset analysis
    """
    elec_fit = line_reg(read_volt, offset)
    a_elec, y_0 = elec_fit['coefs'][0], elec_fit['coefs'][1]
    x_0 = -y_0 / a_elec if a_elec != 0 else np.NaN
    r_square = elec_fit['r**2']
    offset_res = {
        'a_elec': a_elec,
        'y_0': y_0,
        'x_0': x_0,
        'r_square': r_square
    }

    fig = plot_offset_analysis(a_elec, y_0, x_0, r_square, read_volt, elec_fit,
                               offset, dict_str=dict_str) if make_plots else []

    return offset_res, fig


def differential_analysis(loop_on, loop_off, offset_off=0, bias_min=-5.,
                          bias_max=5., dict_str=None, make_plots=False):
    """
    Electrostatic analysis: method based on 'on' and 'off' field hysteresis
    nanoloop difference to decouple electrostatic from ferroelectric
    contribution (x_0=CPD valid if the only origin of offset for off field
    measurement is electrostatic)
    N. Balke et al. « Current and Surface Charge Modified Hysteresis Loops in
    Ferroelectric Thin Films ». Journal of Applied Physics 118, nᵒ 7 2015.
    https://doi.org/10.1063/1.4927811.

    Parameters
    ----------
    loop_on: loop (MeanLoop or MultiLoop) object
        MeanLoop or MultiLoop class object, On Field loop
    loop_off: loop (MeanLoop or MultiLoop) object
        MeanLoop or MultiLoop class object, Off Field loop
    offset_off: float, optional
        Offset of off field fit loop (electrostatic constant component)
    bias_min: float, optional
        Initial minimum value of write voltage axis range for the differential
        analysis (in V)
    bias_max: float, optional
        Initial maximum value of write voltage axis range for the differential
        analysis (in V)
    dict_str: dict, optional
        Dict used for figure annotation
    make_plots: bool, optional
        Activation keywords for figure generation

    Returns
    -------
    mean_voltage: list(n) or numpy.array(n) of float
        Array of mean (left and right) diff voltage values (in V)
    diff_piezorep_mean: list(n) or numpy.array(n) of float
        Array of mean (left and right) diff piezoresponse values (in a.u or nm)
    diff_res: dict
        All differential analysis results:
        - a_diff: float
            Slope of differential analysis: y_diff = a_diff*x+y_0_diff:
            should be equal to a_elec (slope of electrostatic component:
            y_elec = a_elec*U+y_0)
        - y_0_diff: float
            Offset of differential analysis: y_diff = a_diff*x+y_0_diff:
            should be equal to 0
        - x_0_diff: float
            y_diff(x_0_diff)=0: should be equal to 0
        - r_square: float
            R² of differential line regression
    fig: plt.figure
    """
    out = gen_differential_loop(loop_on, loop_off, offset_off=offset_off)
    (write_volt_left, diff_piezorep_left, write_volt_right, diff_piezorep_right,
     diff_piezorep_mean) = out

    diff_piezorep_grad = np.gradient(diff_piezorep_mean, write_volt_right)

    fig = []
    (_, _, fit_res) = linreg_differential(
        write_volt_right, diff_piezorep_mean, bias_min, bias_max)
    (a_diff, y_0_diff, x_0_diff, r_square, diff_fit) = fit_res
    if make_plots:
        fig = plot_differential_analysis(
            write_volt_left, write_volt_right, diff_fit, diff_piezorep_left,
            diff_piezorep_right, diff_piezorep_mean, diff_piezorep_grad,
            a_diff, y_0_diff, r_square, bias_min=bias_min,
            bias_max=bias_max, dict_str=dict_str)

    diff_res = {'a': a_diff,
                'y_0': y_0_diff,
                'x_0': x_0_diff,
                'r_2': r_square}

    mean_voltage = write_volt_right

    return mean_voltage, diff_piezorep_mean, diff_res, fig


def linreg_differential(write_volt, piezorep_diff, bias_min=-5., bias_max=5.):
    """
    Linear regression analysis for differential piezoresponse

    Parameters
    ----------
    write_volt: list(n) or numpy.array(n) of float
        Array of write voltage values for differential piezoresponse (in V)
    piezorep_diff: list(n) or numpy.array(n) of float
        Array of piezoresponse value for on and off field difference
        (in a.u or nm)
    bias_min: float, optional
        Initial minimum value of write voltage axis range for the differential
        analysis (in V)
    bias_max: float, optional
        Initial maximum value of write voltage axis range for the differential
        analysis (in V)

    Returns
    -------
    red_write_volt: list(m) or numpy.array(m) of float (m<n)
        Array of write voltage values for differential piezoresponse reduced in
        [bias_min, bias_max] range (in V)
    red_piezorep_diff: list(m) or numpy.array(m) of float (m<n)
        Array of piezoresponse value for on and off field difference reduced in
        [bias_min, bias_max] range (in a.u or nm)
    fit_res: tuple(5)
        Result of linear regression of differential piezoresponse
    """
    # Linear regression
    red_write_volt, red_piezorep_diff = [], []
    for cont, elem in enumerate(write_volt):
        if bias_min <= elem <= bias_max:
            red_write_volt.append(elem)
            red_piezorep_diff.append(piezorep_diff[cont])
    diff_fit = line_reg(red_write_volt, red_piezorep_diff)
    a_diff, y_0_diff = diff_fit['coefs']
    x_0_diff = -y_0_diff / a_diff if a_diff != 0 else np.NaN
    r_square = diff_fit['r**2']
    fit_res = (a_diff, y_0_diff, x_0_diff, r_square, diff_fit)

    return red_write_volt, red_piezorep_diff, fit_res


def gen_differential_loop(loop_on, loop_off, offset_off=0):
    """
    Construct differential on / off field piezoresponse loop

    Parameters
    ----------
    loop_on: loop (MeanLoop or MultiLoop) object
        MeanLoop or MultiLoop class object, On Field loop
    loop_off: loop (MeanLoop or MultiLoop) object
        MeanLoop or MultiLoop class object, Off Field loop
    offset_off: float, optional
        Offset of off field fit loop (electrostatic constant component)

    Returns
    -------
    write_volt_left: list(n) or numpy.array(n) of float
        Array of write voltage values for left segment (in V)
    diff_piezorep_left: list(n) of float
        List of piezoresponse values for on and off field difference
        (left segment) (in a.u or nm)
    write_volt_right: list(n) or numpy.array(n) of float
        Array of write voltage values for right segment (in V)
    diff_piezorep_right: list(n) of float
        List of piezoresponse values for on and off field difference
        (right segment) (in a.u or nm)
    diff_piezorep_mean: list(n) of float
        List of piezoresponse mean left / right segment value for on and off
        field difference (in a.u or nm)
    """
    # Subtract on and off field hysteresis loop
    write_volt_left, diff_piezorep_left = substract_on_off_loop(
        loop_off.piezorep.write_volt_left, loop_off.piezorep.y_meas_left,
        loop_on.piezorep.write_volt_left, loop_on.piezorep.y_meas_left,
        offset_off=offset_off)
    write_volt_right, diff_piezorep_right = substract_on_off_loop(
        loop_off.piezorep.write_volt_right, loop_off.piezorep.y_meas_right,
        loop_on.piezorep.write_volt_right, loop_on.piezorep.y_meas_right,
        offset_off=offset_off)

    # Compute mean piezoresponse for left and right segments
    diff_piezorep_mean = [(right + left) / 2 for right, left in zip(
        diff_piezorep_right, np.flip(diff_piezorep_left))]

    return (write_volt_left, diff_piezorep_left, write_volt_right,
            diff_piezorep_right, diff_piezorep_mean)


def substract_on_off_loop(write_voltage_off, pr_off, write_voltage_on, pr_on,
                          offset_off=0):
    """
    Find the difference between on and off field piezoresponse

    Parameters
    ----------
    write_voltage_off: list(n) or numpy.array(n) of float
        Array of write voltage values for off_field measurement (in V)
    pr_off: list(n) or numpy.array(n) of float
        Array of piezoresponse values for off_field measurement (in a.u or nm)
    write_voltage_on: list(n) or numpy.array(n) of float
        Array of write voltage values for on_field measurement (in V)
    pr_on: list(n) or numpy.array(n) of float
        Array of piezoresponse values for on_field measurement (in a.u or nm)
    offset_off: float, optional
        Offset of off field fit loop (electrostatic constant component)

    Returns
    -------
    write_voltage: list(n) of float
        List of write voltage values corresponding to the list pr_sub (in V)
    pr_sub: list(n) of float
        List of piezoresponse values for on and off field difference
        (in a.u or nm)
    """
    assert len(write_voltage_off) == len(pr_off)
    assert len(write_voltage_on) == len(pr_on)

    write_voltage, pr_sub = [], []
    for elem_off, elem_on in zip(write_voltage_off, write_voltage_on):
        if elem_off == elem_on:
            write_voltage.append(elem_off)
            index_on = np.where(write_voltage_on == elem_on)[0][0]
            index_off = np.where(write_voltage_off == elem_off)[0][0]
            pr_sub.append(pr_on[index_on] - (pr_off[index_off] - offset_off))

    return write_voltage, pr_sub
