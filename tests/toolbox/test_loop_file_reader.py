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
    #     print(np.sum(nanoloop.piezorep.y_meas))

    assert np.sum(out[0].piezorep.y_meas) == approx(-0.0071040007941460355)
    assert np.sum(out[1].piezorep.y_meas) == approx(-0.0030957909636012133)
    assert np.sum(out[2].piezorep.y_meas) == approx(-0.002491171905122655)
    assert np.sum(out[3].piezorep.y_meas) == approx(-0.00228582007060475)
    assert np.sum(out[4].piezorep.y_meas) == approx(-0.001837495609928858)
    assert np.sum(out[5].piezorep.y_meas) == approx(-0.002237673504772637)
    assert np.sum(out[6].piezorep.y_meas) == approx(-0.002378292790837367)
    assert np.sum(out[7].piezorep.y_meas) == approx(-0.0026344524341999475)
