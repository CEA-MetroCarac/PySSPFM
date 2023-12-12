"""
Example of plot methods
"""

from examples.utils.datacube_to_nanoloop.ex_gen_data import \
    ex_gen_segments, pars_segment
from examples.utils.datacube_to_nanoloop.ex_analysis import \
    ex_segments, list_segs
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.datacube_to_nanoloop.plot import \
    amp_pha_map, plt_bias, plt_amp, plt_signals


def ex_plt_bias():
    """ Example of plt_bias function """
    # Generate segments
    dict_meas = ex_gen_segments('dfrt', make_plots=False)
    # ex plt_bias
    fig = plt_bias(dict_meas['tip_bias'], dict_meas['sspfm bias'], dict_meas)

    return [fig]


def ex_plt_amp():
    """ Example of plt_amp functions """
    # Generate segments
    dict_meas = ex_gen_segments('dfrt', make_plots=False)
    # ex plt_amp
    fig = plt_amp(dict_meas, unit='nm')

    return [fig]


def ex_plt_signals():
    """ Example of plt_signals functions """
    # Generate segments
    dict_meas = ex_gen_segments('dfrt', make_plots=False)
    # ex plt_signals
    fig = plt_signals(dict_meas, unit='nm')

    return [fig]


def ex_amp_pha_map(analysis, mode):
    """
    Example of amp_pha_map function

    Parameters
    ----------
    analysis: str
        Analysis type
    mode: str
        Mode type ('on f' or 'off f')

    Returns
    -------
    fig: list
        List containing the figure object
    """
    assert mode in ['on f', 'off f']

    # Get parameters
    seg_pars, sign_pars, _, _, _, _, _ = pars_segment()
    mapping_label = {'on f': 'On Field', 'off f': 'Off Field'}
    index_hold = {'start': 20, 'end': 20}
    sweep_freq = {'start': 200, 'end': 400}
    unit = 'nm'

    # Get segments and measurement dictionary
    segs, dict_meas = list_segs(analysis, nb_seg_str='all')

    # ex amp_pha_map
    fig = amp_pha_map(
        segs[mode], dict_meas, index_hold_start=index_hold['start'],
        index_hold_end=index_hold['end'], freq_range=sweep_freq,
        read_nb_voltages=sign_pars['Nb volt (R)'],
        cut_seg=seg_pars['cut seg [%]'], mapping_label=mapping_label[mode],
        unit=unit, mode=seg_pars['mode'])
    fig.sfn += f"_{analysis}"
    return [fig]


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "datacube_to_nanoloop_plot", save_example_exe=True, save_test_exe=False)
    figs = []
    figs += ex_plt_bias()
    figs += ex_plt_amp()
    figs += ex_plt_signals()
    figs += ex_amp_pha_map('max', 'off f')
    figs += ex_amp_pha_map('dfrt', 'off f')
    figs += ex_segments('max', 'off f', make_plots=True)
    figs += ex_segments('fit', 'off f', make_plots=True)
    figs += ex_segments('dfrt', 'off f', make_plots=True)
    print_plots(figs, save_plots=save_plots, show_plots=True,
                dirname=dir_path_out, transparent=False)
