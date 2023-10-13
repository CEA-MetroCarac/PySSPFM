"""
Theory of nanoloops: ferroelectric and electrostatic part differentiation from
physical equations
"""

import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.core.figure import plot_graph
from PySSPFM.utils.core.basic_func import sigmoid

from settings import FIGSIZE


def analysis(write_voltage, pr_elec, pr_ferro, mode='off field', pha_val=None):
    """
    Plot amplitude, phase and piezoresponse for all contributions
    (ferroelectric, electrostatic, and sum)

    Parameters
    ----------
    write_voltage: list or numpy.array
        List of write voltages (in V)
    pr_elec: list or numpy.array
        List of electrostatic piezoresponse (in a.u or nm)
    pr_ferro: dict
        Dictionary of ferroelectric piezoresponse (in a.u or nm)
    mode: str, optional
        'on field' or 'off field' (default is 'off field')
    pha_val: dict, optional
        Dict of phase forward and reverse value.

    Returns
    -------
    pr_tot: dict
        Total piezoresponse (in a.u or nm)
    fig: list
        Figures for amplitude, phase, and piezoresponse
    """
    pha_val = pha_val or {'fwd': 0, 'rev': 180}
    fig, (ax_1, ax_2, ax_3) = plt.subplots(1, 3, figsize=FIGSIZE)
    fig.sfn = f'{mode} nanoloops'
    pr_tot = {'left': pr_ferro['left'] + pr_elec,
              'right': pr_ferro['right'] + pr_elec}

    # Plot piezorep
    plot_dict = {'title': mode, 'x lab': 'write volt', 'y lab': 'piezorep',
                 'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1}
    tabs_dict = [{'legend': 'electrostatic', 'form': 'g-'},
                 {'legend': 'ferro', 'form': 'b-'},
                 {'legend': 'total', 'form': 'r-'},
                 {'legend': '', 'form': 'b-'},
                 {'legend': '', 'form': 'r-'}]
    piezorep_tabs = [pr_elec, pr_ferro['left'], pr_tot['left'],
                     pr_ferro['right'], pr_tot['right']]
    plot_graph(ax_1, write_voltage, piezorep_tabs, plot_dict=plot_dict,
               tabs_dict=tabs_dict)

    # Plot amplitude
    plot_dict['y lab'] = 'amplitude'
    amp_tabs = [[abs(elem) for elem in piezorep] for piezorep in piezorep_tabs]
    plot_graph(ax_2, write_voltage, amp_tabs, plot_dict=plot_dict,
               tabs_dict=tabs_dict)

    # Plot phase
    plot_dict['y lab'] = 'phase'
    pha_tabs = [[pha_val["fwd"] if elem > 0 else pha_val["rev"]
                 for elem in piezorep] for piezorep in piezorep_tabs]
    plot_graph(ax_3, write_voltage, pha_tabs, plot_dict=plot_dict,
               tabs_dict=tabs_dict)

    return pr_tot, [fig]


def main(pars, pha_val=None):
    """
    Main function

    Parameters
    ----------
    pars: dict
        Dict of parameters for write and read voltage, and for ferro loop and
        electrostatic physical characteristics
    pha_val: dict, optional
        Dict of phase forward and reverse value.

    Returns
    -------
    figs: list(3) of figure
        List of figure object
    """
    pha_val = pha_val or {'fwd': 0, 'rev': 180}
    figs = []
    write_voltage = np.linspace(pars['write']['range'][0],
                                pars['write']['range'][1], pars['write']['nb'])
    pr_elec = {'on': [pars['elec']['slope'] * (elem - pars['elec']['cpd'])
                      for elem in write_voltage],
               'off': [pars['read']['value'] - pars['elec']['slope'] *
                       pars['elec']['cpd'] for _ in write_voltage]}

    hyst_p = sigmoid(write_voltage, pars['ferro']['amp'],
                     1 / pars['ferro']['sw slope'], pars['ferro']['coer l'])
    hyst_m = sigmoid(write_voltage, pars['ferro']['amp'],
                     1 / pars['ferro']['sw slope'], pars['ferro']['coer r'])
    pr_ferro = {'left': hyst_p + pars['ferro']['offset'],
                'right': hyst_m + pars['ferro']['offset']}

    pr_tot_on, figs_1 = analysis(write_voltage, pr_elec['on'], pr_ferro,
                                 mode='on field', pha_val=pha_val)
    pr_tot_off, figs_2 = analysis(write_voltage, pr_elec['off'], pr_ferro,
                                  mode='off field', pha_val=pha_val)

    figs.extend(figs_1 + figs_2)

    pr_tot = {'on': pr_tot_on, 'off': pr_tot_off}

    diff_pr_p = [elem_on - elem_off for elem_on, elem_off in
                 zip(pr_tot['on']['left'], pr_tot['off']['left'])]
    diff_pr_m = [elem_on - elem_off for elem_on, elem_off in
                 zip(pr_tot['on']['right'], pr_tot['off']['right'])]
    pr_diff = {'left': diff_pr_p, 'right': diff_pr_m}

    plot_dict = {'title': 'coupled', 'x lab': 'write volt', 'y lab': 'piezorep'}
    tab_dict_1 = {'legend': 'diff piezorep', 'form': 'k-', 'ms': 5, 'mec': 'k',
                  'lw': 2}
    tab_dict_2 = {'legend': '', 'form': 'k-', 'ms': 5, 'mec': 'k', 'lw': 2}
    tab_dict_3 = {'legend': 'electrostatic\non field piezorep', 'form': 'g-.',
                  'ms': 5, 'mec': 'k', 'lw': 2}
    tab_dict_4 = {'legend': 'electrostatic\noff field piezorep', 'form': 'g:',
                  'ms': 5, 'mec': 'k', 'lw': 2}
    tabs_dict = [tab_dict_1, tab_dict_2, tab_dict_3, tab_dict_4]
    y_tabs = [pr_diff['left'], pr_diff['right'], pr_elec['on'], pr_elec['off']]
    fig, ax = plt.subplots(figsize=FIGSIZE)
    fig.sfn = 'diff on off field piezorep'
    plot_graph(ax, write_voltage, y_tabs, plot_dict=plot_dict,
               tabs_dict=tabs_dict)
    figs.append(fig)

    return figs
