"""
Module used for nanoloop: - save and read files
"""

from datetime import datetime
import os
import numpy as np


def sort_loop(ss_pfm_bias, write_nb_voltages, read_nb_voltages, dict_res,
              unit='a.u'):
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
        2d list of (m) datas (index, read and write voltage, amplitude,
        phase ...) of length n, organized in terms of nanoloop structure
    fmt: tuple(m) of string
        Tuple of data saving format
    header: str
        Title of datas to save
    """
    # Create fmt and header for saving results in txt file
    meas_label = {'Amplitude': {'unit': f'{unit}', 'fmt': '%.3e'},
                  'Phase': {'unit': '°', 'fmt': '%.3f'},
                  'Freq res': {'unit': 'kHz', 'fmt': '%.1f'},
                  'Q fact': {'unit': '', 'fmt': '%.1f'},
                  'inc Amp': {'unit': f'{unit}', 'fmt': '%.1e'},
                  'inc Pha': {'unit': '°', 'fmt': '%.1f'}}
    fmt = ['%i', '%.2f', '%.2f']
    header = 'Loop index\tRead Volt (V)\tWrite Volt (V)\t'

    # Add measurement labels to fmt and header
    for key in dict_res.keys():
        fmt.append(meas_label[key]['fmt'])
        header += f'{key} ({meas_label[key]["unit"]})\t'

    # Separate write and read voltage signal
    ss_pfm_bias_write = ss_pfm_bias[::2]
    ss_pfm_bias_read = ss_pfm_bias[1::2]

    loop = [[] for _ in range(len(dict_res) + 3)]

    # Fill column 0 with loop number
    loop[0] = [i + 1 for i in range(read_nb_voltages) for _ in
               range((write_nb_voltages - 1) * 2)]

    # Fill column 1 with read voltage
    loop[1] = ss_pfm_bias_read

    # Fill column 2 with write voltage
    loop[2] = ss_pfm_bias_write

    # Fill other columns with the different measurements
    for i, key in enumerate(dict_res.keys()):
        loop[3 + i] = dict_res[key]

    return loop, tuple(fmt), header


def txt_loop(dir_path_out, file_name_root, loop_tab, fmt, header,
             mode='Off field'):
    """
    Save loop datas in a text file

    Parameters
    ----------
    dir_path_out: str
        Path of the txt saving loop directory (out)
    file_name_root: str
        Name of root for the file (out)
    loop_tab: list(n*m) or numpy.array(n*m) of float
        2D array of loop datas
    fmt: tuple(n) of string
        Tuple of data saving format
    header: str
        Title of datas to save
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

    file_path_out = os.path.join(dir_path_out, lab + file_name_root + '.txt')
    date = datetime.now().strftime('%Y-%m-%d %H;%M')
    date_str = f'Date of analysis: {date}\n\n'

    indxs = [cont for cont, tab in enumerate(loop_tab) if
             all(elem is None for elem in tab)]
    indxs.reverse()
    header_tab = header.split('\t')

    for indx in indxs:
        header_tab = header_tab[:indx] + header_tab[indx + 1:]
        fmt = fmt[:indx] + fmt[indx + 1:]
        loop_tab = loop_tab[:indx] + loop_tab[indx + 1:]

    header = date_str + '\t'.join(header_tab)

    try:
        np.savetxt(file_path_out, np.array(loop_tab).T, fmt=fmt, newline='\n',
                   delimiter='\t\t', header=header)
    except TypeError:
        print("TypeError management with except: data contain NAN values")
        loop_tab = np.where(np.array(loop_tab) is None, 'np.nan', loop_tab)
        np.savetxt(file_path_out, np.array(loop_tab).T, fmt='%s', newline='\n',
                   delimiter='\t\t', header=header)

    return file_path_out


def extract_loop(file_path_in):
    """
    Extract loop of txt saving file

    Parameters
    ----------
    file_path_in: str
        Path of loop txt file (in)

    Returns
    -------
    datas_dict: dict
        Object containing all the data loop
    dict_str: dict
        Used for figure annotation
    """
    assert os.path.isfile(file_path_in)

    datas_tab = np.transpose(np.genfromtxt(file_path_in, delimiter='\t\t',
                                           skip_header=3))
    with open(file_path_in, encoding='latin-1') as data_file:
        lines = data_file.readlines()
    header = lines[2]
    split_header = header.split('\t')

    datas_dict = {}
    key_labs = ['index', 'read', 'write', 'amplitude', 'phase', 'freq',
                'q fact', 'inc amp', 'inc pha']
    index = -1

    for _, key in enumerate(split_header):
        name = key
        for lab in key_labs:
            if lab in key.lower():
                name = lab
                index += 1
        data_values = datas_tab[index]
        data_values = [np.nan if np.isnan(value) else value for value in
                       data_values]
        datas_dict[name] = data_values

    unit = ''
    for elem in split_header:
        if 'Amplitude' in elem:
            unit = elem.split()[1][1:-1]

    if os.path.split(file_path_in)[1].split('_')[0] == 'on':
        label, col = 'On field', 'y'
    else:
        label, col = 'Off field', 'w'

    dict_str = {'unit': unit, 'label': label, 'col': col}

    data_file.close()

    return datas_dict, dict_str
