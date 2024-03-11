"""
Module used for nanoloop: - phase calibration
"""

import numpy as np

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.peak import find_main_peaks, plot_main_peaks
from PySSPFM.utils.core.fitting import GaussianPeakFit
from PySSPFM.utils.nanoloop.plot_phase import \
    (refocused_phase_histo, histo_init, annotate_histo,
     plot_phase_bias_grad)


def phase_calibration(phase, write_voltage, dict_pha, dict_str=None,
                      make_plots=False):
    """
    Convert a phase list associated to a nanoloop, in calibrated phase
    list up & down (between phase forward and phase reverse value).
    This analysis can be performed either on bipolar or unipolar nanoloop.

    Parameters
    ----------
    phase: numpy.array(n) or list(n) of float
        Array of phase values (in °)
    write_voltage: numpy.array(n) or list(n) of float
        Array of write voltage for all the loops (V)
    dict_pha: dict
        Used for phase calibration
    dict_str: dict, optional
        Used for figure annotation
    make_plots: bool, optional
        Activation key for matplotlib figures generation

    Returns
    -------
    calibrated_phase: numpy.array(n) or list(n) of float
        Array of calibrated phase values (between min_phase_th and max_phase_th)
        (in °)
    result: dict
        Result parameters of the phase calibration
    figs: list(2) of figure
        List of figure object: phase variation and histogram figure
    """
    pha_corr = dict_pha["corr"]
    assert pha_corr in ['raw', 'affine', 'offset', 'up_down'], \
        "'pha_corr' should be 'raw', 'affine', 'offset', 'up_down'"

    # Theoretical nanoloop analysis: generate phase dictionary
    if 'counterclockwise' not in dict_pha.keys():
        dict_pha = gen_dict_pha(
            dict_pha, pha_corr, pha_fwd=dict_pha["pha fwd"],
            pha_rev=dict_pha["pha rev"], func=dict_pha['func'],
            main_elec=dict_pha["main elec"],
            locked_elec_slope=dict_pha["locked elec slope"])

    # No calibration for raw mode
    if pha_corr == 'raw':
        result = {'corr': pha_corr, 'func': dict_pha['func']}
        calibrated_phase = phase
        res_figs = []
        return calibrated_phase, result, res_figs

    # Hysteresis analysis rotation / polarisation analysis
    # (Neumayer et al.: doi: 10.1063 / 5.0011631)
    else:
        # Theoretical nanoloop analysis: Match phase, bias and polarisation
        bias_pola_target, bias_pha_target = theoretical_phase_analysis(
            dict_pha, mode=dict_str["label"])

        # Experimental variation of phase with bias
        fig_pha, positive_pha_grad = phase_bias_grad(
            phase, write_voltage, dict_str=dict_str,
            bias_pola_target=bias_pola_target, bias_pha_target=bias_pha_target,
            make_plots=make_plots)

        filtered_phase = list(filter(None, phase))
        fig_hist, ax_hist, hist_vect, hist = histo_init(
            filtered_phase, dict_str=dict_str, make_plots=make_plots)

        # Find main phase peaks
        res = find_main_peaks(hist_vect, hist, 2, make_plots=make_plots,
                              ax=ax_hist, dist_min=int(len(hist_vect) / 5))
        if make_plots:
            plot_main_peaks(ax_hist, hist_vect, hist, res)

        # If error in peak detection
        if len(res['main peaks']) == 0 or len(res['main peaks']) > 2:
            print("Error in peak detection in phase histogram for phase "
                  "analysis: no phase difference can be calculated for phase "
                  "analysis")
            # Stop calibration
            pha_corr = 'raw'
            result = {'corr': pha_corr, "func": dict_pha["func"]}
            calibrated_phase = phase
            res_figs = []
            return calibrated_phase, result, res_figs
        # If 1 or 2 peaks are detected
        else:
            # Try to fit 1 or 2 phase peaks on phase histogram
            fit_res = None
            histo_phase_method = get_setting('histo_phase_method')
            if histo_phase_method == 'fit':
                try:
                    fit_res = fit_peaks_hist(
                        res, hist_vect, hist, make_plots=make_plots, ax=ax_hist)
                except (ValueError, TypeError):
                    print("ValueError/TypeError management with except: "
                          "for phase analysis, error on gaussian fit peak, "
                          "no fit is performed. Analysis is performed with "
                          "maximum of peak")
                    pass
            # 1 peak is detected: unipolar analysis
            if len(res['main peaks']) == 1:
                print("Only one peak detected in phase histogram for phase "
                      "analysis: unipolar measurements, no phase difference "
                      "can be calculated for phase analysis.\n"
                      "Please be careful to adjust the parameter value "
                      "'unipolar_phase_revert' in settings.json based on "
                      "phase analysis performed on a bipolar nanoloop or on "
                      "theoretical analysis of nanoloop depending on "
                      "measurement condition")
                peak_phase_max = hist_vect[res['main peaks'][0]]
                peak_phase_fit = fit_res[0] if fit_res is not None else None
                reverted = get_setting("unipolar_phase_revert")
                diff_phase_max = None
                diff_phase_fit = None
                coef_a = 1 if reverted is False else -1
                bias_pha_meas = unipolar_revert_analysis(
                    peak_phase_max, dict_pha['pha fwd'], dict_pha['pha rev'],
                    dict_pha['grounded tip'], dict_pha['positive d33'],
                    bias_pha_target, reverted, peak_phase_fit=peak_phase_fit)
            # 2 peaks detected: bipolar analysis
            else:
                coef_a = None
                peak_phase_max = (hist_vect[res['main peaks'][0]],
                                  hist_vect[res['main peaks'][1]])
                diff_phase_max = abs(peak_phase_max[1] - peak_phase_max[0])
                peak_phase_fit = (fit_res[0], fit_res[1]) \
                    if fit_res is not None else None
                diff_phase_fit = abs(peak_phase_fit[1] - peak_phase_fit[0]) \
                    if fit_res is not None else None
                # Determine if phase in reverted or not
                bias_pha_meas, reverted = bipolar_revert_analysis(
                    peak_phase_max, bias_pha_target,
                    positive_pha_grad, peak_phase_fit=peak_phase_fit)
            if make_plots:
                annotate_histo(
                    fig_hist, ax_hist, dict_pha, bias_pha_meas,
                    bias_pola_target, hist, len(res['main peaks']), reverted,
                    diff_phase_max=diff_phase_max,
                    diff_phase_fit=diff_phase_fit)
            # Calibrated phase determination
            calibrated_phase, result = correct_phase_val(
                phase, bias_pha_meas, bias_pha_target, pha_corr=pha_corr,
                coef_a=coef_a, reverted=reverted, make_plots=make_plots,
                fig=fig_hist)
            result["func"] = dict_pha["func"]
            res_figs = [fig_pha, fig_hist]
            return calibrated_phase, result, res_figs


def gen_dict_pha(meas_pars, pha_corr, pha_fwd=0, pha_rev=180, func=None,
                 main_elec=True, locked_elec_slope=None):
    """
    Generate a dictionary with phase calibration parameters

    Parameters
    ----------
    meas_pars: dict
        Dictionary with measurement parameters
    pha_corr: str
        Correction mode for the calibration of phase nanoloop:
        - 'raw': no correction
        - 'offset': offset correction
        - 'affine': affine correction
        - 'up_down': phase = up val or phase = down val
    pha_fwd: float, optional
        Forward phase value (default is 0)
    pha_rev: float, optional
        Reverse phase value (default is 180)
    func: callable, optional
        Function to apply to the phase values to determine piezoresponse
        (default is np.cos)
    main_elec: bool, optional
        If True, electrostatic component is dominating in On Field mode is used
        (default is True)
    locked_elec_slope: str, optional
        Electrostatic slope sign is locked with this parameter

    Returns
    -------
    dict_pha: dict
        Dict used for phase calibration
    """
    func = func or np.cos
    func = eval(func) if isinstance(func, str) else func

    try:
        if meas_pars['SSPFM Bias app'].lower() == 'sample':
            grounded_tip = True
        elif meas_pars['SSPFM Bias app'].lower() == 'tip':
            grounded_tip = False
        else:
            raise IOError('"Bias app" in [\'Sample\',\'Tip\']')
    except KeyError:
        grounded_tip = meas_pars['grounded tip']

    try:
        if meas_pars['Sign of d33'].lower() == 'positive':
            positive_d33 = True
        elif meas_pars['Sign of d33'].lower() == 'negative':
            positive_d33 = False
        else:
            raise IOError('"Sign of d33" in [\'positive\',\'negative\']')
    except KeyError:
        positive_d33 = meas_pars['positive d33']

    counterclockwise = (positive_d33 and grounded_tip) or \
                       (not positive_d33 and not grounded_tip)

    dict_pha = {
        'grounded tip': grounded_tip,
        'positive d33': positive_d33,
        'counterclockwise': counterclockwise,
        'main elec': main_elec,
        'corr': pha_corr,
        'pha fwd': pha_fwd,
        'pha rev': pha_rev,
        'func': func,
        'locked elec slope': locked_elec_slope
    }

    return dict_pha


def theoretical_phase_analysis(dict_pha, mode):
    """
    Perform theoretical phase analysis: match phase, bias and polarisation.

    Parameters
    ----------
    dict_pha: dict
        Used for phase calibration
    mode: str
        Measurement mode: 'On field' or 'Off field'

    Returns
    -------
    bias_pola_target: dict
        Dictionary with bias and polarisation match
    bias_pha_target: dict
        Dictionary with bias and phase match
    """
    bias_pola_target, bias_pha_target = {}, {}
    if dict_pha["grounded tip"]:
        bias_pola_target["low"] = "down"
        bias_pola_target["high"] = "up"
    else:
        bias_pola_target["low"] = "up"
        bias_pola_target["high"] = "down"
    # Valid only for a majority electrostatic component in on field
    # (the electrostatic component imposes the phase value)
    if mode == 'On field' and dict_pha["main elec"]:
        if dict_pha["locked elec slope"] == "positive":
            bias_pha_target["low"] = dict_pha["pha rev"]
            bias_pha_target["high"] = dict_pha["pha fwd"]
        elif dict_pha["locked elec slope"] == "negative":
            bias_pha_target["low"] = dict_pha["pha fwd"]
            bias_pha_target["high"] = dict_pha["pha rev"]
        elif dict_pha["locked elec slope"] is None:
            # Grounded tip -> negative slope of electrostatic component
            if dict_pha["grounded tip"]:
                bias_pha_target["low"] = dict_pha["pha fwd"]
                bias_pha_target["high"] = dict_pha["pha rev"]
            # Grounded bottom -> positive slope of electrostatic component
            else:
                bias_pha_target["low"] = dict_pha["pha rev"]
                bias_pha_target["high"] = dict_pha["pha fwd"]
        else:
            raise NotImplementedError("locked_elec_slope should be None "
                                      "or 'negative' or 'positive'")
    else:
        if dict_pha['counterclockwise']:
            bias_pha_target["low"] = dict_pha["pha rev"]
            bias_pha_target["high"] = dict_pha["pha fwd"]
        else:
            bias_pha_target["low"] = dict_pha["pha fwd"]
            bias_pha_target["high"] = dict_pha["pha rev"]

    return bias_pola_target, bias_pha_target


def phase_bias_grad(phase, write_voltage, bias_pola_target=None,
                    bias_pha_target=None, dict_str=None, make_plots=False):
    """
    Analysis of the phase variation with write voltage values

    Parameters
    ----------
    phase: numpy.array(n) or list(n) of float
        Array of phase values (in °)
    write_voltage: numpy.array(n) or list(n) of float
        Array of write voltage for all the loops (V)
    bias_pola_target: dict, optional
        Dictionary with bias and polarisation match
    bias_pha_target: dict, optional
        Dictionary with bias and phase match
    dict_str: dict, optional
        Dict used for figure annotation
    make_plots: bool, optional
        Activation key for matplotlib figures generation

    Returns
    -------
    fig: plt.figure or []
        Figure object or empty list
    positive_pha_grad: bool
        If True, phase increases with voltage and vice versa
    """
    mode = dict_str.get("label", 'Off field') if dict_str else 'Off field'

    # Set write voltage and phase for analysis
    reduced_write_voltage = []
    index_write = []
    for _, elem in enumerate(write_voltage):
        if elem not in reduced_write_voltage:
            reduced_write_voltage.append(elem)
            index_write.append(
                [cont_v for cont_v, elem_v in enumerate(write_voltage) if
                 elem == elem_v])
    mean_pha = []
    for indices in index_write:
        valid_phases = [phase[sub_elem] for sub_elem in indices if
                        phase[sub_elem] is not None]
        if valid_phases:
            mean_pha.append(np.mean(valid_phases))
        else:
            mean_pha.append(None)
    dictio = dict(zip(reduced_write_voltage, mean_pha))
    reduced_write_voltage = sorted(dictio.keys())
    mean_pha = [dictio[key] for key in reduced_write_voltage]

    # Calcul gradient
    grad_mean_pha = np.gradient(mean_pha, reduced_write_voltage)
    positive_pha_grad = np.mean(grad_mean_pha) >= 0

    if make_plots:
        fig = plot_phase_bias_grad(
            reduced_write_voltage, mean_pha, grad_mean_pha, positive_pha_grad,
            mode, bias_pola_target=bias_pola_target,
            bias_pha_target=bias_pha_target, dict_str=dict_str)
    else:
        fig = []

    return fig, positive_pha_grad


def fit_peaks_hist(res, hist_vect, hist, make_plots=False, ax=None):
    """
    Fit the two main histogram peaks parameters

    Parameters
    ----------
    res: dict
        Dict of two main histogram peaks parameters
    hist_vect: numpy.array(int(m/4)) or list(int(m/4)) of float
        Array of x values for histogram (in °)
    hist: numpy.array(int(m/4)) or list(int(m/4)) of int
        Array of y values for histogram: count
    make_plots: bool, optional
        Activation key for matplotlib figures generation
    ax: plt.axes, optional
        Axes of the figure

    Returns
    -------
    peak_1_pha: float
        Phase value for the 1st hist phase peak determined with fit (in °)
    peak_2_pha: float
        Phase value for the 2nd hist phase peak determined with fit (in °)
    """
    fit_results = []

    # Fit histogram peaks
    fit_xy = {'x': {}, 'y': {}, 'y fit': {}}
    for i, index in enumerate(res['main']):
        ind_min, ind_max = res['lim'][0][index], res['lim'][1][index]
        fit_xy['x'][str(i+1)] = hist_vect[ind_min:ind_max]
        y_data_inter = hist[ind_min:ind_max]
        fit_xy['y'][str(i+1)] = y_data_inter - np.mean(hist)

        # Peak fit
        gaussian_peak = GaussianPeakFit()
        gaussian_peak.fit(np.array(fit_xy['x'][str(i+1)]),
                          np.array(fit_xy['y'][str(i+1)]))
        fit_xy['y fit'][str(i+1)] = \
            gaussian_peak.eval(np.array(fit_xy['x'][str(i+1)])) + np.mean(hist)

        # Determine peak phase
        peak_pha = fit_xy['x'][str(i+1)][np.argmax(fit_xy['y fit'][str(i+1)])]
        fit_results.append(peak_pha)

        if make_plots:
            label = 'fit of the peak' if i == 0 else ''
            xy_coor = \
                fit_xy['x'][str(i+1)][np.argmax(fit_xy['y fit'][str(i+1)])]
            point_max = max(fit_xy['y fit'][str(i+1)])
            ax.plot(fit_xy['x'][str(i+1)], fit_xy['y fit'][str(i+1)], 'k--',
                    label=label)
            ax.plot(xy_coor, point_max, 'ko', ms=10)
            ax.annotate(f'{xy_coor:.1f}', xy=(xy_coor, point_max),
                        xytext=(xy_coor + res['offset'][0],
                                point_max - res['offset'][1]),
                        arrowprops={'facecolor': 'black'}, c='k',
                        size=15, weight='heavy')
    return fit_results


def unipolar_revert_analysis(peak_phase_max, pha_fwd_target, pha_rev_target,
                             grounded_tip, positive_d33, bias_pha_target,
                             reverted, peak_phase_fit=None):
    """
    Perform unipolar phase revert analysis.

    Parameters
    ----------
    peak_phase_max: float
        Phase value determined with peak maximum
    pha_fwd_target: float
        Forward phase target
    pha_rev_target: float
        Revert phase target
    grounded_tip: bool
        Flag indicating grounded tip
    positive_d33: bool
        Flag indicating positive d33
    bias_pha_target: dict
        Dictionary containing bias and phase target
    reverted: bool
        Flag indicating if phase is reverted
    peak_phase_fit: float, optional
        Phase value determined with peak fit (default is None)

    Returns
    -------
    bias_pha_meas: dict
        Dictionary with two measured phase values corresponding to low and
        high bias
    """
    peak_phase = peak_phase_fit \
        if peak_phase_fit is not None else peak_phase_max
    # Generate dictionary dict_bias_pha_str to find a second imaginary to
    # determine the phase value corresponding to the second imaginary phase peak
    pha_bias_target = {'high': str(bias_pha_target['high']),
                       'low': str(bias_pha_target['low'])}
    pha_bias_target = {v: k for k, v in pha_bias_target.items()}
    pha_val_target = {str(pha_fwd_target): 'pha fwd',
                      str(pha_rev_target): 'pha rev'}
    dict_bias_pha_str = {v: pha_val_target[k]
                         for k, v in pha_bias_target.items()}

    # coef calculated to adjust phase attribution values
    target_sign = np.sign(pha_fwd_target - pha_rev_target)
    coef = 1 if reverted else -1
    coef *= -1 if grounded_tip else 1
    coef *= -1 if not positive_d33 else 1

    # Determine experimental phase values (forward and revert)
    if target_sign == -1:
        if pha_rev_target < peak_phase < pha_fwd_target:
            dict_pha_val_meas = {'pha fwd': peak_phase,
                                 'pha rev': peak_phase-coef*180}
        elif peak_phase <= pha_rev_target:
            dict_pha_val_meas = {'pha fwd': peak_phase+coef*180,
                                 'pha rev': peak_phase}
        elif peak_phase >= pha_fwd_target:
            dict_pha_val_meas = {'pha fwd': peak_phase+coef*180,
                                 'pha rev': peak_phase}
    elif target_sign == 1:
        if pha_fwd_target < peak_phase < pha_fwd_target:
            dict_pha_val_meas = {'pha fwd': peak_phase,
                                 'pha rev': peak_phase+coef*180}
        elif peak_phase <= pha_fwd_target:
            dict_pha_val_meas = {'pha fwd': peak_phase-coef*180,
                                 'pha rev': peak_phase}
        elif peak_phase >= pha_rev_target:
            dict_pha_val_meas = {'pha fwd': peak_phase-coef*180,
                                 'pha rev': peak_phase}

    # Create dict_bias_pha_str dictionary
    bias_pha_meas = {key: dict_pha_val_meas[value]
                     for key, value in dict_bias_pha_str.items()}

    return bias_pha_meas


def bipolar_revert_analysis(peak_phase_max, bias_pha_target, positive_pha_grad,
                            peak_phase_fit=None):
    """
    Perform bipolar phase analysis and detect phase inversion.

    Parameters
    ----------
    peak_phase_max: list or tuple
        Peak phase values determined with peak maximum
    bias_pha_target: dict
        Dictionary with two target phase values corresponding to low and
        high bias
    positive_pha_grad: bool
        Indicates whether the phase gradient is positive
    peak_phase_fit: list, optional
        List of peak phase values determined with peak fit

    Returns
    -------
    bias_pha_meas: dict
        Dictionary with two measured phase values corresponding to low and
        high bias
    reverted: bool
        Indicates whether phase inversion occurred
    """
    # Up and down phase value
    bias_pha_meas = {}
    # Determined with fit
    if peak_phase_fit is not None:
        if positive_pha_grad:
            bias_pha_meas["low"] = min(peak_phase_fit)
            bias_pha_meas["high"] = max(peak_phase_fit)
        else:
            bias_pha_meas["low"] = max(peak_phase_fit)
            bias_pha_meas["high"] = min(peak_phase_fit)
    # Determined with max of peak
    elif peak_phase_max is not None:
        if positive_pha_grad:
            bias_pha_meas["low"] = min(peak_phase_max)
            bias_pha_meas["high"] = max(peak_phase_max)
        else:
            bias_pha_meas["low"] = max(peak_phase_max)
            bias_pha_meas["high"] = min(peak_phase_max)

    # Detect phase inversion
    meas_sign = np.sign(bias_pha_meas['high'] - bias_pha_meas['low'])
    target_sign = np.sign(bias_pha_target['high'] - bias_pha_target['low'])
    reverted = not (meas_sign == target_sign)

    return bias_pha_meas, reverted


def correct_phase_val(phase, bias_pha_meas, bias_pha_target, pha_corr,
                      coef_a=None, coef_b=None, reverted=False,
                      make_plots=False, fig=None):
    """
    Perform phase value treatment for bipolar set of phase value, with
    selected mode and calibration parameters

    Parameters
    ----------
    phase: numpy.array(n) or list(n) of float
        Array of phase values (in °)
    bias_pha_meas: dict
        Dictionary with two measured phase values corresponding to low and
        high bias
    bias_pha_target: dict
        Dictionary with two target phase values corresponding to low and
        high bias
    pha_corr: str
        Correction mode for the value of phase nanoloop:
        - 'raw': no correction
        - 'offset': offset correction
        - 'affine': affine correction
        - 'up_down': phase = up val or phase = down val
    coef_a: float, optional
        Coefficient a for affine correction (default is None)
    coef_b: float, optional
        Coefficient b for affine correction (default is None)
    reverted: bool, optional
        If True, phase up and down values are reverted (default is False)
    make_plots: bool, optional
        Activation key for matplotlib figures generation (default is False)
    fig: plt.figure, optional
        Histogram figure (default is None)

    Returns
    -------
    treat_phase: numpy.array(n) or list(n) of float
        Array of treated phase values (between min_phase_th and max_phase_th)
        (in °)
    result: dict
       Result parameters of the phase calibration
    """
    target_meas_pha = [(list(bias_pha_meas.values())[0],
                        list(bias_pha_target.values())[0]),
                       (list(bias_pha_meas.values())[1],
                        list(bias_pha_target.values())[1])]
    meas_threshold = np.mean(list(bias_pha_meas.values()))
    target_threshold = np.mean([target_meas_pha[1][1], target_meas_pha[0][1]])

    if pha_corr == 'offset':
        coef_a = coef_a or -1 if reverted else 1
        coef_b = coef_b or target_threshold - coef_a * meas_threshold
        treat_phase = [elem * coef_a + coef_b if elem is not None else None for
                       elem in phase]
        text_label_1 = f'offset computed = ({coef_a})*x + {coef_b:.1f},'
        pha_1 = bias_pha_meas["high"] * coef_a + coef_b
        pha_2 = bias_pha_meas["low"] * coef_a + coef_b
        text_label_2 = f'new value = [{pha_1:.1f}, {pha_2:.1f}]'
        result = {'corr': pha_corr,
                  'reverse': reverted,
                  'coefs': [coef_a, coef_b],
                  'dict phase target': bias_pha_target,
                  'dict phase meas': bias_pha_meas}

    elif pha_corr == 'affine':
        num = abs(target_meas_pha[1][1] - target_meas_pha[0][1])
        denom = abs(target_meas_pha[1][0] - target_meas_pha[0][0])
        coef_a = coef_a or - num / denom if reverted else num / denom
        coef_b = coef_b or \
            target_meas_pha[0][1] - coef_a * target_meas_pha[0][0]
        treat_phase = [elem * coef_a + coef_b for elem in phase]
        text_label_1 = f'affine computed = ({coef_a:.3f})*x + ({coef_b:.1f})'
        pha_1 = bias_pha_meas["high"] * coef_a + coef_b
        pha_2 = bias_pha_meas["low"] * coef_a + coef_b
        text_label_2 = f'new value = [{pha_1:.1f}, {pha_2:.1f}]'
        result = {'corr': pha_corr,
                  'reverse': reverted,
                  'coefs': [coef_a, coef_b],
                  'dict phase target': bias_pha_target,
                  'dict phase meas': bias_pha_meas}

    elif pha_corr == 'up_down':
        if reverted:
            treat_phase = [np.min(list(bias_pha_target.values())) if
                           elem >= meas_threshold else
                           np.max(list(bias_pha_target.values()))
                           for elem in phase]
        else:
            treat_phase = [np.max(list(bias_pha_target.values())) if
                           elem >= meas_threshold else
                           np.min(list(bias_pha_target.values()))
                           for elem in phase]
        text_label_1 = ''
        text_label_2 = f'new value = [{bias_pha_target["low"]:.1f}, ' \
                       f'{bias_pha_target["high"]:.1f}]'

        result = {'corr': pha_corr,
                  'reverse': reverted,
                  'dict phase target': bias_pha_target,
                  'dict phase meas': bias_pha_meas}

    elif pha_corr == 'raw':
        result = {'corr': pha_corr,
                  'reverse': reverted,
                  'dict phase target': bias_pha_target,
                  'dict phase meas': bias_pha_meas}
        return phase, result

    else:
        raise IOError("'pha_corr' should be 'raw', 'affine', 'offset', "
                      "up_down'")

    # Annotate
    if make_plots:
        fig.text(0.65, 0.92, text_label_1, c='b', size=15, weight='heavy')
        fig.text(0.65, 0.89, text_label_2, c='b', size=15, weight='heavy')
        fig.legend(fontsize=15, loc='upper left')

    return treat_phase, result


def phase_offset_determination(phase, dict_str=None, make_plots=False):
    """
    Determine phase offset by refocusing phase histogram peaks

    Parameters
    ----------
    phase: list
        List of phase values
    dict_str: dict, optional
        Dictionary containing plot label and color (default is None)
    make_plots: bool, optional
        Flag to indicate whether to make plots (default is False)

    Returns
    -------
    phase_offset_val: float or None
        Phase offset value
    fig_hist: plt.figure
        Histogram figure
    """
    filtered_phase = list(filter(None, phase))
    fig_hist, ax_hist, hist_vect, hist = \
        histo_init(filtered_phase, dict_str=dict_str, make_plots=make_plots)

    # Find two phase peaks
    res = find_main_peaks(hist_vect, hist, 2,
                          dist_min=int(len(hist_vect) / 5))
    if make_plots:
        plot_main_peaks(ax_hist, hist_vect, hist, res)

    # If error in peak detection
    if len(res['main peaks']) == 0 or len(res['main peaks']) > 2:
        print("Error in peak detection in phase histogram for phase "
              "analysis: no phase difference can be calculated for phase "
              "analysis")
        phase_offset_val = None
    # If 1 or 2 peaks are detected
    else:
        # Try to fit 1 or 2 phase peaks on phase histogram
        histo_phase_method = get_setting('histo_phase_method')
        fit_res = None
        if histo_phase_method == 'fit':
            try:
                fit_res = fit_peaks_hist(
                    res, hist_vect, hist, make_plots=make_plots, ax=ax_hist)
            except (ValueError, TypeError):
                print("ValueError/TypeError management with except: "
                      "for phase analysis, error on gaussian fit peak, "
                      "no fit is performed. Analysis is performed with "
                      "maximum of peak")
                pass
        # 1 peak is detected: unipolar analysis
        if len(res['main peaks']) == 1:
            print("Only one peak detected in phase histogram for phase "
                  "analysis: unipolar measurements, no phase difference "
                  "can be calculated for phase analysis.")
            peak_phase = fit_res if fit_res is not None \
                else hist_vect[res['main peaks'][0]]
        else:
            peak_phase = fit_res if fit_res is not None \
                else (hist_vect[res['main peaks'][0]],
                      hist_vect[res['main peaks'][1]])

        # Phase offset to center the two peaks in phase measurement range
        phase_offset_val = float(np.mean(peak_phase))

    if make_plots and phase_offset_val is not None:
        refocused_phase_histo(ax_hist, hist_vect, hist, phase_offset_val,
                              make_plots=make_plots)

    return phase_offset_val, fig_hist


def mean_phase_offset(phase_offset_val):
    """
    Calculate mean phase offset

    Parameters
    ----------
    phase_offset_val: dict
        Dictionary containing phase offset values for a single file

    Returns
    -------
    mean_phase_offset_val: float or None
        Mean phase offset value
    """
    if phase_offset_val is not None:
        filtered_phase_offset = \
            list(filter(None, list(phase_offset_val.values())))
        if len(filtered_phase_offset) == 1:
            mean_phase_offset_val = filtered_phase_offset[0]
        elif len(filtered_phase_offset) == 2:
            if filtered_phase_offset[0] >= 0 and filtered_phase_offset[1] >= 0:
                mean_phase_offset_val = np.mean(filtered_phase_offset)
            elif filtered_phase_offset[0] < 0 and filtered_phase_offset[1] < 0:
                mean_phase_offset_val = np.mean(filtered_phase_offset)
            else:
                mean_phase_offset_val = np.mean(np.abs(filtered_phase_offset))
        else:
            mean_phase_offset_val = None
    else:
        mean_phase_offset_val = None

    return mean_phase_offset_val


def apply_phase_offset(phase, offset, phase_min=-180, phase_max=180):
    """
    Apply phase offset to a list of phase values.

    Parameters
    ----------
    phase : list of float
        List of phase values to be adjusted.
    offset : float
        Phase offset to be applied.
    phase_min : float, optional
        Minimum phase value, default is -180.
    phase_max : float, optional
        Maximum phase value, default is 180.

    Returns
    -------
    new_phase : list of float
        List of adjusted phase values.
    """

    phase_range = phase_max - phase_min
    new_phase_min = phase_min + offset
    new_phase_max = phase_max + offset
    new_phase = []
    for elem_pha in phase:
        phase_val = elem_pha
        if elem_pha < new_phase_min:
            phase_val += phase_range
        elif elem_pha > new_phase_max:
            phase_val -= phase_range
        new_phase.append(phase_val)

    return new_phase
