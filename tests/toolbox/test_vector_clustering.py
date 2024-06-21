"""
Test vector_clustering methods
"""
import os
from pytest import approx, skip
import numpy as np

from examples.toolbox.ex_vector_clustering import ex_vector_clustering


# class TestReaderAllMaps(unittest.TestCase):


def test_vector_clustering_piezoresponse():
    """ Test ex_vector_clustering for piezoresponse signal """
    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    out = ex_vector_clustering(['piezoresponse'], obj="loop")
    (cluster_indexs, cluster_info, inertia, avg_loop) = out

    # print(np.sum(avg_loop["off"][0]))
    # print(np.sum(avg_loop["off"][1]))
    # print(np.sum(avg_loop["off"][2]))
    # print(np.sum(avg_loop["off"][3]))
    # print(np.sum(avg_loop["off"][4]))
    #
    # print(np.sum(avg_loop["on"][0]))
    # print(np.sum(avg_loop["on"][1]))
    #
    # print(np.sum(avg_loop["coupled"][0]))
    # print(np.sum(avg_loop["coupled"][1]))
    # print(np.sum(avg_loop["coupled"][2]))
    # print(np.sum(avg_loop["coupled"][3]))

    indexs_off = [3, 0, 4, 3, 3, 2, 0, 3, 1, 1, 1, 0, 4, 4, 3, 3, 1, 1, 1, 1,
                  2, 2, 1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                  0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  4, 3, 3]
    indexs_on = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    indexs_coupled = [2, 3, 2, 2, 2, 1, 3, 2, 1, 1, 1, 3, 2, 2, 1, 1, 0, 1, 1,
                      1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 2, 2, 1]

    assert cluster_indexs["off"] == indexs_off
    assert cluster_indexs["on"] == indexs_on
    assert cluster_indexs["coupled"] == indexs_coupled

    assert inertia["off"] == approx(0.07944603014068753)
    assert inertia["on"] == approx(0.20933604701439257)
    assert inertia["coupled"] == approx(0.12461733324715078)

    assert np.sum(avg_loop["off"][0]) == approx(-0.5104468150964516)
    assert np.sum(avg_loop["off"][1]) == approx(-0.7751403758642857)
    assert np.sum(avg_loop["off"][2]) == approx(-1.960356958566667)
    assert np.sum(avg_loop["off"][3]) == approx(-0.434348507375)
    assert np.sum(avg_loop["off"][4]) == approx(0.40671776894999995)

    assert np.sum(avg_loop["on"][0]) == approx(-0.4599520117610169)
    assert np.sum(avg_loop["on"][1]) == approx(-0.434709211)

    assert np.sum(avg_loop["coupled"][0]) == approx(
        -0.3895835032539335)
    assert np.sum(avg_loop["coupled"][1]) == approx(
        -0.7495477722962939)
    assert np.sum(avg_loop["coupled"][2]) == approx(
        0.2412386496437579)
    assert np.sum(avg_loop["coupled"][3]) == approx(-0.39787115575800425)

    assert cluster_info["off"][0] == [0.0, 0.10199510510814183, 'B', 31, 'A']
    assert cluster_info["off"][1] == [0.10199510510814183, 0.0979474602718143,
                                      'D', 14, 'B']
    assert cluster_info["off"][2] == [0.1744854861684967, 0.1115691578119643,
                                      'B', 6, 'C']
    assert cluster_info["off"][3] == [0.18700892437869035, 0.09686425441888476,
                                      'E', 8, 'D']
    assert cluster_info["off"][4] == [0.19524655549161038, 0.09686425441888476,
                                      'D', 4, 'E']

    assert cluster_info["on"][0] == [0.0, 0.25522712952319054, 'B', 59, 'A']
    assert cluster_info["on"][1] == [0.25522712952319054, 0.2552271295231906,
                                     'A', 4, 'B']

    assert cluster_info["coupled"][0] == \
           [0.0, 0.09374627577813542, 'B', 33, 'A']
    assert cluster_info["coupled"][1] == \
           [0.09374627577813542, 0.09374627577813542, 'A', 18, 'B']
    assert cluster_info["coupled"][2] == \
           [0.16829697669276944, 0.12730871304229927, 'B', 9, 'C']
    assert cluster_info["coupled"][3] == \
           [0.30994264125565674, 0.30994264125565674, 'A', 3, 'D']


def test_vector_clustering_amp_pha():
    """ Test ex_vector_clustering for composed amplitude and phase signal """
    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    out = ex_vector_clustering(['amplitude', 'phase'], obj="loop")
    (cluster_indexs, cluster_info, inertia, avg_loop) = out

    # print(np.sum(avg_loop["off"][0]))
    # print(np.sum(avg_loop["off"][1]))
    # print(np.sum(avg_loop["off"][2]))
    # print(np.sum(avg_loop["off"][3]))
    # print(np.sum(avg_loop["off"][4]))
    #
    # print(np.sum(avg_loop["on"][0]))
    # print(np.sum(avg_loop["on"][1]))

    indexs_on = [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    indexs_off = [3, 2, 3, 3, 3, 4, 2, 3, 1, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 4,
                  4, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                  0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 3, 3, 3]

    assert cluster_indexs["off"] == indexs_off
    assert cluster_indexs["on"] == indexs_on

    assert inertia["off"] == approx(37.046512297968675)
    assert inertia["on"] == approx(52.78743233875454)

    assert np.sum(avg_loop["off"][0]) == approx(67.44480269778579)
    assert np.sum(avg_loop["off"][1]) == approx(83.28619025405112)
    assert np.sum(avg_loop["off"][2]) == approx(47.753035968129524)
    assert np.sum(avg_loop["off"][3]) == approx(100.03013797603236)
    assert np.sum(avg_loop["off"][4]) == approx(75.53979433581819)

    assert np.sum(avg_loop["on"][0]) == approx(114.13229998089432)
    assert np.sum(avg_loop["on"][1]) == approx(87.0701917281026)

    assert cluster_info["off"][0] == [0.0, 2.1945485242366165, 'B', 26, 'A']
    assert cluster_info["off"][1] == \
           [2.1945485242366165, 1.8090346760270957, 'D', 16, 'B']
    assert cluster_info["off"][2] == \
           [2.999787031831033, 2.9493885053482956, 'E', 6, 'C']
    assert cluster_info["off"][3] == \
           [3.81719275583201, 1.8090346760270957, 'B', 12, 'D']
    assert cluster_info["off"][4] == \
           [5.1760152336319445, 2.9493885053482956, 'C', 3, 'E']

    assert cluster_info["on"][0] == [0.0, 2.919513243246092, 'B', 56, 'A']
    assert cluster_info["on"][1] == \
           [2.919513243246092, 2.919513243246092, 'A', 7, 'B']


def test_vector_clustering_deflection():
    """ Test ex_vector_clustering for deflection signal """
    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    out = ex_vector_clustering(['deflection'], obj="curve")
    (cluster_indexs, cluster_info, inertia, avg_curve) = out

    # print(np.sum(avg_curve[0]))
    # print(np.sum(avg_curve[1]))
    # print(np.sum(avg_curve[2]))
    # print(np.sum(avg_curve[3]))

    target_cluster_indexs = [0, 0, 3, 3, 3, 3, 3, 2, 3, 2, 0, 2, 0, 0, 2, 2, 2,
                             1, 0, 1, 0]

    assert cluster_indexs == target_cluster_indexs

    assert inertia == approx(37851.39880850841, rel=1e-4)

    assert np.sum(avg_curve[0]) == approx(3652365.240777172)
    assert np.sum(avg_curve[1]) == approx(3693454.1290251208)
    assert np.sum(avg_curve[2]) == approx(3667616.1327542383)
    assert np.sum(avg_curve[3]) == approx(3629540.754739646)

    assert cluster_info[0][0] == 0.0
    assert cluster_info[0][1] == approx(105.39005326640408, rel=1e-4)
    assert cluster_info[0][2] == 'B'
    assert cluster_info[0][3] == 7
    assert cluster_info[0][4] == 'A'

    assert cluster_info[1][0] == approx(105.39005326640408, rel=1e-2)
    assert cluster_info[1][1] == approx(105.39005326640408, rel=1e-2)
    assert cluster_info[1][2] == 'A'
    assert cluster_info[1][3] == 2
    assert cluster_info[1][4] == 'B'

    assert cluster_info[2][0] == approx(105.39005326640408, rel=1e-2)
    assert cluster_info[2][1] == approx(105.39005326640408, rel=1e-2)
    assert cluster_info[2][2] == 'A'
    assert cluster_info[2][3] == 6
    assert cluster_info[2][4] == 'C'

    assert cluster_info[3][0] == approx(157.23309961426625, rel=1e-2)
    assert cluster_info[3][1] == approx(121.64658315141517, rel=1e-2)
    assert cluster_info[3][2] == 'C'
    assert cluster_info[3][3] == 6
    assert cluster_info[3][4] == 'D'


def test_vector_clustering_height_deflection():
    """ Test ex_vector_clustering for composed height and deflection signal """
    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    out = ex_vector_clustering(['deflection', 'height'], obj="curve")
    (cluster_indexs, cluster_info, inertia, avg_curve) = out

    # print(np.sum(avg_curve[0]))
    # print(np.sum(avg_curve[1]))
    # print(np.sum(avg_curve[2]))
    # print(np.sum(avg_curve[3]))

    target_cluster_indexs = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2,
                             2, 3, 3, 3, 3]

    assert cluster_indexs == target_cluster_indexs

    assert inertia == approx(21.350689661725266)

    assert np.sum(avg_curve[0]) == approx(388222.0719091058)
    assert np.sum(avg_curve[1]) == approx(389860.61779852805)
    assert np.sum(avg_curve[2]) == approx(391220.4847004337)
    assert np.sum(avg_curve[3]) == approx(392565.2548910277)

    assert cluster_info[0][0] == 0.0
    assert cluster_info[0][1] == approx(3.247625541131953, rel=1e-4)
    assert cluster_info[0][2] == 'B'
    assert cluster_info[0][3] == 7
    assert cluster_info[0][4] == 'A'

    assert cluster_info[1][0] == approx(3.247625541131953, rel=1e-4)
    assert cluster_info[1][1] == approx(2.763943758791085, rel=1e-4)
    assert cluster_info[1][2] == 'C'
    assert cluster_info[1][3] == 5
    assert cluster_info[1][4] == 'B'

    assert cluster_info[2][0] == approx(6.003733891088774, rel=1e-4)
    assert cluster_info[2][1] == approx(2.763943758791085, rel=1e-4)
    assert cluster_info[2][2] == 'B'
    assert cluster_info[2][3] == 5
    assert cluster_info[2][4] == 'C'

    assert cluster_info[3][0] == approx(8.86417185900724, rel=1e-4)
    assert cluster_info[3][1] == approx(2.91898743477631, rel=1e-4)
    assert cluster_info[3][2] == 'C'
    assert cluster_info[3][3] == 4
    assert cluster_info[3][4] == 'D'
