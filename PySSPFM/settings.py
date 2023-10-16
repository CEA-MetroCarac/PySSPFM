"""
All constants for PySSPFM

Parameters
----------
EXAMPLE_ROOT_PATH_IN : str
    The root path for example input data.
    Default is r".../examples/datas/PySSPFM_example_in"

EXAMPLE_ROOT_PATH_OUT : str
    The root path for example output data.
    Default is r".../examples/datas/PySSPFM_example_out"

DEFAULT_DATA_PATH_OUT: str
    The default root path for saved output data (figures ...).
    Default is r".../PySSPFM_data_out"

DEFAULT_LOGO_PATH: str
    The default path of the logo PySSPFM for GUI.
    Default is r".../PySSPFM/logo_icon/logoPySSPFM.png"

DEFAULT_ICON_PATH: str
    The default path of the icon PySSPFM for GUI.
    Default is r".../PySSPFM/logo_icon/iconPySSPFM.png"

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
    Key to chose if offset off field loop should be considered for the coupled
    analysis. Coupled analysis is used in order to study artifacts
    (mainly electrostatics) in the measurements. If the main origin of the
    offset of off field measurements is electrostatics and not ferroelectric
    effects (like frozen polarization), this parameter should be True.
    Default is True.
"""

import os

ROOT = pathlib.Path(__file__).parent.parent
EXAMPLES = ROOT / 'examples'
EXAMPLE_ROOT_PATH_IN = EXAMPLES / 'datas' / 'PySSPFM_example_in'
EXAMPLE_ROOT_PATH_OUT = EXAMPLES / 'datas' / 'PySSPFM_example_out'
DEFAULT_DATA_PATH_OUT = ROOT / 'PySSPFM_data_out'
DEFAULT_LOGO_PATH = ROOT / 'PySSPFM' / 'logo_icon' / 'logoPySSPFM.png'
DEFAULT_ICON_PATH = ROOT / 'PySSPFM' / 'logo_icon' / 'iconPySSPFM.png'
SAVE_TEST_EXAMPLE = True
KEY_MEASUREMENT_EXTRACTION = {
    'spm': {
        'classic': {'time': 'times',
                    'HS PR Amplitude (nm)': 'amp',
                    'HS PR Phase (°)': 'pha',
                    'DeflectionIn1B (nm)': 'deflection'},
        'dfrt': {'time': 'times',
                 'Tip Bias (V)': 'amp',
                 'Input3 (V)': 'pha',
                 'DeflectionIn1B (nm)': 'deflection'}},
    'table': {
        'classic': {'time': 'times',
                    'Amplitude': 'amp',
                    'Phase': 'pha',
                    'Deflection': 'deflection'},
        'dfrt': {'time': 'times',
                 'Amplitude': 'amp',
                 'Phase': 'pha',
                 'Deflection': 'deflection'}}
}
HEADER_LINES = 1
INDEX_LINE_MEAS_NAME = 0
DELIMITER = '\t\t'
FIGSIZE = [18, 9]
DETECT_BUG_SEGMENTS = False
FIT_METHOD = 'nelder'
COLOR_AMP_PHA_MAP = 'coolwarm'
HISTO_PHASE_METHOD = 'fit'
COLOR_SSPFM_MAP = 'copper'
COLOR_SSPFM_MAP_PIXEL = 'white'
COLOR_SSPFM_MAP_HIGHLIGHTED_PIXEL = 'red'
COLOR_HYSTERESIS_CLUSTERING = 'turbo'
ELECTROSTATIC_OFFSET = True
