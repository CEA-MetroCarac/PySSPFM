"""
Test file methods
"""
import os
import numpy as np

from examples.utils.nanoloop_to_hyst.ex_file import example_file


# class TestFile(unittest.TestCase):


def test_file():
    """ Test example_file """

    out = example_file()
    (file_paths_from_nanoloops, file_paths_from_raw, meas_pars, sign_pars,
     dict_analysis_1, nb_write_per_read, write_segment, properties, dim_pix,
     dim_mic) = out
    file_names_from_nanoloops = [[os.path.split(path)[1] for path in paths]
                                 for paths in file_paths_from_nanoloops]
    file_names_from_raw = [[os.path.split(path)[1] for path in paths]
                           for paths in file_paths_from_raw]

    assert nb_write_per_read == 100
    assert len(list(write_segment)) == 100
    assert len(dict_analysis_1) == 3
    assert file_names_from_nanoloops == file_names_from_raw
    assert len(meas_pars) == 31
    assert len(sign_pars) == 16
    assert np.sum(list(dim_pix.values())) == 16
    assert np.sum(list(dim_mic.values())) == 7
    assert np.sum(list(properties['on'].values())) == 6269
    assert np.sum(list(properties['off'].values())) == 6408
    assert np.sum(list(properties['coupled'].values())) == 6565
