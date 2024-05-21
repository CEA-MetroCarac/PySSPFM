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
     dict_analysis_1, nb_write_per_read, write_segment, properties,
     dim_pix, dim_mic, main_elec_tab) = out
    file_names_from_raw = [[os.path.split(path)[1] for path in paths]
                           for paths in file_paths_from_raw]
    file_names_from_nanoloops = [[os.path.split(path)[1] for path in paths]
                                 for paths in file_paths_from_nanoloops]

    target_file_names = \
        [['off_f_KNN500n_SSPFM.0_00056.txt', 'on_f_KNN500n_SSPFM.0_00056.txt'],
         ['off_f_KNN500n_SSPFM.0_00057.txt', 'on_f_KNN500n_SSPFM.0_00057.txt'],
         ['off_f_KNN500n_SSPFM.0_00058.txt', 'on_f_KNN500n_SSPFM.0_00058.txt'],
         ['off_f_KNN500n_SSPFM.0_00059.txt', 'on_f_KNN500n_SSPFM.0_00059.txt'],
         ['off_f_KNN500n_SSPFM.0_00060.txt', 'on_f_KNN500n_SSPFM.0_00060.txt'],
         ['off_f_KNN500n_SSPFM.0_00061.txt', 'on_f_KNN500n_SSPFM.0_00061.txt'],
         ['off_f_KNN500n_SSPFM.0_00062.txt', 'on_f_KNN500n_SSPFM.0_00062.txt'],
         ['off_f_KNN500n_SSPFM.0_00063.txt', 'on_f_KNN500n_SSPFM.0_00063.txt'],
         ['off_f_KNN500n_SSPFM.0_00064.txt', 'on_f_KNN500n_SSPFM.0_00064.txt'],
         ['off_f_KNN500n_SSPFM.0_00065.txt', 'on_f_KNN500n_SSPFM.0_00065.txt'],
         ['off_f_KNN500n_SSPFM.0_00066.txt', 'on_f_KNN500n_SSPFM.0_00066.txt'],
         ['off_f_KNN500n_SSPFM.0_00067.txt', 'on_f_KNN500n_SSPFM.0_00067.txt'],
         ['off_f_KNN500n_SSPFM.0_00068.txt', 'on_f_KNN500n_SSPFM.0_00068.txt'],
         ['off_f_KNN500n_SSPFM.0_00069.txt', 'on_f_KNN500n_SSPFM.0_00069.txt'],
         ['off_f_KNN500n_SSPFM.0_00070.txt', 'on_f_KNN500n_SSPFM.0_00070.txt'],
         ['off_f_KNN500n_SSPFM.0_00071.txt', 'on_f_KNN500n_SSPFM.0_00071.txt'],
         ['off_f_KNN500n_SSPFM.0_00072.txt', 'on_f_KNN500n_SSPFM.0_00072.txt'],
         ['off_f_KNN500n_SSPFM.0_00073.txt', 'on_f_KNN500n_SSPFM.0_00073.txt'],
         ['off_f_KNN500n_SSPFM.0_00074.txt', 'on_f_KNN500n_SSPFM.0_00074.txt'],
         ['off_f_KNN500n_SSPFM.0_00075.txt', 'on_f_KNN500n_SSPFM.0_00075.txt'],
         ['off_f_KNN500n_SSPFM.0_00076.txt', 'on_f_KNN500n_SSPFM.0_00076.txt'],
         ['off_f_KNN500n_SSPFM.0_00077.txt', 'on_f_KNN500n_SSPFM.0_00077.txt'],
         ['off_f_KNN500n_SSPFM.0_00078.txt', 'on_f_KNN500n_SSPFM.0_00078.txt'],
         ['off_f_KNN500n_SSPFM.0_00079.txt', 'on_f_KNN500n_SSPFM.0_00079.txt'],
         ['off_f_KNN500n_SSPFM.0_00080.txt', 'on_f_KNN500n_SSPFM.0_00080.txt'],
         ['off_f_KNN500n_SSPFM.0_00081.txt', 'on_f_KNN500n_SSPFM.0_00081.txt'],
         ['off_f_KNN500n_SSPFM.0_00082.txt', 'on_f_KNN500n_SSPFM.0_00082.txt'],
         ['off_f_KNN500n_SSPFM.0_00083.txt', 'on_f_KNN500n_SSPFM.0_00083.txt'],
         ['off_f_KNN500n_SSPFM.0_00084.txt', 'on_f_KNN500n_SSPFM.0_00084.txt'],
         ['off_f_KNN500n_SSPFM.0_00085.txt', 'on_f_KNN500n_SSPFM.0_00085.txt'],
         ['off_f_KNN500n_SSPFM.0_00086.txt', 'on_f_KNN500n_SSPFM.0_00086.txt'],
         ['off_f_KNN500n_SSPFM.0_00087.txt', 'on_f_KNN500n_SSPFM.0_00087.txt'],
         ['off_f_KNN500n_SSPFM.0_00088.txt', 'on_f_KNN500n_SSPFM.0_00088.txt'],
         ['off_f_KNN500n_SSPFM.0_00089.txt', 'on_f_KNN500n_SSPFM.0_00089.txt'],
         ['off_f_KNN500n_SSPFM.0_00090.txt', 'on_f_KNN500n_SSPFM.0_00090.txt'],
         ['off_f_KNN500n_SSPFM.0_00091.txt', 'on_f_KNN500n_SSPFM.0_00091.txt'],
         ['off_f_KNN500n_SSPFM.0_00092.txt', 'on_f_KNN500n_SSPFM.0_00092.txt'],
         ['off_f_KNN500n_SSPFM.0_00093.txt', 'on_f_KNN500n_SSPFM.0_00093.txt'],
         ['off_f_KNN500n_SSPFM.0_00094.txt', 'on_f_KNN500n_SSPFM.0_00094.txt'],
         ['off_f_KNN500n_SSPFM.0_00095.txt', 'on_f_KNN500n_SSPFM.0_00095.txt'],
         ['off_f_KNN500n_SSPFM.0_00096.txt', 'on_f_KNN500n_SSPFM.0_00096.txt'],
         ['off_f_KNN500n_SSPFM.0_00097.txt', 'on_f_KNN500n_SSPFM.0_00097.txt'],
         ['off_f_KNN500n_SSPFM.0_00098.txt', 'on_f_KNN500n_SSPFM.0_00098.txt'],
         ['off_f_KNN500n_SSPFM.0_00099.txt', 'on_f_KNN500n_SSPFM.0_00099.txt'],
         ['off_f_KNN500n_SSPFM.0_00100.txt', 'on_f_KNN500n_SSPFM.0_00100.txt'],
         ['off_f_KNN500n_SSPFM.0_00101.txt', 'on_f_KNN500n_SSPFM.0_00101.txt'],
         ['off_f_KNN500n_SSPFM.0_00102.txt', 'on_f_KNN500n_SSPFM.0_00102.txt'],
         ['off_f_KNN500n_SSPFM.0_00103.txt', 'on_f_KNN500n_SSPFM.0_00103.txt'],
         ['off_f_KNN500n_SSPFM.0_00104.txt', 'on_f_KNN500n_SSPFM.0_00104.txt'],
         ['off_f_KNN500n_SSPFM.0_00105.txt', 'on_f_KNN500n_SSPFM.0_00105.txt'],
         ['off_f_KNN500n_SSPFM.0_00106.txt', 'on_f_KNN500n_SSPFM.0_00106.txt'],
         ['off_f_KNN500n_SSPFM.0_00107.txt', 'on_f_KNN500n_SSPFM.0_00107.txt'],
         ['off_f_KNN500n_SSPFM.0_00108.txt', 'on_f_KNN500n_SSPFM.0_00108.txt'],
         ['off_f_KNN500n_SSPFM.0_00109.txt', 'on_f_KNN500n_SSPFM.0_00109.txt'],
         ['off_f_KNN500n_SSPFM.0_00110.txt', 'on_f_KNN500n_SSPFM.0_00110.txt'],
         ['off_f_KNN500n_SSPFM.0_00111.txt', 'on_f_KNN500n_SSPFM.0_00111.txt'],
         ['off_f_KNN500n_SSPFM.0_00112.txt', 'on_f_KNN500n_SSPFM.0_00112.txt'],
         ['off_f_KNN500n_SSPFM.0_00113.txt', 'on_f_KNN500n_SSPFM.0_00113.txt'],
         ['off_f_KNN500n_SSPFM.0_00114.txt', 'on_f_KNN500n_SSPFM.0_00114.txt'],
         ['off_f_KNN500n_SSPFM.0_00115.txt', 'on_f_KNN500n_SSPFM.0_00115.txt'],
         ['off_f_KNN500n_SSPFM.0_00116.txt', 'on_f_KNN500n_SSPFM.0_00116.txt'],
         ['off_f_KNN500n_SSPFM.0_00117.txt', 'on_f_KNN500n_SSPFM.0_00117.txt'],
         ['off_f_KNN500n_SSPFM.0_00118.txt', 'on_f_KNN500n_SSPFM.0_00118.txt']]

    assert nb_write_per_read == 100
    assert len(list(write_segment)) == 100
    assert len(dict_analysis_1) == 3
    assert target_file_names == file_names_from_raw
    assert target_file_names == file_names_from_nanoloops
    assert len(meas_pars) == 31
    assert len(sign_pars) == 16
    assert np.sum(list(dim_pix.values())) == 16
    assert np.sum(list(dim_mic.values())) == 7
    assert np.sum(list(properties['on'].values())) == 6269
    assert np.sum(list(properties['off'].values())) == 6408
    assert np.sum(list(properties['coupled'].values())) == 6565
    assert np.sum(main_elec_tab) == 57.0
