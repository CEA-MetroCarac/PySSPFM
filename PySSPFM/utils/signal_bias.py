"""
Spectroscopic bias signal functions (sspfm, dynamic, ckpfm)
"""

import numpy as np


def write_vec(sign_pars, thresh=0.):
    """
    Generate write voltage vector

    Parameters
    ----------
    sign_pars: dict
        Dict of signal bias parameters
    thresh: float, optional
        Value of reference for write volt vector 'Up' and 'Low' domain

    Returns
    -------
    write_voltage: list(n) of float
        List of write voltage value (in V)
    """
    mode_w = sign_pars['Mode (W)']
    write_voltage = np.linspace(sign_pars['Min volt (W) [V]'],
                                sign_pars['Max volt (W) [V]'],
                                sign_pars['Nb volt (W)'])

    write_voltage_inverted = np.sort(write_voltage)[::-1]
    new_write_voltage = []

    if mode_w == 'Zero, up':
        new_write_voltage.extend([elem for elem in write_voltage if
                                  elem >= thresh and
                                  elem != sign_pars['Max volt (W) [V]']])
        new_write_voltage.extend(write_voltage_inverted)
        new_write_voltage.extend([elem for elem in write_voltage if
                                  elem < thresh and
                                  elem != sign_pars['Min volt (W) [V]']])
    elif mode_w == 'Zero, down':
        new_write_voltage.extend([elem for elem in
                                  write_voltage_inverted if elem <= thresh])
        new_write_voltage.extend([elem for elem in
                                  write_voltage if elem not in
                                  (sign_pars['Min volt (W) [V]'],
                                   sign_pars['Max volt (W) [V]'])])
        new_write_voltage.extend([elem for elem in write_voltage_inverted if
                                  elem > thresh])
    elif mode_w == 'Low, up':
        new_write_voltage.extend([elem for elem in write_voltage if
                                  elem != sign_pars['Max volt (W) [V]']])
        new_write_voltage.extend([elem for elem in write_voltage_inverted if
                                  elem != sign_pars['Min volt (W) [V]']])
    elif mode_w == 'High, down':
        new_write_voltage.extend([elem for elem in write_voltage_inverted if
                                  elem != sign_pars['Min volt (W) [V]']])
        new_write_voltage.extend([elem for elem in write_voltage if
                                  elem != sign_pars['Max volt (W) [V]']])
    else:
        raise NotImplementedError

    return new_write_voltage


def read_vec(ckpfm_pars):
    """
    Generate read voltage vector (associated with ckpfm signal)

    Parameters
    ----------
    ckpfm_pars: dict
        Dict of ckpfm bias parameters

    Returns
    -------
    read_voltage: list(n) of float
        List of read voltage value (in V)
    """
    mode_r = ckpfm_pars['Mode (R)'].lower()
    if 'sweep' in mode_r:
        read_voltage = np.linspace(ckpfm_pars['Min volt (R) [V]'],
                                   ckpfm_pars['Max volt (R) [V]'],
                                   ckpfm_pars['Seg sample (R)'])
        if 'Dual' in ckpfm_pars['Mode (R)']:
            read_voltage_inverted = np.sort(read_voltage)[::-1]
            new_read_voltage = [elem for elem in read_voltage if elem >= 0
                                and elem != ckpfm_pars['Max volt (R) [V]']]
            new_read_voltage.extend(read_voltage_inverted)
            new_read_voltage.extend([elem for elem in read_voltage if elem < 0
                                     and elem !=
                                     ckpfm_pars['Min volt (R) [V]']])
            read_voltage = new_read_voltage
        if ckpfm_pars['Mode (R)'] == 'Down':
            read_voltage = np.flip(read_voltage)
    elif 'sequence' in mode_r:
        read_voltage = []
        nb_step = int(mode_r.split("_")[1])
        for elem in np.linspace(ckpfm_pars['Min volt (R) [V]'],
                                ckpfm_pars['Max volt (R) [V]'], nb_step):
            read_voltage.extend([elem] *
                                int(ckpfm_pars['Seg sample (R)'] / nb_step))
        if ckpfm_pars['Mode (R)'] == 'Down':
            read_voltage = np.flip(read_voltage)
    else:
        raise NotImplementedError

    return read_voltage


def sspfm_time(ss_pfm_bias, sspfm_pars, start_hold_time=0.):
    """
    Generate time associated with sspfm bias signal

    Parameters
    ----------
    ss_pfm_bias: list(n) or numpy.array(n) of float
        Array of sspfm bias signal single value (in V)
    sspfm_pars: dict
        sspfm bias signal parameters
    start_hold_time: float, optional
        Initial hold time (in s)

    Returns
    -------
    ss_pfm_times_calc: list(n*(nb_samp/seg)) of float
        List of time associated with sspfm bias signal (in s)
    ss_pfm_bias_calc: list(n*(nb_samp/seg)) of float
        List of sspfm bias signal associated with time (in V)
    """
    times_bias = []
    sum_time = start_hold_time
    for cont, _ in enumerate(ss_pfm_bias):
        ite = sspfm_pars['Seg durat (W) [ms]'] / 1000 if cont % 2 == 0 else \
            sspfm_pars['Seg durat (R) [ms]'] / 1000
        times_bias.append(sum_time)
        sum_time += ite

    ss_pfm_times_calc, ss_pfm_bias_calc = [], []
    for cont, (elem_bias, time_bias) in enumerate(zip(ss_pfm_bias, times_bias)):
        ite = sspfm_pars['Seg sample (W)'] if cont % 2 == 0 else \
            sspfm_pars['Seg sample (R)']
        if cont != len(ss_pfm_bias) - 1:
            sub_time = np.linspace(time_bias, times_bias[cont + 1], ite)
        else:
            sub_time = np.linspace(time_bias, time_bias +
                                   sspfm_pars['Seg durat (R) [ms]'] / 1000, ite)
        ss_pfm_bias_calc.extend([elem_bias] * ite)
        ss_pfm_times_calc.extend(sub_time)

    return ss_pfm_times_calc, ss_pfm_bias_calc


def sspfm_generator(sspfm_pars, thresh=0., open_mode=False):
    """
    Generate SS PFM bias function from electrical parameters previously set

    Parameters
    ----------
    sspfm_pars: dict
        Dict of sspfm bias signal parameters
    thresh: float, optional
        Value of reference for write volt vector 'Up' and 'Low' domain
    open_mode: bool, optional
        If True, sspfm write segment range increase linearly for each new sspfm
        cycle (i.e. opening of sspfm piezoresponse loop)

    Returns
    -------
    ss_pfm_bias: list(n) of float
        List of SS PFM signal values calculated (in V)
    """
    ss_pfm_bias = []
    min_volt_w = sspfm_pars['Min volt (W) [V]']
    max_volt_w = sspfm_pars['Max volt (W) [V]']
    med_volt_w = np.mean([max_volt_w, min_volt_w])
    incr = (max_volt_w - min_volt_w) / (2 * sspfm_pars['Nb volt (R)'])

    # Generate initial read voltage
    read_voltage = np.linspace(sspfm_pars['Min volt (R) [V]'],
                               sspfm_pars['Max volt (R) [V]'],
                               sspfm_pars['Nb volt (R)'])
    # If read mode is high to low, flip the initial read voltage
    if sspfm_pars['Mode (R)'] == 'High to Low':
        read_voltage = np.flip(read_voltage)

    # For each sspfm cycle
    for cont, read_value in enumerate(read_voltage):

        # Write voltage range increase for each iteration
        if open_mode:
            sspfm_pars['Min volt (W) [V]'] = med_volt_w - incr * (cont + 1)
            sspfm_pars['Max volt (W) [V]'] = med_volt_w + incr * (cont + 1)
        # Generate write voltage
        write_voltage = write_vec(sspfm_pars, thresh=thresh)

        for write_value in write_voltage:
            ss_pfm_bias += [write_value, read_value]

    return ss_pfm_bias


def dynamic_generator(dynamic_pars):
    """
    Generate dynamic bias function from electrical parameters previously set

    Parameters
    ----------
    dynamic_pars: dict
        Dict of dynamic bias signal parameters

    Returns
    -------
    dynamic_pars: list(n) of float
        List of dynamic signal values calculated (in V)
    dynamic_time: list(n) of float
        List of corresponding time values (in s)
    """
    # Read pulse
    nb_read = int(dynamic_pars['Time (read)'] * dynamic_pars['Freq ech'])
    read_vect = np.ones(nb_read) * dynamic_pars['Bias (read)']
    # Set pulse
    nb_set = int(dynamic_pars['Time (set)'] * dynamic_pars['Freq ech'])
    set_vect = np.ones(nb_set) * dynamic_pars['Bias (set)']
    # Switch pulse
    switch_bias_vect = np.linspace(dynamic_pars['Min bias (switch)'],
                                   dynamic_pars['Max bias (switch)'],
                                   dynamic_pars['Nb bias (switch)'])
    switch_time_vect = np.geomspace(dynamic_pars['Min time (switch)'],
                                    dynamic_pars['Max time (switch)'],
                                    dynamic_pars['Nb time (switch)'],
                                    endpoint=True)
    # Merge all segments
    segs = []
    for cont, bias in enumerate(switch_bias_vect):
        segs.append([])
        for _, time in enumerate(switch_time_vect):
            switch_vect = np.ones(int(time * dynamic_pars['Freq ech'])) * bias
            segs[cont].append(np.concatenate([set_vect, read_vect,
                                              switch_vect, read_vect]))
    dynamic_signal = [elem for seg in segs for sub_seg in seg for elem in
                      sub_seg]
    # Generate time vector
    end_time = len(dynamic_signal) / (1000 * dynamic_pars['Freq ech'])
    dynamic_time = list(np.linspace(0, end_time, len(dynamic_signal)))

    return dynamic_signal, dynamic_time


def ckpfm_generator(ckpfm_pars):
    """
    Generate cKPFM bias function from electrical parameters previously set
    N.Balke et al. : Exploring Local Electrostatic Effects with Scanning Probe
    Microscopy: Implications for Piezoresponse Force Microscopy and
    Triboelectricity ». ACS Nano 8, no 10 - 2014.
    https://doi.org/10.1021/nn505176a

    Parameters
    ----------
    ckpfm_pars: dict
        Dict of cKPFM bias signal parameters

    Returns
    -------
    ckpfm_bias: list(n) of float
        List of cKPFM signal values calculated (in V)
    ckpfm_time: list(n) of float
        List of corresponding time values (in s)
    """
    # Read segment
    read_voltage = read_vec(ckpfm_pars)
    # Write vector
    single_write_voltage = write_vec(ckpfm_pars)

    # Merge all segments
    ckpfm_bias = []
    for elem_write in single_write_voltage:
        for _ in range(ckpfm_pars['Seg sample (W)']):
            ckpfm_bias.append(elem_write)
        for elem_read in read_voltage:
            ckpfm_bias.append(elem_read)

    # Generate time vector
    ckpfm_time = list(np.linspace(0, len(ckpfm_bias) / ckpfm_pars['Freq ech'],
                                  len(ckpfm_bias)) / 1000)

    return ckpfm_bias, ckpfm_time


def extract_sspfm_bias_pars(ss_pfm_bias):
    """
    Extract SSPFM Bias Parameters from the input data.

    Parameters
    ----------
    ss_pfm_bias : list
        List of SSPFM bias values.

    Returns
    -------
    sspfm_bias_pars: dict
        A dictionary containing the extracted SSPFM bias parameters.
    """

    # Separate write and read vectors
    write_vector = ss_pfm_bias[::2]
    read_vector = ss_pfm_bias[1::2]

    # Count the number of cycles with maximum write bias
    nb_cycle = write_vector.count(max(write_vector))

    # Calculate write parameters
    write_nb_volt = len(write_vector) // (nb_cycle * 2) + 1
    if write_vector[0] == max(write_vector):
        write_wave_form = 'High, down'
    elif write_vector[0] == min(write_vector):
        write_wave_form = 'Low, up'
    elif write_vector[1] > write_vector[0]:
        write_wave_form = 'Zero, up'
    elif write_vector[1] < write_vector[0]:
        write_wave_form = 'Zero, down'
    else:
        raise NotImplementedError("Unsupported write waveform detected.")

    # Calculate read parameters
    if min(read_vector) == max(read_vector):
        read_wave_form = 'Single Read Step'
    elif read_vector[0] == max(read_vector):
        read_wave_form = 'High to Low'
    elif read_vector[0] == min(read_vector):
        read_wave_form = 'Low to High'
    else:
        raise NotImplementedError("Unsupported read waveform detected.")

    # Create a dictionary to store the extracted parameters
    sspfm_bias_pars = {
        'Write Voltage Range V': (min(write_vector), max(write_vector)),
        'Write Number of Voltages': write_nb_volt,
        'Write Wave Form': write_wave_form,
        'Read Voltage Range V': (min(read_vector), max(read_vector)),
        'Read Number of Voltages': nb_cycle,
        'Read Wave Form': read_wave_form
    }

    return sspfm_bias_pars
