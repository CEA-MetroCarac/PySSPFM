"""
This module provides functionality to load parameters from a configuration file
in either TOML or JSON format. It includes a custom error class TomlError for
handling errors related to TOML files.
"""

import os
import json


class TomlError(Exception):
    """ TomlError object """
    def __init__(self, message=""):
        """
        Object used to generate error when toml files can't be opened

        Parameters
        ----------
        message: str, optional
            Custom error message (default is an empty string).
        """
        self.message = message
        super().__init__(self.message)


def load_parameters_from_file(file_path):
    """
    Load parameters from a configuration file in either TOML or JSON format.

    Parameters
    ----------
    file_path: str
        Path to the configuration file (in .toml or .json format).

    Returns
    -------
    parameters: dict
        Dictionary containing the loaded parameters.
    """

    def replace_null_with_none(data):
        """
        Recursively replace 'null' with None in a dictionary or list,
        convert strings to raw strings, and handle paths.

        Parameters
        ----------
        data : any
            The data (dict, list, or value) to process.

        Returns
        -------
        any
            The processed data with 'null' replaced by None,
            strings converted to raw strings, and paths processed.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if "path" in key.lower() or "root" in key.lower():
                    if isinstance(value, str):
                        # Replace backslashes with double backslashes
                        data[key] = value.replace(r"\\", r"\\\\")
                else:
                    data[key] = replace_null_with_none(value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = replace_null_with_none(item)
        elif isinstance(data, str):
            if data == "null":
                data = None
            else:
                data = fr"{data}"
        return data

    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.toml':
        try:
            import toml
        except (NotImplementedError, NameError) as error:
            message = "To open toml file , toml module is required"
            raise TomlError(message) from error
        with open(file_path, 'r', encoding='utf-8') as toml_file:
            dict_pars = toml.load(toml_file)
            dict_pars = replace_null_with_none(dict_pars)
            return dict_pars
    elif file_extension == '.json':
        with open(file_path, 'r', encoding='utf-8') as json_file:
            dict_pars = json.load(json_file)
            dict_pars = replace_null_with_none(dict_pars)
            return dict_pars
    else:
        raise ValueError(
            "Invalid file format. Supported formats are .toml and .json.")
