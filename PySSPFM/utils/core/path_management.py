"""
Path management function in order to get or generate path, folder,
or file names
"""

import re
import os
import numpy as np


def get_filenames_with_conditions(directory, prefix=None, extension=None):
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
            files_in_directory.append(filename)

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


def extract_unique_numbers(lists):
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
    indice_column: int or None
        Index of the column where the uniqueness is broken,
        or None if all columns are unique.
    """
    common_numbers, unique_numbers = [], []
    indice_column = None
    for cont, columns in enumerate(zip(*lists)):
        if len(set(columns)) == 1:
            common_numbers.append(columns[0])
        else:
            unique_numbers = list(columns)
            indice_column = cont

    return unique_numbers, common_numbers, indice_column


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


def find_order(numbers, non_numbers, filename):
    """
    Find order of elements based on filename

    Parameters
    ----------
    numbers: list
        List of numbers
    non_numbers: list
        Non-numeric elements
    filename: str
        Name of the file

    Returns
    -------
    mutual_list: list
        Interleaved list of elements from numbers and non_numbers based on
        filename
    """

    def starts_with_number(string):
        """Check if string starts with a number"""
        pattern = r'^\d'
        return bool(re.match(pattern, string))

    def interleave_lists(list1, list2):
        """Interleave elements from two lists"""
        result = []
        min_len = min(len(list1), len(list2))
        for i in range(min_len):
            result.extend([list2[i], list1[i]])
        result.extend(list1[min_len:] or list2[min_len:])
        return result

    mutual_list = interleave_lists(non_numbers, numbers) \
        if starts_with_number(filename) \
        else interleave_lists(numbers, non_numbers)

    return mutual_list


def extract_filename_root(ordered_elems, indice_column):
    """
    Extract filename root from ordered elements

    Parameters
    ----------
    ordered_elems: list of str
        List of ordered elements
    indice_column: int
        Index of the column (for number) to remove

    Returns
    -------
    filename_root: str
        Filename root extracted from ordered elements
    """

    cont_num = -1
    for cont_elem, elem in enumerate(ordered_elems):
        if elem.isnumeric():
            cont_num += 1
        if cont_num == indice_column:
            del ordered_elems[cont_elem]
            break

    filename_root = "".join(ordered_elems)

    return filename_root


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
    indexs, _, indice_column = extract_unique_numbers(numbers)
    # Find filename_root
    ordered_elems = find_order(numbers[0], common_non_numbers, filenames[0])
    filename_root = extract_filename_root(ordered_elems, indice_column)

    # Sort filenames and indices
    indexed_filenames = list(zip(indexs, filenames))
    sorted_indexed_filenames = sorted(indexed_filenames, key=lambda x: x[0])
    sorted_filenames = [filename for _, filename in sorted_indexed_filenames]
    sorted_indexs = [int(index) for index, _ in sorted_indexed_filenames]

    return sorted_filenames, sorted_indexs, filename_root


def generate_filenames(file_indices, file_root):
    """
    Generate filenames based on indices and root, randomly arranged.

    Parameters
    ----------
    file_indices: tuple or list
        Tuple containing start and end indices (inclusive).
    file_root: tuple or list
        Tuple containing prefix and suffix for filenames.

    Returns
    -------
    list of str
        List of generated filenames randomly arranged.
    """
    filenames = [f"{file_root[0]}{i}{file_root[1]}"
                 for i in range(file_indices[0], file_indices[1])]
    np.random.shuffle(filenames)

    return filenames
