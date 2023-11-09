"""
All constants for PySSPFM

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
    'deflection' correspond to the measurements of time, amplitude, and phase
    PFM, SSPFM polarization signal, and tip deflection respectively.

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

DETECT_BUG_SEGMENTS: bool
    If set to True, this parameter compares the theoretically expected number of
    segments based on the SSPFM bias parameters with the actual number of
    experimental segments. It raises an error if these two values do not match.
    Default is False.

FIT_METHOD: str
    Fitting method for the models sho, sho_phase (for amplitude and phase of
    the segments with frequency sweep segments, respectively), and Gaussian
    (for phase histograms).
    Could be "leastsq", "least_square" (fast fitting but harder to converge)
    or "nelder" (vice versa).
    Default is "nelder".

COLOR_AMP_PHA_MAP : str
    The colormap for amplitude and phase mapping.
    Default is 'coolwarm'.

HISTO_PHASE_METHOD : str
    The method used for phase histogram calculation.
    Value can be 'fit' in order to fit the two phase peak of the phase
    histogram (gaussian model) or 'max' to take the maximum for the peak.
    The method is used in order to determine the phase difference between
    the two peaks. 'fit' method is more accurate but slower.
    Default is 'fit'.

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
    effects (like frozen polarization), this parameter should be True.
    Default is True.
"""
import sys
import os
import pathlib

from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file


def get_setting(key):
    """
    Get a setting value based on the specified key. This function allows you
    to check whether the initial code launch is a test or an example.
    In such cases, default settings are used to align with example data and
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

    def get_settings_dict(json_file_name):
        """
        Returns the settings dictionary from a JSON file.

        Parameters
        ----------
        json_file_name: str
            Path to the JSON file.

        Returns
        -------
        json_dict: dict
            The settings dictionary.
        """
        json_file_path = os.path.join(os.path.dirname(__file__), json_file_name)
        # Load the settings dictionary from the JSON file.
        json_dict = load_parameters_from_file(json_file_path)

        return json_dict

    settings_dict = get_settings_dict("settings.json")
    # Update the settings dictionary with the path information.
    settings_dict = get_path_from_json(settings_dict)
    # All default constants for PySSPFM examples and tests
    # Default settings must not be modified
    def_settings_dict = get_settings_dict("default_settings.json")
    # Use the default settings if 'examples' or 'test' is in the script path
    settings_to_use = \
        def_settings_dict if 'examples' in sep_origin_path or \
                             'tests' in sep_origin_path else settings_dict
    try:
        setting = settings_to_use.get(key)
    except KeyError:
        setting = settings_dict.get(key)

    return setting


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
    root = settings_dict["ROOT"]
    if isinstance(root, list):
        for cont, elem in enumerate(root):
            if elem == "PARENT":
                root[cont] = pathlib.Path(__file__).parent.parent
        root = os.path.join(*root)

    # Update the EXAMPLES path.
    examples = settings_dict["EXAMPLES"]
    if isinstance(examples, list):
        for cont, elem in enumerate(examples):
            if elem == "ROOT":
                examples[cont] = root
        examples = os.path.join(*examples)

    settings_dict["ROOT"] = root
    settings_dict["EXAMPLES"] = examples

    # Update other paths.
    for key, value in settings_dict.items():
        if isinstance(value) and "PATH" in key:
            for cont, elem in enumerate(value):
                if elem == "ROOT":
                    settings_dict[key][cont] = root
                elif elem == "EXAMPLES":
                    settings_dict[key][cont] = examples
                else:
                    continue
            settings_dict[key] = os.path.join(*settings_dict[key])

    return settings_dict
