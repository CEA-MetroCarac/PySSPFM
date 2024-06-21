"""
Example of file methods
"""
import os
import shutil

from examples.utils.nanoloop_to_hyst.ex_analysis import ex_sort_prop
from PySSPFM.settings import get_setting
from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.nanoloop_to_hyst.file import \
    (create_file_nanoloop_paths, generate_file_nanoloop_paths,
     save_properties, extract_properties, extract_main_elec_tab)


def example_file(verbose=False):
    """
    Example of file methods.

    Parameters
    ----------
    verbose: bool, optional
        Whether to print verbose output, defaults to False.

    Returns
    -------
    file_paths_from_nanoloops: list
        File paths generated from nanoloops file.
    file_paths_from_raw: list
        File paths generated from raw measurement file.
    meas_pars: dict
        Measurement parameters.
    sign_pars: dict
        Signal parameters.
    dict_analysis_1: dict
        Analysis dictionary.
    nb_write_per_read: int
        Number of writes per read.
    write_segment: list
        Write segment data.
    properties: list
        Sample properties.
    dim_pix: dict
        Dimension in pixels.
    dim_mic: dict
        Dimension in micrometers.
    """
    # Define input and output file paths
    root_data = os.path.join(get_setting("example_root_path_in"),
                             "KNN500n_2023-11-20-16h18m_out_dfrt")
    dir_path_in = os.path.join(root_data, "nanoloops")
    dir_path_raw = os.path.join(get_setting("example_root_path_in"),
                                "KNN500n")
    file_path_in_inversion = \
        os.path.join(get_setting("example_root_path_in"), "KNN500n_toolbox",
                     "phase_inversion_analyzer_2024-05-21-18h13m",
                     "phase_inversion.txt")

    if verbose:
        root_out = os.path.join(
            get_setting("example_root_path_out"), "ex_nanoloop_to_hyst_file")
    else:
        root_out = os.path.join(
            get_setting("default_data_path_out"), "test_nanoloop_to_hyst_file")

    # Remove existing output directory and copy the data
    if os.path.isdir(root_out):
        shutil.rmtree(root_out)
    shutil.copytree(root_data, root_out)

    # Generate file paths from nanoloops and raw measurement files
    file_paths_from_nanoloops = generate_file_nanoloop_paths(dir_path_in)
    file_paths_from_raw = create_file_nanoloop_paths(dir_path_raw)
    if verbose:
        print('\t- ex generate_file_nanoloop_paths')
        for cont, elem in enumerate(file_paths_from_nanoloops):
            print(f'\t\tpath n°{cont + 1}: {elem}')
        print('\n')

    dir_path_out_prop = os.path.join(root_out, "properties")

    properties = ex_sort_prop()
    dim_pix = {'x': 8,
               'y': 8}
    dim_mic = {'x': 3.5,
               'y': 3.5}

    # ex save_properties
    save_properties(properties, dir_path_out_prop, dim_pix=dim_pix,
                    dim_mic=dim_mic)

    # ex extract_properties
    properties, dim_pix, dim_mic = extract_properties(dir_path_out_prop)

    if verbose:
        print('\n\t- ex extract_properties')
        print(f'\t\tproperties: {properties}')
        print(f'\t\tdim pix: {dim_pix}')
        print(f'\t\tdim mic: {dim_mic}')

    # ex extract_main_elec_tab
    main_elec_tab = extract_main_elec_tab(file_path_in_inversion)

    return (file_paths_from_nanoloops, file_paths_from_raw,
            properties, dim_pix, dim_mic, main_elec_tab)


if __name__ == '__main__':
    # saving path management
    dir_path_out, save_plots = save_path_example(
        "nanoloop_to_hyst_file", save_example_exe=True, save_test_exe=False)
    example_file(verbose=True)
