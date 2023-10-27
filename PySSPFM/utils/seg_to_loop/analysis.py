"""
Module used for the scripts of sspfm 1st step data analysis (conv seg to hyst)
    - Data analysis toolbox
"""

import numpy as np

from PySSPFM.utils.utils import get_setting
from PySSPFM.utils.core.noise import filter_mean
from PySSPFM.utils.core.peak import width_peak
from PySSPFM.utils.seg_to_loop.plot import plt_seg
from PySSPFM.utils.core.fitting import ShoPeakFit, ShoPhaseFit


class Segment:
    """
    Segment voltage of sspfm bias signal and associated amplitude and
    phase measure
    """

    def __init__(self, start_ind, end_ind, dict_meas, start_freq_init=200.,
                 end_freq_init=300., write_volt=0., read_volt=0.,
                 type_seg='read', mode='max', numb=0, cut_seg=None,
                 filter_order=None, fit_pars=None, guess_init=None):
        """
        Main function of the class

        Parameters
        ----------
        start_ind: int
            Starting index of the segment
        end_ind: int
            Ending index of the segment
        dict_meas: dict
            Dict of all measurement in extracted file
        start_freq_init: float, optional
            Starting frequency of the sweep (if max or fit mode) (in kHz)
        end_freq_init: float, optional
            Ending frequency of the sweep (if max or fit mode) (in kHz)
        write_volt: float, optional
            Write voltage value associated to the segment (in V)
        read_volt: float, optional
            Read voltage value associated to the segment (in V)
        type_seg: str, optional
            'read' or 'write' depending of segment type
        mode: str, optional
            Operating mode for analysis: three possible mode:
            - 'max' for analysis of the resonance with max peak value
            - 'fit' for analysis of the resonance with a SHO fit of the peak
            - 'dfrt' for analysis performed with the dfrt
        numb: int, optional
            Index associated to the segment
        cut_seg: dict, optional
            Dict of percent cut of the start and end of the segment
        filter_order: int
            Order of the filter for amplitude and phase in the segment
        fit_pars: dict, optional
            Dict of fit parameters (if fit mode)
        guess_init: dict, optional
            Dict of initial parameters to perform the fit (if fit mode)
        """
        assert type_seg in ['read', 'write']
        self.start_ind_init = start_ind
        self.end_ind_init = end_ind
        self.cut_seg = cut_seg
        (self.amp, self.pha, self.res_freq, self.q_fact, self.inc_amp,
         self.inc_pha, self.bckgnd) = (None, None, None, None, None, None, None)
        self.best_fit, self.pha_best_fit = [], []
        self.error = ''
        self.seg_infos = {
            'read volt': read_volt,
            'write volt': write_volt,
            'type': type_seg,
            'mode': mode,
            'index': numb,
            'start time': dict_meas['times'][start_ind],
            'end time': dict_meas['times'][end_ind]
        }
        self.len_init = self.end_ind_init - self.start_ind_init
        self.amp_tab_init = dict_meas['amp'][self.start_ind_init:
                                             self.end_ind_init]
        self.pha_tab_init = dict_meas['pha'][self.start_ind_init:
                                             self.end_ind_init]
        self.time_tab_init = dict_meas['times'][self.start_ind_init:
                                                self.end_ind_init]
        self.freq_tab_init = np.linspace(start_freq_init, end_freq_init,
                                         self.len_init, endpoint=False)

        # Cut beginning and end of the segment
        if cut_seg is None:
            self.start_ind = self.start_ind_init
            self.end_ind = self.end_ind_init
            self.len = self.len_init
            self.amp_tab = self.amp_tab_init
            self.pha_tab = self.pha_tab_init
            self.time_tab = self.time_tab_init
            self.freq_tab = self.freq_tab_init
        else:
            incr_start = int(cut_seg['start'] / 100 * self.len_init)
            incr_end = int(cut_seg['end'] / 100 * self.len_init)
            self.start_ind = self.start_ind_init + incr_start
            self.end_ind = self.end_ind_init - incr_end
            self.len = self.end_ind - self.start_ind
            self.amp_tab = dict_meas['amp'][self.start_ind:self.end_ind]
            self.pha_tab = dict_meas['pha'][self.start_ind:self.end_ind]
            self.time_tab = dict_meas['times'][self.start_ind:self.end_ind]
            self.freq_tab = self.freq_tab_init[incr_start:-incr_end]

        # Measure filtered
        if filter_order:
            self.amp_tab = filter_mean(self.amp_tab, filter_order)
            self.amp_tab_init = filter_mean(self.amp_tab_init, filter_order)
            self.pha_tab = filter_mean(self.pha_tab, filter_order)
            self.pha_tab_init = filter_mean(self.pha_tab_init, filter_order)

        # Segment treatment
        if mode == 'max':
            self.amp = max(self.amp_tab)
            self.pha = self.pha_tab[np.argmax(self.amp_tab)]
            self.res_freq = self.freq_tab[np.argmax(self.amp_tab)]
            self.q_fact = self.q_fact_max()
        elif mode == 'fit':
            self.treatment_fit(fit_pars=fit_pars, guess_init=guess_init)
        elif mode == 'dfrt':
            self.amp = np.mean(self.amp_tab)
            self.pha = np.mean(self.pha_tab)
            self.inc_amp = np.sqrt(np.var(self.amp_tab))
            self.inc_pha = np.sqrt(np.var(self.pha_tab))
        else:
            raise IOError('mode in [\'max\',\'fit\',\'dfrt\']')

    def treatment_fit(self, fit_pars=None, guess_init=None):
        """
        Treatment for fit mode

        Parameters
        ----------
        fit_pars: dict, optional
            Dict of fit parameters
        guess_init: list(5) of float, optional
            List of initial guess peak parameters for the fit

        Returns
        -------
        None
        """
        fit_pars = fit_pars or {
            'sens peak detect': 1.5,
            'detect peak': False,
            'fit pha': False
        }

        # Peak detection
        is_there_a_peak = True
        if fit_pars['detect peak']:
            is_there_a_peak = False
            threshold = np.mean(self.amp_tab) * fit_pars['sens peak detect']
            for elem in self.amp_tab:
                if elem > threshold:
                    is_there_a_peak = True
                    break

        # Signal (amp + phase) fitting
        if is_there_a_peak:
            try:
                self.peak_fit(guess_init)
                if fit_pars['fit pha']:
                    try:
                        self.phase_fit()
                    except (ValueError, IndexError):
                        print("ValueError/IndexError management with except: "
                              "error on phase fitting for segment analysis")
                        self.error += '_error phase fitting'
                        pass
            except KeyError:
                self.error += '_error amplitude fitting'
                print("KeyError management with except: "
                      "error on amplitude fitting for segment analysis")
        else:
            self.error += '_error no peak'
            print("No peak detected on the segment")

    def peak_fit(self, guess_init):
        """
        Function used to fit the resonance peak with SHO model

        Parameters
        ----------
        guess_init: list(5) of float, optional
            List of initial guess peak parameters for the fit

        Returns
        -------
        None
        """
        sho_peak = ShoPeakFit()
        if guess_init:
            init_pars = {
                "ampli": {"value": guess_init[0], "vary": True, "min": 0,
                          "max": None},
                "coef": {"value": guess_init[1], "vary": True, "min": 0,
                         "max": None},
                "x0": {"value": guess_init[2], "vary": True, "min": 0,
                       "max": None},
                "offset": {"value": guess_init[3], "vary": True, "min": 0,
                           "max": None},
                "slope": {"value": guess_init[4], "vary": False, "min": None,
                          "max": None}}
        else:
            init_pars = None
        sho_peak.fit(self.freq_tab, self.amp_tab, init_pars=init_pars)
        peak_pars = sho_peak.report_fit_results()

        # Extraction of parameters
        self.amp = peak_pars['ampli'].value * peak_pars['coef'].value
        self.res_freq = peak_pars['x0'].value
        self.bckgnd = peak_pars['offset'].value
        self.q_fact = peak_pars['coef'].value
        self.best_fit = sho_peak.eval(self.freq_tab)
        self.pha = self.pha_tab[np.argmax(self.best_fit)]

        # print and plot fit results
        # print(guess_init)
        # print(res_fit)
        # import matplotlib.pyplot as plt
        # plt.figure()
        # plt.plot(self.freq_tab, self.amp_tab)
        # plt.plot(self.freq_tab, self.best_fit)
        # plt.plot(self.freq_tab, peak.eval(self.freq_tab, guess_init))
        # plt.plot(self.res_freq, self.amp, 'sk')
        # plt.axvline(self.res_freq, ls=':', c='k')
        # plt.show()

    def phase_fit(self):
        """ Function used to fit the resonance phase with SHO model """
        # Reduce domain of phase signal to fit
        width = width_peak(
            self.freq_tab, self.best_fit, np.argmax(self.best_fit),
            (self.best_fit.max() - self.best_fit.min()) / 2 +
            self.best_fit.min()
        )
        ind_range = width['ind right'] - width['ind left']
        ind_left = width['ind left'] - ind_range * 2
        ind_right = width['ind right'] + ind_range * 2
        x = self.freq_tab[ind_left:ind_right]
        y = self.pha_tab[ind_left:ind_right]

        # Detect if there is a switch or not and sign of the function
        switch, coef_func = self.phase_fit_analysis(y)
        # Free parameters and guess init
        init_pars = {
            "ampli": {"value": coef_func * 180 / np.pi, "vary": True,
                      "min": 0 if coef_func == 1 else 2*coef_func * 180/np.pi,
                      "max": 0 if coef_func == -1 else 2*coef_func * 180/np.pi},
            "coef": {"value": self.q_fact, "vary": True,
                     "min": min(x) / (max(x) - min(x)), "max": None},
            "x0": {"value": self.res_freq, "vary": True,
                   "min": min(x), "max": max(x)},
            "offset": {"value": self.pha - coef_func * 90 * (not switch),
                       "vary": True, "min": min(y), "max": max(y)},
            "slope": {"value": 0, "vary": False, "min": None, "max": None}}
        # Creation of Curve and fit
        sho_phase = ShoPhaseFit(switch=switch)
        sho_phase.fit(x, y, init_pars=init_pars)
        # Extraction of parameters
        self.pha_best_fit = sho_phase.eval(self.freq_tab)
        self.pha = sho_phase.eval(self.res_freq)

        # print and plot fit results
        # print(guess_init)
        # print(res_fit)
        # import matplotlib.pyplot as plt
        # plt.figure()
        # plt.plot(self.freq_tab, self.pha_tab)
        # plt.plot(self.freq_tab, self.pha_best_fit)
        # plt.plot(self.freq_tab, pha_model.eval(self.freq_tab, guess_init))
        # plt.plot(self.res_freq, self.pha, 'hk')
        # plt.axvline(self.res_freq, ls=':', c='k')
        # plt.show()

    @staticmethod
    def phase_fit_analysis(y_val):
        """
        Analysis before fitting the phase signal to determine the appropriate
        model.

        Parameters
        ----------
        y_val: list(n) of float
            Reduced list of phase signal values in the domain of the peak BW
            (in °).

        Returns
        -------
        switch: bool
            True if there is a switch in the phase signal, False otherwise.
        coef_func: int
            Sign (1 or -1) of the phase model depending on the direction of
            variation of the function.
        """
        dif1 = abs(y_val[0] - y_val[-1])
        dif_y = [y_val[i + 1] - y_val[i] for i in range(len(y_val) - 1)]
        dif2 = max(abs(elem) for elem in dif_y)
        switch = dif2 > dif1

        if switch:
            coef_func = -1 if dif2 == max(dif_y) else 1
        else:
            coef_func = -1 if np.mean(y_val[:int(len(y_val) / 10)]) > np.mean(
                y_val[-int(len(y_val) / 10):]) else 1

        return switch, coef_func

    def q_fact_max(self):
        """
        Find the quality factor without peak fitting and return the quality
        factor.

        Parameters
        ----------

        Returns
        -------
        qual_factor: float or None
            The calculated quality factor if it can be determined, otherwise
            None.
        """
        thresh_amp = self.amp / np.sqrt(2)
        coord_wid = []
        for elem_freq, elem_amp in zip(self.freq_tab, self.amp_tab):
            if elem_amp >= thresh_amp:
                coord_wid.append(elem_freq)
                break
        for elem_freq, elem_amp in zip(self.freq_tab, self.amp_tab):
            if elem_freq >= self.res_freq:
                if elem_amp <= thresh_amp:
                    coord_wid.append(elem_freq)
                    break
        qual_factor = self.res_freq / (coord_wid[1] - coord_wid[0]) \
            if len(coord_wid) == 2 else np.nan

        return qual_factor


def zi_calib(amplitude_zi, phase_zi, meas_pars=None):
    """
    Convert output zhinst amplitude and phase (in V) to physical units.

    Parameters
    ----------
    amplitude_zi: list or numpy.array of float
        List of zhinst PFM amplitude measurements (in V).
    phase_zi: list or numpy.array of float
        List of zhinst PFM phase measurements (in V).
    meas_pars: dict, optional
        Dictionary of conversion sensibility and offset factors.
        Default is None.

    Returns
    -------
    amplitude: list of float
        List of PFM amplitude measurements after conversion (in a.u. or nm).
    phase: list of float
        List of PFM phase measurements after conversion (in °).
    """
    meas_pars = meas_pars or {
        'Sens 1': 1, 'Offset 1 [V]': 0,
        'Sens 2 [mV/°]': 1000, 'Offset 2 [V]': 0
    }
    amplitude = [(elem_amp - meas_pars['Offset 1 [V]']) / meas_pars['Sens 1']
                 for elem_amp in amplitude_zi]
    phase = [(elem_pha - meas_pars['Offset 2 [V]']) /
             (meas_pars['Sens 2 [mV/°]'] / 1000) for elem_pha in phase_zi]

    return amplitude, phase


def init_parameters(dict_meas, sign_pars, verbose=False, make_plots=False):
    """
    Correct the measurement file with corrected values of some parameters.

    Parameters
    ----------
    dict_meas: dict
        Dictionary of all measurements in the extracted file.
    sign_pars: dict
        Dictionary of sspfm bias signal parameters.
    verbose: bool, optional
        If True, print information on the number of segments. Default is False.
    make_plots: bool, optional
        If True, print graphs of the cut analysis. Default is False.

    Returns
    -------
    cut_dict: dict
        Dictionary of cut parameters.
    read_mode: str
        Application order of read voltage:
        - 'Low to High'
        - 'High to Low'
        - 'Single Read Step'
    """
    read_mode = sign_pars['Mode (R)']
    if sign_pars['Min volt (R) [V]'] == sign_pars['Max volt (R) [V]']:
        read_mode = 'Single Read Step'

    cut_dict = cut_function(dict_meas, sign_pars, verbose=verbose,
                            make_plots=make_plots)

    return cut_dict, read_mode


def cut_function(dict_meas, sign_pars, verbose=False, make_plots=False):
    """
    Function used for init_parameters function:
    Cut the measures in segment

    Parameters
    ----------
    dict_meas: dict
        Dictionary of all measurements in the extracted file.
    sign_pars: dict
        Dictionary of sspfm bias signal parameters.
    verbose: bool, optional
        If True, print information on the number of segments. Default is False.
    make_plots: bool, optional
        If True, print graphs of the cut analysis. Default is False.

    Returns
    -------
    cut_dict: dict
        Dictionary of cut parameters.
    """
    # Compute the last index of starting hold segment and first index of
    # ending hold segment
    hold_dict = index_hold_segment(dict_meas['times'])

    # Calculation of the number of segment and check if there is a problem
    # with the application of sspfm measure
    nb_segment = nb_measure_segment(dict_meas['times'], sign_pars, hold_dict)

    # Compute the list of time value for each beginning of on field and off
    # field segment
    index = generate_cut_time_values(hold_dict['index']['start'][1],
                                     sign_pars, nb_segment)

    # Time analysis
    experimental_time = dict_meas['times'][-1]
    start_hold_time_exp = dict_meas['times'][hold_dict['index']['start'][1] + 1]
    end_hold_time_exp = dict_meas['times'][-1] - dict_meas['times'][
        hold_dict['index']['end'][0] - 1]
    segment_time = (sign_pars['Seg durat (W) [ms]'] +
                    sign_pars['Seg durat (R) [ms]']) / 1000
    hold_time = start_hold_time_exp + end_hold_time_exp
    theoretical_time = int(nb_segment / 2) * segment_time + hold_time

    if verbose:
        print('------------')
        print('- Cut results')
        print(f'Theoretical total time = {theoretical_time} s')
        print(f'Experimental total time = {experimental_time} s')
        print(f'Experimental init hold time = {start_hold_time_exp} s')
        print(f'Experimental end hold time = {end_hold_time_exp} s')
        print(f'Total number of segment = {nb_segment}')
        print('------------')

    # Plot time function and holding segment to verify the analysis
    fig = plt_seg(dict_meas, hold_dict, index,
                  sign_pars) if make_plots else None

    return {
        'index hold': hold_dict['index'],
        'start hold seg': hold_dict['seg']['start'],
        'end hold seg': hold_dict['seg']['end'],
        'index on field': index['on f'],
        'index off field': index['off f'],
        'nb seg': nb_segment,
        'experimental time': experimental_time,
        'start hold time exp': start_hold_time_exp,
        'end hold time exp': end_hold_time_exp,
        'theoretical time': theoretical_time,
        'fig': fig
    }


def index_hold_segment(times):
    """
    This function is used by `cut_function` to compute the indices of the
    starting and ending hold segments.

    Parameters
    ----------
    times: list or numpy.array
        Array of time measurements (in seconds).

    Returns
    -------
    hold_dict: dict
        Dictionary containing the indices and segments for the starting and
        ending hold segments.
    """
    start_index_hold, end_index_hold = -1, 0
    dt_hold_start = round(times[1] - times[0], 9)
    dt_hold_end = round(times[-1] - times[-2], 9)
    start_hold_seg = []
    end_hold_seg = []

    for i in range(len(times) - 1):
        if round(times[i + 1] - times[i], 9) == dt_hold_start:
            start_index_hold += 1
            start_hold_seg.append(times[start_index_hold])
        else:
            break

    for i in range(len(times) - 1):
        if round(
                times[(len(times) - 1) - i] - times[(len(times) - 1) - (i + 1)],
                9) == dt_hold_end:
            end_index_hold += 1
            end_hold_seg.append(times[len(times) - end_index_hold])
        else:
            break

    end_index_hold = len(times) - end_index_hold

    return {
        'index': {
            'start': [0, start_index_hold],
            'end': [end_index_hold, len(times)]
        },
        'seg': {
            'start': start_hold_seg,
            'end': end_hold_seg
        }
    }


def nb_measure_segment(times, sign_pars, hold_dict):
    """
    This function is used by `cut_function` to compute the number of segments
    in the measure and check if there is a discrepancy between the theoretical
    and experimental number of samples.

    Parameters
    ----------
    times: list or numpy.array
        Array of time measurements (in seconds).
    sign_pars: dict
        Dictionary of sspfm bias signal parameters.
    hold_dict: dict
        Dictionary containing the indices and segments for the starting and
        ending hold segments.

    Returns
    -------
    nb_seg: int
        Number of segments in the measure (excluding the 2 hold segments).
    """
    nb_seg = (sign_pars['Nb volt (W)'] - 1) * 4 * sign_pars['Nb volt (R)']
    nb_seg_th = (sign_pars['Nb volt (W)'] - 1) * 2 * sign_pars['Nb volt (R)']
    nb_samp_th = (sign_pars['Seg sample (R)'] + sign_pars['Seg sample (W)'])
    nb_sample_th = nb_seg_th * nb_samp_th
    nb_sample_exp = len(times[hold_dict['index']['start'][1] +
                              1:hold_dict['index']['end'][0] - 1])

    detect_bug_segments = get_setting('detect bug segments')
    if nb_sample_th != nb_sample_exp and detect_bug_segments:
        print(f"Theoretical number of samples: {nb_sample_th}")
        print(f"Experimental number of samples: {nb_sample_exp}")
        print("Error with the application of ss_pfm_signal or parameters "
              "saving in the spm file")
        raise NotImplementedError

    return nb_seg


def generate_cut_time_values(start_ind_hold, sign_pars, nb_segment):
    """
    This function is used by `cut_function` to cut the measure into segments
    and compute the index values for each start of on field and off field
    segments.

    Parameters
    ----------
    start_ind_hold: int
        Last index of the starting hold segment.
    sign_pars: dict
        Dictionary of sspfm bias signal parameters.
    nb_segment: int
        Number of segments in the measure (excluding the 2 hold segments).

    Returns
    -------
    index: dict
        Dictionary of index values for each on and off field segment.
    """
    index_on_f, index_off_f = [], []
    seg_ite = sign_pars['Seg sample (W)'] + sign_pars['Seg sample (R)']

    for index_seg in range(int(nb_segment / 2)):
        seg_increment = start_ind_hold + 1 + index_seg * seg_ite
        index_on_f.append(seg_increment)

        seg_increment += sign_pars['Seg sample (W)']
        index_off_f.append(seg_increment)

    return {'off f': index_off_f, 'on f': index_on_f}
