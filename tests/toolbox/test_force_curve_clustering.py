"""
Test force_curve_clustering methods
"""
import os
from pytest import approx, skip
import numpy as np

from examples.toolbox.ex_force_curve_clustering import ex_force_curve_clustering


# class TestReaderAllMaps(unittest.TestCase):


def test_force_curve_clustering():
    """ Test ex_force_curve_clustering """
    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    out = ex_force_curve_clustering()
    (cluster_labels, cluster_info, inertia, _, y_avg,
     tab_other_properties) = out

    # print(np.sum(y_avg[0]))
    # print(np.sum(y_avg[1]))
    # print(np.sum(y_avg[2]))

    sum_dict = {key: np.sum([elem[key] for elem in tab_other_properties]) for
                key in tab_other_properties[0].keys()}

    indexs = [2, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0]

    assert cluster_labels == indexs

    assert inertia == approx(24.923362481879337)

    assert np.sum(y_avg[0]) == approx(11550293.277229719)
    assert np.sum(y_avg[1]) == approx(11553785.698724665)
    assert np.sum(y_avg[2]) == approx(11552898.75019331)

    assert cluster_info[0][0] == approx(0.0)
    assert cluster_info[1][0] == approx(1.7723394378480912)
    assert cluster_info[2][0] == approx(6.12878519392628)

    assert cluster_info[0][1] == approx(1.7723394378480912)
    assert cluster_info[1][1] == approx(1.7723394378480912)
    assert cluster_info[2][1] == approx(6.12878519392628)

    assert cluster_info[0][2] == 'B'
    assert cluster_info[1][2] == 'A'
    assert cluster_info[2][2] == 'A'

    assert cluster_info[0][3] == 12
    assert cluster_info[1][3] == 8
    assert cluster_info[2][3] == 1

    assert cluster_info[0][4] == 'A'
    assert cluster_info[1][4] == 'B'
    assert cluster_info[2][4] == 'C'

    assert sum_dict['height'] == approx(11094.942759414136)
    assert sum_dict['deflection'] == approx(413.25535651235157)
    assert sum_dict['deflection error'] == approx(5.9098166617518375)
    assert sum_dict['adhesion approach'] == approx(340.724254008648)
    assert sum_dict['adhesion retract'] == approx(1282.700241308925)
