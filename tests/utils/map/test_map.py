"""
Test map methods
"""
import numpy as np

from examples.utils.map.ex_map import example_map


# class TestMap(unittest.TestCase):


def test_map_auto():
    """ Test example_map: mask_mode='ref prop: auto' """

    mask = example_map(mask_mode='ref prop: auto')

    # print(np.sum(mask))

    assert np.sum(mask) == 154


def test_map_mask():
    """ Test example_map: mask_mode='man mask' """

    mask = example_map(mask_mode='man mask')

    # print(np.sum(mask))

    assert np.sum(mask) == 154
