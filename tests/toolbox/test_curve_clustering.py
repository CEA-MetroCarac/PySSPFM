"""
Test curve_clustering methods
"""
import sys
from pytest import approx, skip
import numpy as np

from examples.toolbox.ex_curve_clustering import ex_curve_clustering


# class TestReaderAllMaps(unittest.TestCase):


def test_curve_clustering_piezoresponse():
    """ Test ex_curve_clustering for piezoresponse signal """

    if "/home/runner/work" in sys.argv[0]:
        skip("Test skipped for Github source")

    out = ex_curve_clustering(['piezoresponse'])
    (cluster_indexs, cluster_info, inertia, avg_curve) = out

    # print(np.sum(avg_curve["off"][0]))
    # print(np.sum(avg_curve["off"][1]))
    # print(np.sum(avg_curve["off"][2]))
    # print(np.sum(avg_curve["off"][3]))
    # print(np.sum(avg_curve["off"][4]))
    #
    # print(np.sum(avg_curve["on"][0]))
    # print(np.sum(avg_curve["on"][1]))
    #
    # print(np.sum(avg_curve["coupled"][0]))
    # print(np.sum(avg_curve["coupled"][1]))
    # print(np.sum(avg_curve["coupled"][2]))
    # print(np.sum(avg_curve["coupled"][3]))

    indexs_off = [3, 1, 3, 3, 3, 4, 1, 3, 2, 2, 2, 1, 3, 3, 3, 3, 2, 2, 2, 2,
                  4, 4, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                  0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2,
                  3, 3, 3]
    indexs_on = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 0, 0, 0]
    indexs_coupled = [2, 3, 2, 2, 2, 1, 3, 2, 1, 1, 1, 3, 2, 2, 1, 1, 0, 1,
                      1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 2, 2, 1]

    assert cluster_indexs["off"] == indexs_off
    assert cluster_indexs["on"] == indexs_on
    assert cluster_indexs["coupled"] == indexs_coupled

    assert inertia["off"] == approx(0.13523678975557835)
    assert inertia["on"] == approx(0.28663984068106296)
    assert inertia["coupled"] == approx(0.1620727015123082)

    assert np.sum(avg_curve["off"][0]) == approx(-0.5604060286538461)
    assert np.sum(avg_curve["off"][1]) == approx(-0.32359891999833335)
    assert np.sum(avg_curve["off"][2]) == approx(-0.8637471184000002)
    assert np.sum(avg_curve["off"][3]) == approx(-0.15399308193333336)
    assert np.sum(avg_curve["off"][4]) == approx(-2.242400310125)

    assert np.sum(avg_curve["on"][0]) == approx(-0.4599520117610169)
    assert np.sum(avg_curve["on"][1]) == approx(-0.434709211)

    assert np.sum(avg_curve["coupled"][0]) == approx(
        -0.3895835032539335)
    assert np.sum(avg_curve["coupled"][1]) == approx(
        -0.7495477722962939)
    assert np.sum(avg_curve["coupled"][2]) == approx(
        0.2412386496437579)
    assert np.sum(avg_curve["coupled"][3]) == approx(-0.39787115575800425)

    assert cluster_info["off"][0] == [0.0, 0.07695897085508642, 'B', 26, 'A']
    assert cluster_info["off"][1] == [0.07695897085508642, 0.07695897085508642,
                                      'A', 6, 'B']
    assert cluster_info["off"][2] == [0.0991076879668917, 0.09910768796689168,
                                      'A', 15, 'C']
    assert cluster_info["off"][3] == [0.17859580758813837, 0.11473940080561688,
                                      'C', 12, 'D']
    assert cluster_info["off"][4] == [0.1911772239978829, 0.14257219838645985,
                                      'C', 4, 'E']

    assert cluster_info["on"][0] == [0.0, 0.25579396755296596, 'B', 59, 'A']
    assert cluster_info["on"][1] == [0.25579396755296596, 0.25579396755296596,
                                     'A', 4, 'B']

    assert cluster_info["coupled"][0] == \
           [0.0, 0.09424982911577919, 'B', 33, 'A']
    assert cluster_info["coupled"][1] == \
           [0.09424982911577919, 0.09424982911577919, 'A', 18, 'B']
    assert cluster_info["coupled"][2] == \
           [0.169070781895064, 0.12835058633199692, 'B', 9, 'C']
    assert cluster_info["coupled"][3] == \
           [0.31060770971176105, 0.31060770971176105, 'A', 3, 'D']


def test_curve_clustering_amp_pha():
    """ Test ex_curve_clustering for composed amplitude and phase signal """

    if "/home/runner/work" in sys.argv[0]:
        skip("Test skipped for Github source")

    out = ex_curve_clustering(['amplitude', 'phase'])
    (cluster_indexs, cluster_info, inertia, avg_curve) = out

    # print(np.sum(avg_curve["off"][0]))
    # print(np.sum(avg_curve["off"][1]))
    # print(np.sum(avg_curve["off"][2]))
    # print(np.sum(avg_curve["off"][3]))
    # print(np.sum(avg_curve["off"][4]))
    #
    # print(np.sum(avg_curve["on"][0]))
    # print(np.sum(avg_curve["on"][1]))

    indexs_on = [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 0, 0, 0]
    indexs_off = [3, 2, 3, 3, 3, 4, 2, 3, 1, 1, 1, 2, 3, 3, 3, 3, 1, 1, 1, 1,
                  4, 4, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                  0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 3,
                  3, 3, 3]

    assert cluster_indexs["off"] == indexs_off
    assert cluster_indexs["on"] == indexs_on

    assert inertia["off"] == approx(111.13578587730699)
    assert inertia["on"] == approx(91.94596697427032)

    assert np.sum(avg_curve["off"][0]) == approx(67.44480269778579)
    assert np.sum(avg_curve["off"][1]) == approx(85.049189857557)
    assert np.sum(avg_curve["off"][2]) == approx(47.21474992974796)
    assert np.sum(avg_curve["off"][3]) == approx(98.4523948723894)
    assert np.sum(avg_curve["off"][4]) == approx(73.05500191702258)

    assert np.sum(avg_curve["on"][0]) == approx(114.13229998089432)
    assert np.sum(avg_curve["on"][1]) == approx(87.0701917281026)

    assert cluster_info["off"][0] == [0.0, 2.436570085411072, 'B', 26, 'A']
    assert cluster_info["off"][1] == \
           [2.436570085411072, 2.436570085411072, 'A', 14, 'B']
    assert cluster_info["off"][2] == \
           [3.1368359442253464, 3.1368359442253464, 'A', 6, 'C']
    assert cluster_info["off"][3] == \
           [3.8185458951727846, 2.4426456403161194, 'B', 13, 'D']
    assert cluster_info["off"][4] == \
           [4.861100035372178, 3.620470997547831, 'C', 4, 'E']

    assert cluster_info["on"][0] == [0.0, 2.9493831147512637, 'B', 56, 'A']
    assert cluster_info["on"][1] == \
           [2.9493831147512637, 2.9493831147512637, 'A', 7, 'B']
