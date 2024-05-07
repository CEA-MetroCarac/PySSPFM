"""
Test curve_clustering methods
"""
import os
from pytest import approx, skip
import numpy as np

from examples.toolbox.ex_curve_clustering import ex_curve_clustering


# class TestReaderAllMaps(unittest.TestCase):


def test_curve_clustering_deflection():
    """ Test ex_curve_clustering for deflection signal """
    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    out = ex_curve_clustering(['deflection'])
    (cluster_indexs, cluster_info, inertia, avg_curve) = out

    # print(np.sum(avg_curve[0]))
    # print(np.sum(avg_curve[1]))
    # print(np.sum(avg_curve[2]))

    target_cluster_indexs = [1, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             1, 1, 1, 0]

    assert cluster_indexs == target_cluster_indexs

    assert inertia == approx(354140.1914109529)

    assert np.sum(avg_curve[0]) == approx(3659427.028688297)
    assert np.sum(avg_curve[1]) == approx(3669009.191778517)
    assert np.sum(avg_curve[2]) == approx(3629449.0314160236)

    assert cluster_info[0] == [0.0, 146.99328263341397, 'B', 12, 'A']
    assert cluster_info[1] == [146.99328263341397, 146.99328263341397, 'A', 4,
                               'B']
    assert cluster_info[2] == [147.71545254648586, 147.71545254648586, 'A', 5,
                               'C']


def test_curve_clustering_height_deflection():
    """ Test ex_curve_clustering for composed height and deflection signal """
    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    out = ex_curve_clustering(['deflection', 'height'])
    (cluster_indexs, cluster_info, inertia, avg_curve) = out

    # print(np.sum(avg_curve[0]))
    # print(np.sum(avg_curve[1]))
    # print(np.sum(avg_curve[2]))

    target_cluster_indexs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2,
                             2, 2, 2, 2]

    assert cluster_indexs == target_cluster_indexs

    assert inertia == approx(76.06496724200191)

    assert np.sum(avg_curve[0]) == approx(388455.9994825708)
    assert np.sum(avg_curve[1]) == approx(390740.1297729185)
    assert np.sum(avg_curve[2]) == approx(392387.2263338187)

    assert cluster_info[0] == [0.0, 4.517480463827678, 'B', 9, 'A']
    assert cluster_info[1] == [4.517480463827678, 3.684231929402842, 'C', 7,
                               'B']
    assert cluster_info[2] == [8.006028411446396, 3.684231929402842, 'B', 5,
                               'C']
