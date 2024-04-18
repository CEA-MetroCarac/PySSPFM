"""
Path management function in order to get or generate path, folder,
or file names
"""

import re
import os
import random


def get_files_with_conditions(directory, prefix=None, extension=None):
    """
    Get files in a directory with specified conditions.

    Parameters
    ----------
    directory: str
        Path to the directory.
    prefix: str, optional
        Prefix to filter filenames (default is None).
    extension: str, optional
        Extension to filter filenames (default is None).

    Returns
    -------
    list of str
        List of filenames in the directory that meet the conditions.
    """
    files_in_directory = []
    for filename in os.listdir(directory):
        if (prefix is None or filename.startswith(prefix)) and \
                (extension is None or filename.endswith(extension)):
            files_in_directory.append(os.path.join(directory, filename))

    return files_in_directory


def gen_bruker_filenames(filenames):
    """
    Generate Bruker filenames.

    Parameters
    ----------
    filenames: list of str
        List of filenames.

    Returns
    -------
    list of str
        List of Bruker filenames.
    """
    bruker_filenames = []
    _, sorted_indexs, filename_root = sort_filenames(filenames)
    filename_root, extension = os.path.splitext(filename_root)
    filename_root = filename_root.replace('__', '_')
    for index in sorted_indexs:
        bruker_filenames.append(f"{filename_root}.0_{index:05d}{extension}")
    return bruker_filenames


def unique_numbers(lists):
    """
    Find unique numbers in lists.

    Parameters
    ----------
    lists: list of lists
        List of lists containing numbers.

    Returns
    -------
    list of lists
        List of lists containing unique numbers.
    common_numbers: list
        Common numbers shared by all sublists.
    """
    common_numbers = set(lists[0])
    for lst in lists[1:]:
        common_numbers.intersection_update(lst)
    result = [[num for num in lst if num not in common_numbers]
              for lst in lists]

    return result, list(common_numbers)


def separate_numbers_from_filenames(filenames):
    """
    Extract numbers from filenames.

    Parameters
    ----------
    filenames: list of str
        List of filenames.

    Returns
    -------
    list of list of int
        List of lists containing numbers extracted from filenames.
    list_non_numbers: list of str
        Common parts shared by all filenames, extracted based on non-numeric
        elements.
    """
    list_numbers = [list(re.findall(r'\d+', filename)) for filename in
                    filenames]
    list_non_numbers = [item for item in re.split(r'\d+', filenames[0]) if
                        item]

    return list_numbers, list_non_numbers


def sort_filenames(filenames):
    """
    Sort filenames based on extracted numbers in their names.

    Parameters
    ----------
    filenames: list of str
        List of filenames.

    Returns
    -------
    sorted_filenames: list of str
        List of sorted filenames.
    sorted_indexs: list of int
        List of corresponding indices.
    filename_root: str
        Common part shared by all filenames, extracted based on the order of
        appearance of elements in the filenames.
    """
    # Separate numbers and char
    numbers, common_non_numbers = separate_numbers_from_filenames(filenames)
    # Separate indices from number of filename root
    reduced_numbers, common_numbers = unique_numbers(numbers)

    def find_order_in_string(elements, string):
        indices = []
        for element in elements:
            index = string.index(element)
            indices.append(index)
        sorted_indices = sorted(range(len(indices)), key=lambda k: indices[k])
        order = [sorted_indices.index(cont) for cont in range(len(indices))]
        return order

    # Find filename root
    common_patterns = common_non_numbers + common_numbers
    order_patterns = find_order_in_string(common_patterns, filenames[0])
    filename_root = ""
    for elem in order_patterns:
        filename_root += common_patterns[elem]

    # Check if the list is empty and add zero to the empty list
    for i, lst in enumerate(reduced_numbers):
        if not lst:
            reduced_numbers[i].append('0')

    def dimensions_list_nd(list_object):
        if isinstance(list_object, list):
            return (len(list_object),) + dimensions_list_nd(list_object[0])
        else:
            return ()

    dimensions = dimensions_list_nd(reduced_numbers)
    if dimensions[1] == 1:
        indexs = [int(index[0]) for index in reduced_numbers]
    else:
        raise NotImplementedError("File index is not unique")

    # Sort filenames and indices
    indexed_filenames = list(zip(indexs, filenames))
    sorted_indexed_filenames = sorted(indexed_filenames, key=lambda x: x[0])
    sorted_filenames = [filename for _, filename in sorted_indexed_filenames]
    sorted_indexs = [index for index, _ in sorted_indexed_filenames]

    return sorted_filenames, sorted_indexs, filename_root


def generate_filenames(file_indices, file_root):
    """
    Generate filenames based on indices and root.

    Parameters
    ----------
    file_indices: tuple or list
        Tuple containing start and end indices (inclusive).
    file_root: tuple or list
        Tuple containing prefix and suffix for filenames.

    Returns
    -------
    list of str
        List of generated filenames.
    """
    filenames = [f"{file_root[0]}{i}{file_root[1]}"
                 for i in range(file_indices[0], file_indices[1])]
    random.shuffle(filenames)

    return filenames
