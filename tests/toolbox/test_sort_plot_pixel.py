"""
Test sort_plot_pixel methods
"""
from pytest import approx, skip
import os

from examples.toolbox.ex_sort_plot_pixel import example_sort_plot_pixel


# class TestPlotExtremum(unittest.TestCase):


def test_sort_plot_pixel():
    """ Test example_sort_plot_pixel """

    list_file_path = example_sort_plot_pixel()
    list_file_name = [os.path.split(file_path)[1]
                      for file_path in list_file_path]
    target_f_name = [
        'off_f_KNN500n_SSPFM.0_00058.txt', 'off_f_KNN500n_SSPFM.0_00060.txt',
        'off_f_KNN500n_SSPFM.0_00059.txt', 'off_f_KNN500n_SSPFM.0_00063.txt',
        'off_f_KNN500n_SSPFM.0_00117.txt', 'off_f_KNN500n_SSPFM.0_00056.txt',
        'off_f_KNN500n_SSPFM.0_00118.txt', 'off_f_KNN500n_SSPFM.0_00116.txt',
        'off_f_KNN500n_SSPFM.0_00061.txt', 'off_f_KNN500n_SSPFM.0_00071.txt',
        'off_f_KNN500n_SSPFM.0_00064.txt', 'off_f_KNN500n_SSPFM.0_00070.txt',
        'off_f_KNN500n_SSPFM.0_00069.txt', 'off_f_KNN500n_SSPFM.0_00065.txt',
        'off_f_KNN500n_SSPFM.0_00074.txt', 'off_f_KNN500n_SSPFM.0_00073.txt',
        'off_f_KNN500n_SSPFM.0_00077.txt', 'off_f_KNN500n_SSPFM.0_00066.txt',
        'off_f_KNN500n_SSPFM.0_00068.txt', 'off_f_KNN500n_SSPFM.0_00078.txt',
        'off_f_KNN500n_SSPFM.0_00079.txt', 'off_f_KNN500n_SSPFM.0_00094.txt',
        'off_f_KNN500n_SSPFM.0_00075.txt', 'off_f_KNN500n_SSPFM.0_00072.txt',
        'off_f_KNN500n_SSPFM.0_00080.txt', 'off_f_KNN500n_SSPFM.0_00081.txt',
        'off_f_KNN500n_SSPFM.0_00115.txt', 'off_f_KNN500n_SSPFM.0_00082.txt',
        'off_f_KNN500n_SSPFM.0_00083.txt', 'off_f_KNN500n_SSPFM.0_00085.txt',
        'off_f_KNN500n_SSPFM.0_00084.txt', 'off_f_KNN500n_SSPFM.0_00099.txt',
        'off_f_KNN500n_SSPFM.0_00087.txt', 'off_f_KNN500n_SSPFM.0_00086.txt',
        'off_f_KNN500n_SSPFM.0_00088.txt', 'off_f_KNN500n_SSPFM.0_00089.txt',
        'off_f_KNN500n_SSPFM.0_00090.txt', 'off_f_KNN500n_SSPFM.0_00108.txt',
        'off_f_KNN500n_SSPFM.0_00100.txt', 'off_f_KNN500n_SSPFM.0_00091.txt',
        'off_f_KNN500n_SSPFM.0_00104.txt', 'off_f_KNN500n_SSPFM.0_00105.txt',
        'off_f_KNN500n_SSPFM.0_00095.txt', 'off_f_KNN500n_SSPFM.0_00098.txt',
        'off_f_KNN500n_SSPFM.0_00101.txt', 'off_f_KNN500n_SSPFM.0_00076.txt',
        'off_f_KNN500n_SSPFM.0_00092.txt', 'off_f_KNN500n_SSPFM.0_00096.txt',
        'off_f_KNN500n_SSPFM.0_00107.txt', 'off_f_KNN500n_SSPFM.0_00106.txt',
        'off_f_KNN500n_SSPFM.0_00093.txt', 'off_f_KNN500n_SSPFM.0_00097.txt',
        'off_f_KNN500n_SSPFM.0_00110.txt', 'off_f_KNN500n_SSPFM.0_00067.txt',
        'off_f_KNN500n_SSPFM.0_00103.txt', 'off_f_KNN500n_SSPFM.0_00102.txt',
        'off_f_KNN500n_SSPFM.0_00109.txt', 'off_f_KNN500n_SSPFM.0_00111.txt',
        'off_f_KNN500n_SSPFM.0_00112.txt', 'off_f_KNN500n_SSPFM.0_00114.txt',
        'off_f_KNN500n_SSPFM.0_00057.txt', 'off_f_KNN500n_SSPFM.0_00062.txt',
        'off_f_KNN500n_SSPFM.0_00113.txt']
    assert list_file_name == target_f_name
