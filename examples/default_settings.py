"""
All default constants for PySSPFM examples and tests
Path and option to save datas generated from tests and examples
(SAVE_TEST_EXAMPLE) can be adjusted
All other settings must not be modified
"""

import pathlib

EXAMPLES = pathlib.Path(__file__)
EXAMPLE_ROOT_PATH_IN = EXAMPLES / 'datas' / 'PySSPFM_example_in'
EXAMPLE_ROOT_PATH_OUT = EXAMPLES / 'datas' / 'PySSPFM_example_out'
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
DETECT_BUG_SEGMENTS = False
FIT_METHOD = 'nelder'
HISTO_PHASE_METHOD = 'fit'
ELECTROSTATIC_OFFSET = True
