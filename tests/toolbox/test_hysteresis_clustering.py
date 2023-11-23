"""
Test hysteresis_clustering methods
"""
import sys
from pytest import approx
import numpy as np

from examples.toolbox.ex_hysteresis_clustering import ex_curve_clustering


# class TestReaderAllMaps(unittest.TestCase):


def test_hysteresis_clustering_piezoresponse():
    """ Test ex_curve_clustering for piezoresponse signal """

    out = ex_curve_clustering(['piezoresponse'])
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

    indexs_off = [3, 1, 3, 3, 3, 4, 1, 3, 2, 2, 2, 1, 3, 3, 3, 3, 2, 2, 2,
                  2, 0, 4, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  1, 1, 2, 3, 3, 3]
    indexs_on = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 0, 0, 0]

    # Get Python version
    version_info = sys.version_info
    python_version = f"{version_info.major}.{version_info.minor}"

    # Target adapted depending on Python version
    if python_version in ["3.8", "3.9", "3.10"] or version_info.minor >= 8:
        indexs_coupled = [2, 3, 2, 2, 2, 1, 3, 2, 1, 1, 1, 3, 2, 2, 1, 1, 0, 1,
                          1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 2, 1, 1]
        sum_avg_hysteresis_coupled_0 = 0.009878486114671473
        sum_avg_hysteresis_coupled_1 = 0.022249788685527537
        cluster_info_coupled_1_0 = 0.0018836636880818609
        cluster_info_coupled_2_0 = 0.0024577990105899027
        cluster_info_coupled_3_0 = 0.005585684068363985
        cluster_info_coupled_0_3 = 36
        cluster_info_coupled_1_3 = 16

    else:
        indexs_coupled = [2, 3, 2, 2, 2, 1, 3, 2, 1, 1, 1, 3, 2, 2, 1, 1, 0,
                          1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1]
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

    assert inertia["off"] == approx(0.139395115757726)
    assert inertia["on"] == approx(0.28498500984901537)
    assert inertia["coupled"] == approx(0.1642794418242845)

    assert np.sum(avg_hysteresis["off"][0]) == approx(0.5936781031803703)
    assert np.sum(avg_hysteresis["off"][1]) == approx(0.2831871919714286)
    assert np.sum(avg_hysteresis["off"][2]) == approx(0.8627956580466666)
    assert np.sum(avg_hysteresis["off"][3]) == approx(0.15602010488333334)
    assert np.sum(avg_hysteresis["off"][4]) == approx(2.3118014035)

    assert np.sum(avg_hysteresis["on"][0]) == approx(0.45226276894237294)
    assert np.sum(avg_hysteresis["on"][1]) == approx(0.5239598472500001)

    assert np.sum(avg_hysteresis["coupled"][0]) == approx(
        0.448606402302103)
    assert np.sum(avg_hysteresis["coupled"][1]) == approx(
        0.6988583802447283)
    assert np.sum(avg_hysteresis["coupled"][2]) == approx(
        -0.36790395567739304)
    assert np.sum(avg_hysteresis["coupled"][3]) == approx(0.5236255422617767)

    assert cluster_info["off"][0][0] == approx(0.0)
    assert cluster_info["off"][1][0] == approx(0.07786968990413191)
    assert cluster_info["off"][2][0] == approx(0.09866019954139532)
    assert cluster_info["off"][3][0] == approx(0.1802770711211079)
    assert cluster_info["off"][4][0] == approx(0.2146512578110123)

    assert cluster_info["on"][0][0] == approx(0.0)
    assert cluster_info["on"][0][1] == approx(0.2519488588987771)

    assert cluster_info["coupled"][0][0] == approx(0.0)
    assert cluster_info["coupled"][1][0] == approx(0.09978083565264455)
    assert cluster_info["coupled"][2][0] == approx(0.17830418305190662)
    assert cluster_info["coupled"][3][0] == approx(0.3133612845140547)

    assert cluster_info["off"][0][1] == approx(0.07786968990413191)
    assert cluster_info["off"][1][1] == approx(0.07786968990413191)
    assert cluster_info["off"][2][1] == approx(0.09866019954139532)
    assert cluster_info["off"][3][1] == approx(0.11514522098772867)
    assert cluster_info["off"][4][1] == approx(0.15693006953830294)

    assert cluster_info["on"][0][1] == approx(0.2519488588987771)
    assert cluster_info["on"][1][1] == approx(0.25194885889877716)

    assert cluster_info["coupled"][0][1] == approx(0.09978083565264455)
    assert cluster_info["coupled"][1][1] == approx(0.09978083565264455)
    assert cluster_info["coupled"][2][1] == approx(0.13008345719926323)
    assert cluster_info["coupled"][3][1] == approx(0.3133612845140547)

    assert cluster_info["off"][0][2] == "B"
    assert cluster_info["off"][1][2] == "A"
    assert cluster_info["off"][2][2] == "A"
    assert cluster_info["off"][3][2] == "C"
    assert cluster_info["off"][4][2] == "C"

    assert cluster_info["on"][0][2] == "B"
    assert cluster_info["on"][1][2] == "A"

    assert cluster_info["coupled"][0][2] == "B"
    assert cluster_info["coupled"][1][2] == "A"
    assert cluster_info["coupled"][2][2] == "B"
    assert cluster_info["coupled"][3][2] == "A"

    assert cluster_info["off"][0][3] == 27
    assert cluster_info["off"][1][3] == 7
    assert cluster_info["off"][2][3] == 15
    assert cluster_info["off"][3][3] == 12
    assert cluster_info["off"][4][3] == 2

    assert cluster_info["on"][0][3] == 59
    assert cluster_info["on"][1][3] == 4

    assert cluster_info["coupled"][0][3] == 34
    assert cluster_info["coupled"][1][3] == 18
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


def test_hysteresis_clustering_amp_pha():
    """ Test ex_curve_clustering for composed amplitude and phase
    signal """

    out = ex_curve_clustering(['amplitude', 'phase'])
    (cluster_indexs, cluster_info, inertia, avg_hysteresis) = out

    # print(np.sum(avg_hysteresis["off"][0]))
    # print(np.sum(avg_hysteresis["off"][1]))
    # print(np.sum(avg_hysteresis["off"][2]))
    # print(np.sum(avg_hysteresis["off"][3]))
    # print(np.sum(avg_hysteresis["off"][4]))
    #
    # print(np.sum(avg_hysteresis["on"][0]))
    # print(np.sum(avg_hysteresis["on"][1]))

    indexs_on = [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 0, 0, 0]

    # Get Python version
    version_info = sys.version_info
    python_version = f"{version_info.major}.{version_info.minor}"

    # Target adapted depending on Python version
    if python_version in ["3.8", "3.9", "3.10"] or version_info.minor >= 8:
        indexs_off = [3, 1, 3, 3, 3, 4, 1, 3, 3, 3, 2, 1, 3, 3, 3, 3, 3, 2, 2,
                      2, 4, 4, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                      1, 1, 3, 3, 3, 3]
        inertia_off = 96.59258253235751
        avg_hysteresis_off_1 = 69.47246188061166
        avg_hysteresis_off_2 = 83.07405484256466
        avg_hysteresis_off_3 = 91.95712529778717
        cluster_info_off_1_0 = 2.1301929582074703
        cluster_info_off_2_0 = 2.1743304237987306
        cluster_info_off_3_0 = 3.342860315025872
    else:
        indexs_off = [3, 1, 3, 3, 3, 4, 1, 3, 2, 2, 2, 1, 3, 3, 3, 3, 2, 2, 2,
                      2, 4, 4, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                      1, 1, 3, 3, 3, 3]
        inertia_off = 94.9635356607568
        avg_hysteresis_off_1 = 72.50786208611287
        avg_hysteresis_off_2 = 82.10108346249717
        avg_hysteresis_off_3 = 94.46671008317617
        cluster_info_off_1_0 = 2.1113160018913417
        cluster_info_off_2_0 = 2.254872025351866
        cluster_info_off_3_0 = 3.5300633820041
    assert cluster_indexs["off"] == indexs_off
    assert cluster_indexs["on"] == indexs_on

    assert inertia["off"] == approx(inertia_off)
    assert inertia["on"] == approx(85.9572013452021)

    assert np.sum(avg_hysteresis["off"][0]) == approx(66.12804145794577)
    assert np.sum(avg_hysteresis["off"][1]) == approx(avg_hysteresis_off_1)
    assert np.sum(avg_hysteresis["off"][2]) == approx(avg_hysteresis_off_2)
    assert np.sum(avg_hysteresis["off"][3]) == approx(avg_hysteresis_off_3)
    assert np.sum(avg_hysteresis["off"][4]) == approx(72.96209700766119)

    assert np.sum(avg_hysteresis["on"][0]) == approx(108.58805972420119)
    assert np.sum(avg_hysteresis["on"][1]) == approx(86.93195273947686)

    assert cluster_info["off"][0][0] == approx(0.0)
    assert cluster_info["off"][1][0] == approx(cluster_info_off_1_0)
    assert cluster_info["off"][2][0] == approx(cluster_info_off_2_0)
    assert cluster_info["off"][3][0] == approx(cluster_info_off_3_0)
    assert cluster_info["off"][4][0] == approx(5.1303263806638535)

    assert cluster_info["on"][0][0] == approx(0.0)
    assert cluster_info["on"][0][1] == approx(2.732333357603488)

    assert cluster_info["off"][0][1] == approx(cluster_info_off_1_0)
    assert cluster_info["off"][1][1] == approx(cluster_info_off_1_0)
    assert cluster_info["off"][2][1] == approx(cluster_info_off_2_0)
    assert cluster_info["off"][3][1] == approx(2.29989794039676)
    assert cluster_info["off"][4][1] == approx(4.18485558614015)

    assert cluster_info["on"][0][1] == approx(2.732333357603488)
    assert cluster_info["on"][1][1] == approx(2.732333357603488)

    assert cluster_info["off"][0][2] == "B"
    assert cluster_info["off"][1][2] == "A"
    assert cluster_info["off"][2][2] == "A"
    assert cluster_info["off"][3][2] == "C"
    assert cluster_info["off"][4][2] == "C"

    assert cluster_info["on"][0][2] == "B"
    assert cluster_info["on"][1][2] == "A"

    assert cluster_info["off"][0][3] == 26
    assert cluster_info["off"][1][3] == 6
    assert cluster_info["off"][2][3] == 12
    assert cluster_info["off"][3][3] == 16
    assert cluster_info["off"][4][3] == 3

    assert cluster_info["on"][0][3] == 56
    assert cluster_info["on"][1][3] == 7

    assert cluster_info["off"][0][4] == "A"
    assert cluster_info["off"][1][4] == "B"
    assert cluster_info["off"][2][4] == "C"
    assert cluster_info["off"][3][4] == "D"
    assert cluster_info["off"][4][4] == "E"

    assert cluster_info["on"][0][4] == "A"
    assert cluster_info["on"][1][4] == "B"
