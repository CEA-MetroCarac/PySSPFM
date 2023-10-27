"""
Module used to generate nanoloops and sspfm maps from physical equation
"""

from PySSPFM.utils.nanoloop.gen_datas import gen_loops


def gen_datas_dict(pars, q_fact=100., mode='off', pha_val=None):
    """
    Generate txt loop file data form.

    Parameters
    ----------
    pars: dict
        Dictionary of parameters for write and read voltage, and for ferro loop
        and electrostatic physical characteristics.
    q_fact: float, optional
        Quality factor value.
    mode: str
        'on' for on field measurements or 'off' for off field measurements.
    pha_val: dict, optional
        Dict of phase forward and reverse value.

    Returns
    -------
    datas_dict: dict
        Dictionary containing all the data of the loop (txt loop file data
        form).
    dict_str: dict
        Dictionary used for figure annotation.
    """
    assert mode in ['off', 'on']
    pha_val = pha_val or {'fwd': 0, 'rev': 180}

    datas_dict = {}
    out = gen_loops(pars, noise_pars=pars['noise'], pha_val=pha_val)
    write_voltage, read_voltage, amplitude, phase = out
    key_labs = ['index', 'read', 'write', 'amplitude', 'phase', 'freq',
                'q fact', 'inc amp', 'inc pha']
    for lab in key_labs:
        datas_dict[lab] = []

    for cont, tab in enumerate(amplitude[mode]):
        for i, _ in enumerate(tab):
            for key, meas in zip(['amplitude', 'phase'], [amplitude, phase]):
                datas_dict[key].append(meas[mode][cont][i])
            datas_dict['index'].append(cont + 1)
            datas_dict['read'].append(read_voltage[cont])
            datas_dict['write'].append(write_voltage[cont][i])
            datas_dict['q fact'].append(q_fact)

    if mode == 'on':
        label, col = 'On field', 'y'
    else:
        label, col = 'Off field', 'w'

    dict_str = {'unit': 'nm',
                'label': label,
                'col': col}

    return datas_dict, dict_str
