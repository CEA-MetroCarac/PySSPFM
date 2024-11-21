"""
Test curve_clustering methods
"""
from pytest import approx
import numpy as np

from examples.toolbox.ex_curve_clustering import ex_curve_clustering


# class TestReaderAllMaps(unittest.TestCase):


def test_curve_clustering_piezoresponse():
    """ Test ex_curve_clustering for piezoresponse signal """

    out = ex_curve_clustering(['piezoresponse'])
    (cluster_labels, cluster_info, inertia, _, avg_loop_y) = out

    # print(np.sum(avg_loop_y["off"][0]))
    # print(np.sum(avg_loop_y["off"][1]))
    # print(np.sum(avg_loop_y["off"][2]))
    # print(np.sum(avg_loop_y["off"][3]))
    # print(np.sum(avg_loop_y["off"][4]))
    #
    # print(np.sum(avg_loop_y["on"][0]))
    # print(np.sum(avg_loop_y["on"][1]))
    #
    # print(np.sum(avg_loop_y["coupled"][0]))
    # print(np.sum(avg_loop_y["coupled"][1]))
    # print(np.sum(avg_loop_y["coupled"][2]))
    # print(np.sum(avg_loop_y["coupled"][3]))

    indexs_off = [3, 0, 4, 3, 3, 2, 0, 3, 1, 1, 1, 0, 4, 4, 3, 3, 1, 1, 1, 1,
                  2, 2, 1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0,
                  0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                  4, 3, 3]
    indexs_on = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    indexs_coupled = [2, 3, 2, 2, 2, 1, 3, 2, 2, 1, 1, 3, 1, 1, 1, 1, 0, 1, 1,
                      1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 2, 2, 2]

    assert cluster_labels["off"] == indexs_off
    assert cluster_labels["on"] == indexs_on
    assert cluster_labels["coupled"] == indexs_coupled

    assert inertia["off"] == approx(0.07944603014068753)
    assert inertia["on"] == approx(0.20933604701439257)
    assert inertia["coupled"] == approx(0.08837895012864637)

    assert np.sum(avg_loop_y["off"][0]) == approx(-0.5104468150964516)
    assert np.sum(avg_loop_y["off"][1]) == approx(-0.7751403758642857)
    assert np.sum(avg_loop_y["off"][2]) == approx(-1.960356958566667)
    assert np.sum(avg_loop_y["off"][3]) == approx(-0.434348507375)
    assert np.sum(avg_loop_y["off"][4]) == approx(0.40671776894999995)

    assert np.sum(avg_loop_y["on"][0]) == approx(-0.4599520117610169)
    assert np.sum(avg_loop_y["on"][1]) == approx(-0.434709211)

    assert np.sum(avg_loop_y["coupled"][0]) == approx(0.11498561461787861)
    assert np.sum(avg_loop_y["coupled"][1]) == approx(0.3523831755277777)
    assert np.sum(avg_loop_y["coupled"][2]) == approx(0.1932917787999999)
    assert np.sum(avg_loop_y["coupled"][3]) == approx(-0.15572624143333327)

    assert cluster_info["off"][0][0] == approx(0.0)
    assert cluster_info["off"][1][0] == approx(0.10199510510814183)
    assert cluster_info["off"][2][0] == approx(0.1744854861684967)
    assert cluster_info["off"][3][0] == approx(0.18700892437869035)
    assert cluster_info["off"][4][0] == approx(0.19524655549161038)

    assert cluster_info["off"][0][1] == approx(0.10199510510814183)
    assert cluster_info["off"][1][1] == approx(0.0979474602718143)
    assert cluster_info["off"][2][1] == approx(0.1115691578119643)
    assert cluster_info["off"][3][1] == approx(0.09686425441888476)
    assert cluster_info["off"][4][1] == approx(0.09686425441888476)

    assert cluster_info["off"][0][2] == 'B'
    assert cluster_info["off"][1][2] == 'D'
    assert cluster_info["off"][2][2] == 'B'
    assert cluster_info["off"][3][2] == 'E'
    assert cluster_info["off"][4][2] == 'D'

    assert cluster_info["off"][0][3] == 31
    assert cluster_info["off"][1][3] == 14
    assert cluster_info["off"][2][3] == 6
    assert cluster_info["off"][3][3] == 8
    assert cluster_info["off"][4][3] == 4

    assert cluster_info["off"][0][4] == 'A'
    assert cluster_info["off"][1][4] == 'B'
    assert cluster_info["off"][2][4] == 'C'
    assert cluster_info["off"][3][4] == 'D'
    assert cluster_info["off"][4][4] == 'E'

    assert cluster_info["on"][0][0] == approx(0.0)
    assert cluster_info["on"][1][0] == approx(0.25522712952319054)

    assert cluster_info["on"][0][1] == approx(0.25522712952319054)
    assert cluster_info["on"][1][1] == approx(0.2552271295231906)

    assert cluster_info["on"][0][2] == 'B'
    assert cluster_info["on"][1][2] == 'A'

    assert cluster_info["on"][0][3] == 59
    assert cluster_info["on"][1][3] == 4

    assert cluster_info["on"][0][4] == 'A'
    assert cluster_info["on"][1][4] == 'B'

    assert cluster_info["coupled"][0][0] == approx(0.0)
    assert cluster_info["coupled"][1][0] == approx(0.08393038519587828)
    assert cluster_info["coupled"][2][0] == approx(0.16493083696526195)
    assert cluster_info["coupled"][3][0] == approx(0.3109653160871185)

    assert cluster_info["coupled"][0][1] == approx(0.08393038519587828)
    assert cluster_info["coupled"][1][1] == approx(0.08393038519587828)
    assert cluster_info["coupled"][2][1] == approx(0.08867084657630969)
    assert cluster_info["coupled"][3][1] == approx(0.3109653160871185)

    assert cluster_info["coupled"][0][2] == 'B'
    assert cluster_info["coupled"][1][2] == 'A'
    assert cluster_info["coupled"][2][2] == 'B'
    assert cluster_info["coupled"][3][2] == 'A'

    assert cluster_info["coupled"][0][3] == 33
    assert cluster_info["coupled"][1][3] == 18
    assert cluster_info["coupled"][2][3] == 9
    assert cluster_info["coupled"][3][3] == 3

    assert cluster_info["coupled"][0][4] == 'A'
    assert cluster_info["coupled"][1][4] == 'B'
    assert cluster_info["coupled"][2][4] == 'C'
    assert cluster_info["coupled"][3][4] == 'D'


def test_curve_clustering_amp_pha():
    """ Test ex_curve_clustering for composed amplitude and phase signal """

    out = ex_curve_clustering(['amplitude', 'phase'])
    (cluster_labels, cluster_info, inertia, _, avg_loop_y) = out

    # print(np.sum(avg_loop_y["off"][0]))
    # print(np.sum(avg_loop_y["off"][1]))
    # print(np.sum(avg_loop_y["off"][2]))
    # print(np.sum(avg_loop_y["off"][3]))
    # print(np.sum(avg_loop_y["off"][4]))
    #
    # print(np.sum(avg_loop_y["on"][0]))
    # print(np.sum(avg_loop_y["on"][1]))

    indexs_off = [3, 1, 3, 3, 3, 4, 1, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 4,
                  4, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
                  0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 2, 3, 3, 3]
    indexs_on = [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                 0, 0, 0]

    assert cluster_labels["off"] == indexs_off
    assert cluster_labels["on"] == indexs_on

    assert inertia["off"] == approx(136.77703494076198)
    assert inertia["on"] == approx(85.15271262410181)

    assert np.sum(avg_loop_y["off"][0]) == approx(69.42789538322052)
    assert np.sum(avg_loop_y["off"][1]) == approx(38.50070725713884)
    assert np.sum(avg_loop_y["off"][2]) == approx(101.46061276960461)
    assert np.sum(avg_loop_y["off"][3]) == approx(133.85779308158186)
    assert np.sum(avg_loop_y["off"][4]) == approx(96.90435953411367)

    assert np.sum(avg_loop_y["on"][0]) == approx(112.67682902054267)
    assert np.sum(avg_loop_y["on"][1]) == approx(78.01544593821242)

    assert cluster_info["off"][0][0] == approx(0.0)
    assert cluster_info["off"][1][0] == approx(3.014463673402082)
    assert cluster_info["off"][2][0] == approx(4.225669199992433)
    assert cluster_info["off"][3][0] == approx(7.357720006229469)
    assert cluster_info["off"][4][0] == approx(9.12806848917019)

    assert cluster_info["off"][0][1] == approx(3.014463673402082)
    assert cluster_info["off"][1][1] == approx(3.014463673402082)
    assert cluster_info["off"][2][1] == approx(3.994394100445928)
    assert cluster_info["off"][3][1] == approx(3.994394100445928)
    assert cluster_info["off"][4][1] == approx(6.500727410887572)

    assert cluster_info["off"][0][2] == 'B'
    assert cluster_info["off"][1][2] == 'A'
    assert cluster_info["off"][2][2] == 'D'
    assert cluster_info["off"][3][2] == 'C'
    assert cluster_info["off"][4][2] == 'C'

    assert cluster_info["off"][0][3] == 24
    assert cluster_info["off"][1][3] == 7
    assert cluster_info["off"][2][3] == 16
    assert cluster_info["off"][3][3] == 12
    assert cluster_info["off"][4][3] == 4

    assert cluster_info["off"][0][4] == 'A'
    assert cluster_info["off"][1][4] == 'B'
    assert cluster_info["off"][2][4] == 'C'
    assert cluster_info["off"][3][4] == 'D'
    assert cluster_info["off"][4][4] == 'E'

    assert cluster_info["on"][0][0] == approx(0.0)
    assert cluster_info["on"][1][0] == approx(3.7398958940201763)

    assert cluster_info["on"][0][1] == approx(3.7398958940201763)
    assert cluster_info["on"][1][1] == approx(3.7398958940201763)

    assert cluster_info["on"][0][2] == 'B'
    assert cluster_info["on"][1][2] == 'A'

    assert cluster_info["on"][0][3] == 56
    assert cluster_info["on"][1][3] == 7

    assert cluster_info["on"][0][4] == 'A'
    assert cluster_info["on"][1][4] == 'B'
