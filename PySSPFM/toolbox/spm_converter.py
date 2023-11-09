"""
--> Executable Script
Conversion of .spm datacube file (SS PFM) to other datacube file extension
(txt, csv, xlsx)
Inspired by SS_PFM script, Nanoscope, Bruker
"""

import os
import shutil
import tkinter.filedialog as tkf
import time
import pandas as pd
import numpy as np

from PySSPFM.settings import get_setting
from PySSPFM.utils.raw_extraction import data_extraction
from PySSPFM.utils.path_for_runable import load_parameters_from_file


def single_script(dir_path_out, file_path_in, extension='txt', mode='classic',
                  verbose=False):
    """
    Extraction and saving of spm file data (i.e a pixel) in txt file

    Parameters
    ----------
    dir_path_out: str
        Directory path for saving the measurement file (out)
    file_path_in: str
        Path of the SPM measurement file (in)
    mode: str, optional
        Measurement mode ('classic' or 'dfrt')
    extension: str, optional
        File extension for saving ('txt', 'csv', 'xlsx')
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    None
    """
    assert extension in ['txt', 'csv', 'xlsx']

    # Print file name
    _, file_name_in = os.path.split(file_path_in)
    if verbose:
        print(f'- {file_name_in}\n')

    # Data extraction from spm measurement file
    dict_meas, _ = data_extraction(
        file_path_in, mode_dfrt=(mode.lower() == 'dfrt'))

    # Data identification
    raw_data = [dict_meas['times']]
    list_meas = [dict_meas['amp'], dict_meas['pha'], dict_meas['deflection']]
    if mode.lower() != 'dfrt':
        list_meas.append(dict_meas['tip_bias'])
    for _, meas in enumerate(list_meas):
        raw_data.append(np.ravel(meas) if len(meas) != 0 else
                        np.zeros(len(dict_meas['times'])))

    # Save the measure
    _, file_name_in = os.path.split(file_path_in)
    file_name_out = file_name_in[:-4]
    file_path_out = os.path.join(dir_path_out, file_name_out + '.' + extension)

    key_measurement_extraction = get_setting("key_measurement_extraction")
    header = list(key_measurement_extraction['table'][mode].keys())

    if extension == 'txt':
        # Text file format
        delimiter = get_setting('delimiter')
        header = delimiter.join(header)
        np.savetxt(file_path_out, np.array(raw_data).T, delimiter=delimiter,
                   newline='\n', header=header)
    elif extension in ['csv', 'xlsx']:
        save_dict = dict(zip(header, raw_data))
        data_frame = pd.DataFrame(save_dict)
        # CSV file format
        if extension == 'csv':
            csv_file_path = os.path.join(dir_path_out, file_name_out + '.csv')
            data_frame.to_csv(csv_file_path, index=False)
        # Excel file format
        else:
            excel_file_path = os.path.join(dir_path_out,
                                           file_name_out + f'.{extension}')
            with pd.ExcelWriter(excel_file_path) as writer:  # noqa
                data_frame.to_excel(writer, sheet_name='Measurements',
                                    index=False)

    else:
        raise IOError("extension should be 'txt', or 'csv', or 'xlsx'")


def multi_script(dir_path_in, mode='classic', extension='txt',
                 dir_path_out=None, verbose=False):
    """
    Data extraction of list of spm files in a directory by using single
    script for each file

    Parameters
    ----------
    dir_path_in: str
        Directory path of spm measurement (in)
    mode: str, optional
        Measurement mode ('classic' or 'dfrt')
    extension: str, optional
        File extension for saving ('txt', 'csv', 'xlsx')
    dir_path_out: str, optional
        Directory path of saving txt measurement (out)
    verbose: bool, optional
        Activation key for verbosity

    Returns
    -------
    None
    """
    # Create a new folder to save txt files
    dir_path_out = dir_path_out or f'{dir_path_in}_datacube_{extension}'
    root_out, dir_name_out = os.path.split(dir_path_out)
    if verbose:
        print(f'saving folder: {dir_name_out}\n')
    if dir_name_out not in os.listdir(root_out):
        os.makedirs(dir_path_out)

    # Copy measurement sheet to saving folder in another extension
    file_name_csv_in = ''
    for elem in os.listdir(dir_path_in):
        if elem.endswith('.csv') and 'measurement sheet' in elem:
            file_name_csv_in = os.path.join(dir_path_in, elem)
            if verbose:
                print(os.path.split(file_name_csv_in)[1] + '\n')
    shutil.copyfile(file_name_csv_in,
                    os.path.join(dir_path_out,
                                 os.path.split(file_name_csv_in)[1]))

    # Start single script for each spm file
    i = 0
    for elem in os.listdir(dir_path_in):
        if elem.endswith('.spm'):
            file_path_in = os.path.join(dir_path_in, elem)
            single_script(dir_path_out=dir_path_out, file_path_in=file_path_in,
                          mode=mode, extension=extension, verbose=verbose)
            i += 1


def main_spm_converter(dir_path_in, mode='classic', extension='txt',
                       dir_path_out=None, verbose=False):
    """
    Main function used to convert spm file to another extension file

    Parameters
    ----------
    dir_path_in: str
        Directory of datacube SSPFM raw file measurements.
        This parameter specifies the directory where SPM datacube SSPFM raw file
        measurements are located. It is used to indicate the path to the
        directory containing these measurement files.
    mode: str, optional
        Treatment used for segment data analysis
        (extraction of PFM measurements).
        This parameter determines the treatment method used for segment data
        analysis, specifically for the extraction of PFM measurements.
        Two possible values: 'classic' (sweep) or 'dfrt'.
    extension: str, optional
        Extension of converted spm files.
        This parameter determines the extension type used for conversion of
        .spm file.
        Three possible values: 'txt' or 'csv' or 'xlsx'.
    dir_path_out: str, optional
        Saving directory for conversion results
        (optional, default: 'title_meas'_datacube_'extension' directory in
        the same root)
        This parameter specifies the directory where the converted files
        generated as a result of the analysis will be saved.
    verbose: bool, optional
        Activation key for printing verbosity during analysis.
        This parameter serves as an activation key for printing verbose
        information during the analysis.

    Returns
    -------
    None
    """
    # Multi script
    if verbose:
        print('############################################\n')
        print(f'\nconversion spm to {extension} in progress ...\n')
    multi_script(dir_path_in, mode=mode, extension=extension,
                 dir_path_out=dir_path_out, verbose=verbose)
    if verbose:
        print(f'\nconversion spm to {extension} end with success !')
        print('############################################\n')

    # Ending
    if verbose:
        print('\n############################################\n')
        for _ in range(3):
            print('\n.')
            time.sleep(1)
        print('\n\nData analysis end with success !')
        print('############################################\n')


def main(file_name_user_params=None):
    """
    Main function for data analysis

    Parameters
    ----------
    file_name_user_params: str, optional
        Name of user parameters file (json or toml extension), optional
        (default is None, user parameters are used from original python script)
    """
    script_directory = os.path.dirname(os.path.realpath(__file__))
    file_path_user_params = os.path.join(
        script_directory, file_name_user_params) \
        if file_name_user_params else "no file"
    if os.path.exists(file_path_user_params):
        # Load parameters from the specified configuration file
        print(f"user parameters from {file_name_user_params} file")
        config_params = load_parameters_from_file(file_path_user_params)
        dir_path_in = config_params['dir_path_in']
        dir_path_out = config_params['dir_path_out']
        verbose = config_params['verbose']
        mode = config_params['mode']
        extension = config_params['extension']
    else:
        # Get directory path
        dir_path_in = tkf.askdirectory()
        # dir_path_in = r'...\KNN500n
        dir_path_out = None
        # dir_path_out = r'...\KNN500n_datacube_txt
        verbose = True
        # mode = 'dfrt' or 'classic'
        mode = 'classic'
        # extension = 'txt' or 'csv' or 'xlsx'
        extension = 'txt'

    # Main function
    main_spm_converter(dir_path_in, mode=mode, extension=extension,
                       dir_path_out=dir_path_out, verbose=verbose)


if __name__ == '__main__':
    main()
