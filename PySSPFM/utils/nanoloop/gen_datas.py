"""
Module used to generate nanoloops from physical equations
"""

import numpy as np

from PySSPFM.utils.core.basic_func import sigmoid
from PySSPFM.utils.core.noise import noise


def gen_loops(pars, noise_pars=None, pha_val=None):
    """
    Generate nanoloops amplitude and phase datas with associated voltage from
    ferroelectric and electrostatic physical equations

    Parameters
    ----------
    pars: dict
        Dict of parameters for write and read voltage, and for ferro loop and
        electrostatic physical characteristics
    noise_pars: dict, optional
        Dict of noise parameters
    pha_val: dict, optional
        Dict of phase forward and reverse value

    Returns
    -------
    write_voltage_loop: numpy.array(n*m) of float
        Array of write voltage in measure shape (Zero, Up) (in V)
    read_voltage: numpy.array(p) of float
        Array of read voltage (in V)
    amp_loop: numpy.array(n*m) of float
        Array of amplitude values in measure shape (Zero, Up) (in a.u or nm)
    pha_loop: numpy.array(n*m) of float
        Array of phase values in measure shape (Zero, Up) (in °)
    """
    noise_pars = noise_pars or {'type': 'normal', 'ampli': 0.}
    pha_val = pha_val or {'fwd': 0, 'rev': 180}

    write_voltage = np.linspace(pars['write']['range'][0],
                                pars['write']['range'][1], pars['write']['nb'])
    read_voltage = np.linspace(pars['read']['range'][0],
                               pars['read']['range'][1], pars['read']['nb'])

    pr_elec = {'on': [], 'off': []}
    for cont, elem_read in enumerate(read_voltage):
        pr_elec['on'].append([pars['elec']['slope'] *
                              (elem_write - pars['elec']['cpd'])
                              for elem_write in write_voltage])
        pr_elec['off'].append([pars['elec']['slope'] *
                               (elem_read - pars['elec']['cpd'])
                               for _ in range(len(write_voltage))])

    hyst_p = sigmoid(write_voltage, pars['ferro']['amp'],
                     1 / pars['ferro']['sw slope'], pars['ferro']['coer l'])
    hyst_m = sigmoid(write_voltage, pars['ferro']['amp'],
                     1 / pars['ferro']['sw slope'], pars['ferro']['coer r'])
    pr_ferro = {'left': hyst_p + pars['ferro']['offset'],
                'right': hyst_m + pars['ferro']['offset']}

    pr_tot = {'on': [], 'off': []}
    for cont, elem in enumerate(read_voltage):
        pr_tot['on'].append({
            'left': pr_ferro['left'] + pr_elec['on'][cont],
            'right': pr_ferro['right'] + pr_elec['on'][cont]
        })
        pr_tot['off'].append({
            'left': pr_ferro['left'] + pr_elec['off'][cont],
            'right': pr_ferro['right'] + pr_elec['off'][cont]
        })

    amp, pha = {}, {}
    for mode in ['on', 'off']:
        amp[mode], pha[mode] = [], []
        for cont, _ in enumerate(read_voltage):
            amp[mode].append({})
            pha[mode].append({})
            for sens in ['left', 'right']:
                amp_val = [abs(elem) for elem in pr_tot[mode][cont][sens]]
                amp[mode][cont][sens] = noise(amp_val, noise_pars,
                                              relative=True)
                phase_val = [pha_val['fwd'] if elem > 0 else
                             pha_val['rev'] for elem in
                             pr_tot[mode][cont][sens]]
                pha[mode][cont][sens] = noise(phase_val, noise_pars,
                                              relative=True)

    amp_loop, pha_loop = {}, {}
    write_voltage_loop, amp_loop['on'] = transform_datas(
        write_voltage, amp['on'], read_voltage)
    _, pha_loop['on'] = transform_datas(write_voltage, pha['on'], read_voltage)
    _, amp_loop['off'] = transform_datas(
        write_voltage, amp['off'], read_voltage)
    _, pha_loop['off'] = transform_datas(
        write_voltage, pha['off'], read_voltage)

    return write_voltage_loop, read_voltage, amp_loop, pha_loop


def transform_datas(write_volt, signal, read_volt):
    """
    Transform 'left' and 'right' write voltage and signal in real measure shape
    (Zero, Up)

    Parameters
    ----------
    write_volt: numpy.array(n) or list(n) of float
        List of write voltage (in V)
    signal: numpy.array(p) or list(p) of dict
        List of considered signal for 'left' and 'right' segment
    read_volt: numpy.array(p) or list(p) of float
        List of read voltage (in V)

    Returns
    -------
    write_volt_loop: numpy.array(p*(n-2))
        Array of write voltage in measure shape (Zero, Up) (in V)
    signal_loop: numpy.array(p*(n-2))
        Array of signal values in measure shape (Zero, Up)
    """
    write_volt_loop, signal_loop = [], []
    for cont, _ in enumerate(read_volt):
        neg_part_volt, pos_part_volt, neg_part_sign, pos_part_sign = \
            [], [], [], []
        for sub_cont, elem in enumerate(write_volt):
            if elem >= 0:
                pos_part_volt.append(elem)
                pos_part_sign.append(signal[cont]['right'][sub_cont])
            else:
                neg_part_volt.append(elem)
                neg_part_sign.append(signal[cont]['right'][sub_cont])

        write_volt_loop.append(np.concatenate(
            [pos_part_volt, np.flip(write_volt[1:-1]), neg_part_volt]))
        signal_loop.append(np.concatenate(
            [pos_part_sign, np.flip(signal[cont]['left'][1:-1]),
             neg_part_sign]))

    return write_volt_loop, signal_loop
