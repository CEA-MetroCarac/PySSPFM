"""
--> Executable Script
Viewing of raw signal of a sspfm datacube file
Inspired by SS_PFM script, Nanoscope, Bruker
"""
import tkinter.filedialog as tkf

from PySSPFM.settings import get_setting, get_config
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.datacube_to_nanoloop.plot import plt_signals
from PySSPFM.utils.raw_extraction import data_extraction
from PySSPFM.utils.path_for_runable import save_path_management


def main_raw_file_reader(file_path_in, mode='classic', verbose=False):
    """
    Main function used for raw file viewing

    Parameters
    ----------
    file_path_in: str
        Path of datacube SSPFM raw file measurements.
        This parameter specifies the path where datacube SSPFM raw file
        measurements are located. It is used to indicate the path to the file
        containing these measurements.
    mode: str, optional
        Treatment used for segment data analysis
        (extraction of PFM measurements).
        This parameter determines the treatment method used for segment data
        analysis, specifically for the extraction of PFM measurements.
        Two possible values: 'classic' (sweep or single frequency) or 'dfrt'.
    verbose: bool, optional
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.

    Returns
    -------
    fig: plt.figure
    """
    # Data extraction from measurement file and identification
    dict_meas, _ = data_extraction(
        file_path_in, mode_dfrt=bool(mode.lower() == 'dfrt'), verbose=verbose)
    # Plot raw signals in time
    fig = plt_signals(dict_meas, unit='')

    return [fig]


def main(fname_json=None):
    """
    Main function for data analysis.

    fname_json: str
        Path to the JSON file containing user parameters. If None,
        the file is created in a default path:
        (your_user_disk_access/.pysspfm/script_name_params.json)
    """
    if get_setting("extract_parameters") in ['json', 'toml']:
        config_params, _ = get_config(__file__, fname_json)
        file_path_in = config_params['file_path_in']
        dir_path_out = config_params['dir_path_out']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save_plots = config_params['save_plots']
        mode = config_params['mode']
    elif get_setting("extract_parameters") == 'python':
        file_path_in = tkf.askopenfilename()
        # file_path_in = r'...\KNN500n\KNN500n.0_00001.spm
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_toolbox\plot_pix_extrem_2023-10-02-16h38m
        verbose = True
        show_plots = True
        save_plots = False
        # Mode = 'dfrt' or 'classic' (sweep or single frequency)
        mode = 'classic'
    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    figs = []
    # Generate default path out
    dir_path_out = save_path_management(
        file_path_in, dir_path_out, save=save_plots,
        dirname="raw_file_reader", lvl=1, create_path=True, post_analysis=False)
    # Main function
    figs += main_raw_file_reader(file_path_in, mode=mode, verbose=verbose)
    # Plot figures
    print_plots(figs, show_plots=show_plots, save_plots=save_plots,
                dirname=dir_path_out, transparent=False)


if __name__ == '__main__':
    main()
