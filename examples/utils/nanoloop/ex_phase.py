"""
Example of phase methods
"""
import os
import numpy as np
import matplotlib.pyplot as plt

from examples.utils.nanoloop.ex_analysis import init_pars

from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots, plot_graph
from PySSPFM.utils.nanoloop.gen_data import gen_nanoloops
from PySSPFM.utils.nanoloop.file import extract_nanoloop_data
from PySSPFM.utils.nanoloop.phase import \
    (phase_calibration, gen_dict_pha, apply_phase_offset,
     phase_offset_determination, mean_phase_offset)
from PySSPFM.utils.raw_extraction import data_extraction


def ex_exp_phase_calibration(type_of_data='bipolar', pha_corr='offset',
                             make_plots=False):
    """
    Example of phase_calibration function on experimental phase data.

    Parameters
    ----------
    type_of_data: str, optional
        Type of nanoloop: bipolar or unipolar nanoloop phase value.
    pha_corr: str, optional
        Phase correction type.
    make_plots: bool, optional
        Flag indicating whether to generate plots.

    Returns
    -------
    out: tuple or list
        When make_plots is True, returns a list of figures.
        When make_plots is False, returns a tuple containing treat_phase,
        and result dictionaries.
    """
    assert type_of_data in ['unipolar', 'bipolar'], \
        "'type_of_data' should be 'unipolar', 'bipolar'"
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(
        example_root_path_in, "KNN500n_2023-11-20-16h15m_out_dfrt",
        "nanoloops")
    if type_of_data == 'bipolar':
        file_path_in = os.path.join(dir_path_in,
                                    "off_f_KNN500n_SSPFM.0_00056.txt")
    elif type_of_data == 'unipolar':
        file_path_in = os.path.join(dir_path_in,
                                    "off_f_KNN500n_SSPFM.0_00076.txt")

    dict_pha = {
        'grounded tip': False,
        'positive d33': True,
        'counterclockwise': False,
        'main elec': True,
        'corr': pha_corr,
        'pha fwd': 0,
        'pha rev': 180,
        'func': np.cos,
        'locked elec slope': None
    }
    # extract experimental data
    datas_dict, dict_str, _ = extract_nanoloop_data(file_path_in)

    # ex phase_calibration
    out = phase_calibration(np.array(datas_dict['phase']).ravel(),
                            np.array(datas_dict['write']).ravel(),
                            dict_pha=dict_pha, dict_str=dict_str,
                            make_plots=make_plots)
    treat_phase, result, figs_phase_calibration = out

    if make_plots:
        for fig in figs_phase_calibration:
            fig.sfn += f"_{pha_corr}_{type_of_data}"
        return figs_phase_calibration
    else:
        return treat_phase, result


def ex_simulated_phase_calibration(pha_corr='raw', make_plots=False):
    """
    Example of phase_calibration function on simulated phase data.

    Parameters
    ----------
    pha_corr: str, optional
        Phase correction type.
    make_plots: bool, optional
        Flag indicating whether to generate plots.

    Returns
    -------
    out: tuple or list
        When make_plots is True, returns a list of figures.
        When make_plots is False, returns a tuple containing treat_phase,
        result and phase calibration dictionaries.
    """
    np.random.seed(0)
    pars, _, pha_val, noise_pars = init_pars()

    # Affine background component to phase
    affine_bck_pha = {'a': 1.05, 'b': 50}

    meas_pars = {'SSPFM Bias app': 'Sample', 'Sign of d33': 'positive'}
    # ex gen_dict_pha
    dict_pha = gen_dict_pha(meas_pars, pha_corr, pha_fwd=pha_val["fwd"],
                            pha_rev=pha_val["rev"], func=np.cos, main_elec=True)

    figs_pha, treat_phase, result = [], {}, {}

    plot_dict_on = {'label': 'On field', 'col': 'y'}
    plot_dict_off = {'label': 'Off field', 'col': 'w'}
    plot_dict = [plot_dict_on, plot_dict_off]

    for cont, mode in enumerate(['on', 'off']):
        # Generate nanoloop data
        write_voltage, _, _, pha = gen_nanoloops(
            pars, noise_pars=noise_pars, pha_val=pha_val)

        # Add affine background to phase signal
        pha[mode] = [elem * affine_bck_pha['a'] + affine_bck_pha['b']
                     for elem in pha[mode]]

        # ex phase_calibration
        out = phase_calibration(np.array(pha[mode]).ravel(),
                                np.array(write_voltage).ravel(),
                                dict_pha=dict_pha, dict_str=plot_dict[cont],
                                make_plots=make_plots)
        treat_phase[mode], result[mode], figs_phase_calibration = out
        figs_pha.extend(figs_phase_calibration)

    if make_plots:
        for fig in figs_pha:
            fig.sfn += f"_{pha_corr}"
        return figs_pha
    else:
        return treat_phase, result, dict_pha


def ex_phase_offset_determination(type_of_data='bipolar', verbose=False,
                                  make_plots=False):
    """
    Example of phase_offset_determination and mean_phase_offset functions.

    Parameters
    ----------
    type_of_data: str, optional
        Type of nanoloop: bipolar or unipolar nanoloop phase value.
    verbose: bool, optional
        Flag to activate verbosity (default is False)
    make_plots: bool, optional
        Flag to indicate whether to generate plots or not (default is False)

    Returns
    -------
    figs_hist_tab: list of plt.figure or tuple
        If make_plots is True, returns a list containing the generated figures.
        If make_plots is False, returns a tuple containing phase offset values
        and mean phase offset value.
    """
    assert type_of_data in ['unipolar', 'bipolar'], \
        "'type_of_data' should be 'unipolar', 'bipolar'"

    # File management and data extraction
    root_path_in = get_setting("example_root_path_in")
    if type_of_data == 'bipolar':
        dir_path_in = os.path.join(root_path_in,
                                   "PZT100n_reduced_2024-02-22-17h23m_out_dfrt",
                                   "nanoloops")
        file_path_in_off_f = os.path.join(
            dir_path_in, 'off_f_PIT_SSPFM_DFRT_T2ms_map.0_00000.txt')
        file_path_in_on_f = os.path.join(
            dir_path_in, 'on_f_PIT_SSPFM_DFRT_T2ms_map.0_00000.txt')
    elif type_of_data == 'unipolar':
        dir_path_in = os.path.join(root_path_in,
                                   "KNN500n_2023-11-20-16h15m_out_dfrt",
                                   "nanoloops")
        file_path_in_off_f = os.path.join(
            dir_path_in, 'off_f_KNN500n_SSPFM.0_00076.txt')
        file_path_in_on_f = os.path.join(
            dir_path_in, 'on_f_KNN500n_SSPFM.0_00076.txt')
    phase_offset_val_dict, figs_hist_tab = {}, []

    if verbose:
        print('\nex_phase_offset_determination:')
    for mode, file in zip(
            ['off', 'on'], [file_path_in_off_f, file_path_in_on_f]):
        data_dict, dict_str, _ = extract_nanoloop_data(file)

        # ex phase_offset_determination
        out = phase_offset_determination(data_dict['phase'], dict_str=dict_str,
                                         make_plots=make_plots)
        (phase_offset_val, fig_hist) = out
        phase_offset_val_dict[mode] = phase_offset_val
        figs_hist_tab += [fig_hist]
        if verbose:
            print(f'Phase offset ({mode}): {phase_offset_val}°')

    # ex mean_phase_offset
    mean_phase_offset_val = mean_phase_offset(phase_offset_val_dict)
    if verbose:
        print('\nex_mean_phase_offset:')
        print(f'Mean phase offset: {mean_phase_offset_val}°')

    if make_plots:

        return figs_hist_tab
    else:
        return phase_offset_val_dict, mean_phase_offset_val


def ex_apply_phase_offset(make_plots=False):
    """
    Example of apply_phase_offset function.

    Parameters
    ----------
    make_plots: bool, optional
        Flag to indicate whether to generate plots or not (default is False)

    Returns
    -------
    fig: plt.figure or dict
        If make_plots is True, returns a list containing the generated figure.
        If make_plots is False, returns the cleared phase data.
    """
    # File management and data extraction
    dir_path_in = os.path.join(get_setting("example_root_path_in"), "PZT100n")
    file_path_in = os.path.join(dir_path_in,
                                'PIT_SSPFM_DFRT_T2ms_map.0_00000.spm')
    dict_meas, _ = data_extraction(file_path_in, mode_dfrt=True,
                                   verbose=False)
    # Conversion factor applied to phase to convert it in °
    raw_phase = dict_meas["pha"]/5e-3

    # ex apply_phase_offset : clear switched phase data
    offset_phase = apply_phase_offset(raw_phase, offset=84)

    if make_plots:
        figsize = get_setting("figsize")
        fig, ax = plt.subplots(figsize=figsize)
        fig.sfn = "ex_apply_phase_offset"
        plot_dict = {'title': '', 'x lab': 'time (s)',
                     'y lab': 'phase (°)', 'fs': 13, 'edgew': 3,
                     'tickl': 5, 'gridw': 1, 'lw': 1}
        tab_dict = {'form': 'r-', 'legend': 'raw phase'}
        plot_graph(ax, dict_meas['times'], raw_phase,
                   plot_dict=plot_dict, tabs_dict=tab_dict)
        tab_dict = {'form': 'g-', 'legend': 'offset phase'}
        plot_graph(ax, dict_meas['times'], offset_phase,
                   plot_dict=plot_dict, tabs_dict=tab_dict, plot_leg=True)

        return [fig]
    else:
        return offset_phase


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_phase", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_exp_phase_calibration(type_of_data='bipolar', pha_corr='offset',
                                     make_plots=True)
    figs += ex_exp_phase_calibration(type_of_data='unipolar', pha_corr='offset',
                                     make_plots=True)
    figs += ex_simulated_phase_calibration(pha_corr='raw', make_plots=True)
    figs += ex_simulated_phase_calibration(pha_corr='offset', make_plots=True)
    figs += ex_simulated_phase_calibration(pha_corr='affine', make_plots=True)
    figs += ex_simulated_phase_calibration(pha_corr='up_down', make_plots=True)
    figs += ex_phase_offset_determination(type_of_data='bipolar', verbose=True,
                                          make_plots=True)
    figs += ex_phase_offset_determination(type_of_data='unipolar', verbose=True,
                                          make_plots=True)
    figs += ex_apply_phase_offset(make_plots=True)

    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
