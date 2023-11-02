"""
Example of phase methods
"""
import numpy as np

from examples.utils.nanoloop.ex_analysis import init_pars
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.nanoloop.gen_data import gen_nanoloops
from PySSPFM.utils.nanoloop.phase import phase_calibration, gen_dict_pha


def ex_phase_calibration(pha_corr='raw', make_plots=False):
    """
    Example of phase_calibration function.

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

    meas_pars = {'Bias app': 'Sample', 'Sign of d33': 'positive'}
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


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_phase", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_phase_calibration(pha_corr='raw', make_plots=True)
    figs += ex_phase_calibration(pha_corr='offset', make_plots=True)
    figs += ex_phase_calibration(pha_corr='affine', make_plots=True)
    figs += ex_phase_calibration(pha_corr='up_down', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
