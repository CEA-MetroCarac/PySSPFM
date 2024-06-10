"""
Perform all the setting management for PySSPFM

For json settings file, paths can be:
    - A list of path (string) that will be joined
    - An absolute string corresponding to the path
ROOT or PARENT corresponds to the parent directory of the analyzed measurement
folder
EXAMPLES corresponds to the data root for examples and tests

Parameters
----------
EXAMPLE_ROOT_PATH_IN : str
    The root path for example input data.
    Default is r".../examples/data/PySSPFM_example_in"

EXAMPLE_ROOT_PATH_OUT : str
    The root path for example output data.
    Default is r".../examples/data/PySSPFM_example_out"

DEFAULT_DATA_PATH_OUT: str
    The default root path for saved output data (figures ...).
    Default is r".../PySSPFM_data_out"

DEFAULT_LOGO_PATH: str
    The default path of the logo PySSPFM for GUI.
    Default is r".../PySSPFM/logo_icon/logoPySSPFM.png"

DEFAULT_ICON_PATH: str
    The default path of the icon PySSPFM for GUI.
    Default is r".../PySSPFM/logo_icon/iconPySSPFM.png"

DEFAULT_PARAMETERS_FILE_NAME: str
    The default name of txt file saving parameters (processing and measure)
    Default is r'parameters.txt'

DEFAULT_FIGURES_FOLDER_NAME: str
    The default name of saving folder figures
    Default is r'figs'

DEFAULT_NANOLOOPS_FOLDER_NAME: str
    The default name of saving folder for txt nanoloops
    (generated after first step of data processing)
    Default is r'nanoloops'

DEFAULT_BEST_NANOLOOP_FOLDER_NAME: str
    The default name of saving folder for txt best nanoloops
    (generated after second step of data processing)
    Default is r'best_nanoloops'

DEFAULT_PROPERTIES_FOLDER_NAME: str
    The default name of saving folder for txt sample properties
    (generated after second step of data processing)
    Default is r'properties'

SAVE_TEST_EXAMPLE: bool
    Flag to control whether to save generated data (figures ...) with tests
    or examples or not.
    Default is True.

MULTI_PROCESSING: bool
    Flag to control whether data analysis is performed in multiprocessing or
    not. This option applies for steps 1 and 2 of the data analysis,
    and the offset analyzer of the toolbox.
    Default is False.

EXTRACT_PARAMETERS: str
    Method used to extract processing parameters. It can be extracted from json
    file (extract_parameters = 'json') that have been created in the same
    directory, toml file (extract_parameters = 'toml') that has to be created,
    or directly from the current python file (extract_parameters = 'python').
    The name of the json or toml file must be the same as the corresponding
    executable python file, followed by "_params" and the file extension.

KEY_MEASUREMENT_EXTRACTION: dict
    Correspondence between the names of measurements extracted from the
    initial file and the keys of the measurement dictionary created for
    SSPFM processing.
    The names of measurements extracted from the initial file can be adjusted
    by the user.
    However, the names of the keys in the measurement dictionary created for
    SSPFM processing should not be changed, but they can be
    added or removed depending on the measurements performed.
    For SPM files, the dictionary key corresponds to the name of the associated
    channel.
    For table files, the dictionary key corresponds to the measurement name in
    the header.
    For output values corresponding to the measurement dictionary created
    for SSPFM processing, the names 'times', 'amp', 'pha', 'tip_bias',
    'deflection', 'height' correspond to the measurements of time, amplitude,
    and phase PFM, SSPFM polarisation signal, tip deflection and piezo sensor
    height respectively.

HEADER_LINES : int
    The number of header lines in the raw measurement data file.
    Default is 1.

INDEX_LINE_MEAS_NAME: int
    Index of the line of the measurement name in the raw measurement data file.
    Default is 0.

DELIMITER : str
    The delimiter used in the raw measurement data file.
    Default is '\t\t'.

FIGSIZE : list
    The size of the figure for visualization, specified as [width, height].
    Default is [18, 9].

FIT_METHOD: str
    Fitting method for the models sho, sho_phase (for amplitude and phase of
    the segments with frequency sweep segments, respectively), and Gaussian
    (for phase histograms).
    Could be "leastsq", "least_square" (fast fitting but harder to converge)
    or "nelder" (vice versa).
    Default is "least_square".

COLOR_AMP_PHA_MAP : str
    The colormap for amplitude and phase mapping.
    Default is 'coolwarm'.

HISTO_PHASE_METHOD : str
    The method used for phase histogram calculation.
    Value can be 'fit' in order to fit the two phase peak of the phase
    histogram (gaussian model) or 'max' to take the maximum for the peak.
    The method is used in order to determine the phase difference between
    the two peaks. 'fit' method is more accurate but slower.
    Default is 'max'.

RADIANS_INPUT_PHASE: bool
    Flag to indicate whether the input phase data is in radians or not.
    If so, it is converted into degrees for data analysis.
    Default is False.

UNIPOLAR_PHASE_REVERT : bool
    Flag to indicate if phase inversion occur for unipolar nanoloop.
    Large vertical offsets can influence the PFM amplitude measurement,
    especially in the case of Off Field measurements (electrostatic effects,
    frozen polarization etc.). Also, some of the nanoloops can have a single
    associated phase value: the phase is unipolar. In this case, the analysis
    performed for the phase calibration asks the user to fill in if a phase
    inversion takes place. This parameter is considered only for unipolar
    nanoloops, and must be adjusted by the user based on phase analysis
    performed on a bipolar nanoloop or on theoretical analysis of nanoloop
    depending on measurement condition.

COLOR_SSPFM_MAP : str
    The colormap for SSPFM mapping.
    Default is 'copper'.

COLOR_SSPFM_MAP_PIXEL : str
    The color for individual pixels in SSPFM mapping.
    Default is 'white'.

COLOR_SSPFM_MAP_HIGHLIGHTED_PIXEL : str
    The color for highlighted pixels in SSPFM mapping.
    Default is 'red'.

COLOR_HYSTERESIS_CLUSTERING: str
    The colormap for hysteresis clustering figures.
    Default is 'turbo'.

ELECTROSTATIC_OFFSET: bool
    Key to chose if offset off field nanoloop should be considered for the
    coupled analysis. Coupled analysis is used in order to study artifacts
    (mainly electrostatics) in the measurements. If the main origin of the
    offset of off field measurements is electrostatics and not ferroelectric
    effects (like frozen polarisation), this parameter should be True.
    Default is True.
"""
import sys
import os
from pathlib import Path
import shutil

from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file


def get_setting(key):
    """
    Get a setting value based on the specified key. This function allows you
    to check whether the initial code launch is a test or an example.
    In such cases, examples settings are used to align with example data and
    achieve the correct target values for tests. Otherwise, user-adjustable
    settings are extracted.

    Parameters
    ----------
    key : str
        The key to look up in the settings dictionaries.

    Returns
    -------
    setting : object
        The value associated with the provided key in the settings dictionaries.
    """
    origin_path = sys.argv[0]
    sep_origin_path = origin_path.split(os.path.sep)

    # Define the examples configuration file path and the user configuration file path
    examples_config_path = Path(__file__).parent / 'examples_settings.json'
    user_config_path = Path.home() / '.pysspfm' / 'pysspfm.json'

    # If the ~/.pysspfm directory doesn't exist, create it
    user_config_path.parent.mkdir(parents=True, exist_ok=True)

    # If the user configuration file doesn't exist, copy the default configuration file
    if not user_config_path.exists():
        shutil.copy(Path(__file__).parent / 'default_settings.json', user_config_path)

    settings_dict = get_settings_dict(user_config_path)
    # Update the settings dictionary with the path information.
    settings_dict = get_path_from_json(settings_dict)
    
    # All default constants for PySSPFM examples and tests
    # examples settings must not be modified
    def_settings_dict = get_settings_dict(examples_config_path)

    # Use the examples settings if 'examples' or 'test' is in the script path
    if "PySSPFM" not in sep_origin_path:
        settings_to_use = def_settings_dict
    elif 'examples' in sep_origin_path or 'test' in sep_origin_path:
        settings_to_use = def_settings_dict
    else:
        settings_to_use = settings_dict
    try:
        setting = settings_to_use[key]
    except KeyError:
        setting = settings_dict[key]

    return setting


def get_settings_dict(json_file_name):
    """
    Returns the settings dictionary from a JSON file.

    Parameters
    ----------
    json_file_name: str
        Path or name to the JSON file.

    Returns
    -------
    json_dict: dict
        The settings dictionary.
    """
    if os.path.exists(json_file_name):
        json_file_path = os.path.join(json_file_name)
    else:
        json_file_path = os.path.join(os.path.dirname(__file__), json_file_name)
    # Load the settings dictionary from the JSON file.
    json_dict = load_parameters_from_file(json_file_path)

    return json_dict


def get_path_from_json(settings_dict):
    """
    Updates the settings dictionary with the path information.

    Parameters
    ----------
    settings_dict: dict
        The settings dictionary.

    Returns
    -------
    settings_dict: dict
        The updated settings dictionary.
    """
    # Update the ROOT path.
    root = settings_dict["root"]
    if isinstance(root, list):
        for cont, elem in enumerate(root):
            if elem == "PARENT":
                root[cont] = Path(__file__).parent.parent
        root = os.path.join(*root)

    # Update the EXAMPLES path.
    examples = settings_dict["examples"]
    if isinstance(examples, list):
        for cont, elem in enumerate(examples):
            if elem == "ROOT":
                examples[cont] = root
        examples = os.path.join(*examples)

    settings_dict["root"] = root
    settings_dict["examples"] = examples

    # Update other paths.
    for key, value in settings_dict.items():
        if isinstance(value, list) and "path" in key:
            for cont, elem in enumerate(value):
                if elem == "ROOT":
                    settings_dict[key][cont] = root
                elif elem == "EXAMPLES":
                    settings_dict[key][cont] = examples
                else:
                    continue
            settings_dict[key] = os.path.join(*settings_dict[key])

    return settings_dict

def copy_default_settings_if_not_exist(file_path):
    """
    Copy the default settings file to the user directory if it does not exist.
    """
    # Convert string to Path object if necessary
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    filename = file_path.name

    # Get the path from the settings
    user_params_file_path = get_setting(filename.replace('.py', '_params'))

    # Expand the ~ to the home directory
    user_params_file_path = Path(user_params_file_path).expanduser()
    
    # if json file in get_setting(filename_user_params) doesn't exists, copy default to ~/.pysspfm/
    if not user_params_file_path.exists():
        default_file_path = file_path.with_name(f"{file_path.stem}_params.{get_setting('extract_parameters')}")
        shutil.copy(default_file_path, user_params_file_path)
        
    return user_params_file_path

def get_config(current_file, fname_json):
    # if fname_json is provided, use it, else use the default one
    if fname_json is not None:
        file_path_user_params = fname_json
    else:
        file_path = os.path.realpath(current_file)
        file_path_user_params = \
            copy_default_settings_if_not_exist(file_path)

    # Load parameters from the specified configuration file
    print(f"user parameters from {os.path.split(file_path_user_params)[1]} "
          f"file")
    config_params = load_parameters_from_file(file_path_user_params)

    return config_params