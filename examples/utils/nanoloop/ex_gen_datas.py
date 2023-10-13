"""
Example of gen_datas methods
"""
import numpy as np
import matplotlib.pyplot as plt

from examples.utils.nanoloop.ex_analysis import init_pars
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import plot_graph, print_plots
from PySSPFM.utils.nanoloop.gen_datas import gen_loops

from settings import FIGSIZE


def ex_gen_loops(mode, make_plots=False):
    """
    Example of gen_loops function.

    Parameters
    ----------
    mode: str
        Mode of operation, either 'on' or 'off'.
    make_plots: bool, optional
        Flag indicating whether to generate plots.

    Returns
    -------
    output: tuple or list
        Depending on the value of `make_plots`, either a list of figures or a
        tuple of loop-related results.
    """
    assert mode in ['on', 'off']

    # Initialize parameters
    pars, _, pha_val, noise_pars = init_pars()
    np.random.seed(0)

    # ex gen_loops
    out = gen_loops(pars, noise_pars=noise_pars, pha_val=pha_val)
    write_voltage, read_voltage, amp, pha = out

    # Plot
    if make_plots:
        figs_genloop = []
        plot_dict = {'fs': 13, 'edgew': 3, 'tickl': 5, 'gridw': 1}
        fig, axs = plt.subplots(2, pars['read']['nb'], figsize=FIGSIZE)
        fig.sfn = f'ex_gen_loops_{mode}_field'
        fig.suptitle(f'{mode} field', size=plot_dict['fs'], weight='heavy')
        for i in range(pars['read']['nb']):
            plot_dict['y lab'] = 'Amplitude [nm]' if i == 0 else ''
            plot_dict['x lab'] = ''
            plot_graph(axs[0, i], write_voltage[i], amp[mode][i],
                       plot_dict=plot_dict)
            plot_dict['y lab'] = 'Phase [°]' if i == 0 else ''
            plot_dict['x lab'] = 'Write voltage [V]'
            plot_graph(axs[1, i], write_voltage[i], pha[mode][i],
                       plot_dict=plot_dict)
        figs_genloop.append(fig)

        return figs_genloop
    else:
        return write_voltage, read_voltage, amp[mode], pha[mode]


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_gen_datas", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_gen_loops('on', make_plots=True)
    figs += ex_gen_loops('off', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
