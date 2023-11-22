"""
Test settings methods
"""
import pytest

from examples.ex_settings import ex_get_settings_dict


# class TestSignalBias(unittest.TestCase):


def test_get_settings_dict_classic():
    """ Test get_settings_dict for mode = "classic"  """

    settings_dict = ex_get_settings_dict(mode='classic')

    target_settings_dict = {
        "default_parameters_file_name": "parameters.txt",
        "default_figures_folder_name": "figs",
        "default_nanoloops_folder_name": "nanoloops",
        "default_best_nanoloop_folder_name": "best_nanoloops",
        "default_properties_folder_name": "properties",
        "save_test_example": true,
        "extract_parameters": "json",
        "key_measurement_extraction": {
            "spm": {
                "classic": {"time": "times",
                            "HS PR Amplitude (nm)": "amp",
                            "HS PR Phase (°)": "pha",
                            "DeflectionIn1B (nm)": "deflection",
                            "Tip Bias (V)": "tip_bias"},
                "dfrt": {"time": "times",
                         "Tip Bias (V)": "amp",
                         "Input3 (V)": "pha",
                         "InputFreq": "freq",
                         "DeflectionIn1B (nm)": "deflection",
                         "InputBias": "tip_bias",
                         "Amplitude SB1": "amp sb_l",
                         "Phase SB1": "pha sb_l",
                         "Freq SB1": "freq sb_l",
                         "Amplitude SB2": "amp sb_r",
                         "Phase SB2": "pha sb_r",
                         "Freq SB2": "freq sb_r"}},
            "table": {
                "classic": {"time": "times",
                            "Amplitude": "amp",
                            "Phase": "pha",
                            "Deflection": "deflection",
                            "Bias": "tip_bias"},
                "dfrt": {"time": "times",
                         "Amplitude": "amp",
                         "Phase": "pha",
                         "Freq": "freq",
                         "Deflection": "deflection",
                         "Bias": "tip_bias",
                         "Amplitude SB1": "amp sb_l",
                         "Phase SB1": "pha sb_l",
                         "Freq SB1": "freq sb_l",
                         "Amplitude SB2": "amp sb_r",
                         "Phase SB2": "pha sb_r",
                         "Freq SB2": "freq sb_r"}}
        },
        "header_lines": 1,
        "index_line_meas_name": 0,
        "delimiter": "\t\t",
        "figsize": [18, 9],
        "detect_bug_segments": false,
        "fit_method": "nelder",
        "color_amp_pha_map": "coolwarm",
        "histo_phase_method": "fit",
        "color_sspfm_map": "copper",
        "color_sspfm_map_pixel": "white",
        "color_sspfm_map_highlighted_pixel": "red",
        "color_curve_clustering": "turbo",
        "electrostatic_offset": true}

    for key in target_settings_dict.keys():
        assert settings_dict[key] == target_settings_dict[key]


def test_get_settings_dict_default():
    """ Test get_settings_dict for mode = "default"  """

    def_settings_dict = ex_get_settings_dict(mode='default')

    target_def_settings_dict = {
        "default_parameters_file_name": "parameters.txt",
        "default_figures_folder_name": "figs",
        "default_nanoloops_folder_name": "nanoloops",
        "default_best_nanoloop_folder_name": "best_nanoloops",
        "default_properties_folder_name": "properties",
        "key_measurement_extraction": {
            "spm": {
                "classic": {"time": "times",
                            "HS PR Amplitude (nm)": "amp",
                            "HS PR Phase (°)": "pha",
                            "DeflectionIn1B (nm)": "deflection",
                            "Tip Bias (V)": "tip_bias"},
                "dfrt": {"time": "times",
                         "Tip Bias (V)": "amp",
                         "Input3 (V)": "pha",
                         "InputFreq": "freq",
                         "DeflectionIn1B (nm)": "deflection",
                         "InputBias": "tip_bias",
                         "Amplitude SB1": "amp sb_l",
                         "Phase SB1": "pha sb_l",
                         "Freq SB1": "freq sb_l",
                         "Amplitude SB2": "amp sb_r",
                         "Phase SB2": "pha sb_r",
                         "Freq SB2": "freq sb_r"}},
            "table": {
                "classic": {"time": "times",
                            "Amplitude": "amp",
                            "Phase": "pha",
                            "Deflection": "deflection",
                            "Bias": "tip_bias"},
                "dfrt": {"time": "times",
                         "Amplitude": "amp",
                         "Phase": "pha",
                         "Freq": "freq",
                         "Deflection": "deflection",
                         "Bias": "tip_bias",
                         "Amplitude SB1": "amp sb_l",
                         "Phase SB1": "pha sb_l",
                         "Freq SB1": "freq sb_l",
                         "Amplitude SB2": "amp sb_r",
                         "Phase SB2": "pha sb_r",
                         "Freq SB2": "freq sb_r"}}},
        "header_lines": 1,
        "index_line_meas_name": 0,
        "delimiter": "\t\t",
        "detect_bug_segments": false,
        "fit_method": "nelder",
        "histo_phase_method": "fit",
        "electrostatic_offset": true}

    assert def_settings_dict == target_def_settings_dict
