"""
Module used for nanoloop: - phase calibration
"""

import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.figure import plot_graph
from PySSPFM.utils.core.peak import find_main_peaks
from PySSPFM.utils.core.fitting import GaussianPeakFit

from PySSPFM.settings import FIGSIZE


def phase_calibration(phase, write_voltage, dict_pha, dict_str=None,
                      make_plots=False):
    """
    Convert a phase list in calibrated phase list up & down
    (between phase forward and phase reverse value)

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

    # No calibration for raw mode
    if pha_corr == 'raw':
        result = {'corr': pha_corr, 'func': dict_pha['func']}
        calibrated_phase = phase
        res_figs = []

    # Hysteresis analysis rotation / polarisation analysis
    # (Neumayer et al.: doi: 10.1063 / 5.0011631)
    else:
        bias_pola_target, pola_pha_target, bias_pha_target = {}, {}, {}
        if dict_pha["grounded tip"]:
            bias_pola_target["low"] = "down"
            bias_pola_target["high"] = "up"
        else:
            bias_pola_target["low"] = "up"
            bias_pola_target["high"] = "down"

        # Valid only for a majority electrostatic component
        # (the electrostatic component imposes the phase value)
        if dict_str["label"] == 'On field' and dict_pha["main elec"]:
            if dict_pha["locked elec slope"] is None:
                # Grounded tip -> negative slope of electrostatic component
                if dict_pha["grounded tip"]:
                    pola_pha_target["down"] = dict_pha["pha fwd"]
                    pola_pha_target["up"] = dict_pha["pha rev"]
                # Grounded bottom -> positive slope of electrostatic component
                else:
                    pola_pha_target["down"] = dict_pha["pha rev"]
                    pola_pha_target["up"] = dict_pha["pha fwd"]
            elif dict_pha["locked elec slope"] == "positive":
                pola_pha_target["down"] = dict_pha["pha rev"]
                pola_pha_target["up"] = dict_pha["pha fwd"]
            elif dict_pha["locked elec slope"] == "negative":
                pola_pha_target["down"] = dict_pha["pha fwd"]
                pola_pha_target["up"] = dict_pha["pha rev"]
            else:
                raise NotImplementedError("locked_elec_slope should be None "
                                          "or 'negative' or 'positive'")
        else:
            if dict_pha["positive d33"]:
                pola_pha_target["down"] = dict_pha["pha rev"]
                pola_pha_target["up"] = dict_pha["pha fwd"]
            else:
                pola_pha_target["down"] = dict_pha["pha fwd"]
                pola_pha_target["up"] = dict_pha["pha rev"]
        for key, value in bias_pola_target.items():
            bias_pha_target[key] = pola_pha_target[value]

        # Variation of phase with bias
        fig_pha, positive_pha_grad = phase_analysis(
            phase, write_voltage, dict_str=dict_str,
            bias_pola_target=bias_pola_target, bias_pha_target=bias_pha_target,
            make_plots=make_plots)

        filtered_phase = list(filter(None, phase))
        fig_hist, ax_hist, hist_vect, hist = histo_init(
            filtered_phase, dict_str=dict_str, make_plots=make_plots)

        peak_phase_fit = None
        peak_phase_max = None
        diff_phase_fit = None
        diff_phase_max = None
        try:
            # Find two phase peaks
            res = find_main_peaks(hist_vect, hist, 2, make_plots=make_plots,
                                  ax=ax_hist, dist_min=int(len(hist_vect) / 5))
            peak_phase_max = (hist_vect[res['peaks'][res['main'][0]]],
                              hist_vect[res['peaks'][res['main'][1]]])
            diff_phase_max = abs(peak_phase_max[1] - peak_phase_max[0])
            histo_phase_method = get_setting('histo phase method')
            if histo_phase_method == 'fit':
                try:
                    # Fit two phase peaks
                    peak_1_pha, peak_2_pha = fit_peak_hist(
                        res, hist_vect, hist, make_plots=make_plots, ax=ax_hist)
                    peak_phase_fit = (peak_1_pha, peak_2_pha)
                    diff_phase_fit = abs(peak_phase_fit[1] - peak_phase_fit[0])
                except (ValueError, TypeError):
                    print("ValueError/TypeError management with except: "
                          "for phase analysis, error on gaussian fit peak, "
                          "no fit is performed. Phase difference is "
                          "performed with maximum of peak")
                    pass
        except (ValueError, IndexError):
            print("ValueError/TypeError management with except: no phase "
                  "difference can be calculated for phase analysis")
            pass

        # Up and down phase value
        bias_pha_meas = {}
        # Determined with fit
        if peak_phase_fit is not None:
            if positive_pha_grad:
                bias_pha_meas["low"] = peak_phase_fit[0]
                bias_pha_meas["high"] = peak_phase_fit[1]
            else:
                bias_pha_meas["low"] = peak_phase_fit[1]
                bias_pha_meas["high"] = peak_phase_fit[0]
        # Determined with max of peak
        elif peak_phase_max is not None:
            if positive_pha_grad:
                bias_pha_meas["low"] = peak_phase_max[0]
                bias_pha_meas["high"] = peak_phase_max[1]
            else:
                bias_pha_meas["low"] = peak_phase_max[1]
                bias_pha_meas["high"] = peak_phase_max[0]
        # If error: stop calibration
        else:
            pha_corr = 'raw'
            result = {'corr': pha_corr, "func": dict_pha["func"]}
            calibrated_phase = phase
            res_figs = []
            return calibrated_phase, result, res_figs

        # Detect phase inversion
        meas_sign = np.sign(bias_pha_meas['high'] - bias_pha_meas['low'])
        target_sign = np.sign(bias_pha_target['high'] - bias_pha_target['low'])
        reverted = not (meas_sign == target_sign)

        if make_plots:

            if dict_pha["grounded tip"]:
                pola_pha_meas = {"down": bias_pha_meas["low"],
                                 "up": bias_pha_meas["high"]}
            else:
                pola_pha_meas = {"up": bias_pha_meas["low"],
                                 "down": bias_pha_meas["high"]}

            pola_bias_target = {value: key for key, value in
                                bias_pola_target.items()}
            for annot, value in pola_pha_meas.items():
                txt = str(annot) + f" pola\n{pola_bias_target[annot]} bias"
                ax_hist.text(value, np.mean(hist), txt, c='r', size=15,
                             weight='heavy', ha='center', va='top')
            diff_phase_target = abs(dict_pha["pha rev"] - dict_pha["pha fwd"])
            try:
                txt = f'diff phase with fit = {diff_phase_fit:.1f} ' \
                      f'(expected = {diff_phase_target:.1f})'
                fig_hist.text(0.65, 0.95, txt, c='g', size=15, weight='heavy')
            except (ValueError, TypeError):
                pass
            try:
                txt = f'diff phase without fit = {diff_phase_max:.1f} ' \
                      f'(expected = {diff_phase_target:.1f})'
                fig_hist.text(0.65, 0.98, txt, c='g', size=15, weight='heavy')
            except (ValueError, TypeError):
                pass
            fig_hist.text(0.72, 0.02, f'Reverted phase value: {reverted}',
                          c='c', size=15, weight='heavy')

        # Calibrated phase
        calibrated_phase, result = corr_phase(
            phase, bias_pha_meas, bias_pha_target, pha_corr=pha_corr,
            reverted=reverted, make_plots=make_plots, fig=fig_hist)
        result["func"] = dict_pha["func"]
        res_figs = [fig_pha, fig_hist]

    return calibrated_phase, result, res_figs


def phase_analysis(phase, write_voltage, bias_pola_target=None,
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
        Dictionary with bias and polarization match
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
        fig, (ax_1, ax_2) = plt.subplots(1, 2, figsize=FIGSIZE)
        add = mode.lower().replace(' ', '_')
        fig.sfn = f'phase_analysis_{add}'
        fig.suptitle('Phase up & down analysis', size=24, weight='heavy')
        plot_dict = {'form': 'r+-', 'fs': 13, 'edgew': 3, 'tickl': 5,
                     'gridw': 1, 'title': 'Phase repartition with voltage',
                     'y lab': 'Mean phase [°]', 'x lab': 'Write voltage [V]'}
        plot_graph(ax_1, reduced_write_voltage, mean_pha, plot_dict=plot_dict)

        if bias_pola_target is not None:
            # Arrow for polarisation and phase target
            x_rel = 0.5
            delta_x_rel = 0.4
            y_rel = 0.5
            arrowstyle = '->, head_length=1.5, head_width=1.5'
            arrow_props = {"edgecolor": 'red', "arrowstyle": arrowstyle,
                           "linewidth": 10, "relpos": (0.5, 0.5)}
            len_x = ax_1.get_xlim()[1] - ax_1.get_xlim()[0]
            len_y = ax_1.get_ylim()[1] - ax_1.get_ylim()[0]
            x_text = ax_1.get_xlim()[0] + x_rel * len_x
            y_text = ax_1.get_ylim()[0] + y_rel * len_y
            delta_x = delta_x_rel * len_x
            x_arrow = x_text
            y_arrow = y_text
            txt = f"Polarization {bias_pola_target['low']}"
            if bias_pha_target is not None:
                txt += f"\n({bias_pha_target['low']} °)"
            ax_1.annotate(txt, xy=(x_text - delta_x, y_text),
                          xytext=(x_arrow - delta_x, y_arrow),
                          xycoords='data', textcoords='data', va='center',
                          ha='left', fontsize=12, fontweight='heavy',
                          arrowprops=arrow_props)
            txt = f"Polarization {bias_pola_target['high']}"
            if bias_pha_target is not None:
                txt += f"\n({bias_pha_target['high']} °)"
            ax_1.annotate(txt, xy=(x_text + delta_x, y_text),
                          xytext=(x_arrow + delta_x, y_arrow),
                          xycoords='data', textcoords='data', va='center',
                          ha='right', fontsize=12, fontweight='heavy',
                          arrowprops=arrow_props)

        # Plot phase gradient
        plot_dict.update({'form': 'm*-',
                          'title': 'Phase variation with voltage',
                          'y lab': 'Phase gradient'})
        plot_graph(ax_2, reduced_write_voltage, grad_mean_pha,
                   plot_dict=plot_dict)
        ax_2.axhline(y=0, ls='--', c='lime', label='gradient=0')
        ax_2.axhline(y=np.mean(grad_mean_pha), ls='--', c='c',
                     label='mean gradient')
        ax_2.legend(fontsize=plot_dict['fs'], loc='best')
        # Annotate
        annot = "positive" if positive_pha_grad else "negative"
        fig.text(0.72, 0.02, f'Phase gradient: {annot}', c='c', size=15,
                 weight='heavy')
        if dict_str:
            add_txt(fig, dict_str)
    else:
        fig = []

    return fig, positive_pha_grad


def histo_init(filtered_phase, dict_str=None, make_plots=False):
    """
    Initialize the histogram figure and data

    Parameters
    ----------
    filtered_phase: numpy.array(m=n-nb_err) or list(m=n-nb_-nb_err) of float
        Array of phase values with deleted errors (None values) (in °)
    dict_str: dict, optional
        Dict used for figure annotation
    make_plots: bool, optional
        Activation key for matplotlib figures generation

    Returns
    -------
    fig: plt.figure
        Figure of the histogram (generated when make_plots=True)
    ax: plt.axes
        Axes of the figure
    hist_vect: numpy.array(int(m/4)) or list(int(m/4)) of float
        Array of x values for histogram (in °)
    hist: numpy.array(int(m/4)) or list(int(m/4)) of int
        Array of y values for histogram: count
    """
    mode = dict_str["label"] if dict_str else 'Off field'

    discret = int(len(filtered_phase) / 4)
    hist_vect = np.linspace(min(filtered_phase), max(filtered_phase),
                            discret + 1)
    hist, _ = np.histogram(filtered_phase, bins=hist_vect)

    fig, ax = [], []
    if make_plots:
        fig, ax = plt.subplots(figsize=FIGSIZE)
        add = mode.lower().replace(' ', '_')
        fig.sfn = f'histo_phase_{add}'
        plot_dict = {'title': 'Histogram phase', 'x lab': 'Phase (°)',
                     'y lab': 'Count', 'form': 'c.-', 'lw': 1,
                     'legend': 'phase repartition'}
        plot_graph(ax, hist_vect[:-1], hist, plot_dict=plot_dict,
                   plot_leg=False)
        if dict_str:
            add_txt(fig, dict_str)

    return fig, ax, hist_vect[:-1], hist


def fit_peak_hist(res, hist_vect, hist, make_plots=False, ax=None):
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
    # Domain of two main hist peaks
    (ind1_min, ind1_max, ind2_min, ind2_max) = (
        res['lim'][0][0], res['lim'][1][0], res['lim'][0][1], res['lim'][1][1])

    # Fit two main hist peaks
    fit_xy = {'x': {}, 'y': {}, 'y fit': {}}
    for i, (ind_min, ind_max) in enumerate(zip([ind1_min, ind2_min],
                                               [ind1_max, ind2_max]), 1):
        fit_xy['x'][str(i)] = hist_vect[ind_min:ind_max]
        y_data_inter = hist[ind_min:ind_max]
        fit_xy['y'][str(i)] = y_data_inter - np.mean(hist)

        # Peak fit
        gaussian_peak = GaussianPeakFit()
        gaussian_peak.fit(np.array(fit_xy['x'][str(i)]),
                          np.array(fit_xy['y'][str(i)]))
        fit_xy['y fit'][str(i)] = \
            gaussian_peak.eval(np.array(fit_xy['x'][str(i)])) + np.mean(hist)

    tab = [fit_xy['x']['2'][np.argmax(fit_xy['y fit']['2'])],
           fit_xy['x']['1'][np.argmax(fit_xy['y fit']['1'])]]
    peak_1_pha, peak_2_pha = min(tab), max(tab)

    if make_plots:
        for i in range(1, 3):
            label = 'fit of the peak' if i == 1 else ''
            xy_coor = fit_xy['x'][str(i)][np.argmax(fit_xy['y fit'][str(i)])]
            point_max = max(fit_xy['y fit'][str(i)])
            ax.plot(fit_xy['x'][str(i)], fit_xy['y fit'][str(i)], 'k--',
                    label=label)
            ax.plot(xy_coor, point_max, 'ko', ms=10)
            ax.annotate(f'{xy_coor:.1f}', xy=(xy_coor, point_max),
                        xytext=(xy_coor + res['offset'][0],
                                point_max - res['offset'][1]),
                        arrowprops={'facecolor': 'black'}, c='k',
                        size=15, weight='heavy')

    return peak_1_pha, peak_2_pha


def corr_phase(phase, bias_pha_meas, bias_pha_target, pha_corr, coef_a=None,
               coef_b=None, reverted=False, make_plots=False, fig=None):
    """
    Perform phase value treatment with selected mode and calibration parameters

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


def add_txt(fig, dict_str):
    """
    Add annotations to figures

    Parameters
    ----------
    fig: plt.figure
        Figure object to annotate
    dict_str: dict
        Dictionary of annotations for the plot

    Returns
    -------
    None
    """
    if 'label' in dict_str and 'col' in dict_str:
        # Add label annotation with color
        fig.text(0.01, 0.85, dict_str["label"], c=dict_str["col"],
                 size=20, weight='heavy', backgroundcolor='black')

    if 'index' in dict_str:
        # Add file index annotation
        fig.text(0.01, 0.80, f'file n°{dict_str["index"]}', size=15,
                 weight='heavy')


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

    if meas_pars['Bias app'].lower() == 'sample':
        grounded_tip = True
    elif meas_pars['Bias app'].lower() == 'tip':
        grounded_tip = False
    else:
        raise IOError('"Bias app" in [\'Sample\',\'Tip\']')

    if meas_pars['Sign of d33'].lower() == 'positive':
        positive_d33 = True
    elif meas_pars['Sign of d33'].lower() == 'negative':
        positive_d33 = False
    else:
        raise IOError('"Sign of d33" in [\'positive\',\'negative\']')

    counterclockwise = bool(positive_d33) if grounded_tip else not positive_d33

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
