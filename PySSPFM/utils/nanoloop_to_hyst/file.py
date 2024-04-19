"""
Module used for the scripts of sspfm 2d step data analysis
(convert nanoloop to hyst)
    - Open and read files
    - Print info
    - Save measurements and parameters
"""

import os
import time
import numpy as np

from PySSPFM.utils.core.path_management import \
    get_filenames_with_conditions, sort_filenames
from PySSPFM.utils.signal_bias import write_vec


def create_file_nanoloop_paths(dir_path_in_raw, mode=''):
    """
    Create file paths for NanoLoop files.

    Parameters
    ----------
    dir_path_in_raw: str
        Directory path where the files are located.
    mode: str, optional
        Mode to filter filenames, must be in ['', 'off_f', 'on_f']
        (default is '').

    Returns
    -------
    file_paths_in: list of lists
        List of lists containing file paths for NanoLoop files.
    """
    filenames = get_filenames_with_conditions(dir_path_in_raw)
    filenames = [filename for filename in filenames
                 if "measurement sheet model SSPFM.csv" not in filename]

    file_paths_in = []

    if mode == '':
        keys = ['off_f_', 'on_f_']
    else:
        keys = [mode + '_']

    for cont, filename in enumerate(filenames):
        file_paths_in.append([])
        filename_root, _ = os.path.splitext(filename)
        for key in keys:
            nanoloop_filename = key + filename_root + '.txt'
            file_paths_in[cont].append(
                os.path.join(dir_path_in_raw, nanoloop_filename))

    return file_paths_in


def generate_file_nanoloop_paths(dir_path_in, mode=''):
    """
    Generate paths of all nanoloop txt loop files (i.e. pixel)

    Parameters
    ----------
    dir_path_in: str
        Path of the txt nanoloop files directory (in)
    mode: str, optional
        To not have a restricted selection, mode = ''
        To select only Off Field measurement: mode = 'off_f'
        To select only On Field measurement: mode = 'on_f'

    Returns
    ----------
    file_paths_in: list of str
        List of all txt nanoloop file paths (in)
    """
    assert os.path.isdir(dir_path_in)
    assert mode in ['', 'off_f', 'on_f']

    tab_file_name = {'off_f': [], 'on_f': []}
    if mode == '':
        for key in ['off_f', 'on_f']:
            filenames = get_filenames_with_conditions(dir_path_in, prefix=key,
                                                      extension=".txt")
            tab_file_name[key], _, _ = sort_filenames(filenames)
    else:
        filenames = get_filenames_with_conditions(dir_path_in, prefix=mode,
                                                  extension=".txt")
        tab_file_name[mode], _, _ = sort_filenames(filenames)

    file_paths_in = []
    if mode == '':
        for elem_off, elem_on in zip(
                tab_file_name['off_f'], tab_file_name['on_f']):
            file_paths_in.append([os.path.join(dir_path_in, elem_off),
                                  os.path.join(dir_path_in, elem_on)])
    else:
        for elem in tab_file_name[mode]:
            file_paths_in.append([os.path.join(dir_path_in, elem)])

    return file_paths_in


def print_parameters(file_path_in, verbose=False):
    """
    Extract, identifies and print measurement + treatment parameters of
    the txt file in the main directory

    Parameters
    ----------
    file_path_in: str
        Path of txt saving parameters file (in)
    verbose: bool, optional
        If True, print info of measurement and treatment parameters

    Returns
    -------
    meas_pars: dict
        Measurement parameters
    sign_pars: dict
        sspfm bias signal parameters
    dict_analysis_1: dict
        First step treatment parameters
    nb_write_per_read: int
        Number of write segment for a read value
    write_segment: list(n) or numpy.array(n) of float
        List of value for a write segment corresponding to one hysteresis (in V)
    """
    assert os.path.isfile(file_path_in)

    with open(file_path_in, encoding='utf-8') as parameter_file:
        lines = parameter_file.readlines()

    cont = 0
    for line in lines:
        cont += 1
        if 'second step' in line:
            break
    lines = lines[:cont - 1]

    add_lines = [[]]
    cont = 0
    for line in lines:
        if verbose:
            print(line.replace('\n', ''))
        if not (line.startswith('#') or line.startswith('-')):
            if line.startswith('\n'):
                add_lines.append([])
                cont += 1
            else:
                add_lines[cont].append(
                    line.replace('\n', '').replace('[Î¼m]', '[um]'))

    (meas_pars, sign_pars, info, glob_pars, fit) = ({}, {}, {}, {}, {})
    dictio = [meas_pars, sign_pars, info, glob_pars, fit]

    cont = 0
    for lst in add_lines:
        if len(lst) > 0:
            for txt in lst:
                txt_split = txt.split(':', 1)
                if txt_split[1][1:] in ["sin", "cos"]:
                    value = eval("np." + txt_split[1][1:])
                else:
                    try:
                        value = int(txt_split[1][1:])
                    except ValueError:
                        try:
                            value = float(txt_split[1][1:])
                        except ValueError:
                            value = txt_split[1][1:]
                dictio[cont][txt_split[0]] = value
            cont += 1

    nb_write_per_read = (sign_pars['Nb volt (W)'] - 1) * 2
    write_segment = write_vec(sign_pars)
    dict_analysis_1 = {'info': info, 'glob pars': glob_pars, 'fit': fit}

    parameter_file.close()

    return (meas_pars, sign_pars, dict_analysis_1, nb_write_per_read,
            write_segment)


def complete_parameters(file_path_in, user_pars, t0, date, file_path_out=None):
    """
    Fill second step analysis parameters in the saving txt file

    Parameters
    ----------
    file_path_in: str
        Path of the txt file for saving parameters (output)
    user_pars: dict
        Dictionary of all user parameters for the treatment
    t0: float
        Time passed (in seconds since 01/01/1970) at the moment of
        generating saving folder paths
    date: str
        Current date (Year-Month-Day Hour:Minute)
    file_path_out: str, optional
        Path of the txt file for saving parameters (output)

    Returns
    -------
    None
    """
    assert os.path.isfile(file_path_in)
    file_path_out = file_path_out or file_path_in

    with open(file_path_in, encoding='utf-8') as parameter_file:
        prev_lines = parameter_file.readlines()

    # Suppress previous second step parameters of prev_lines
    for index, line in enumerate(prev_lines):
        if 'second step' in line:
            prev_lines = prev_lines[:index]
            break
    # 2nd step duration
    treatment_time = time.time() - t0
    treatment_time_h_m_s = time.strftime('%Hh:%Mm:%Ss',
                                         time.gmtime(treatment_time))
    pha_func_str = user_pars['pha func'] \
        if isinstance(user_pars['pha func'], str) \
        else getattr(user_pars["pha func"], "__name__")
    new_lines = [
        '### Treatment parameters: second step ###',
        '- Info',
        f'start of analysis: {date}',
        f'analysis duration: {treatment_time_h_m_s}',
        '- Hysteresis / loop treatment parameters',
        f'fit hyst func: {user_pars["func"]}',
        f'fit hyst method: {user_pars["method"]}',
        f'fit hyst asym: {user_pars["asymmetric"]}',
        f'threshold value (in percent) for the calculation of nucleation '
        f'bias: {user_pars["inf thresh"]}',
        f'threshold value (in percent) for the calculation of saturation '
        f'domain: {user_pars["sat thresh"]}',
        f'first nanoloop deleted for analysis ?: {user_pars["del 1st loop"]}',
        '- Phase treatment parameters',
        f'phase correction: {user_pars["pha corr"]}',
        f'phase value (forward): {user_pars["pha fwd"]}',
        f'phase value (reverse): {user_pars["pha rev"]}',
        f'phase function: {pha_func_str}',
        f'main electrostatic component (on field): {user_pars["main elec"]}',
        f'locked electrostatic slope (on field): '
        f'{user_pars["locked elec slope"]}',
        '- Other parameters',
        f'differential domain between on/off field nanoloops: '
        f'{user_pars["diff domain"]}',
        f'differential domain between on/off field nanoloops, mode ?: '
        f'{user_pars["diff mode"]}',
        f'saturation domain for electrostatic decoupling procedure: '
        f'{user_pars["sat domain"]}',
        f'saturation domain for electrostatic decoupling procedure, mode ?: '
        f'{user_pars["sat mode"]}\n']

    raw_lines = prev_lines + new_lines
    treat_lines = [line.replace('\n', '') for line in raw_lines if
                   line.strip() != '']
    treat_lines = [treat_lines[0]] + ['\n\n\n' + line if line.startswith(
        '#') else '\n' + line if not line.startswith('-') else '\n\n' + line for
                   line in treat_lines[1:]]

    with open(file_path_out, 'w', encoding='utf-8') as file:
        file.write(''.join(treat_lines))

    parameter_file.close()
    file.close()


def save_properties(properties, dir_path_out, dim_pix=None, dim_mic=None,
                    file_prefix_out=None):
    """
    Save properties for sspfm maps in a text file

    Parameters
    ----------
    properties: dict
        Dictionary of properties of sspfm maps
    dir_path_out: str
        Path of the directory for saving the property files (output)
    dim_pix: dict('x': ,'y':) of int, optional
        Dictionary of map dimensions for 'x' and 'y' axis (in pixels)
    dim_mic: dict('x': ,'y':) of float, optional
        Dictionary of map dimensions for 'x' and 'y' axis (in microns)
    file_prefix_out: str, optional
        Prefix for the names of the property files (output)

    Returns
    -------
    None
    """
    file_prefix_out = file_prefix_out or "properties_"
    if not os.path.isdir(dir_path_out):
        os.makedirs(dir_path_out)

    header_lab_add = ''
    if (dim_pix is not None) and (dim_mic is not None):
        dict_dim = {'x pix': dim_pix['x'], 'y pix': dim_pix['y'],
                    'x mic': dim_mic['x'], 'y mic': dim_mic['y']}
        header_lab_tab = [f'{key}={val}, ' for key, val in dict_dim.items()]
        header_lab_add = ''.join(header_lab_tab)

    for key, values in properties.items():
        file_path_out = os.path.join(dir_path_out,
                                     file_prefix_out + key + '.txt')
        header = f'{key}\n{header_lab_add}\n'
        # fmt = '%.5e'
        tab_props = []

        for sub_key, sub_values in values.items():
            header += f'{sub_key}\t\t'
            list_sub_values = \
                [elem if elem != 'None' else np.nan for elem in sub_values]
            tab_props.append(np.array(list_sub_values, dtype=float).ravel())
        tab_props = np.where(np.isnan(tab_props), 'nan', tab_props)
        np.savetxt(file_path_out, np.array(tab_props).T, delimiter='\t\t',
                   newline='\n', header=header, fmt='%s')


def save_best_nanoloops(tab_best_loops, dir_path_out,
                        file_prefix_out="best_loop_"):
    """
    Save best nanoloops in a text file

    Parameters
    ----------
    tab_best_loops : dict
        Dictionary of all best loops classified for each mode
    dir_path_out : str
        Path of the directory for saving the best loops files (output)
    file_prefix_out : str, optional
        Prefix for the names of the best loops files (output)

    Returns
    -------
    None
    """
    if not os.path.isdir(dir_path_out):
        os.makedirs(dir_path_out)
    tab_data = ['piezoresponse', 'amplitude', 'phase']
    fmt = ('%i', '%.5e', '%.5e', '%.5e', '%.5e')
    tab_data, fmt = add_header_labels(tab_best_loops, tab_data, fmt)

    header_lab_add = 'index pix\t\tvoltage\t\t' + '\t\t'.join(tab_data)
    for key, value in tab_best_loops.items():
        header = f"{key}\n{header_lab_add}"
        file_path_out = os.path.join(dir_path_out,
                                     f"{file_prefix_out}{key}.txt")
        tab_index = []
        data_saved = []
        for _ in range(len(tab_data)+1):
            data_saved.append([])
        for cont, loop in enumerate(value):
            tab_index.append([])
            dict_best_loop = {'voltage': loop.amp.write_volt,
                              'piezoresponse': loop.piezorep.y_meas,
                              'amp': loop.amp.y_meas,
                              'pha': loop.pha.y_meas}
            if 'res freq' in tab_data:
                dict_best_loop['res freq'] = loop.res_freq.y_meas
            if 'q factor' in tab_data:
                dict_best_loop['q factor'] = loop.q_fact.y_meas

            for sub_cont, key_name in enumerate(dict_best_loop.keys()):
                data_saved[sub_cont].append(dict_best_loop[key_name])
                if sub_cont == 0:
                    tab_index[cont] = [cont+1 for _ in dict_best_loop[key_name]]
        for cont, elem in enumerate(data_saved):
            data_saved[cont] = np.ravel(elem)
        data_saved.insert(0, np.ravel(tab_index))
        data_saved = np.array(data_saved).T
        np.savetxt(file_path_out, data_saved,
                   delimiter='\t\t', newline='\n', header=header, fmt=fmt)


def add_header_labels(tab_best_loops, tab_data=None, fmt=None):
    """
    Add header labels for resonance frequency and Q factor based on available
    attributes

    Parameters
    ----------
    tab_best_loops: dict
        List of best loops for all file
    tab_data: list, optional
        List of data labels of best loop to save in txt file header. Default: []
    fmt: tuple, optional
        Format specification for the additional header labels. Default: ()

    Returns
    -------
    tab_data: list
        Updated tab_data
    fmt: tuple
        Updated fmt
    """
    fmt = fmt or ()
    tab_data = tab_data or []
    # Check for resonance frequency attribute and add header label if present
    try:
        if list(tab_best_loops.values())[0].res_freq:
            tab_data += 'res freq'
            fmt += '.5e'
    except AttributeError:
        pass

    # Check for Q factor attribute and add header label if present
    try:
        if list(tab_best_loops.values())[0].q_fact:
            tab_data += 'q factor'
            fmt += '.5e'
    except AttributeError:
        pass

    return tab_data, fmt


def extract_properties(dir_path_in):
    """
    Extract properties from txt saving files in the specified directory.

    Parameters
    ----------
    dir_path_in: str
        Path of the directory containing the property files.

    Returns
    -------
    properties: dict
        Dictionary of properties of sspfm maps.
    dim_pix: dict('x': ,'y':) of int
        Dictionary of map dimensions for 'x' and 'y' axis (in pixels).
    dim_mic: dict('x': ,'y':) of float
        Dictionary of map dimensions for 'x' and 'y' axis (in microns).
    """
    (properties, dim_pix, dim_mic) = ({}, {}, {})
    dim = ''

    for file_name_in in os.listdir(dir_path_in):
        file_path_in = os.path.join(dir_path_in, file_name_in)

        # Header extraction
        with open(file_path_in, encoding="latin-1") as file:
            lines = file.readlines()
        mode = lines[0][2:-1]
        dim = lines[1][2:-3].split(', ')

        # Properties extraction
        prop_keys = lines[2][2:].split('\t\t')[:-1]
        props = np.genfromtxt(
            file_path_in, dtype=float, delimiter='\t\t', skip_header=3,
            encoding='latin-1')
        properties[mode] = {}
        for key, prop in zip(prop_keys, np.array(props).T):
            properties[mode][key] = list(prop)

        # Close the file
        file.close()

    # Dictionary generation for dim_pix and dim_mic
    for elem in dim:
        sub_dim = elem.replace('=', ' ').split(' ')
        key = sub_dim[0]
        if sub_dim[1] == 'pix':
            dim_pix[key] = int(sub_dim[2])
        else:
            dim_mic[key] = float(sub_dim[2])

    if not dim_mic:
        dim_mic = None

    return properties, dim_pix, dim_mic
