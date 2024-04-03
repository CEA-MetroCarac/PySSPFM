"""
Example of settings methods
"""
import os

from PySSPFM.settings import get_settings_dict, get_path_from_json, get_setting


def ex_get_settings_dict(mode='classic', verbose=False):
    """
    Example of get_setting function

    Parameters
    ----------
    mode: str, optional
        Mode of operation.
    verbose: bool, optional
        If True, prints the script dictionary.

    Returns
    -------
    settings_dict: dict
        The settings dictionary.
    """
    if mode == "classic":
        json_file_name = "settings.json"
    elif mode == "default":
        json_file_name = "default_settings.json"
    else:
        raise NotImplementedError("mode should be in ['classic', 'default']")

    # ex get_settings_dict
    json_file_path = os.path.join(get_setting("example_root_path_in"),
                                  json_file_name)
    settings_dict = get_settings_dict(json_file_path)

    if mode == "classic":
        # ex get_path_from_json
        settings_dict = get_path_from_json(settings_dict)

    if verbose:
        print("\n| Key | Value |")
        print("|---|---|")
        for key, value in settings_dict.items():
            print(f"| {key} | {value} |")
        print("|---|---|")

    return settings_dict


if __name__ == "__main__":
    ex_get_settings_dict(mode='classic', verbose=True)
    ex_get_settings_dict(mode='default', verbose=True)
