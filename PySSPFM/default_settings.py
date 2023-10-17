"""
All default constants for PySSPFM examples and tests
Default settings must not be modified
"""

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

DEF_SETTINGS_DICT = {'key meas extract': KEY_MEASUREMENT_EXTRACTION,
                     'header lines': HEADER_LINES,
                     'index line meas name': INDEX_LINE_MEAS_NAME,
                     'delimiter': DELIMITER,
                     'detect bug segments': DETECT_BUG_SEGMENTS,
                     'fit method': FIT_METHOD,
                     'histo phase method': HISTO_PHASE_METHOD,
                     'elec offset': ELECTROSTATIC_OFFSET}
