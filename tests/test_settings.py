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
        "default_parameters_file_name": "measurement sheet model SSPFM.csv",
        "default_figures_folder_name": "figs",
        "default_nanoloops_folder_name": "nanoloops",
        "default_best_nanoloop_folder_name": "best_nanoloops",
        "default_properties_folder_name": "properties",
        "save_test_example": True,
        "multi_processing": False,
        "extract_parameters": "json",
        "key_measurement_extraction": {
            "spm": {
                "classic": {"time": "times",
                            "HS PR Amplitude (nm)": "amp",
                            "HS PR Phase (°)": "pha",
                            "DeflectionIn1B (nm)": "deflection",
                            "Tip Bias (V)": "tip_bias",
                            "Height Sensor (nm)":  "height"},
                "dfrt": {"time": "times",
                         "Tip Bias (V)": "amp",
                         "Input3 (V)": "pha",
                         "InputFreq": "freq",
                         "DeflectionIn1B (nm)": "deflection",
                         "InputBias": "tip_bias",
                         "Height Sensor (nm)": "height",
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
                            "Bias": "tip_bias",
                            "Height Sensor (nm)":  "height"},
                "dfrt": {"time": "times",
                         "Amplitude": "amp",
                         "Phase": "pha",
                         "Freq": "freq",
                         "Deflection": "deflection",
                         "Bias": "tip_bias",
                         "Height Sensor (nm)": "height",
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
        "fit_method": "least_square",
        "color_amp_pha_map": "coolwarm",
        "histo_phase_method": "max",
        "radians_input_phase": False,
        "unipolar_phase_revert": False,
        "color_sspfm_map": "copper",
        "color_sspfm_map_pixel": "white",
        "color_sspfm_map_highlighted_pixel": "red",
        "color_curve_clustering": "turbo",
        "electrostatic_offset": True}

    for key, value in target_settings_dict.items():
        assert settings_dict[key] == value


def test_get_settings_dict_default():
    """ Test get_settings_dict for mode = "default"  """

    def_settings_dict = ex_get_settings_dict(mode='default')

    target_def_settings_dict = {
        "default_parameters_file_name": "measurement sheet model SSPFM.csv",
        "default_figures_folder_name": "figs",
        "default_nanoloops_folder_name": "nanoloops",
        "default_best_nanoloop_folder_name": "best_nanoloops",
        "default_properties_folder_name": "properties",
        "multi_processing": False,
        "key_measurement_extraction": {
            "spm": {
                "classic": {"time": "times",
                            "HS PR Amplitude (nm)": "amp",
                            "HS PR Phase (°)": "pha",
                            "DeflectionIn1B (nm)": "deflection",
                            "Tip Bias (V)": "tip_bias",
                            "Height Sensor (nm)":  "height"},
                "dfrt": {"time": "times",
                         "Tip Bias (V)": "amp",
                         "Input3 (V)": "pha",
                         "InputFreq": "freq",
                         "DeflectionIn1B (nm)": "deflection",
                         "InputBias": "tip_bias",
                         "Height Sensor (nm)": "height",
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
                            "Bias": "tip_bias",
                            "Height Sensor (nm)":  "height"},
                "dfrt": {"time": "times",
                         "Amplitude": "amp",
                         "Phase": "pha",
                         "Freq": "freq",
                         "Deflection": "deflection",
                         "Bias": "tip_bias",
                         "Height Sensor (nm)": "height",
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
        "fit_method": "nelder",
        "histo_phase_method": "fit",
        "radians_input_phase": False,
        "unipolar_phase_revert": True,
        "electrostatic_offset": True}

    assert def_settings_dict == target_def_settings_dict
