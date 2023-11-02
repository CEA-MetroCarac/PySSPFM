"""
Module used for nanoloop: - signal treatment
"""

import numpy as np

from PySSPFM.utils.core.iterable import sort_2d_arr
from PySSPFM.utils.signal_bias import write_vec
from PySSPFM.utils.nanoloop.phase import phase_calibration, correct_phase_val


class MultiLoop:
    """ Amplitude, phase and piezorep loops """

    def __init__(self, write_volt, amp, pha, read_volt, pha_calib,
                 mode='Off field'):
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
        read_volt: list(p) or numpy.array(p) of float
            Array of read voltage values for each loop (in V)
        pha_calib: dict
            Phase calibration parameters
        mode: str, optional
            'On field' or 'Off field'
        """
        assert mode in ['Off field', 'On field']

        self.write_volt = write_volt
        self.amp = amp
        self.pha = pha
        self.read_volt = read_volt
        self.type = mode
        self.write_marker = []
        self.amp_marker = []
        self.pha_marker = []
        self.piezorep_marker = []

        self.write_volt_right = []
        self.write_volt_left = []
        self.amp_right = []
        self.amp_left = []
        self.pha_right = []
        self.pha_left = []

        self.write_mode = ''
        self.guess_write_mode()
        self.find_marker()
        self.divide_left_right()

        self.treat_pha = self.pha
        self.treat_pha_left = self.pha_left
        self.treat_pha_right = self.pha_right
        self.treat_pha_marker = self.pha_marker

        func = pha_calib["func"]
        self.pha_treat(pha_calib)

        self.piezorep = np.array(self.amp)
        for i, (elem_pr, elem_pha) in enumerate(zip(self.piezorep, self.pha)):
            if elem_pr is not None and elem_pha is not None:
                self.piezorep[i] = elem_pr * func(np.deg2rad(elem_pha))

        self.piezorep_left = np.array(self.amp_left)
        for i, (elem_pr, elem_pha) in enumerate(
                zip(self.piezorep_left, self.treat_pha_left)):
            if elem_pr is not None and elem_pha is not None:
                self.piezorep_left[i] = elem_pr * func(np.deg2rad(elem_pha))

        self.piezorep_right = np.array(self.amp_right)
        for i, (elem_pr, elem_pha) in enumerate(
                zip(self.piezorep_right, self.treat_pha_right)):
            if elem_pr is not None and elem_pha is not None:
                self.piezorep_right[i] = elem_pr * func(np.deg2rad(elem_pha))

        self.piezorep_marker = np.array(self.amp_marker)
        for i, (elem_pr, elem_pha) in enumerate(
                zip(self.piezorep_marker, self.treat_pha_marker)):
            if elem_pr is not None and elem_pha is not None:
                self.piezorep_marker[i] = elem_pr * func(np.deg2rad(elem_pha))

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
            self.write_marker = [0, max(self.write_volt), min(self.write_volt),
                                 self.write_volt[-1]]
            self.amp_marker = [self.amp[0],
                               self.amp[np.argmax(self.write_volt)],
                               self.amp[np.argmin(self.write_volt)],
                               self.amp[-1]]
            self.pha_marker = [self.pha[0],
                               self.pha[np.argmax(self.write_volt)],
                               self.pha[np.argmin(self.write_volt)],
                               self.pha[-1]]
        elif self.write_mode == 'Zero, down':
            self.write_marker = [0, min(self.write_volt), max(self.write_volt),
                                 self.write_volt[-1]]
            self.amp_marker = [self.amp[0],
                               self.amp[np.argmin(self.write_volt)],
                               self.amp[np.argmax(self.write_volt)],
                               self.amp[-1]]
            self.pha_marker = [self.pha[0],
                               self.pha[np.argmin(self.write_volt)],
                               self.pha[np.argmax(self.write_volt)],
                               self.pha[-1]]
        elif self.write_mode == 'High, down':
            self.write_marker = [max(self.write_volt), min(self.write_volt),
                                 self.write_volt[-1]]
            self.amp_marker = [self.amp[np.argmax(self.write_volt)],
                               self.amp[np.argmin(self.write_volt)],
                               self.amp[-1]]
            self.pha_marker = [self.pha[np.argmax(self.write_volt)],
                               self.pha[np.argmin(self.write_volt)],
                               self.pha[-1]]
        elif self.write_mode == 'Low, up':
            self.write_marker = [min(self.write_volt), max(self.write_volt),
                                 self.write_volt[-1]]
            self.amp_marker = [self.amp[np.argmin(self.write_volt)],
                               self.amp[np.argmax(self.write_volt)],
                               self.amp[-1]]
            self.pha_marker = [self.pha[np.argmin(self.write_volt)],
                               self.pha[np.argmax(self.write_volt)],
                               self.pha[-1]]
        else:
            raise IOError('write_mode should be "Zero, up", or "Zero, down", '
                          'or "High, down", or "Low, up"')

    def divide_left_right(self, closed=True):
        """
        Divide the loop into 2 segments: left and right

        Parameters
        ----------
        closed: bool, optional
            If close is True, duplicate the first measurement in the last
            position
            to close the loop

        Returns
        -------
        None
        """
        ite = len(self.write_volt)
        lab = ''
        write_v_seg = {'right': [], 'left': []}
        amp_seg = {'right': [], 'left': []}
        pha_seg = {'right': [], 'left': []}

        write_v_max, write_v_min = max(self.write_volt), min(self.write_volt)
        amp_min, amp_max = self.amp[np.argmin(self.write_volt)], self.amp[
            np.argmax(self.write_volt)]
        pha_min, pha_max = self.pha[np.argmin(self.write_volt)], self.pha[
            np.argmax(self.write_volt)]

        for cont in range(ite - 1):
            if self.write_volt[cont + 1] > self.write_volt[cont]:
                write_v_seg['right'].append(self.write_volt[cont])
                amp_seg['right'].append(self.amp[cont])
                pha_seg['right'].append(self.pha[cont])
                lab = 'right'
            else:
                write_v_seg['left'].append(self.write_volt[cont])
                amp_seg['left'].append(self.amp[cont])
                pha_seg['left'].append(self.pha[cont])
                lab = 'left'

        for key in ['right', 'left']:
            if lab == key:
                write_v_seg[key].append(self.write_volt[-1])
                amp_seg[key].append(self.amp[-1])
                pha_seg[key].append(self.pha[-1])

        seg_left = np.array(
            [write_v_seg['left'], amp_seg['left'], pha_seg['left']])
        seg_right = np.array(
            [write_v_seg['right'], amp_seg['right'], pha_seg['right']])

        seg = {
            'right': sort_2d_arr(seg_right, 'line', 0),
            'left': sort_2d_arr(seg_left, 'line', 0, reverse=True)
        }

        for key in ['right', 'left']:
            write_v_seg[key] = seg[key][0]
            amp_seg[key] = seg[key][1]
            pha_seg[key] = seg[key][2]

        if closed:
            if write_v_seg['right'][0] != write_v_min:
                write_v_seg['right'] = np.insert(write_v_seg['right'], 0,
                                                 write_v_min)
                amp_seg['right'] = np.insert(amp_seg['right'], 0, amp_min)
                pha_seg['right'] = np.insert(pha_seg['right'], 0, pha_min)
            if write_v_seg['left'][0] != write_v_max:
                write_v_seg['left'] = np.insert(write_v_seg['left'], 0,
                                                write_v_max)
                amp_seg['left'] = np.insert(amp_seg['left'], 0, amp_max)
                pha_seg['left'] = np.insert(pha_seg['left'], 0, pha_max)
            if write_v_seg['right'][-1] != write_v_max:
                write_v_seg['right'] = np.append(write_v_seg['right'],
                                                 write_v_max)
                amp_seg['right'] = np.append(amp_seg['right'], amp_max)
                pha_seg['right'] = np.append(pha_seg['right'], pha_max)
            if write_v_seg['left'][-1] != write_v_min:
                write_v_seg['left'] = np.append(write_v_seg['left'],
                                                write_v_min)
                amp_seg['left'] = np.append(amp_seg['left'], amp_min)
                pha_seg['left'] = np.append(pha_seg['left'], pha_min)

        self.write_volt_right = write_v_seg['right']
        self.write_volt_left = write_v_seg['left']
        self.amp_right = amp_seg['right']
        self.amp_left = amp_seg['left']
        self.pha_right = pha_seg['right']
        self.pha_left = pha_seg['left']

    def pha_treat(self, pha_calib):
        """
        Phase treatment: up & down, affine, or offset treatment

        Parameters
        ----------
        pha_calib: dict
            Dict of phase calibration parameters

        Returns
        -------
        None
        """
        if pha_calib['corr'] == 'raw':
            pass
        else:
            try:
                coef_a = pha_calib['coefs'][0]
                coef_b = pha_calib['coefs'][1]
            except KeyError:
                coef_a = None
                coef_b = None
            self.treat_pha, _ = correct_phase_val(
                self.pha, pha_calib['dict phase meas'],
                pha_calib['dict phase target'], pha_corr=pha_calib['corr'],
                coef_a=coef_a, coef_b=coef_b, reverted=pha_calib['reverse'])
            self.treat_pha_left, _ = correct_phase_val(
                self.pha_left, pha_calib['dict phase meas'],
                pha_calib['dict phase target'], pha_corr=pha_calib['corr'],
                coef_a=coef_a, coef_b=coef_b, reverted=pha_calib['reverse'])
            self.treat_pha_right, _ = correct_phase_val(
                self.pha_right, pha_calib['dict phase meas'],
                pha_calib['dict phase target'], pha_corr=pha_calib['corr'],
                coef_a=coef_a, coef_b=coef_b, reverted=pha_calib['reverse'])
            self.treat_pha_marker, _ = correct_phase_val(
                self.pha_marker, pha_calib['dict phase meas'],
                pha_calib['dict phase target'], pha_corr=pha_calib['corr'],
                coef_a=coef_a, coef_b=coef_b, reverted=pha_calib['reverse'])


class MeanLoop:
    """Mean loop of a Multiloop, for amplitude, phase, and piezoresponse"""

    def __init__(self, multi_loops, pha_calib=None):
        """
        Main function of the class

        Parameters
        ----------
        multi_loops: Multiloop class
            Multiloop object
        pha_calib: dict, optional
            Dict of phase calibration parameters
        """
        start_ind = 1 if len(multi_loops) > 0 else 0

        loop = multi_loops[start_ind]

        self.write_volt = loop.write_volt
        self.write_volt_left = loop.write_volt_left
        self.write_volt_right = loop.write_volt_right
        self.write_marker = loop.write_marker

        self.multi_amp = [loop.amp for loop in multi_loops]
        try:
            self.multi_pha = [loop.treat_pha for loop in multi_loops]
        except AttributeError:
            self.multi_pha = [loop.pha for loop in multi_loops]
        self.multi_piezorep = [loop.piezorep for loop in multi_loops]
        self.multi_amp_marker = [loop.amp_marker for loop in multi_loops]
        try:
            self.multi_pha_marker = [loop.treat_pha_marker for loop in
                                     multi_loops]
        except AttributeError:
            self.multi_pha_marker = [loop.pha_marker for loop in multi_loops]
        self.multi_piezorep_marker = [loop.piezorep_marker
                                      for loop in multi_loops]
        self.multi_amp_left = [loop.amp_left for loop in multi_loops]
        self.multi_amp_right = [loop.amp_right for loop in multi_loops]
        try:
            self.multi_pha_left = [loop.treat_pha_left for loop in multi_loops]
        except AttributeError:
            self.multi_pha_left = [loop.pha_left for loop in multi_loops]
        try:
            self.multi_pha_right = [loop.treat_pha_right for loop in
                                    multi_loops]
        except AttributeError:
            self.multi_pha_right = [loop.pha_right for loop in multi_loops]
        self.multi_piezorep_left = [loop.piezorep_left for loop in multi_loops]
        self.multi_piezorep_right = [loop.piezorep_right
                                     for loop in multi_loops]

        def mean_measure(multi_meas):
            """
            Function used for MeanLoop class : compute mean array of a multi
            measure
            (amplitude, phase, piezoresponse)

            Parameters
            ----------
            multi_meas: list(m*n) or numpy.array(m*n) of float
                2d array of multi measure

            Returns
            -------
            mean_meas: list(m) of float
                Mean of mean multi measure values
            """
            mean_meas = []
            transp = np.transpose(multi_meas)
            for i in range(np.shape(transp)[0]):
                mean_meas.append(np.mean(list(filter(
                    lambda x: x is not None, transp[i]))))

            return mean_meas

        self.amp = mean_measure(self.multi_amp)
        self.pha = mean_measure(self.multi_pha)
        self.piezorep = mean_measure(self.multi_piezorep)
        self.amp_marker = mean_measure(self.multi_amp_marker)
        self.pha_marker = mean_measure(self.multi_pha_marker)
        self.piezorep_marker = mean_measure(self.multi_piezorep_marker)
        self.amp_left = mean_measure(self.multi_amp_left)
        self.amp_right = mean_measure(self.multi_amp_right)
        self.pha_left = mean_measure(self.multi_pha_left)
        self.pha_right = mean_measure(self.multi_pha_right)
        self.piezorep_left = mean_measure(self.multi_piezorep_left)
        self.piezorep_right = mean_measure(self.multi_piezorep_right)

        # Phase up and down treatment
        if pha_calib is not None and pha_calib['corr'] == 'up_down':
            if pha_calib['reverse']:
                treat_pha = [
                    np.min(list(pha_calib['dict phase target'].values())) if
                    elem >= np.mean(
                        list(pha_calib['dict phase target'].values()))
                    else
                    np.max(list(pha_calib['dict phase target'].values()))
                    for elem in self.pha]
            else:
                treat_pha = [
                    np.max(list(pha_calib['dict phase target'].values())) if
                    elem >= np.mean(
                        list(pha_calib['dict phase target'].values()))
                    else
                    np.min(list(pha_calib['dict phase target'].values()))
                    for elem in self.pha]
            self.pha = treat_pha


def nanoloop_treatment(data_dict, sign_pars, dict_pha=None, dict_str=None,
                       q_fact=100.):
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
    q_fact: float, optional
        Quality factor value

    Returns
    -------
    loop_tab: list of Multiloop
        All MultiLoops
    pha_calib: dict
        Phase calibration parameters
    init_meas: dict
        Initial amplitude and phase value
    """
    dict_pha = dict_pha or {'corr': 'raw', 'func': np.cos}

    # Perform phase treatment and get pha_calib
    (_, pha_calib, _) = phase_calibration(
        data_dict['phase'], data_dict['write'], dict_pha, dict_str=dict_str)
    loop_tab = []
    for num in range(1, int(max(data_dict['index']) + 1)):
        # Extract values for the current loop
        out = extract_value(data_dict, sign_pars, num)
        (read_v, write_volt, amplitude, phase, quality_factors) = out
        # Perform amplitude / quality factor calculation
        amplitude = amp_div_q(amplitude, list_q=quality_factors, mean_q=q_fact)
        # Create MultiLoop object and append to loop_tab
        loop_tab.append(MultiLoop(write_volt, amplitude, phase, read_v,
                                  pha_calib, mode=dict_str["label"]))
    # Get initial amplitude and phase values
    amp_0, pha_0 = (loop_tab[0].amp[0], loop_tab[0].pha[0]) \
        if loop_tab[0].write_volt[0] == 0 else (None, None)

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
    quality_factors: list(n) or numpy.array(n) of float
        Array of quality factor values of the loop
    """
    write_volt = write_vec(sign_pars)
    read_v = next((data_dict['read'][cont] for cont, index in
                   enumerate(data_dict['index']) if index == num), 0)
    amplitude = [data_dict['amplitude'][cont] for cont, index in
                 enumerate(data_dict['index']) if index == num]
    phase = [data_dict['phase'][cont] for cont, index in
             enumerate(data_dict['index']) if index == num]
    quality_factors = [data_dict['q fact'][cont] for cont, index in
                       enumerate(data_dict['index']) if index == num
                       and 'q fact' in data_dict]

    return read_v, write_volt, amplitude, phase, quality_factors


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


def gen_ckpfm_meas(loop_tab):
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
    loop_tab: list(n) or numpy.array(n) of MultiLoop
        Array of MultiLoop objects

    Returns
    -------
    dict
        Measurement organized in terms of cKPFM measures
    """
    write_volt = loop_tab[0].write_volt
    read_voltage = [loop.read_volt for loop in loop_tab]
    piezorep_ckpfm = [[loop.piezorep[cont] for loop in loop_tab]
                      for cont, _ in enumerate(write_volt)]

    return {'write volt': write_volt,
            'piezorep': piezorep_ckpfm,
            'read volt': read_voltage}
