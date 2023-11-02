"""
Test loop_file_reader methods
"""
from pytest import approx
import numpy as np

from examples.toolbox.ex_loop_file_reader import example_loop_file_reader


# class TestLoopFileReader(unittest.TestCase):


def test_loop_file_reader():
    """ Test example_loop_file_reader """

    out = example_loop_file_reader()

    # for nanoloop in out:
    #     print(np.sum(nanoloop.piezorep))

    assert np.sum(out[0].piezorep) == approx(0.006412847641863103)
    assert np.sum(out[1].piezorep) == approx(0.00396073347920191)
    assert np.sum(out[2].piezorep) == approx(0.0038047340826059856)
    assert np.sum(out[3].piezorep) == approx(0.00286302205388792)
    assert np.sum(out[4].piezorep) == approx(0.0025335644354628583)
    assert np.sum(out[5].piezorep) == approx(0.0023652681809282383)
    assert np.sum(out[6].piezorep) == approx(0.002520349672402297)
    assert np.sum(out[7].piezorep) == approx(0.0022468716047811467)
