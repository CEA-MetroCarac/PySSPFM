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

    assert np.sum(out[0].piezorep.y_meas) == approx(0.007081196191521127)
    assert np.sum(out[1].piezorep.y_meas) == approx(0.0030950251475542184)
    assert np.sum(out[2].piezorep.y_meas) == approx(0.002495189589386597)
    assert np.sum(out[3].piezorep.y_meas) == approx(0.0022313696987980723)
    assert np.sum(out[4].piezorep.y_meas) == approx(0.0018318402751288214)
    assert np.sum(out[5].piezorep.y_meas) == approx(0.0022254565110847615)
    assert np.sum(out[6].piezorep.y_meas) == approx(0.002313203349539847)
    assert np.sum(out[7].piezorep.y_meas) == approx(0.002579800042060846)
