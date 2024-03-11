"""
Module used for nanoloop: - save and read files
"""

from datetime import datetime
import os
import numpy as np


def sort_nanoloop_data(ss_pfm_bias, write_nb_voltages, read_nb_voltages,
                       dict_res, unit='a.u'):
    """
    Generate a nanoloop 2D array of multi measurements (amplitude, phase ...)

    Parameters
    ----------
    ss_pfm_bias: list(p) or numpy.array(p) of float
        Array of sspfm signal values calculated (in V)
    write_nb_voltages: int
        Number of write voltage values
    read_nb_voltages: int
        Number of read voltage values
    dict_res: dict
        Results (amplitude, phase ...) for the loop
    unit: str, optional
        Unit label for amplitude measurement:
        - 'a.u' if no calibration is performed
        - 'nm' in the other case

    Returns
    -------
    loop: list(n*m) of float
        2d list of (m) data (index, read and write voltage, amplitude,
        phase ...) of length n, organized in terms of nanoloop structure
    fmt: tuple(m) of string
        Tuple of data saving format
    header: str
        Title of data to save
    """
    # Create fmt and header for saving results in txt file
    meas_label = {'Amplitude': {'unit': f'{unit}', 'fmt': '%.3e'},
                  'Phase': {'unit': 'deg', 'fmt': '%.3f'},
                  'Res Freq': {'unit': 'kHz', 'fmt': '%.1f'},
                  'Q Fact': {'unit': '', 'fmt': '%.1f'},
                  'Sigma Amp': {'unit': f'{unit}', 'fmt': '%.3e'},
                  'Sigma Pha': {'unit': 'deg', 'fmt': '%.3f'},
                  'Sigma Res Freq': {'unit': 'kHz', 'fmt': '%.1f'},
                  'Sigma Q Fact': {'unit': '', 'fmt': '%.1f'}}
    fmt = ['%i', '%.2f', '%.2f']
    header = 'Loop index\tRead Volt (V)\tWrite Volt (V)\t'
    loop = {}

    # Add measurement labels to fmt and header
    for key in dict_res.keys():
        if not all(elem is None for elem in dict_res[key]):
            fmt.append(meas_label[key]['fmt'])
            header += f'{key} ({meas_label[key]["unit"]})\t'
            loop[key] = dict_res[key]
        else:
            loop[key] = None

    for key in meas_label:
        if key not in dict_res:
            loop[key] = None

    # Separate write and read voltage signal
    ss_pfm_bias_write = ss_pfm_bias[::2]
    ss_pfm_bias_read = ss_pfm_bias[1::2]

    loop['Index Pix'] = [i + 1 for i in range(read_nb_voltages) for _ in
                         range((write_nb_voltages - 1) * 2)]
    loop['Read Volt'] = ss_pfm_bias_read
    loop['Write Volt'] = ss_pfm_bias_write

    return loop, tuple(fmt), header


def save_nanoloop_file(dir_path_out, file_name_root, loop_dict, fmt, header,
                       segment_info=None, mode='Off field'):
    """
    Save nanoloop data in a text file

    Parameters
    ----------
    dir_path_out: str
        Path of the txt saving loop directory (out)
    file_name_root: str
        Name of root for the file (out)
    loop_dict: list(n*m) or numpy.array(n*m) of float
        2D array of loop data
    fmt: tuple(n) of string
        Tuple of data saving format
    header: str
        Title of data to save
    segment_info: dict, optional
        Other info about the segment (topography, mechanical measurement ...) to
        add in the header
    mode: str, optional
        'Off field' or 'On field'

    Returns
    -------
    file_path_out: str
        Path of saving loop txt file (out)
    """
    if not os.path.isdir(dir_path_out):
        os.makedirs(dir_path_out)

    if mode == 'Off field':
        lab = 'off_f_'
    elif mode == 'On field':
        lab = 'on_f_'
    else:
        raise IOError('mode in [\'Off field\',\'On field\']')

    usual_keys = ['Index Pix', 'Read Volt', 'Write Volt', 'Amplitude', 'Phase',
                  'Res Freq', 'Q Fact', 'Sigma Amp', 'Sigma Pha',
                  'Sigma Res Freq', 'Sigma Q Fact']
    file_path_out = os.path.join(dir_path_out, lab + file_name_root + '.txt')

    # Add data and segment info in the file header
    date = datetime.now().strftime('%Y-%m-%d %H;%M')
    date_str = f'Date of analysis: {date}\n'
    if segment_info:
        segment_info_str = 'Segment other properties: '
        for key, value in segment_info.items():
            segment_info_str += f'{key}: {value}, '
        segment_info_str = segment_info_str[:-2] + '\n\n'
    else:
        segment_info_str = ''
    # Title of the rows
    loop_tab = [loop_dict[key]
                for key in usual_keys if loop_dict[key] is not None]

    header = date_str + segment_info_str + header

    try:
        np.savetxt(file_path_out, np.array(loop_tab).T, fmt=fmt, newline='\n',
                   delimiter='\t\t', header=header)
    except TypeError:
        print("TypeError management with except: data contain NAN values")
        loop_tab = np.where(np.array(loop_tab) is None, 'np.nan', loop_tab)
        np.savetxt(file_path_out, np.array(loop_tab).T, fmt='%s', newline='\n',
                   delimiter='\t\t', header=header)

    return file_path_out


def extract_nanoloop_data(file_path_in):
    """
    Extract nanoloop data of txt saving file

    Parameters
    ----------
    file_path_in: str
        Path of loop txt file (in)

    Returns
    -------
    data_dict: dict
        Object containing all the data loop
    dict_str: dict
        Used for figure annotation
    other_properties: dict
        Other properties about the segment (topography, mechanical measurement)
    """
    assert os.path.isfile(file_path_in)

    def count_header_lines(f_path):
        """
        Count the header of lines starting with '#' at the beginning of the
        file.

        Parameters
        ----------
        f_path : str
            Path to the text file.

        Returns
        -------
        count : int
            Number of lines starting with '#' at the beginning of the file.
        """
        count = 0
        with open(f_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip().startswith('#'):
                    count += 1
                else:
                    break
        return count

    num_header_lines = count_header_lines(file_path_in)
    data_tab = np.transpose(np.genfromtxt(file_path_in, delimiter='\t\t',
                                          skip_header=num_header_lines))
    with open(file_path_in, encoding='latin-1') as data_file:
        lines = data_file.readlines()

    header = [line.replace('# ', '') for line in lines if line.startswith('#')]

    # Extract other segment properties
    other_properties = None
    for line in header:
        if 'Segment other properties: ' in line:
            line_other_properties = \
                line.replace('Segment other properties: ', '')
            tab_other_properties = line_other_properties.split(', ')
            other_properties = {}
            for prop in tab_other_properties:
                splited_prop = prop.split(': ')
                other_properties[splited_prop[0]] = splited_prop[1]

    # Extract title of the rows
    meas_keys = header[-1].split('\t')
    if "\n" in meas_keys:
        meas_keys.remove("\n")

    data_dict = {}
    key_labs = ['index', 'read', 'write', 'amplitude', 'phase', 'freq',
                'q fact', 'sigma amp', 'sigma pha']
    index = -1

    for _, key in enumerate(meas_keys):
        name = key
        for lab in key_labs:
            if lab in key.lower():
                name = lab
                index += 1
        data_values = data_tab[index]
        data_values = [np.nan if np.isnan(value) else value for value in
                       data_values]
        data_dict[name] = data_values

    unit = ''
    for elem in meas_keys:
        if 'Amplitude' in elem:
            unit = elem.split()[1][1:-1]

    if os.path.split(file_path_in)[1].split('_')[0] == 'on':
        label, col = 'On field', 'y'
    else:
        label, col = 'Off field', 'w'

    dict_str = {'unit': unit, 'label': label, 'col': col}

    data_file.close()

    return data_dict, dict_str, other_properties
