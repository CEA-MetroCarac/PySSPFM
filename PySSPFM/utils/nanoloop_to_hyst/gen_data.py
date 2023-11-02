"""
Module used to generate nanoloops and sspfm maps from physical equation
"""

from PySSPFM.utils.nanoloop.gen_data import gen_nanoloops


def gen_data_dict(pars, q_fact=100., mode='off', pha_val=None):
    """
    Generate txt nanoloop file data form.

    Parameters
    ----------
    pars: dict
        Dictionary of parameters for write and read voltage, and for ferro
        nanoloop
        and electrostatic physical characteristics.
    q_fact: float, optional
        Quality factor value.
    mode: str
        'on' for on field measurements or 'off' for off field measurements.
    pha_val: dict, optional
        Dict of phase forward and reverse value.

    Returns
    -------
    data_dict: dict
        Dictionary containing all the data of the nanoloop (txt nanoloop file
        data form).
    dict_str: dict
        Dictionary used for figure annotation.
    """
    assert mode in ['off', 'on']
    pha_val = pha_val or {'fwd': 0, 'rev': 180}

    data_dict = {}
    out = gen_nanoloops(pars, noise_pars=pars['noise'], pha_val=pha_val)
    write_voltage, read_voltage, amplitude, phase = out
    key_labs = ['index', 'read', 'write', 'amplitude', 'phase', 'freq',
                'q fact', 'inc amp', 'inc pha']
    for lab in key_labs:
        data_dict[lab] = []

    for cont, tab in enumerate(amplitude[mode]):
        for i, _ in enumerate(tab):
            for key, meas in zip(['amplitude', 'phase'], [amplitude, phase]):
                data_dict[key].append(meas[mode][cont][i])
            data_dict['index'].append(cont + 1)
            data_dict['read'].append(read_voltage[cont])
            data_dict['write'].append(write_voltage[cont][i])
            data_dict['q fact'].append(q_fact)

    if mode == 'on':
        label, col = 'On field', 'y'
    else:
        label, col = 'Off field', 'w'

    dict_str = {'unit': 'nm',
                'label': label,
                'col': col}

    return data_dict, dict_str
