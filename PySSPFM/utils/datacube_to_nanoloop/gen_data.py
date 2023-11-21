"""
Module used to generate segment of sspfm datacube measure
"""

import random
import numpy as np

from PySSPFM.utils.core.noise import noise
from PySSPFM.utils.core.basic_func import sho, sho_phase
from PySSPFM.utils.signal_bias import sspfm_generator, sspfm_time
from PySSPFM.utils.nanoloop.gen_data import gen_nanoloops


def alea_targets(meas_range, ite=1):
    """
    Generate alea targets measurement (amplitude and phase) for each segment

    Parameters
    ----------
    meas_range: dict
        Dict of alea measurement range for segments
    ite: int, optional
        Nb of target amplitude and phase values

    Returns
    -------
    targets: dict
        Target amplitude and phase values associated for each segment
    """
    targets = {'on': {'amp': [], 'pha': []}, 'off': {'amp': [], 'pha': []}}

    for field in ['on', 'off']:
        for _ in range(ite):
            for key in ['amp', 'pha']:
                targets[field][key].append(random.randint(meas_range[key][0],
                                                          meas_range[key][1]))

    return targets


def loop_targets(loop_pars, noise_pars=None, pha_val=None):
    """
    Generate nanoloop targets measurement (amplitude and phase) for each segment

    Parameters
    ----------
    loop_pars: dict
        Dict of physical parameters of the nanoloop
    noise_pars: dict, optional
        Dict of nanoloop noise
    pha_val: dict, optional
        Dict of phase forward and reverse value

    Returns
    -------
    targets: dict
        Target amplitude and phase values associated for each segment
    """
    noise_pars = noise_pars or {'type': 'normal', 'ampli': 0.}
    pha_val = pha_val or {'fwd': 0, 'rev': 180}

    _, _, amp, pha = gen_nanoloops(
        loop_pars, noise_pars=noise_pars, pha_val=pha_val)

    targets = {'on': {'amp': [], 'pha': []}, 'off': {'amp': [], 'pha': []}}

    for field in ['on', 'off']:
        for key, meas in zip(['amp', 'pha'], [amp, pha]):
            targets[field][key] = [elem for sublist in meas[field]
                                   for elem in sublist]

    return targets


def measure_stable(nb_samp=100, target=None, noise_pars=None):
    """
    Generate amplitude and phase segment more or less stable values with noise

    Parameters
    ----------
    nb_samp: int, optional
        Number of samples in the segment
    target: dict, optional
        Dict of amplitude and phase target values for the segment
    noise_pars: dict, optional
        Dict of noise parameters

    Returns
    -------
    seg_amp: numpy.array(n) of float
        Array of amplitude values of the segment (in nm or a.u)
    seg_pha: numpy.array(n) of float
        Array of phase values of the segment (in °)
    """
    noise_pars = noise_pars or {'type': 'normal', 'ampli': 0.}
    target = target or {'amp': 10., 'pha': 0.}

    seg_amp = np.ones(nb_samp) * target['amp']
    seg_pha = np.ones(nb_samp) * target['pha']

    seg_amp[0], seg_pha[0] = 0, 0

    seg_amp = noise(seg_amp, noise_pars, relative=True)
    seg_pha = noise(seg_pha, noise_pars, relative=True)

    return seg_amp, seg_pha


def measure_peak(nb_samp=100, target=None, noise_pars=None):
    """
    Generate amplitude and phase segment values with noise for sweep mode

    Parameters
    ----------
    nb_samp: int, optional
        Number of samples in the segment
    target: dict, optional
        Dict of amplitude and phase target values
    noise_pars: dict, optional
        Dict of noise parameters

    Returns
    -------
    seg_amp: numpy.array(n) of float
        Array of amplitude values of the segment (in nm or a.u)
    seg_pha: numpy.array(n) of float
        Array of phase values of the segment (in °)
    """
    noise_pars = noise_pars or {'type': 'normal', 'ampli': 0.}
    target = target or {'amp': 10., 'pha': 0.}

    x_range = [0, 10]
    x0_range = [3, 7]
    qfact_range = [50, 150]

    peak_pars = {'ampli': target['amp'],
                 'x0': random.randint(x0_range[0] * 10, x0_range[1] * 10) / 10,
                 'qfact': random.randint(qfact_range[0] * 10,
                                         qfact_range[1] * 10) / 10}

    seg_amp = sho(np.linspace(x_range[0], x_range[1], nb_samp),
                  peak_pars['ampli'], peak_pars['qfact'], peak_pars['x0'])

    offset = target['pha']
    seg_pha = sho_phase(np.linspace(x_range[0], x_range[1], nb_samp),
                        180 / np.pi, peak_pars['qfact'], peak_pars['x0'])
    seg_pha += offset

    seg_amp = noise(seg_amp, noise_pars, relative=True)
    seg_pha = noise(seg_pha, noise_pars, relative=True)

    return seg_amp, seg_pha


def gen_segments(sign_pars, mode='dfrt', seg_noise_pars=None, hold_dict=None,
                 loop_pars=None, alea_target_range=None):
    """
    Transform 'left' and 'right' write voltage and signal in real measure shape
    (Zero, Up)

    Parameters
    ----------
    sign_pars: dict
        Dict of sspfm bias signal parameters
    mode: str, optional
        Operating mode for analysis: four possible modes:
        - 'max': for analysis of the resonance with max peak value
        (frequency sweep in resonance)
        - 'fit': for analysis of the resonance with a SHO fit of the peak
        (frequency sweep in resonance)
        - 'single_freq': for analysis performed at single frequency,
        average of segment (in or out of resonance)
        - 'dfrt': for analysis performed with dfrt, average of segment
    seg_noise_pars: dict, optional
        Dict of noise parameters for segment
    hold_dict: dict, optional
        Dict containing hold segment parameters
    loop_pars: dict, optional
        Dict of nanoloop parameters for generation of physical target
        measurement (amplitude and phase)
    alea_target_range: dict, optional
        Dict of range for generation of alea target measurement
        (amplitude and phase)

    Returns
    -------
    dict_meas: dict
        Dict of all measurements
    """
    assert mode in ['max', 'fit', 'single_freq', 'dfrt']
    seg_noise_pars = seg_noise_pars or {'type': 'normal', 'ampli': 0.}

    dict_meas = {'sspfm bias': sspfm_generator(sign_pars)}
    out = sspfm_time(dict_meas['sspfm bias'], sign_pars,
                     start_hold_time=hold_dict['start time'])
    dict_meas['times'], dict_meas['tip_bias'] = out

    dict_meas['amp'], dict_meas['pha'] = [], []

    ite = (sign_pars['Nb volt (W)'] - 1) * 2 * sign_pars['Nb volt (R)']

    if alea_target_range is not None:
        targets = alea_targets(alea_target_range, ite=ite)
    else:
        targets = loop_targets(loop_pars, noise_pars=loop_pars['noise'])

    for i in range(ite):
        for field, nb_samp in zip(['on', 'off'], [sign_pars['Seg sample (W)'],
                                                  sign_pars['Seg sample (R)']]):
            if mode in ['dfrt', 'single_freq']:
                seg_amp, seg_pha = measure_stable(nb_samp=nb_samp, target={
                    'amp': targets[field]['amp'][i],
                    'pha': targets[field]['pha'][i]}, noise_pars=seg_noise_pars)
            else:
                seg_amp, seg_pha = measure_peak(nb_samp=nb_samp, target={
                    'amp': targets[field]['amp'][i],
                    'pha': targets[field]['pha'][i]}, noise_pars=seg_noise_pars)
            dict_meas['amp'].extend(seg_amp)
            dict_meas['pha'].extend(seg_pha)

    hold_seg = {'times': {'start': [], 'end': []},
                'tip_bias': {'start': [], 'end': []},
                'amp': {'start': [], 'end': []},
                'pha': {'start': [], 'end': []}}

    if hold_dict is not None:
        for i in range(hold_dict['start samp']):
            hold_time = i / hold_dict['start samp'] * hold_dict['start time']
            hold_seg['times']['start'].append(hold_time)
            for key in ['tip_bias', 'amp', 'pha']:
                hold_seg[key]['start'].append(0)

        offset_time = dict_meas['times'][-1]
        for i in range(hold_dict['end samp']):
            hold_time = i / hold_dict['end samp'] * hold_dict['end time']
            hold_time += offset_time
            hold_seg['times']['end'].append(hold_time)
            for key in ['tip_bias', 'amp', 'pha']:
                hold_seg[key]['end'].append(0)

        for key in ['times', 'tip_bias', 'amp', 'pha']:
            dict_meas[key] = np.concatenate([hold_seg[key]['start'],
                                             dict_meas[key],
                                             hold_seg[key]['end']])

    dict_meas['deflection'] = []
    dict_meas['times_bias'] = dict_meas['times']

    return dict_meas
