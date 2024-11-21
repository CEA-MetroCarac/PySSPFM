"""
Test clustering_inertia methods
"""
import os
from pytest import approx, skip
import numpy as np

from examples.toolbox.ex_clustering_inertia import ex_clustering_inertia


# class TestReaderAllMaps(unittest.TestCase):


def test_clustering_inertia():
    """ Test ex_clustering_inertia for piezoresponse signal """

    if os.getenv('GITHUB_ACTIONS') == 'true':
        skip("Test skipped for Github source")

    dict_inertia = ex_clustering_inertia()

    # print(np.sum(dict_inertia["off"]))
    # print(np.sum(dict_inertia["on"]))
    # print(np.sum(dict_inertia["coupled"]))

    assert np.sum(dict_inertia["off"]) == approx(0.8478612784374686)
    assert np.sum(dict_inertia["on"]) == approx(0.7012273122813835)
    assert np.sum(dict_inertia["coupled"]) == approx(0.777708823169472)
