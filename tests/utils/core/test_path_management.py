"""
Test path management methods
"""
import os
from pytest import approx

from examples.utils.core.ex_path_management import \
    ex_get_files_with_conditions, ex_filename_management


def test_get_files_with_conditions():
    """ Test ex_get_files_with_conditions """

    filepaths_sspfm = ex_get_files_with_conditions()
    filenames = [os.path.split(filepath_sspfm)[1]
                 for filepath_sspfm in filepaths_sspfm]
    target_filenames = \
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

    assert filenames == target_filenames


def test_filename_management():
    """ Test ex_filename_management """

    out = ex_filename_management()
    (filenames_sspfm, sorted_filenames, sorted_indexs, filename_root,
     bruker_filenames) = out

    target_filenames_sspfm = \
        ['SSPFM_map1_32pix_29_PZT.spm', 'SSPFM_map1_32pix_38_PZT.spm',
         'SSPFM_map1_32pix_42_PZT.spm', 'SSPFM_map1_32pix_35_PZT.spm',
         'SSPFM_map1_32pix_20_PZT.spm', 'SSPFM_map1_32pix_43_PZT.spm',
         'SSPFM_map1_32pix_44_PZT.spm', 'SSPFM_map1_32pix_34_PZT.spm',
         'SSPFM_map1_32pix_28_PZT.spm', 'SSPFM_map1_32pix_50_PZT.spm',
         'SSPFM_map1_32pix_47_PZT.spm', 'SSPFM_map1_32pix_41_PZT.spm',
         'SSPFM_map1_32pix_33_PZT.spm', 'SSPFM_map1_32pix_26_PZT.spm',
         'SSPFM_map1_32pix_31_PZT.spm', 'SSPFM_map1_32pix_48_PZT.spm',
         'SSPFM_map1_32pix_23_PZT.spm', 'SSPFM_map1_32pix_32_PZT.spm',
         'SSPFM_map1_32pix_46_PZT.spm', 'SSPFM_map1_32pix_40_PZT.spm',
         'SSPFM_map1_32pix_19_PZT.spm', 'SSPFM_map1_32pix_30_PZT.spm',
         'SSPFM_map1_32pix_24_PZT.spm', 'SSPFM_map1_32pix_22_PZT.spm',
         'SSPFM_map1_32pix_36_PZT.spm', 'SSPFM_map1_32pix_39_PZT.spm',
         'SSPFM_map1_32pix_37_PZT.spm', 'SSPFM_map1_32pix_27_PZT.spm',
         'SSPFM_map1_32pix_25_PZT.spm', 'SSPFM_map1_32pix_49_PZT.spm',
         'SSPFM_map1_32pix_45_PZT.spm', 'SSPFM_map1_32pix_21_PZT.spm',
         'SSPFM_map1_32pix_18_PZT.spm']

    target_sorted_filenames = \
        ['SSPFM_map1_32pix_18_PZT.spm', 'SSPFM_map1_32pix_19_PZT.spm',
         'SSPFM_map1_32pix_20_PZT.spm', 'SSPFM_map1_32pix_21_PZT.spm',
         'SSPFM_map1_32pix_22_PZT.spm', 'SSPFM_map1_32pix_23_PZT.spm',
         'SSPFM_map1_32pix_24_PZT.spm', 'SSPFM_map1_32pix_25_PZT.spm',
         'SSPFM_map1_32pix_26_PZT.spm', 'SSPFM_map1_32pix_27_PZT.spm',
         'SSPFM_map1_32pix_28_PZT.spm', 'SSPFM_map1_32pix_29_PZT.spm',
         'SSPFM_map1_32pix_30_PZT.spm', 'SSPFM_map1_32pix_31_PZT.spm',
         'SSPFM_map1_32pix_32_PZT.spm', 'SSPFM_map1_32pix_33_PZT.spm',
         'SSPFM_map1_32pix_34_PZT.spm', 'SSPFM_map1_32pix_35_PZT.spm',
         'SSPFM_map1_32pix_36_PZT.spm', 'SSPFM_map1_32pix_37_PZT.spm',
         'SSPFM_map1_32pix_38_PZT.spm', 'SSPFM_map1_32pix_39_PZT.spm',
         'SSPFM_map1_32pix_40_PZT.spm', 'SSPFM_map1_32pix_41_PZT.spm',
         'SSPFM_map1_32pix_42_PZT.spm', 'SSPFM_map1_32pix_43_PZT.spm',
         'SSPFM_map1_32pix_44_PZT.spm', 'SSPFM_map1_32pix_45_PZT.spm',
         'SSPFM_map1_32pix_46_PZT.spm', 'SSPFM_map1_32pix_47_PZT.spm',
         'SSPFM_map1_32pix_48_PZT.spm', 'SSPFM_map1_32pix_49_PZT.spm',
         'SSPFM_map1_32pix_50_PZT.spm']

    target_sorted_indexs = [
        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
        36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

    target_bruker_filenames = [
        'SSPFM_map1_32pix_PZT.0_00018.spm', 'SSPFM_map1_32pix_PZT.0_00019.spm',
        'SSPFM_map1_32pix_PZT.0_00020.spm', 'SSPFM_map1_32pix_PZT.0_00021.spm',
        'SSPFM_map1_32pix_PZT.0_00022.spm', 'SSPFM_map1_32pix_PZT.0_00023.spm',
        'SSPFM_map1_32pix_PZT.0_00024.spm', 'SSPFM_map1_32pix_PZT.0_00025.spm',
        'SSPFM_map1_32pix_PZT.0_00026.spm', 'SSPFM_map1_32pix_PZT.0_00027.spm',
        'SSPFM_map1_32pix_PZT.0_00028.spm', 'SSPFM_map1_32pix_PZT.0_00029.spm',
        'SSPFM_map1_32pix_PZT.0_00030.spm', 'SSPFM_map1_32pix_PZT.0_00031.spm',
        'SSPFM_map1_32pix_PZT.0_00032.spm', 'SSPFM_map1_32pix_PZT.0_00033.spm',
        'SSPFM_map1_32pix_PZT.0_00034.spm', 'SSPFM_map1_32pix_PZT.0_00035.spm',
        'SSPFM_map1_32pix_PZT.0_00036.spm', 'SSPFM_map1_32pix_PZT.0_00037.spm',
        'SSPFM_map1_32pix_PZT.0_00038.spm', 'SSPFM_map1_32pix_PZT.0_00039.spm',
        'SSPFM_map1_32pix_PZT.0_00040.spm', 'SSPFM_map1_32pix_PZT.0_00041.spm',
        'SSPFM_map1_32pix_PZT.0_00042.spm', 'SSPFM_map1_32pix_PZT.0_00043.spm',
        'SSPFM_map1_32pix_PZT.0_00044.spm', 'SSPFM_map1_32pix_PZT.0_00045.spm',
        'SSPFM_map1_32pix_PZT.0_00046.spm', 'SSPFM_map1_32pix_PZT.0_00047.spm',
        'SSPFM_map1_32pix_PZT.0_00048.spm', 'SSPFM_map1_32pix_PZT.0_00049.spm',
        'SSPFM_map1_32pix_PZT.0_00050.spm']

    assert filenames_sspfm == target_filenames_sspfm
    assert sorted_filenames == target_sorted_filenames
    assert sorted_indexs == target_sorted_indexs
    assert filename_root == 'SSPFM_map1_32pix__PZT.spm'
    assert bruker_filenames == target_bruker_filenames
