"""
Examples of path management applications
"""
import os
import numpy as np

from PySSPFM.settings import get_setting
from PySSPFM.utils.core.path_management import \
    (generate_filenames, get_files_with_conditions, sort_filenames,
     gen_bruker_filenames)


def ex_get_files_with_conditions():
    """
    Example get_files_with_conditions function.

    Parameters
    ----------

    Returns
    -------
    filepaths_sspfm : list
        File paths satisfying the conditions.
    """
    example_root_path_in = get_setting("example_root_path_in")
    dir_path_in = os.path.join(example_root_path_in, "KNN500n")

    # ex generate_filenames
    filepaths_sspfm = get_files_with_conditions(dir_path_in, prefix="KNN",
                                                extension=".txt")

    return filepaths_sspfm


def ex_filename_management(verbose=False):
    """
    Example filename management functions.

    Parameters
    ----------
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    filenames_sspfm : list
        Filenames generated based on indices and root.
    sorted_filenames : list
        Sorted filenames.
    sorted_indexs : list
        Sorted indices.
    filename_root : list
        Filename root.
    bruker_filenames : list
        Bruker filenames.
    """
    np.random.seed(0)

    # Generate randomly anranged filenames based on indices and root.
    file_indices = [18, 51]
    file_root = ["SSPFM_map1_32pix_", "_PZT.spm"]

    # ex generate_filenames
    filenames_sspfm = generate_filenames(file_indices, file_root)
    # ex sort_filenames
    out = sort_filenames(filenames_sspfm)
    (sorted_filenames, sorted_indexs, filename_root) = out
    # ex gen_bruker_filenames
    bruker_filenames = gen_bruker_filenames(filenames_sspfm)

    if verbose:
        print("\n- ex sort_filenames:")
        print(f"sorted indices : {sorted_indexs}")
        print(f"root of file name : {filename_root}")

    return (filenames_sspfm, sorted_filenames, sorted_indexs, filename_root,
            bruker_filenames)


if __name__ == '__main__':
    ex_get_files_with_conditions()
    ex_filename_management(verbose=True)
