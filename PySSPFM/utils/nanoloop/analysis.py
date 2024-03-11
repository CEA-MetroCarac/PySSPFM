"""
Module used for nanoloop: - signal treatment
"""

import numpy as np

from PySSPFM.utils.core.iterable import sort_2d_arr
from PySSPFM.utils.signal_bias import write_vec
from PySSPFM.utils.nanoloop.phase import phase_calibration, correct_phase_val


class MultiLoop:
    """ MultiLoop object associated to a y measure """

    def __init__(self, write_volt, y_meas, read_volt, mode='Off field',
                 y_sigma=None):
        """
        Main function of the class

        Parameters
        ----------
        write_volt: list or numpy.array
            Write voltage value (in V)
        y_meas: list or numpy.array
            List or array of measured values
        read_volt: float
            Read voltage value (in V)
        mode: str, optional
            Measurement mode ('Off field' or 'On field')
        y_sigma: list or numpy.array, optional
            List or array of uncertainties in the measured values

        Returns
        -------
        None
        """
        assert mode in ['Off field', 'On field']
        self.write_volt = write_volt
        self.y_meas = y_meas
        self.y_sigma = y_sigma
        self.read_volt = read_volt
        self.type = mode
        self.write_marker = []
        self.y_marker = []

        self.write_volt_right = []
        self.write_volt_left = []
        self.y_meas_right = []
        self.y_meas_left = []
        self.y_sigma_right = [] if self.y_sigma is not None else None
        self.y_sigma_left = [] if self.y_sigma is not None else None
        self.write_mode = ''
        self.guess_write_mode()
        self.find_marker()
        self.divide_left_right()

    def guess_write_mode(self):
        """ Guess write mode of sspfm bias with write segment """
        if self.write_volt[0] == max(self.write_volt):
            self.write_mode = 'High, down'
        elif self.write_volt[0] == min(self.write_volt):
            self.write_mode = 'Low, up'
        else:
            self.write_mode = 'Zero, up' if \
                self.write_volt[1] > self.write_volt[0] else 'Zero, down'

    def find_marker(self):
        """ Find marker coordinates of start/end point of write segment """
        if self.write_mode == 'Zero, up':
            self.write_marker = [
                0, max(self.write_volt), min(self.write_volt),
                self.write_volt[-1]]
            self.y_marker = [
                self.y_meas[0], self.y_meas[np.argmax(self.write_volt)],
                self.y_meas[np.argmin(self.write_volt)], self.y_meas[-1]]
        elif self.write_mode == 'Zero, down':
            self.write_marker = [
                0, min(self.write_volt), max(self.write_volt),
                self.write_volt[-1]]
            self.y_marker = [
                self.y_meas[0], self.y_meas[np.argmin(self.write_volt)],
                self.y_meas[np.argmax(self.write_volt)], self.y_meas[-1]]
        elif self.write_mode == 'High, down':
            self.write_marker = [
                max(self.write_volt), min(self.write_volt),
                self.write_volt[-1]]
            self.y_marker = [
                self.y_meas[np.argmax(self.write_volt)],
                self.y_meas[np.argmin(self.write_volt)], self.y_meas[-1]]
        elif self.write_mode == 'Low, up':
            self.write_marker = [
                min(self.write_volt), max(self.write_volt),
                self.write_volt[-1]]
            self.y_marker = [
                self.y_meas[np.argmin(self.write_volt)],
                self.y_meas[np.argmax(self.write_volt)], self.y_meas[-1]]
        else:
            raise IOError(
                'write_mode should be "Zero, up", or "Zero, down", '
                'or "High, down", or "Low, up"')

    def divide_left_right(self, closed=True):
        """
        Divide the loop into 2 segments: left and right

        Parameters
        ----------
        closed: bool, optional
            If close is True, duplicate the first measurement in the last
            position to close the loop

        Returns
        -------
        None
        """
        ite = len(self.write_volt)
        lab = ''
        write_v_seg = {'right': [], 'left': []}
        y_meas_seg = {'right': [], 'left': []}
        y_sigma_seg = {'right': [], 'left': []} \
            if self.y_sigma is not None else None

        write_v_max, write_v_min = max(self.write_volt), min(self.write_volt)
        y_meas_min = self.y_meas[np.argmin(self.write_volt)]
        y_meas_max = self.y_meas[np.argmax(self.write_volt)]
        y_sigma_min = self.y_sigma[np.argmin(self.write_volt)] \
            if self.y_sigma is not None else None
        y_sigma_max = self.y_sigma[np.argmax(self.write_volt)] \
            if self.y_sigma is not None else None

        for cont in range(ite - 1):
            if self.write_volt[cont + 1] > self.write_volt[cont]:
                write_v_seg['right'].append(self.write_volt[cont])
                y_meas_seg['right'].append(self.y_meas[cont])
                if self.y_sigma is not None:
                    y_sigma_seg['right'].append(self.y_sigma[cont])
                lab = 'right'
            else:
                write_v_seg['left'].append(self.write_volt[cont])
                y_meas_seg['left'].append(self.y_meas[cont])
                if self.y_sigma is not None:
                    y_sigma_seg['left'].append(self.y_sigma[cont])
                lab = 'left'

        for key in ['right', 'left']:
            if lab == key:
                write_v_seg[key].append(self.write_volt[-1])
                y_meas_seg[key].append(self.y_meas[-1])
                if self.y_sigma is not None:
                    y_sigma_seg[key].append(self.y_sigma[-1])

        seg_left, seg_right = [], []
        for elem in [write_v_seg, y_meas_seg, y_sigma_seg]:
            if elem:
                seg_left.append(elem['left'])
                seg_right.append(elem['right'])

        seg = {
            'right': sort_2d_arr(np.array(seg_right), 'line', 0),
            'left': sort_2d_arr(np.array(seg_left), 'line', 0, reverse=True)
        }

        for key in ['right', 'left']:
            cont = 0
            if self.write_volt is not None:
                write_v_seg[key] = seg[key][cont]
                cont += 1
            if self.y_meas is not None:
                y_meas_seg[key] = seg[key][cont]
                cont += 1
            if self.y_sigma is not None:
                y_sigma_seg[key] = seg[key][cont]
                cont += 1

        if closed:
            if write_v_seg['right'][0] != write_v_min:
                write_v_seg['right'] = \
                    np.insert(write_v_seg['right'], 0, write_v_min)
                y_meas_seg['right'] = \
                    np.insert(y_meas_seg['right'], 0, y_meas_min)
                if self.y_sigma is not None:
                    y_sigma_seg['right'] = \
                        np.insert(y_sigma_seg['right'], 0, y_sigma_min)
            if write_v_seg['left'][0] != write_v_max:
                write_v_seg['left'] = \
                    np.insert(write_v_seg['left'], 0, write_v_max)
                y_meas_seg['left'] = \
                    np.insert(y_meas_seg['left'], 0, y_meas_max)
                if self.y_sigma is not None:
                    y_sigma_seg['left'] = \
                        np.insert(y_sigma_seg['left'], 0, y_sigma_max)
            if write_v_seg['right'][-1] != write_v_max:
                write_v_seg['right'] = \
                    np.append(write_v_seg['right'], write_v_max)
                y_meas_seg['right'] = np.append(y_meas_seg['right'], y_meas_max)
                if self.y_sigma is not None:
                    y_sigma_seg['right'] = \
                        np.append(y_sigma_seg['right'], y_sigma_max)
            if write_v_seg['left'][-1] != write_v_min:
                write_v_seg['left'] = \
                    np.append(write_v_seg['left'], write_v_min)
                y_meas_seg['left'] = np.append(y_meas_seg['left'], y_meas_min)
                if self.y_sigma is not None:
                    y_sigma_seg['left'] = \
                        np.append(y_sigma_seg['left'], y_sigma_min)

        self.write_volt_right = write_v_seg['right']
        self.write_volt_left = write_v_seg['left']
        self.y_meas_right = y_meas_seg['right']
        self.y_meas_left = y_meas_seg['left']
        self.y_sigma_right = y_sigma_seg['right'] \
            if self.y_sigma is not None else None
        self.y_sigma_left = y_sigma_seg['left'] \
            if self.y_sigma is not None else None


class MeanLoop:
    """ Mean loop of a MultiLoop object associated to a y measure """

    def __init__(self, multi_loop, del_1st_loop=True):
        """
        Main function of the class

        Parameters
        ----------
        multi_loop: MultiLoop class
            MultiLoop object
        del_1st_loop: bool, optional
            If True, remove first loop for analysis
        """
        start_ind = 1 if len(multi_loop) > 1 and del_1st_loop else 0
        multi_loop = multi_loop[start_ind:]
        loop = multi_loop[0]

        # Write voltage
        self.write_volt = loop.write_volt
        self.write_volt_left = loop.write_volt_left
        self.write_volt_right = loop.write_volt_right
        self.write_marker = loop.write_marker

        # Multi measurement
        self.multi_y_meas = [single_loop.y_meas for single_loop in multi_loop]
        self.multi_y_marker = \
            [single_loop.y_marker for single_loop in multi_loop]
        self.multi_y_meas_left = \
            [single_loop.y_meas_left for single_loop in multi_loop]
        self.multi_y_meas_right = \
            [single_loop.y_meas_right for single_loop in multi_loop]

        def sigma_treatment(sigmas):
            """
            Treat uncertainty values.

            Parameters
            ----------
            sigmas: list or None
                List of uncertainty values

            Returns
            -------
            sigmas: list or None
                Processed uncertainty values or None
            """
            if sigmas:
                return None if all(elem is None for elem in sigmas) \
                               or len(sigmas) == 0 else sigmas
            else:
                return None

        try:
            read_volts = [single_loop.read_volt for single_loop in multi_loop]
            sigma_mean_flag = all(elem == read_volts[0] for elem in read_volts)
        except AttributeError:
            sigma_mean_flag = True

        # Mean measurement
        y_sigma = [single_loop.y_sigma for single_loop in multi_loop]
        y_sigma = sigma_treatment(y_sigma)
        self.y_meas, self.y_sigma = \
            mean_measure(self.multi_y_meas, sigma_mean_flag, y_sigma)
        self.y_marker, _ = mean_measure(self.multi_y_marker)
        y_sigma_left = \
            [single_loop.y_sigma_left for single_loop in multi_loop]
        y_sigma_left = sigma_treatment(y_sigma_left)
        self.y_meas_left, self.y_sigma_left = mean_measure(
            self.multi_y_meas_left, sigma_mean_flag, y_sigma_left)
        y_sigma_right = \
            [single_loop.y_sigma_right for single_loop in multi_loop]
        y_sigma_right = sigma_treatment(y_sigma_right)
        self.y_meas_right, self.y_sigma_right = mean_measure(
            self.multi_y_meas_right, sigma_mean_flag, y_sigma_right)


class AllMultiLoop:
    """
    All MultiLoop objects associated with all measurements (amplitude, phase,
    piezoresponse, resonance frequency, quality factor)
    """
    def __init__(self, write_volt, amp, pha, pha_calib, read_volt,
                 mode='Off field', res_freq=None, q_fact=None,
                 amp_sigma=None, pha_sigma=None, res_freq_sigma=None,
                 q_fact_sigma=None):
        """
        Main function of the class

        Parameters
        ----------
        write_volt: list(n*m) or numpy.array(n*m) of float
            Multiloop 2d array of write voltage values (in V)
        amp: list(n*m) or numpy.array(n*m) of float
            Multiloop 2d array of amplitude values (in a.u or nm)
        pha: list(n*m) or numpy.array(n*m) of float
            Multiloop 2d array of phase values (in °)
        pha_calib: dict
            Phase calibration parameters
        read_volt: list(p) or numpy.array(p) of float
            Array of read voltage values for each loop (in V)
        mode: str, optional
            'On field' or 'Off field'
        res_freq: list(n*m) or numpy.array(n*m) of float, optional
            Multiloop 2d array of resonance frequency values (in kHz)
        q_fact: list(n*m) or numpy.array(n*m) of float, optional
            Multiloop 2d array of quality factor values
        amp_sigma: list(n*m) or numpy.array(n*m) of float, optional
            Multiloop 2d array of uncertainties associated with amplitude
            values (in a.u or nm)
        pha_sigma: list(n*m) or numpy.array(n*m) of float, optional
            Multiloop 2d array of uncertainties associated with phase values
            (in °)
        res_freq_sigma: list(n*m) or numpy.array(n*m) of float, optional
            Multiloop 2d array of uncertainties associated with resonance
            frequency values (in kHz)
        q_fact_sigma: list(n*m) or numpy.array(n*m) of float, optional
            Multiloop 2d array of uncertainties associated with quality factor
            values
        """

        self.read_volt = read_volt

        # Amplitude and phase
        amp_loops = MultiLoop(
            write_volt, amp, read_volt, mode=mode, y_sigma=amp_sigma)
        self.amp = amp_loops
        pha_loops = MultiLoop(
            write_volt, pha, read_volt, mode=mode, y_sigma=pha_sigma)
        self.pha = pha_loops

        # Treated phase
        treated_pha = phase_treatment(pha, pha_calib)
        treated_pha_loops = MultiLoop(
            write_volt, treated_pha, read_volt, mode=mode, y_sigma=pha_sigma)
        self.treated_pha = treated_pha_loops

        func = pha_calib["func"]

        # Piezoresponse
        piezorep = list(np.zeros(len(amp)))
        for i, (elem_amp, elem_pha) in enumerate(zip(amp, treated_pha)):
            if elem_amp is not None and elem_pha is not None:
                piezorep[i] = elem_amp * func(np.deg2rad(elem_pha))

        # Uncertainty on piezoresponse
        if amp_sigma and pha_sigma:
            piezorep_sigma = np.abs(piezorep) * np.sqrt(
                (np.array(amp_sigma) / np.array(amp))**2 +
                (np.array(pha_sigma) / np.array(pha))**2)
        else:
            piezorep_sigma = None

        # MultiLoop of piezoresponse
        piezorep_loops = MultiLoop(
            write_volt, piezorep, read_volt, mode=mode, y_sigma=piezorep_sigma)
        self.piezorep = piezorep_loops

        # Resonance frequency
        if res_freq:
            res_freq_loops = MultiLoop(
                write_volt, res_freq, read_volt, mode=mode,
                y_sigma=res_freq_sigma)
            self.res_freq = res_freq_loops
        else:
            self.res_freq, res_freq_loops = None, None

        # Quality factor
        if q_fact:
            q_fact_loops = MultiLoop(
                write_volt, q_fact, read_volt, mode=mode,
                y_sigma=q_fact_sigma)
            self.q_fact = q_fact_loops
        else:
            self.q_fact, q_fact_loops = None, None

        self.meas = {
            "amp": amp_loops, 
            "pha": pha_loops, 
            "treat pha": treated_pha_loops,
            "piezorep": piezorep_loops,
            "res freq": res_freq_loops,
            "q fact": q_fact_loops
        }


class AllMeanLoop:
    """
    All MeanLoop associated to a AllMultiLoop object
    (associated to all measurement:
    amplitude, phase, piezoresponse, resonance frequency, quality factor)
    """
    def __init__(self, all_multi_loop, pha_calib=None, del_1st_loop=True):
        """
        Main function of the class

        Parameters
        ----------
        all_multi_loop: AllMultiLoop class
            AllMultiLoop object
        pha_calib: dict, optional
            Dict of phase calibration parameters
        del_1st_loop: bool, optional
            If True, remove first loop for analysis
        """
        amp_loops = MeanLoop(
            [loop.amp for loop in all_multi_loop], del_1st_loop)
        self.amp = amp_loops
        pha_loops = MeanLoop(
            [loop.pha for loop in all_multi_loop], del_1st_loop)
        self.pha = pha_loops
        treated_pha_loops = MeanLoop(
            [loop.treated_pha for loop in all_multi_loop], del_1st_loop)
        self.treated_pha = treated_pha_loops

        # Phase calibration: up and and down
        if pha_calib is not None and pha_calib['corr'] == 'up_down':
            self.treated_pha.y_meas = \
                phase_up_down(self.treated_pha.y_meas, pha_calib)
            self.treated_pha.y_meas_left = \
                phase_up_down(self.treated_pha.y_meas_left, pha_calib)
            self.treated_pha.y_meas_right = \
                phase_up_down(self.treated_pha.y_meas_right, pha_calib)
            self.treated_pha.y_marker = \
                phase_up_down(self.treated_pha.y_marker, pha_calib)

        piezorep_loops = MeanLoop(
            [loop.piezorep for loop in all_multi_loop], del_1st_loop)
        self.piezorep = piezorep_loops
        if all_multi_loop[0].res_freq:
            res_freq_loops = MeanLoop(
                [loop.res_freq for loop in all_multi_loop], del_1st_loop)
            self.res_freq = res_freq_loops
        else:
            self.res_freq, res_freq_loops = None, None
        if all_multi_loop[0].q_fact:
            q_fact_loops = MeanLoop(
                [loop.q_fact for loop in all_multi_loop], del_1st_loop)
            self.q_fact = q_fact_loops
        else:
            self.q_fact, q_fact_loops = None, None
        self.meas = {
            "amp": amp_loops, 
            "pha": pha_loops, 
            "treat pha": treated_pha_loops,
            "piezorep": piezorep_loops,
            "res freq": res_freq_loops,
            "q fact": q_fact_loops
        }


def phase_up_down(phase_tab, pha_calib):
    """
    Phase up and down treatment

    Parameters
    ----------
    phase_tab: list or numpy.array of float
        List of phase values (in °)
    pha_calib: dict
       Phase calibration parameters

    Returns
    -------
    treated_phase_tab: list or numpy.array of float
        Treated phase values (in °)
    """
    # Determine treatment direction based on the 'reverse' parameter
    target_values = list(pha_calib['dict phase target'].values())
    reference_value = np.mean(target_values)

    # Phase up and down treatment
    if pha_calib['reverse']:
        treated_phase_tab = [
            np.min(list(target_values)) if elem >= np.mean(reference_value)
            else np.max(list(target_values)) for elem in phase_tab]
    else:
        treated_phase_tab = [
            np.max(list(target_values)) if elem >= np.mean(list(target_values))
            else np.min(list(target_values)) for elem in phase_tab]

    return treated_phase_tab


def nanoloop_treatment(data_dict, sign_pars, dict_pha=None, dict_str=None,
                       q_fact_scalar=100., resonance=True, make_plots=False):
    """
    Perform treatment value on nanoloops

    Parameters
    ----------
    data_dict: dict
        Dict containing all the data loop
    sign_pars: dict
        SSPFM voltage signal parameters
    dict_pha: dict, optional
        Used for phase treatment
    dict_str: dict, optional
        Used for figure annotation
    q_fact_scalar: float, optional
        Quality factor value (scalar)
    resonance: bool, optional
        True if measurement are performed at resonance frequency and vice versa
    make_plots: bool, optional
        Activation key for matplotlib figures generation

    Returns
    -------
    loop_tab: list of AllMultiLoop
        All MultiLoops
    pha_calib: dict
        Phase calibration parameters
    init_meas: dict
        Initial amplitude and phase value
    """
    dict_pha = dict_pha or {
        'corr': 'raw', 'func': np.cos, 'pha fwd': 0, 'pha rev': 180,
        'main elec': False, 'locked elec slope': False, 'grounded tip': False,
        'positive d33': True}

    # Perform phase treatment and get pha_calib
    (_, pha_calib, _) = phase_calibration(
        data_dict['phase'], data_dict['write'], dict_pha, dict_str=dict_str,
        make_plots=make_plots)
    loop_tab = []
    for num in range(1, int(max(data_dict['index']) + 1)):
        # Extract values for the current loop
        out = extract_value(data_dict, sign_pars, num)
        (read_v, write_volt, amplitude, phase, unc_amp, unc_pha, res_freq,
         unc_res_freq, q_facts, unc_q_facts) = out
        # Perform amplitude / quality factor calculation
        if resonance:
            amplitude = amp_div_q(
                amplitude, list_q=q_facts, mean_q=q_fact_scalar)
            if unc_amp:
                unc_amp = amp_div_q(
                    unc_amp, list_q=q_facts, mean_q=q_fact_scalar)
        # Create AllMultiLoop object and append to loop_tab
        loop_tab.append(AllMultiLoop(
            write_volt, amplitude, phase, pha_calib, read_v,
            mode=dict_str["label"], res_freq=res_freq, q_fact=q_facts,
            amp_sigma=unc_amp, pha_sigma=unc_pha,
            res_freq_sigma=unc_res_freq, q_fact_sigma=unc_q_facts))

    # Get initial amplitude and phase values
    amp_0, pha_0 = (loop_tab[0].amp.y_meas[0], loop_tab[0].pha.y_meas[0]) \
        if loop_tab[0].amp.write_volt[0] == 0 else (None, None)

    return loop_tab, pha_calib, {'amp': amp_0, 'pha': pha_0}


def extract_value(data_dict, sign_pars, num):
    """
    Extract value of data_dict for a single loop

    Parameters
    ----------
    data_dict: dict
        Object containing all the data loop
    sign_pars: dict
        SSPFM voltage signal parameters
    num: int
        Loop number

    Returns
    -------
    read_v: list(n) or numpy.array(n) of float
        Array of read voltage values of the loop (in V)
    write_volt: list(n) or numpy.array(n) of float
        Array of write voltage values of the loop (in V)
    amplitude: list(n) or numpy.array(n) of float
        Array of amplitude values of the loop (in nm or a.u)
    phase: list(n) or numpy.array(n) of float
        Array of phase values of the loop (in °)
    sigma_amp: list(n) or numpy.array(n) of float
        Array of uncertainties associated with amplitude values of the loop
        (in nm or a.u)
    sigma_pha: list(n) or numpy.array(n) of float
        Array of uncertainties associated with phase values of the loop (in °)
    res_freq: list(n) or numpy.array(n) of float
        Array of resonance frequency values of the loop (in kHz)
    sigma_res_freq: list(n) or numpy.array(n) of float
        Array of uncertainties associated with resonance frequency values of
        the loop (in kHz)
    q_fact: list(n) or numpy.array(n) of float
        Array of quality factor values of the loop
    sigma_q_fact: list(n) or numpy.array(n) of float
        Array of uncertainties associated with quality factor values of
        the loop
    """

    def extract_measurement(data, index_extract, key):
        """
        Extract measurements for a specific key and index.

        Parameters
        ----------
        data: dict
            Dictionary containing measurement data
        index_extract: int
            Index for extraction
        key: str
            Key for measurement extraction

        Returns
        -------
        measurements: list or None
            List of measurements for the specified key and index,
            or None if not found
        """
        measurements = [data[key][cont] for cont, index in
                        enumerate(data['index']) if index == index_extract] \
            if key in data and len(data[key]) > 0 \
            else None
        return measurements

    write_volt = write_vec(sign_pars)
    read_v = next((data_dict['read'][cont] for cont, index in
                   enumerate(data_dict['index']) if index == num), 0)
    amplitude = [data_dict['amplitude'][cont] for cont, index in
                 enumerate(data_dict['index']) if index == num]
    phase = [data_dict['phase'][cont] for cont, index in
             enumerate(data_dict['index']) if index == num]
    sigma_amp = extract_measurement(data_dict, num, 'unc amp')
    sigma_pha = extract_measurement(data_dict, num, 'unc pha')
    res_freq = extract_measurement(data_dict, num, 'res freq')
    sigma_res_freq = extract_measurement(data_dict, num, 'unc res freq')
    q_fact = extract_measurement(data_dict, num,  'q fact')
    sigma_q_fact = extract_measurement(data_dict, num, 'unc q fact')

    return read_v, write_volt, amplitude, phase, sigma_amp, sigma_pha, \
        res_freq, sigma_res_freq, q_fact, sigma_q_fact


def amp_div_q(amp, list_q=None, mean_q=100.):
    """
    Generate a new list of amplitude / quality factor values for quantitative
    analysis

    Parameters
    ----------
    amp: list(n) or numpy.array(n) of float
        Array of amplitude values (in a.u or nm)
    list_q: list(n) or numpy.array(n) of float, optional
        Array of quality factor values
    mean_q: float, optional
        Single value of quality factor

    Returns
    -------
    amp_q: list(n) of float or None
        List of amp/Q values (in a.u or nm)
    """
    amp_q = []
    list_q = list_q or []
    if len(list_q) == 0:
        for elem in amp:
            if not np.isnan(elem):
                amp_q.append(elem / mean_q)
            else:
                amp_q.append(np.nan)
    else:
        for elem_amp, elem_q in zip(amp, list_q):
            if not np.isnan(elem_amp) and not np.isnan(elem_q):
                amp_q.append(elem_amp / elem_q)
            else:
                amp_q.append(np.nan)

    return amp_q


def phase_treatment(pha, pha_calib):
    """
    Phase treatment: up & down, affine, or offset treatment

    Parameters
    ----------
    pha: list(n*m) or numpy.array(n*m) of float
        Multiloop 2d array of phase values (in °)
    pha_calib: dict
        Phase calibration parameters

    Returns
    -------
    treated_pha: list(n*m) or numpy.array(n*m) of float
        Multiloop 2d array of phase values (in °)
    """

    if pha_calib['corr'] == 'raw':
        treated_pha = pha
    else:
        try:
            coef_a = pha_calib['coefs'][0]
            coef_b = pha_calib['coefs'][1]
        except KeyError:
            coef_a = None
            coef_b = None
        treated_pha, _ = correct_phase_val(
            pha, pha_calib['dict phase meas'],
            pha_calib['dict phase target'], pha_corr=pha_calib['corr'],
            coef_a=coef_a, coef_b=coef_b, reverted=pha_calib['reverse'])

    return treated_pha


def mean_measure(multi_meas, sigma_flag=True, multi_meas_sigma=None):
    """
    Function used for MeanLoop class : compute mean and sigma array
    of a multi measure (amplitude, phase, piezoresponse)

    Parameters
    ----------
    multi_meas: list(m*n) or numpy.array(m*n) of float
        2d array of multi measure
    sigma_flag: bool, optional
        Flag to calculate sigma_mean, default is True
    multi_meas_sigma: list of float, optional
        List of uncertainties for weighted mean calculation

    Returns
    -------
    mean_meas: list(m) of float
        Mean of mean multi measure values
    sigma_meas: list(m) of float
        Sigma of mean multi measure values
    """
    mean_meas, sigma_meas = [], []

    def weighted_mean_with_uncertainty(sigmas):
        """
        Calculate weighted mean with uncertainty.

        Parameters
        ----------
        sigmas: list of float
            List of uncertainties

        Returns
        -------
        sigma: float
            Weighted uncertainty
        """
        weights = 1 / np.array(sigmas) ** 2
        sigma = 1 / np.sqrt(np.sum(weights))
        return sigma

    transp = np.transpose(multi_meas)
    for i in range(np.shape(transp)[0]):
        mean_meas_val = np.mean(list(filter(
            lambda x: x is not None, transp[i])))
        mean_meas.append(mean_meas_val)
        if sigma_flag:
            sigma_meas.append(np.sqrt(np.var(list(filter(
                lambda x: x is not None, transp[i])))))
        elif multi_meas_sigma:
            unc = weighted_mean_with_uncertainty(multi_meas_sigma)
            sigma_meas.append(unc)

    if not sigma_meas:
        sigma_meas = None

    return mean_meas, sigma_meas


def gen_ckpfm_meas(piezorep_loop_tab):
    """
    Organize sspfm loop data in terms of cKPFM measure:
    piezorep = f(read volt) for each write volt values
    Valid for multi read voltage values off-field measurements
    N.Balke et al. : Exploring Local Electrostatic Effects with Scanning Probe
    Microscopy: Implications for Piezoresponse Force Microscopy and
    Triboelectricity ». ACS Nano 8, no 10 - 2014.
    https://doi.org/10.1021/nn505176a

    Parameters
    ----------
    piezorep_loop_tab: list(n) or numpy.array(n) of MultiLoop
        Array of piezoresponse MultiLoop objects

    Returns
    -------
    dict
        Measurement organized in terms of cKPFM measures
    """
    write_volt = piezorep_loop_tab[0].write_volt
    read_voltage = [loop.read_volt for loop in piezorep_loop_tab]
    piezorep_ckpfm = [[loop.y_meas[cont] for loop in piezorep_loop_tab]
                      for cont, _ in enumerate(write_volt)]

    return {'write volt': write_volt,
            'piezorep': piezorep_ckpfm,
            'read volt': read_voltage}
