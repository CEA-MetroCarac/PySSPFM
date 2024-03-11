"""
Module used for the scripts of sspfm 1st step data analysis
(convert datacube to nanoloop)
    - Data analysis toolbox
"""

import numpy as np

from PySSPFM.utils.core.basic_func import sho, sho_phase
from PySSPFM.utils.core.noise import filter_mean, butter_filter
from PySSPFM.utils.core.peak import width_peak
from PySSPFM.utils.core.fitting import ShoPeakFit, ShoPhaseFit


class SegmentInfo:
    """ Init all segment info (common for all Segment classes) """
    def __init__(self, start_ind, end_ind, times, write_volt=0.,
                 read_volt=0., type_seg='read',  mode='max', numb=0):
        """
        Class to initialize segment information.

        Parameters
        ----------
        start_ind: int
            Starting index of the segment
        end_ind: int
            Ending index of the segment
        times: array-like
            Array containing time values
        write_volt: float, optional
            Write voltage value associated to the segment (in V)
            (default is 0.0)
        read_volt: float, optional
            Read voltage value associated to the segment (in V)
            (default is 0.0)
        type_seg: str, optional
            Type of segment ('read' or 'write', default is 'read')
        mode: str, optional
            Operating mode for analysis: four possible modes:
            - 'max': for analysis of the resonance with max peak value
            (frequency sweep in resonance)
            - 'fit': for analysis of the resonance with a SHO fit of the peak
            (frequency sweep in resonance)
            - 'single_freq': for analysis performed at single frequency,
            average of segment (in or out of resonance)
            - 'dfrt': for analysis performed with dfrt, average of segment
        numb: int, optional
            Index number of the segment (default is 0)
        """
        assert type_seg in ['read', 'write']
        self.start_ind_init = start_ind
        self.end_ind_init = end_ind
        self.len_init = end_ind - start_ind
        self.seg_info = {
            'read volt': read_volt,
            'write volt': write_volt,
            'type': type_seg,
            'mode': mode,
            'index': numb,
            'start time': times[start_ind],
            'end time': times[end_ind]
        }


class SegmentSweep:
    """
    Segment voltage of sspfm bias signal and associated amplitude and
    phase measure for frequency sweep in resonance
    """

    def __init__(self, segment_info, dict_meas, start_freq_init=200.,
                 end_freq_init=300., cut_seg=None, filter_type=None,
                 filter_cutoff_frequency=None, filter_order=None, fit_pars=None,
                 guess_init=None):
        """
        Main function of the class

        Parameters
        ----------
        segment_info: SegmentInfo
            Instance of SegmentInfo class containing segment information
        dict_meas: dict
            All measurement in extracted file
        start_freq_init: float, optional
            Starting frequency of the sweep (if max or fit mode) (in kHz)
        end_freq_init: float, optional
            Ending frequency of the sweep (if max or fit mode) (in kHz)
        cut_seg: dict, optional
            Dict of percent cut of the start and end of the segment
        filter_type: str
            Type of the filter for amplitude and phase in the segment
        filter_cutoff_frequency: float or tuple
            Cutoff frequency of the filter for amplitude and phase in the
            segment
        filter_order: int
            Order of the filter for amplitude and phase in the segment
        fit_pars: dict, optional
            Dict of fit parameters (if fit mode)
        guess_init: dict, optional
            Dict of initial parameters to perform the fit (if fit mode)
        """
        (self.amp, self.pha, self.res_freq, self.q_fact, self.bckgnd) = \
            (None, None, None, None, None)
        self.best_fit, self.pha_best_fit = [], []
        self.error = ''
        self.segment_info = segment_info
        mode = segment_info.seg_info['mode']
        self.time_tab_init = dict_meas['times'][segment_info.start_ind_init:
                                                segment_info.end_ind_init]
        self.freq_tab_init = np.linspace(start_freq_init, end_freq_init,
                                         segment_info.len_init, endpoint=False)
        self.amp_tab_init = dict_meas['amp'][segment_info.start_ind_init:
                                             segment_info.end_ind_init]
        self.pha_tab_init = dict_meas['pha'][segment_info.start_ind_init:
                                             segment_info.end_ind_init]

        # Cut beginning and end of the segment
        if cut_seg is None:
            self.start_ind = segment_info.start_ind_init
            self.end_ind = segment_info.end_ind_init
            self.len = segment_info.len_init
            self.time_tab = self.time_tab_init
            self.freq_tab = self.freq_tab_init
            self.amp_tab = self.amp_tab_init
            self.pha_tab = self.pha_tab_init
        else:
            incr_start = int(cut_seg['start'] / 100 * segment_info.len_init)
            incr_end = int(cut_seg['end'] / 100 * segment_info.len_init)
            self.start_ind = segment_info.start_ind_init + incr_start
            self.end_ind = segment_info.end_ind_init - incr_end
            self.len = self.end_ind - self.start_ind
            self.time_tab = dict_meas['times'][self.start_ind:self.end_ind]
            incr_end = incr_end if incr_end != 0 else 1
            self.freq_tab = self.freq_tab_init[incr_start:-incr_end]
            self.amp_tab = dict_meas['amp'][self.start_ind:self.end_ind]
            self.pha_tab = dict_meas['pha'][self.start_ind:self.end_ind]

        # Measure filtered
        if filter_type == 'mean':
            self.amp_tab = filter_mean(self.amp_tab, filter_order)
            self.amp_tab_init = filter_mean(self.amp_tab_init, filter_order)
            self.pha_tab = filter_mean(self.pha_tab, filter_order)
            self.pha_tab_init = filter_mean(self.pha_tab_init, filter_order)
        elif filter_type in ['low', 'high', 'bandpass', 'bandstop']:
            sampling_frequency = \
                len(self.time_tab) / (self.time_tab[-1] - self.time_tab[0])
            self.amp_tab = butter_filter(
                self.amp_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.amp_tab_init = butter_filter(
                self.amp_tab_init, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.pha_tab = butter_filter(
                self.pha_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.pha_tab_init = butter_filter(
                self.pha_tab_init, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)

        # Segment treatment
        if mode == 'max':
            self.amp = max(self.amp_tab)
            self.pha = self.pha_tab[np.argmax(self.amp_tab)]
            self.res_freq = self.freq_tab[np.argmax(self.amp_tab)]
            self.q_fact = self.q_fact_max()
        elif mode == 'fit':
            self.treatment_fit(fit_pars=fit_pars, guess_init=guess_init)
        else:
            raise IOError('mode in [\'max\',\'fit\']')

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
            init_params = {
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
            init_params = None
        sho_peak.fit(self.freq_tab, self.amp_tab, init_params=init_params)
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
            self.freq_tab, self.best_fit, int(np.argmax(self.best_fit)),
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
        init_params = {
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
        sho_pha = ShoPhaseFit(switch=switch)
        sho_pha.fit(x, y, init_params=init_params)
        # Extraction of parameters
        self.pha_best_fit = sho_pha.eval(self.freq_tab)
        self.pha = sho_pha.eval(self.res_freq)

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


class SegmentStable:
    """
    Segment voltage of sspfm bias signal and associated amplitude and
    phase measure for dfrt or single frequency measure
    """

    def __init__(self, segment_info, dict_meas, cut_seg=None,
                 filter_type=None, filter_cutoff_frequency=None,
                 filter_order=None):
        """
        Main function of the class

        Parameters
        ----------
        segment_info: SegmentInfo
            Instance of SegmentInfo class containing segment information
        dict_meas: dict
            All measurement in extracted file
        cut_seg: dict, optional
            Dict of percent cut of the start and end of the segment
        filter_type: str
            Type of the filter for amplitude and phase in the segment
        filter_cutoff_frequency: float or tuple
            Cutoff frequency of the filter for amplitude and phase in the
            segment
        filter_order: int
            Order of the filter for amplitude and phase in the segment
        """
        (self.amp, self.pha, self.res_freq, self.inc_amp, self.inc_pha,
         self.inc_res_freq) = (None, None, None, None, None, None)
        self.segment_info = segment_info
        self.time_tab_init = dict_meas['times'][segment_info.start_ind_init:
                                                segment_info.end_ind_init]
        self.amp_tab_init = dict_meas['amp'][segment_info.start_ind_init:
                                             segment_info.end_ind_init]
        self.pha_tab_init = dict_meas['pha'][segment_info.start_ind_init:
                                             segment_info.end_ind_init]
        self.freq_tab_init = dict_meas.get('freq', None)
        self.freq_tab_init = dict_meas['freq'][segment_info.start_ind_init:
                                               segment_info.end_ind_init] \
            if self.freq_tab_init else None

        # Measure filtered
        if filter_type == 'mean':
            self.amp_tab_init = filter_mean(self.amp_tab_init, filter_order)
            self.pha_tab_init = filter_mean(self.pha_tab_init, filter_order)
            self.freq_tab_init = filter_mean(self.freq_tab_init, filter_order) \
                if self.freq_tab_init else None
        elif filter_type in ['low', 'high', 'bandpass', 'bandstop']:
            sampling_frequency = \
                len(self.time_tab_init) / (self.time_tab_init[-1] -
                                           self.time_tab_init[0])
            self.amp_tab_init = butter_filter(
                self.amp_tab_init, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.pha_tab_init = butter_filter(
                self.pha_tab_init, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.freq_tab_init = butter_filter(
                self.freq_tab_init, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order) if self.freq_tab_init else None

        # Cut beginning and end of the segment
        if cut_seg is None:
            self.start_ind = segment_info.start_ind_init
            self.end_ind = segment_info.end_ind_init
            self.len = segment_info.len_init
            self.time_tab = self.time_tab_init
            self.amp_tab = self.amp_tab_init
            self.pha_tab = self.pha_tab_init
            self.freq_tab = self.freq_tab_init
        else:
            incr_start = int(cut_seg['start'] / 100 * segment_info.len_init)
            incr_end = int(cut_seg['end'] / 100 * segment_info.len_init)
            self.start_ind = segment_info.start_ind_init + incr_start
            self.end_ind = segment_info.end_ind_init - incr_end
            self.len = self.end_ind - self.start_ind
            self.time_tab = dict_meas['times'][self.start_ind:self.end_ind]
            incr_end = incr_end if incr_end != 0 else 1
            self.amp_tab = \
                self.amp_tab_init[incr_start:segment_info.len_init-incr_end]
            self.pha_tab = \
                self.pha_tab_init[incr_start:segment_info.len_init-incr_end]
            self.freq_tab = \
                self.freq_tab_init[incr_start:segment_info.len_init-incr_end] \
                if self.freq_tab_init else None

        # Segment treatment
        self.amp = np.mean(self.amp_tab)
        self.pha = np.mean(self.pha_tab)
        self.res_freq = np.mean(self.freq_tab) if self.freq_tab else None
        self.inc_amp = np.sqrt(np.var(self.amp_tab))
        self.inc_pha = np.sqrt(np.var(self.pha_tab))
        self.inc_res_freq = np.sqrt(np.var(self.freq_tab)) \
            if self.freq_tab else None


class SegmentStableDFRT:
    """
    Segment voltage of sspfm bias signal and associated amplitude and
    phase measure for dfrt if sidebands are measured
    """

    def __init__(self, segment_info, dict_meas, cut_seg=None,
                 filter_type=None, filter_cutoff_frequency=None,
                 filter_order=None):
        """
        Main function of the class

        Parameters
        ----------
        segment_info: SegmentInfo
            Instance of SegmentInfo class containing segment information
        dict_meas: dict
            All measurement in extracted file
        cut_seg: dict, optional
            Dict of percent cut of the start and end of the segment
        filter_type: str
            Type of the filter for amplitude and phase in the segment
        filter_cutoff_frequency: float or tuple
            Cutoff frequency of the filter for amplitude and phase in the
            segment
        filter_order: int
            Order of the filter for amplitude and phase in the segment
        """
        (self.amp, self.pha, self.res_freq, self.q_fact) = \
            (None, None, None, None)
        self.segment_info = segment_info
        self.time_tab_init = dict_meas['times'][segment_info.start_ind_init:
                                                segment_info.end_ind_init]
        self.amp_main_tab_init = dict_meas['amp'][segment_info.start_ind_init:
                                                  segment_info.end_ind_init]
        self.pha_main_tab_init = dict_meas['pha'][segment_info.start_ind_init:
                                                  segment_info.end_ind_init]
        self.freq_main_tab_init = dict_meas['freq'][segment_info.start_ind_init:
                                                    segment_info.end_ind_init]
        self.amp_sbl_tab_init = \
            dict_meas['amp sb_l'][segment_info.start_ind_init:
                                  segment_info.end_ind_init]
        self.pha_sbl_tab_init = \
            dict_meas['pha sb_l'][segment_info.start_ind_init:
                                  segment_info.end_ind_init]
        self.freq_sbl_tab_init = \
            dict_meas['freq sb_l'][segment_info.start_ind_init:
                                   segment_info.end_ind_init]
        self.amp_sbr_tab_init = \
            dict_meas['amp sb_r'][segment_info.start_ind_init:
                                  segment_info.end_ind_init]
        self.pha_sbr_tab_init = \
            dict_meas['pha sb_r'][segment_info.start_ind_init:
                                  segment_info.end_ind_init]
        self.freq_sbr_tab_init = \
            dict_meas['freq sb_r'][segment_info.start_ind_init:
                                   segment_info.end_ind_init]

        # Cut beginning and end of the segment
        if cut_seg is None:
            self.start_ind = segment_info.start_ind_init
            self.end_ind = segment_info.end_ind_init
            self.len = segment_info.len_init
            self.time_tab = self.time_tab_init
            self.amp_main_tab = self.amp_main_tab_init
            self.pha_main_tab = self.pha_main_tab_init
            self.freq_main_tab = self.freq_main_tab_init
            self.amp_sbl_tab = self.amp_sbl_tab_init
            self.pha_sbl_tab = self.pha_sbl_tab_init
            self.freq_sbl_tab = self.freq_sbl_tab_init
            self.amp_sbr_tab = self.amp_sbr_tab_init
            self.pha_sbr_tab = self.pha_sbr_tab_init
            self.freq_sbr_tab = self.freq_sbr_tab_init
        else:
            incr_start = int(cut_seg['start'] / 100 * segment_info.len_init)
            incr_end = int(cut_seg['end'] / 100 * segment_info.len_init)
            self.start_ind = segment_info.start_ind_init + incr_start
            self.end_ind = segment_info.end_ind_init - incr_end
            self.len = self.end_ind - self.start_ind
            self.time_tab = dict_meas['times'][self.start_ind:self.end_ind]
            self.amp_main_tab = dict_meas['amp'][self.start_ind:self.end_ind]
            self.pha_main_tab = dict_meas['pha'][self.start_ind:self.end_ind]
            self.freq_main_tab = dict_meas['freq'][self.start_ind:self.end_ind]
            self.amp_sbl_tab = dict_meas['amp sb_l'][self.start_ind:
                                                     self.end_ind]
            self.pha_sbl_tab = dict_meas['pha sb_l'][self.start_ind:
                                                     self.end_ind]
            self.freq_sbl_tab = dict_meas['freq sb_l'][self.start_ind:
                                                       self.end_ind]
            self.amp_sbr_tab = dict_meas['amp sb_r'][self.start_ind:
                                                     self.end_ind]
            self.pha_sbr_tab = dict_meas['pha sb_r'][self.start_ind:
                                                     self.end_ind]
            self.freq_sbr_tab = dict_meas['freq sb_r'][self.start_ind:
                                                       self.end_ind]
        # Measure filtered
        if filter_type == 'mean':
            self.amp_main_tab = filter_mean(self.amp_main_tab, filter_order)
            self.amp_main_tab_init = filter_mean(self.amp_main_tab_init,
                                                 filter_order)
            self.pha_main_tab = filter_mean(self.pha_main_tab, filter_order)
            self.pha_main_tab_init = filter_mean(self.pha_main_tab_init,
                                                 filter_order)
            self.freq_main_tab = filter_mean(self.freq_main_tab, filter_order)
            self.freq_main_tab_init = filter_mean(self.freq_main_tab_init,
                                                  filter_order)
            self.amp_sbl_tab = filter_mean(self.amp_sbl_tab, filter_order)
            self.amp_sbl_tab_init = filter_mean(self.amp_sbl_tab_init,
                                                filter_order)
            self.pha_sbl_tab = filter_mean(self.pha_sbl_tab, filter_order)
            self.pha_sbl_tab_init = filter_mean(self.pha_sbl_tab_init,
                                                filter_order)
            self.freq_sbl_tab = filter_mean(self.freq_sbl_tab, filter_order)
            self.freq_sbl_tab_init = filter_mean(self.freq_sbl_tab_init,
                                                 filter_order)
            self.amp_sbr_tab = filter_mean(self.amp_sbr_tab, filter_order)
            self.amp_sbr_tab_init = filter_mean(self.amp_sbr_tab_init,
                                                filter_order)
            self.pha_sbr_tab = filter_mean(self.pha_sbr_tab, filter_order)
            self.pha_sbr_tab_init = filter_mean(self.pha_sbr_tab_init,
                                                filter_order)
            self.freq_sbr_tab = filter_mean(self.freq_sbr_tab, filter_order)
            self.freq_sbr_tab_init = filter_mean(self.freq_sbr_tab_init,
                                                 filter_order)
        elif filter_type in ['low', 'high', 'bandpass', 'bandstop']:
            sampling_frequency = \
                len(self.time_tab) / (self.time_tab[-1] - self.time_tab[0])
            self.amp_main_tab = butter_filter(
                self.amp_main_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.amp_main_tab_init = butter_filter(
                self.amp_main_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.pha_main_tab = butter_filter(
                self.pha_main_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.pha_main_tab_init = butter_filter(
                self.pha_main_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.freq_main_tab = butter_filter(
                self.freq_main_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.freq_main_tab_init = butter_filter(
                self.freq_main_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.amp_sbl_tab = butter_filter(
                self.amp_sbl_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.amp_sbl_tab_init = butter_filter(
                self.amp_sbl_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.pha_sbl_tab = butter_filter(
                self.pha_sbl_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.pha_sbl_tab_init = butter_filter(
                self.pha_sbl_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.freq_sbl_tab = butter_filter(
                self.freq_sbl_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.freq_sbl_tab_init = butter_filter(
                self.freq_sbl_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.amp_sbr_tab = butter_filter(
                self.amp_sbr_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.amp_sbr_tab_init = butter_filter(
                self.amp_sbr_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.pha_sbr_tab = butter_filter(
                self.pha_sbr_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.pha_sbr_tab_init = butter_filter(
                self.pha_sbr_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)
            self.freq_sbr_tab = butter_filter(
                self.freq_sbr_tab, sampling_frequency, filter_cutoff_frequency,
                filter_type, filter_order)
            self.freq_sbr_tab_init = butter_filter(
                self.freq_sbr_tab_init, sampling_frequency,
                filter_cutoff_frequency, filter_type, filter_order)

        # Segment treatment
        self.amp_main = np.mean(self.amp_main_tab)
        self.pha_main = np.mean(self.pha_main_tab)
        self.freq_main = np.mean(self.freq_main_tab)
        self.amp_sbl = np.mean(self.amp_sbl_tab)
        self.pha_sbl = np.mean(self.pha_sbl_tab)
        self.freq_sbl = np.mean(self.freq_sbl_tab)
        self.amp_sbr = np.mean(self.amp_sbr_tab)
        self.pha_sbr = np.mean(self.pha_sbr_tab)
        self.freq_sbr = np.mean(self.freq_sbr_tab)

        self.process_sidebands()

    def process_sidebands(self):
        """
        Compute peak parameters from sidebands amplitude, phase and frequency
        values. Conditions: pha_sbr > pha_sbl for freq_sbr > freq_sbl.
        Source : doi:10.1088/0957-4484/24/15/159501
        """
        assert self.pha_sbr > self.pha_sbl, \
            "pha_sbr must be greater than pha_sbl"
        assert self.freq_sbr > self.freq_sbl, \
            "freq_sbr must be greater than freq_sbl"

        phi = np.tan(self.pha_sbr - self.pha_sbl)
        omega = self.freq_sbl * self.amp_sbl / (self.freq_sbr * self.amp_sbr)

        x_1 = - (1 - np.sign(phi) * np.sqrt(1 + phi ** 2) / omega) / phi
        x_2 = (1 - np.sign(phi) * np.sqrt(1 + phi ** 2) * omega) / phi

        frac = (self.freq_sbr * x_1 - self.freq_sbl * x_2) / \
               (self.freq_sbl * x_1 - self.freq_sbr * x_2)
        self.res_freq = np.sqrt(self.freq_sbl * self.freq_sbr * frac)

        num = self.freq_sbl * self.freq_sbr * \
            (self.freq_sbr * x_1 - self.freq_sbl * x_2) * \
            (self.freq_sbl * x_1 - self.freq_sbr * x_2)
        denom = self.freq_sbr**2 - self.freq_sbl**2
        self.q_fact = np.sqrt(num) / denom

        self.amp = self.amp_sbl * self.q_fact / \
            sho(self.freq_sbl, 1, self.q_fact, self.res_freq)
        self.pha = self.pha_sbl + \
            sho_phase(self.freq_sbl, 1, self.q_fact, self.res_freq)


def external_calib(amplitude_out, phase_out, meas_pars=None):
    """
    Convert the output amplitude and phase from an external acquisition device
    (in V) to physical units. Additional measurements like frequency can
    be added here.

    Parameters
    ----------
    amplitude_out: list or numpy.array of float
        List of output PFM amplitude measurements of external acquisition
        device (in V).
    phase_out: list or numpy.array of float
        List of output PFM phase measurements of external acquisition
        device (in V).
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
        'Sens ampli': 1, 'Offset ampli [V]': 0,
        'Sens phase [mV/°]': 1000, 'Offset phase [V]': 0
    }
    amplitude = [(elem_amp - meas_pars['Offset ampli [V]']) /
                 meas_pars['Sens ampli'] for elem_amp in amplitude_out]
    phase = [(elem_pha - meas_pars['Offset phase [V]']) /
             (meas_pars['Sens phase [mV/°]'] / 1000) for elem_pha in phase_out]

    return amplitude, phase


def cut_function(sign_pars):
    """
    This function is used to cut the measure into segments and compute the
    index values for each start of on field and off field segments.

    Parameters
    ----------
    sign_pars: dict
        Dictionary of sspfm bias signal parameters.

    Returns
    -------
    index: dict
        Dictionary of index values for each on and off field segment.
    nb_seg_tot: int
        Total number of segments.
    """

    nb_seg_read_write = \
        (sign_pars['Nb volt (W)'] - 1) * 2 * sign_pars['Nb volt (R)']
    seg_ite = sign_pars['Seg sample (W)'] + sign_pars['Seg sample (R)']
    nb_seg_tot = nb_seg_read_write*2
    # nb_sample = nb_seg * seg_ite

    index_on_f, index_off_f = [], []
    for index_seg in range(int(nb_seg_read_write)):
        seg_increment = \
            sign_pars['Hold sample (start)'] + index_seg * seg_ite
        index_on_f.append(seg_increment)

        seg_increment += sign_pars['Seg sample (W)']
        index_off_f.append(seg_increment)

    return {'off f': index_off_f, 'on f': index_on_f}, nb_seg_tot


def extract_other_properties(dict_meas, start_ind, end_ind):
    """
    Extract other properties from measurement dictionary

    Parameters
    ----------
    dict_meas: dict
        Dictionary containing measurement data
    start_ind: int
        Starting index for data extraction
    end_ind: int
        Ending index for data extraction

    Returns
    -------
    other_properties: dict
        Dictionary containing extracted properties
    """
    mean_height, diff_height, mean_deflection, deflection_error, adhesion = \
        None, None, None, None, None

    if "height" in list(dict_meas.keys()):
        if len(dict_meas["height"]) > 0:
            mean_height = np.mean(dict_meas["height"][start_ind:-end_ind])
            diff_height = abs(np.mean(
                [dict_meas["height"][0],
                 dict_meas["height"][-1]]) - mean_height)
    if "deflection" in list(dict_meas.keys()):
        if len(dict_meas["deflection"]) > 0:
            mean_deflection = abs(np.mean(
                [dict_meas["deflection"][0],
                 dict_meas["deflection"][-1]]) -
                                  np.mean(dict_meas["deflection"][
                                          start_ind:-end_ind]))
            deflection_error = np.sqrt(np.var(dict_meas["deflection"][
                                              start_ind:-end_ind]))
            adhesion = np.mean(dict_meas["deflection"][-(int(end_ind/2)):]) - \
                min(dict_meas["deflection"][-end_ind:])

    other_properties = {
        "height": mean_height,
        "diff height": diff_height,
        "deflection": mean_deflection,
        "deflection error": deflection_error,
        "adhesion": adhesion,
    }

    return other_properties
