"""
Example of file methods
"""
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.signal_bias import sspfm_generator
from PySSPFM.utils.nanoloop.gen_data import gen_nanoloops
from PySSPFM.utils.nanoloop.file import \
    sort_nanoloop_data, save_nanoloop_file, extract_nanoloop_data

from PySSPFM import EXAMPLE_ROOT_PATH_OUT, DEFAULT_DATA_PATH_OUT
from PySSPFM.settings import FIGSIZE


def example_file(make_plots=False, verbose=False):
    """
    Example of file functions.

    Parameters
    ----------
    make_plots: bool, optional
        Flag indicating whether to generate plots.
    verbose: bool, optional
        Flag indicating whether to print verbose output.

    Returns
    -------
    results: tuple or list
        Depending on the value of `make_plots`, either a list of figures or a
        tuple of file-related results.
    """
    # File management
    if make_plots:
        dir_path_out_data = os.path.join(
            EXAMPLE_ROOT_PATH_OUT, "ex_nanoloop_file")
    else:
        dir_path_out_data = os.path.join(
            DEFAULT_DATA_PATH_OUT, "test_nanoloop_file")
    if os.path.isdir(dir_path_out_data):
        shutil.rmtree(dir_path_out_data)
    os.makedirs(dir_path_out_data)
    f_name_out = 'txt_file.txt'

    # Parameters
    elec_pars = {'cpd': 0.3,
                 'slope': -2}
    ferro_pars = {'amp': 5,
                  'coer l': -4,
                  'coer r': 3,
                  'sw slope': 1,
                  'offset': 1}
    pha_val = {"fwd": 0, "rev": 180}
    # Noise (relative amplitude in %)
    noise_pars = {'type': 'normal',
                  'ampli': 10}
    sign_pars = {'Min volt (R) [V]': 0,
                 'Max volt (R) [V]': 0,
                 'Nb volt (R)': 5,
                 'Mode (R)': 'Low to High',
                 'Seg durat (R) [ms]': 500,
                 'Seg sample (R)': 100,
                 'Min volt (W) [V]': -10,
                 'Max volt (W) [V]': 10,
                 'Nb volt (W)': 51,
                 'Mode (W)': 'Zero, up',
                 'Seg durat (W) [ms]': 500,
                 'Seg sample (W)': 100}

    write_pars = {'range': [sign_pars['Min volt (W) [V]'],
                            sign_pars['Max volt (W) [V]']],
                  'nb': sign_pars['Nb volt (W)'],
                  'mode': sign_pars['Mode (W)']}
    read_pars = {'range': [sign_pars['Min volt (R) [V]'],
                           sign_pars['Max volt (R) [V]']],
                 'nb': sign_pars['Nb volt (R)']}
    pars = {'write': write_pars,
            'read': read_pars,
            'elec': elec_pars,
            'ferro': ferro_pars}

    np.random.seed(0)
    # Generate nanoloop data
    _, _, amp, pha = gen_nanoloops(pars, noise_pars=noise_pars, pha_val=pha_val)

    plt_dict_on = {'label': 'On field',
                   'col': 'y',
                   'unit': 'u.a',
                   'mode': 'dfrt'}
    plt_dict_off = {'label': 'Off field',
                    'col': 'w',
                    'unit': 'u.a',
                    'mode': 'dfrt'}
    plt_dict = [plt_dict_on, plt_dict_off]

    # Generate bias signal
    sspfm_bias = sspfm_generator(sign_pars)

    figs_file = []
    (loop_tabs, fmts, headers, file_paths_out, datas_dicts,
     dict_strs) = ({}, {}, {}, {}, {}, {})
    for cont, mode in enumerate(['on', 'off']):
        amp[mode] = np.concatenate(amp[mode])
        pha[mode] = np.concatenate(pha[mode])
        dict_res = {'Amplitude': amp[mode], 'Phase': pha[mode]}
        # ex sort_nanoloop_data
        out = sort_nanoloop_data(
            sspfm_bias, sign_pars['Nb volt (W)'], sign_pars['Nb volt (R)'],
            dict_res, unit='nm')
        (loop_tab, fmt, header) = out

        # ex save_nanoloop_file
        file_path_out = save_nanoloop_file(
            dir_path_out_data, f_name_out, loop_tab, fmt, header,
            mode=plt_dict[cont]['label'])
        # ex extract_nanoloop_data
        datas_dict, dict_str = extract_nanoloop_data(file_path_out)
        if verbose:
            print(f'dict_str: {dict_str}')

        # Plot
        if make_plots:
            fig, axs = plt.subplots(1, 2, figsize=FIGSIZE)
            fig.sfn = f'ex_file_{mode}_field'
            amp_tab_dict, pha_tab_dict = {'form': 'r.-'}, {'form': 'b.-'}
            (y_tabs_amp, y_tabs_pha, amp_tabs_dict, pha_tabs_dict,
             write_volt) = ([], [], [], [], [])
            for i in range(1, sign_pars['Nb volt (R)'] + 1):
                y_tabs_amp.append([])
                y_tabs_pha.append([])
                amp_tabs_dict.append(amp_tab_dict)
                pha_tabs_dict.append(pha_tab_dict)
                for j, index in enumerate(datas_dict['index']):
                    if i == index:
                        y_tabs_amp[i - 1].append(datas_dict['amplitude'][j])
                        y_tabs_pha[i - 1].append(datas_dict['phase'][j])
                        if index == 1:
                            write_volt.append(datas_dict['write'][j])
            plot_dict = {'title': 'Amp Loops', 'x lab': 'Write voltage [V]',
                         'y lab': 'Amplitude [nm]',
                         'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1}
            plot_graph(axs[0], write_volt, y_tabs_amp, plot_dict=plot_dict,
                       tabs_dict=amp_tabs_dict)
            plot_dict = {'title': 'Pha Loops', 'x lab': 'Write voltage [V]',
                         'y lab': 'Phase [°]',
                         'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1}
            plot_graph(axs[1], write_volt, y_tabs_pha, plot_dict=plot_dict,
                       tabs_dict=pha_tabs_dict)
            fig.suptitle(f'{mode} field', size=15)
            figs_file.append(fig)
        else:
            (loop_tabs[mode], fmts[mode], headers[mode], file_paths_out[mode],
             datas_dicts[mode], dict_strs[mode]) = \
                (loop_tab, fmt, header, file_path_out, datas_dict, dict_str)

    if make_plots:
        return figs_file
    else:
        return loop_tabs, fmts, headers, datas_dicts, dict_strs


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_file", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += example_file(make_plots=True, verbose=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
