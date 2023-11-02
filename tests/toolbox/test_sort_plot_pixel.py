"""
Test sort_plot_pixel methods
"""
import os

from examples.toolbox.ex_sort_plot_pixel import example_sort_plot_pixel


# class TestPlotExtremum(unittest.TestCase):


def test_sort_plot_pixel():
    """ Test example_sort_plot_pixel """

    list_file_path = example_sort_plot_pixel()
    list_file_name = [os.path.split(file_path)[1]
                      for file_path in list_file_path]
    target_f_name = ['KNN500n_SSPFM.0_00058.spm', 'KNN500n_SSPFM.0_00060.spm',
                     'KNN500n_SSPFM.0_00059.spm', 'KNN500n_SSPFM.0_00063.spm',
                     'KNN500n_SSPFM.0_00117.spm', 'KNN500n_SSPFM.0_00056.spm',
                     'KNN500n_SSPFM.0_00118.spm', 'KNN500n_SSPFM.0_00116.spm',
                     'KNN500n_SSPFM.0_00061.spm', 'KNN500n_SSPFM.0_00071.spm',
                     'KNN500n_SSPFM.0_00064.spm', 'KNN500n_SSPFM.0_00070.spm',
                     'KNN500n_SSPFM.0_00069.spm', 'KNN500n_SSPFM.0_00065.spm',
                     'KNN500n_SSPFM.0_00074.spm', 'KNN500n_SSPFM.0_00077.spm',
                     'KNN500n_SSPFM.0_00073.spm', 'KNN500n_SSPFM.0_00068.spm',
                     'KNN500n_SSPFM.0_00066.spm', 'KNN500n_SSPFM.0_00078.spm',
                     'KNN500n_SSPFM.0_00079.spm', 'KNN500n_SSPFM.0_00094.spm',
                     'KNN500n_SSPFM.0_00075.spm', 'KNN500n_SSPFM.0_00072.spm',
                     'KNN500n_SSPFM.0_00080.spm', 'KNN500n_SSPFM.0_00081.spm',
                     'KNN500n_SSPFM.0_00115.spm', 'KNN500n_SSPFM.0_00082.spm',
                     'KNN500n_SSPFM.0_00083.spm', 'KNN500n_SSPFM.0_00085.spm',
                     'KNN500n_SSPFM.0_00084.spm', 'KNN500n_SSPFM.0_00087.spm',
                     'KNN500n_SSPFM.0_00086.spm', 'KNN500n_SSPFM.0_00088.spm',
                     'KNN500n_SSPFM.0_00089.spm', 'KNN500n_SSPFM.0_00090.spm',
                     'KNN500n_SSPFM.0_00108.spm', 'KNN500n_SSPFM.0_00100.spm',
                     'KNN500n_SSPFM.0_00091.spm', 'KNN500n_SSPFM.0_00104.spm',
                     'KNN500n_SSPFM.0_00105.spm', 'KNN500n_SSPFM.0_00095.spm',
                     'KNN500n_SSPFM.0_00098.spm', 'KNN500n_SSPFM.0_00101.spm',
                     'KNN500n_SSPFM.0_00092.spm', 'KNN500n_SSPFM.0_00096.spm',
                     'KNN500n_SSPFM.0_00107.spm', 'KNN500n_SSPFM.0_00093.spm',
                     'KNN500n_SSPFM.0_00106.spm', 'KNN500n_SSPFM.0_00097.spm',
                     'KNN500n_SSPFM.0_00110.spm', 'KNN500n_SSPFM.0_00067.spm',
                     'KNN500n_SSPFM.0_00103.spm', 'KNN500n_SSPFM.0_00102.spm',
                     'KNN500n_SSPFM.0_00109.spm', 'KNN500n_SSPFM.0_00111.spm',
                     'KNN500n_SSPFM.0_00112.spm', 'KNN500n_SSPFM.0_00076.spm',
                     'KNN500n_SSPFM.0_00114.spm', 'KNN500n_SSPFM.0_00099.spm',
                     'KNN500n_SSPFM.0_00113.spm', 'KNN500n_SSPFM.0_00062.spm',
                     'KNN500n_SSPFM.0_00057.spm']
    assert list_file_name == target_f_name
