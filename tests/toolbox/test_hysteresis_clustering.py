"""
Test hysteresis_clustering methods
"""
import sys
from pytest import approx
import numpy as np

from examples.toolbox.ex_hysteresis_clustering import ex_hysteresis_clustering


# class TestReaderAllMaps(unittest.TestCase):


def test_hysteresis_clustering():
    """ Test ex_hysteresis_clustering """

    out = ex_hysteresis_clustering()
    (cluster_indexs, cluster_info, inertia, avg_hysteresis) = out

    # print(np.sum(avg_hysteresis["off"][0]))
    # print(np.sum(avg_hysteresis["off"][1]))
    # print(np.sum(avg_hysteresis["off"][2]))
    # print(np.sum(avg_hysteresis["off"][3]))
    # print(np.sum(avg_hysteresis["off"][4]))
    #
    # print(np.sum(avg_hysteresis["on"][0]))
    # print(np.sum(avg_hysteresis["on"][1]))
    #
    # print(np.sum(avg_hysteresis["coupled"][0]))
    # print(np.sum(avg_hysteresis["coupled"][1]))
    # print(np.sum(avg_hysteresis["coupled"][2]))
    # print(np.sum(avg_hysteresis["coupled"][3]))

    indexs_off = [3, 0, 4, 3, 3, 2, 0, 3, 1, 1, 1, 0, 4, 4, 3, 3, 1, 1, 1, 1,
                  2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                  0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  4, 3, 3]
    indexs_on = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 0, 0, 0]

    # Get Python version
    version_info = sys.version_info
    python_version = f"{version_info.major}.{version_info.minor}"

    # Target adapted depending on Python version
    if python_version in ["3.8", "3.9", "3.10"] or version_info.minor >= 8:
        indexs_coupled = [2, 3, 2, 2, 2, 1, 3, 2, 1, 1, 1, 3, 2, 2, 0, 1, 0,
                          1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1]
        inertia_coupled = 7.441939806296323e-05
        sum_avg_hysteresis_coupled_0 = 0.009878486114671473
        sum_avg_hysteresis_coupled_1 = 0.022249788685527537
        cluster_info_coupled_1_0 = 0.0018836636880818609
        cluster_info_coupled_2_0 = 0.0024577990105899027
        cluster_info_coupled_3_0 = 0.005585684068363985
        cluster_info_coupled_0_3 = 36
        cluster_info_coupled_1_3 = 16

    else:
        indexs_coupled = [2, 3, 2, 2, 2, 1, 3, 2, 1, 1, 1, 3, 2, 2, 0, 1, 0,
                          1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1]
        inertia_coupled = 7.459011731571997e-05
        sum_avg_hysteresis_coupled_0 = 0.009546531839895579
        sum_avg_hysteresis_coupled_1 = 0.021502224252231337
        cluster_info_coupled_1_0 = 0.0018234490228291962
        cluster_info_coupled_2_0 = 0.0024690239940242165
        cluster_info_coupled_3_0 = 0.005547935923473194
        cluster_info_coupled_0_3 = 34
        cluster_info_coupled_1_3 = 18

    assert cluster_indexs["off"] == indexs_off
    assert cluster_indexs["on"] == indexs_on
    assert cluster_indexs["coupled"] == indexs_coupled

    assert inertia["off"] == approx(2.568030435477057e-05)
    assert inertia["on"] == approx(8.946253170285287e-05)
    assert inertia["coupled"] == approx(inertia_coupled)

    assert np.sum(avg_hysteresis["off"][0]) == approx(0.010461290050570967)
    assert np.sum(avg_hysteresis["off"][1]) == approx(0.013119232693312501)
    assert np.sum(avg_hysteresis["off"][2]) == approx(0.032121214212025004)
    assert np.sum(avg_hysteresis["off"][3]) == approx(0.007594395031249999)
    assert np.sum(avg_hysteresis["off"][4]) == approx(-0.005317195847500001)

    assert np.sum(avg_hysteresis["on"][0]) == approx(0.008961507408067797)
    assert np.sum(avg_hysteresis["on"][1]) == approx(0.023619468449999997)

    assert np.sum(avg_hysteresis["coupled"][0]) == approx(
        sum_avg_hysteresis_coupled_0)
    assert np.sum(avg_hysteresis["coupled"][1]) == approx(
        sum_avg_hysteresis_coupled_1)
    assert np.sum(avg_hysteresis["coupled"][2]) == approx(
        -0.0027894943553524987)
    assert np.sum(avg_hysteresis["coupled"][3]) == approx(0.011706520416978458)

    assert cluster_info["off"][0][0] == approx(0.0)
    assert cluster_info["off"][1][0] == approx(0.00144966779086903)
    assert cluster_info["off"][2][0] == approx(0.00253323179361360)
    assert cluster_info["off"][3][0] == approx(0.00267925921785449)
    assert cluster_info["off"][4][0] == approx(0.00295029991414103)

    assert cluster_info["on"][0][0] == approx(0.0)
    assert cluster_info["on"][0][1] == approx(0.00499325920622482)

    assert cluster_info["coupled"][0][0] == approx(0.0)
    assert cluster_info["coupled"][1][0] == approx(cluster_info_coupled_1_0)
    assert cluster_info["coupled"][2][0] == approx(cluster_info_coupled_2_0)
    assert cluster_info["coupled"][3][0] == approx(cluster_info_coupled_3_0)

    assert cluster_info["off"][0][1] == approx(0.001449667790869031)
    assert cluster_info["off"][1][1] == approx(0.0014467444231610026)
    assert cluster_info["off"][2][1] == approx(0.001975983171525822)
    assert cluster_info["off"][3][1] == approx(0.0014467444231610026)
    assert cluster_info["off"][4][1] == approx(0.001541163462540264)

    assert cluster_info["on"][0][1] == approx(0.00499325920622482)
    assert cluster_info["on"][1][1] == approx(0.00499325920622482)

    assert cluster_info["coupled"][0][1] == approx(cluster_info_coupled_1_0)
    assert cluster_info["coupled"][1][1] == approx(cluster_info_coupled_1_0)
    assert cluster_info["coupled"][2][1] == approx(cluster_info_coupled_2_0)
    assert cluster_info["coupled"][3][1] == approx(cluster_info_coupled_3_0)

    assert cluster_info["off"][0][2] == "B"
    assert cluster_info["off"][1][2] == "D"
    assert cluster_info["off"][2][2] == "B"
    assert cluster_info["off"][3][2] == "B"
    assert cluster_info["off"][4][2] == "D"

    assert cluster_info["on"][0][2] == "B"
    assert cluster_info["on"][1][2] == "A"

    assert cluster_info["coupled"][0][2] == "B"
    assert cluster_info["coupled"][1][2] == "A"
    assert cluster_info["coupled"][2][2] == "A"
    assert cluster_info["coupled"][3][2] == "A"

    assert cluster_info["off"][0][3] == 31
    assert cluster_info["off"][1][3] == 16
    assert cluster_info["off"][2][3] == 4
    assert cluster_info["off"][3][3] == 8
    assert cluster_info["off"][4][3] == 4

    assert cluster_info["on"][0][3] == 59
    assert cluster_info["on"][1][3] == 4

    assert cluster_info["coupled"][0][3] == cluster_info_coupled_0_3
    assert cluster_info["coupled"][1][3] == cluster_info_coupled_1_3
    assert cluster_info["coupled"][2][3] == 8
    assert cluster_info["coupled"][3][3] == 3

    assert cluster_info["off"][0][4] == "A"
    assert cluster_info["off"][1][4] == "B"
    assert cluster_info["off"][2][4] == "C"
    assert cluster_info["off"][3][4] == "D"
    assert cluster_info["off"][4][4] == "E"

    assert cluster_info["on"][0][4] == "A"
    assert cluster_info["on"][1][4] == "B"

    assert cluster_info["coupled"][0][4] == "A"
    assert cluster_info["coupled"][1][4] == "B"
    assert cluster_info["coupled"][2][4] == "C"
    assert cluster_info["coupled"][3][4] == "D"
