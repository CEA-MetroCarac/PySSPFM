"""
Example of extract_params_from_file methods
"""
import os

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.extract_params_from_file import \
    load_parameters_from_file


def ex_load_parameters_from_file(verbose=False):
    """
    Example of load_parameters_from_file function

    Parameters
    ----------
    verbose: bool, optional
        If True, prints the script dictionary.

    Returns
    -------
    params_dict: dict
        The parameters dictionary.
    """

    # ex get_settings_dict
    json_file_path = os.path.join(get_setting("example_root_path_in"),
                                  "mean_hyst_params.json")
    params_dict = load_parameters_from_file(json_file_path)

    if verbose:
        print("| Key | Value |")
        print("|---|---|")
        for key, value in params_dict.items():
            print(f"| {key} | {value} |")

    return params_dict


if __name__ == "__main__":
    ex_load_parameters_from_file(verbose=True)
