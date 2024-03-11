r"""
--> Executable Script
Extraction of .txt local nanoloop of the sample surface file data and
visualisation
Inspired by SS_PFM script, Nanoscope, Bruker
"""

import os
import tkinter.filedialog as tkf
from datetime import datetime
import numpy as np

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.raw_extraction import csv_meas_sheet_extract
from PySSPFM.utils.nanoloop.plot import main_plot
from PySSPFM.utils.nanoloop.file import extract_nanoloop_data
from PySSPFM.utils.nanoloop.analysis import nanoloop_treatment
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


def main_loop_file_reader(file_path, csv_path=None, dict_pha=None,
                          del_1st_loop=False, verbose=False,
                          make_plots=False):
    """
    Main function for nanoloops visualisation

    Parameters
    ----------
    file_path: str
        Path of txt nanoloop file (in)
    csv_path: str, optional
        Path of csv params measurement file (in)
    dict_pha: dict, optional
        Dict used for phase treatment
    del_1st_loop: bool, optional
        If True, remove the first nanoloop for analysis
    verbose: bool, optional
        Activation key for verbosity
    make_plots: bool, optional
        Activation key for matplotlib figures generation

    Returns
    -------
    figures: list(6)
        List of matplotlib.pyplot.figure objects
    """
    if csv_path is None:
        path, _ = os.path.split(file_path)
        path, _ = os.path.split(path)
        tab_path = path.split('_')[:-3]
        csv_path = '_'.join(tab_path)
    if verbose:
        if 'dfrt' in file_path:
            print('Mean DFRT treatment')
        elif 'single_freq' in file_path:
            print('Mean single frequency treatment')
        elif 'maximum' in file_path:
            print('Maximum classic treatment')
        elif 'fit' in file_path:
            print('Fit sho model treatment')
    # SSPFM params extraction
    _, sign_pars = csv_meas_sheet_extract(csv_path, verbose=verbose)

    # Extract nanoloop data
    data_dict, dict_str, other_properties = extract_nanoloop_data(file_path)

    # Print other properties
    if verbose and other_properties is not None:
        print('File properties:')
        for key, value in other_properties.items():
            print(f"{key}: {value}")

    # Treat nanoloop data
    dict_pha['func'] = eval(dict_pha['func']) \
        if isinstance(dict_pha['func'], str) else dict_pha['func']
    res = nanoloop_treatment(
        data_dict, sign_pars, dict_pha=dict_pha, dict_str=dict_str,
        make_plots=make_plots)
    (loop_tab, pha_calib, _) = res

    # Plot nanoloops
    if make_plots:
        figures = main_plot(
            loop_tab, pha_calib, dict_str=dict_str, del_1st_loop=del_1st_loop)
        return figures
    else:
        return loop_tab


def parameters():
    """
    To complete by user of the script: return parameters for analysis

    - del_1st_loop: bool
        Delete First Loop
        If this parameter is set to True, it deletes the first nanoloop of the
        analysis, which is typically used for calculating the mean hysteresis.
        This can be useful when the first write voltage values are equal to
        zero, indicating that the material is in a pristine state, and the
        nanoloop shape would be different from the polarized state.
        Deleting the first nanoloop helps to avoid artifacts in the analysis.
        This parameter has influence only on figure.
    - corr: str
        Phase Correction Mode
        This parameter specifies the correction mode for the value of the
        phase nanoloop. There are four possible correction modes:
        - 'raw': No correction is applied.
        - 'offset': Offset correction is applied.
        - 'affine': Affine correction is applied.
        - 'up_down': Phase is set to the up value or down value.
    - pha_fwd: float
        Phase Forward Target Value
        This parameter represents the target value for the phase in the
        forward direction. It is used to generate a multiplied coefficient
        equal to 1 between amplitude and piezoresponse.
    - pha_rev: float
        Phase Reverse Target Value
        This parameter represents the target value for the phase in the
        reverse direction. It is used to generate a multiplied coefficient
        equal to -1 between amplitude and piezoresponse.
    - func: algebraic func
        Piezoresponse Function
        This parameter represents the function used to determine the
        piezoresponse from amplitude and phase.
        The piezoresponse (PR) is calculated as PR = amp * func(pha),
        where 'amp' is the amplitude and 'pha' is the phase.
        Value: Algebraic function (np.cos or np.sin)
    - main_elec: bool
        Dominant Electrostatics in On Field Mode
        It determines whether the electrostatics are higher than
        ferroelectric effects. In other words, it indicates if the
        electrostatics are responsible for the phase loop's sense of
        rotation in the On Field mode.
        Active if On Field mode is selected.
    - grounded_tip: bool
        Flag indicating whether the tip is grounded.
        This parameter must be activated if the tip is grounded.
        It influences the polarisation value, the sense of rotation of
        hysteresis, and the sign of the electrostatic slope.
    - positive_d33: bool
        Flag indicating positive d33.
        This parameter must be activated if the d33 value is positive.
        It influences the sense of rotation of hysteresis.
    - locked_elec_slope: str
        Locked Electrostatic Slope
        It specifies and locks the sign of the electrostatic slope in
        the loop whatever measurement parameters
        (theory: grounded tip: negative, bottom: positive).
        Value: 'negative', 'positive', or None
        Active if On Field mode is selected.

    - file_path_in: str
        File path for the text loop file generated after the first step of
        the analysis (default: in the 'nanoloops' directory).
        This parameter specifies the file path where the text loop file
        generated after the first step of the analysis is located.
    - dir_path_out: str
        Saving directory for analysis results figures
        (optional, default: toolbox directory in the same root)
        This parameter specifies the directory where the figures
        generated as a result of the analysis will be saved.
    - csv_file_path: str
        File path of the CSV measurement file (measurement sheet model).
        This parameter specifies the file path to the CSV file containing
        measurement parameters. It is used to indicate the location of the
        CSV file, which serves as the source of measurement data for processing.
        If left empty, the system will automatically select the CSV file path.
    - verbose: bool
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.
    - show_plots: bool
        Activation key for generating matplotlib figures during analysis.
        This parameter serves as an activation key for generating
        matplotlib figures during the analysis process.
    - save: bool
        Activation key for saving results of analysis.
        This parameter serves as an activation key for saving results
        generated during the analysis process.
    """
    if get_setting("extract_parameters") in ['json', 'toml']:
        script_directory = os.path.realpath(__file__)
        file_path_user_params = script_directory.split('.')[0] + \
            f'_params.{get_setting("extract_parameters")}'
        # Load parameters from the specified configuration file
        print(f"user parameters from {os.path.split(file_path_user_params)[1]} "
              f"file")
        config_params = load_parameters_from_file(file_path_user_params)
        file_path_in = config_params['file_path_in']
        dir_path_out = config_params['dir_path_out']
        csv_file_path = config_params['csv_file_path']
        verbose = config_params['verbose']
        show_plots = config_params['show_plots']
        save = config_params['save']
        user_pars = config_params['user_pars']
    elif get_setting("extract_parameters") == 'python':
        print("user parameters from python file")
        # Get file path
        file_path_in = tkf.askopenfilename()
        # file_path_in = r'...\KNN500n_15h18m02-10-2023_out_dfrt\nanoloops\
        # off_f_KNN500n.0_00001.txt
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_15h18m02-10-2023_out_dfrt\toolbox\
        # loop_file_reader_2023-10-02-16h38m
        csv_file_path = None
        # csv_file_path =
        # r'...\KNN500n\measurement sheet model SSPFM ZI DFRT.csv'
        verbose = True
        show_plots = True
        save = False

        user_pars = {
            'del 1st loop': True,
            'corr': 'offset',
            'pha fwd': 0,
            'pha rev': 180,
            'func': np.cos,
            'main elec': True,
            'grounded tip': True,
            'positive d33': True,
            'locked elec slope': None,
        }

    else:
        raise NotImplementedError("setting 'extract_parameters' "
                                  "should be in ['json', 'toml', 'python']")

    return user_pars, file_path_in, dir_path_out, csv_file_path, verbose, \
        show_plots, save


def main():
    """ Main function for data analysis. """
    figs = []
    # Extract parameters
    out = parameters()
    (user_pars, file_path_in, dir_path_out, csv_file_path, verbose, show_plots,
     save) = out
    # Generate default path out
    dir_path_out = save_path_management(
        file_path_in, dir_path_out, save=save, dirname="loop_file_reader",
        lvl=2, create_path=True, post_analysis=True)
    start_time = datetime.now()
    # Main function
    figs += main_loop_file_reader(
        file_path_in, csv_path=csv_file_path, dict_pha=user_pars,
        del_1st_loop=user_pars['del 1st loop'], verbose=verbose,
        make_plots=bool(show_plots or save))
    # Plot figures
    print_plots(figs, show_plots=show_plots, save_plots=save,
                dirname=dir_path_out, transparent=False)
    # Save parameters
    if save:
        save_user_pars(user_pars, dir_path_out, start_time=start_time,
                       verbose=verbose)


if __name__ == '__main__':
    main()
