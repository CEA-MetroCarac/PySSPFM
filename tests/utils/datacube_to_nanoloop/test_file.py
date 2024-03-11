"""
Test file methods
"""

from examples.utils.datacube_to_nanoloop.ex_file import example_file


# class TestFile(unittest.TestCase):


def test_file():
    """ Test example_file """

    exp_meas_time, file_names_ordered = example_file()

    target_file_names = \
        ['KNN500n_SSPFM.0_00056.txt', 'KNN500n_SSPFM.0_00057.txt',
         'KNN500n_SSPFM.0_00058.txt', 'KNN500n_SSPFM.0_00059.txt',
         'KNN500n_SSPFM.0_00060.txt', 'KNN500n_SSPFM.0_00061.txt',
         'KNN500n_SSPFM.0_00062.txt', 'KNN500n_SSPFM.0_00063.txt',
         'KNN500n_SSPFM.0_00064.txt', 'KNN500n_SSPFM.0_00065.txt',
         'KNN500n_SSPFM.0_00066.txt', 'KNN500n_SSPFM.0_00067.txt',
         'KNN500n_SSPFM.0_00068.txt', 'KNN500n_SSPFM.0_00069.txt',
         'KNN500n_SSPFM.0_00070.txt', 'KNN500n_SSPFM.0_00071.txt',
         'KNN500n_SSPFM.0_00072.txt', 'KNN500n_SSPFM.0_00073.txt',
         'KNN500n_SSPFM.0_00074.txt', 'KNN500n_SSPFM.0_00075.txt',
         'KNN500n_SSPFM.0_00076.txt', 'KNN500n_SSPFM.0_00077.txt',
         'KNN500n_SSPFM.0_00078.txt', 'KNN500n_SSPFM.0_00079.txt',
         'KNN500n_SSPFM.0_00080.txt', 'KNN500n_SSPFM.0_00081.txt',
         'KNN500n_SSPFM.0_00082.txt', 'KNN500n_SSPFM.0_00083.txt',
         'KNN500n_SSPFM.0_00084.txt', 'KNN500n_SSPFM.0_00085.txt',
         'KNN500n_SSPFM.0_00086.txt', 'KNN500n_SSPFM.0_00087.txt',
         'KNN500n_SSPFM.0_00088.txt', 'KNN500n_SSPFM.0_00089.txt',
         'KNN500n_SSPFM.0_00090.txt', 'KNN500n_SSPFM.0_00091.txt',
         'KNN500n_SSPFM.0_00092.txt', 'KNN500n_SSPFM.0_00093.txt',
         'KNN500n_SSPFM.0_00094.txt', 'KNN500n_SSPFM.0_00095.txt',
         'KNN500n_SSPFM.0_00096.txt', 'KNN500n_SSPFM.0_00097.txt',
         'KNN500n_SSPFM.0_00098.txt', 'KNN500n_SSPFM.0_00099.txt',
         'KNN500n_SSPFM.0_00100.txt', 'KNN500n_SSPFM.0_00101.txt',
         'KNN500n_SSPFM.0_00102.txt', 'KNN500n_SSPFM.0_00103.txt',
         'KNN500n_SSPFM.0_00104.txt', 'KNN500n_SSPFM.0_00105.txt',
         'KNN500n_SSPFM.0_00106.txt', 'KNN500n_SSPFM.0_00107.txt',
         'KNN500n_SSPFM.0_00108.txt', 'KNN500n_SSPFM.0_00109.txt',
         'KNN500n_SSPFM.0_00110.txt', 'KNN500n_SSPFM.0_00111.txt',
         'KNN500n_SSPFM.0_00112.txt', 'KNN500n_SSPFM.0_00113.txt',
         'KNN500n_SSPFM.0_00114.txt', 'KNN500n_SSPFM.0_00115.txt',
         'KNN500n_SSPFM.0_00116.txt', 'KNN500n_SSPFM.0_00117.txt',
         'KNN500n_SSPFM.0_00118.txt']

    assert exp_meas_time == 70.467422
    assert file_names_ordered == target_file_names
