"""
File and directory path management in order to save results from runnable script
"""
import os
import shutil
from datetime import datetime

from PySSPFM.settings import get_setting


def save_path_management(dir_path_in, dir_path_out=None, save=False,
                         dirname='results', lvl=1, create_path=False,
                         post_analysis=True):
    """
    Manage saving directory paths for toolbox results.

    Parameters
    ----------
    dir_path_in : str
        Input directory path.
    dir_path_out : str, optional
        Output directory path (default is None).
    save : bool, optional
        Option to save results (default is False).
    dirname : str, optional
        Name of the output directory (default is 'results').
    lvl : int, optional
        Number of directory levels to go up from the input directory
        (default is 1).
    create_path : bool, optional
        Create the output directory if it doesn't exist (default is False).
    post_analysis : bool, optional
        If True, toolbox is performed post sspfm analysis

    Returns
    -------
    str
        Output directory path.
    """
    # Check if the input directory exists
    assert os.path.exists(dir_path_in), f"{dir_path_in} doesn't exist"

    # Check if the output directory exists
    path_out_exists = dir_path_out is not None and os.path.exists(dir_path_out)

    # If save option is active and the output directory doesn't exist, create it
    if save and not path_out_exists:
        root = dir_path_in
        if lvl > 0:
            for _ in range(lvl):
                root, _ = os.path.split(root)
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d-%Hh%Mm")
        dirname += f'_{date_str}'
        if post_analysis:
            dir_path_out = os.path.join(root, "toolbox", dirname)
        else:
            root += "_toolbox"
            dir_path_out = os.path.join(root, dirname)
        if not os.path.exists(dir_path_out) and create_path:
            os.makedirs(dir_path_out)
            print(f"saving path created: {dir_path_out}")

    return dir_path_out


def save_user_pars(user_pars, dir_path_out, start_time=None, verbose=False):
    """
    Save user parameters to a text file.

    Parameters
    ----------
    user_pars : dict
        Dictionary containing user parameters.
    dir_path_out : str
        Directory path for the output file.
    start_time : datetime.datetime, optional
        Start time of the analysis (default is None).
    verbose: bool, optional
        Activation key to verbosity (default is False).

    Returns
    -------
    None
    """
    saving_file = os.path.join(dir_path_out, "user_params.txt")

    with open(saving_file, 'w', encoding='utf-8') as file:
        if start_time is not None:
            file.write(f"start of analysis: {start_time}\n")
            file.write(f"analysis duration: {datetime.now() - start_time}\n\n")
        file.write("User Parameters:\n")
        for key, value in user_pars.items():
            file.write(f"{key}: {value}\n")

    if verbose:
        print(f"Analysis parameters saved in '{saving_file}' file.")


def save_path_example(folder_name, save_example_exe, save_test_exe=False):
    """
    Generate the output directory path for test or example data.

    Parameters
    ----------
    folder_name: str
        Name of the folder.
    save_example_exe: bool
        If True, it's an example execution; otherwise, it's a test.
    save_test_exe: bool, optional
        If True, save the test data. Default is False.

    Returns
    -------
    dir_path_out: str or None
        Output directory path if either save_example_exe or save_test_exe is
        True; otherwise, None.
    save_plots: bool
        A flag indicating whether to save plots.
    """
    if get_setting("save_test_example"):
        if not save_example_exe and not save_test_exe:
            dir_path_out = None
            save_plots = False
        else:
            if save_example_exe:
                dir_path_out = os.path.join(
                    get_setting("example_root_path_out"), f"ex_{folder_name}")
            elif save_test_exe:
                dir_path_out = os.path.join(
                    get_setting("default_data_path_out"), f"test_{folder_name}")
            else:
                raise IOError("save_example_exe and save_test_exe can't "
                              "be True at the same time")
            if os.path.isdir(dir_path_out):
                shutil.rmtree(dir_path_out)
            save_plots = True
    else:
        dir_path_out = None
        save_plots = False

    return dir_path_out, save_plots
