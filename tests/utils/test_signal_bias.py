"""
Test signal_bias methods
"""
from pytest import approx
import numpy as np

from examples.utils.ex_signal_bias import \
    example_sspfm_bias, example_dynamic_bias, example_ckpfm_bias


# class TestSignalBias(unittest.TestCase):


def test_sspfm_bias():
    """ Test example_sspfm_bias """

    out = example_sspfm_bias()
    (sspfm_bias, real_time_bias, real_sspfm_bias, extracted_bias_pars) = out

    target_extracted_bias_pars = {
        'Read Number of Voltages': 10,
        'Read Voltage Range V': (0.0, 0.0),
        'Read Wave Form': 'Single Read Step',
        'Write Number of Voltages': 9,
        'Write Voltage Range V': (-10.0, 10.0),
        'Write Wave Form': 'Zero, up'}

    assert sspfm_bias[0] == 0.0
    assert sspfm_bias[-1] == 0.0
    assert sspfm_bias[int(len(sspfm_bias) / 4)] == 0.0
    assert sspfm_bias[int(len(sspfm_bias) / 2)] == 0.0
    assert sspfm_bias[int(3 * len(sspfm_bias) / 4)] == 0.0
    assert np.sum(np.absolute(sspfm_bias)) == 800.0
    assert np.sum(real_time_bias) == 2592000.0
    assert np.sum(np.absolute(real_sspfm_bias)) == 80000.0
    assert extracted_bias_pars == target_extracted_bias_pars


def test_sspfm_bias_open():
    """ Test example_sspfm_bias in open mode """

    out = example_sspfm_bias(open_mode=True)
    sspfm_bias, real_time_bias, real_sspfm_bias, _ = out

    assert sspfm_bias[0] == 0.0
    assert sspfm_bias[-1] == 0.0
    assert sspfm_bias[int(len(sspfm_bias) / 4)] == 0.0
    assert sspfm_bias[int(len(sspfm_bias) / 2)] == 0.0
    assert sspfm_bias[int(3 * len(sspfm_bias) / 4)] == 0.0
    assert np.sum(np.absolute(sspfm_bias)) == 440.0
    assert np.sum(real_time_bias) == 2592000.0
    assert np.sum(np.absolute(real_sspfm_bias)) == 44000.0


def test_dynamic_bias():
    """ Test example_dynamic_bias """

    dynamic_time, dynamic_bias = example_dynamic_bias()

    assert dynamic_bias[0] == -5.0
    assert dynamic_bias[-1] == approx(0.0)
    assert dynamic_bias[int(len(dynamic_bias) / 4)] == 3.0
    assert dynamic_bias[int(len(dynamic_bias) / 2)] == 4.0
    assert dynamic_bias[int(3 * len(dynamic_bias) / 4)] == 5
    assert np.sum(dynamic_bias) == 348020.0
    assert np.sum(dynamic_time) == approx(533079.7512500001)


def test_ckpfm_sequence_bias():
    """ Test example_ckpfm_bias in Sequence mode """

    ckfpm_time, ckfpm_bias = example_ckpfm_bias(mode='Sequence_11')

    assert ckfpm_bias[0] == 0.0
    assert ckfpm_bias[-1] == 4.0
    assert ckfpm_bias[int(len(ckfpm_bias) / 4)] == 10.0
    assert ckfpm_bias[int(len(ckfpm_bias) / 2)] == 0.0
    assert ckfpm_bias[int(3 * len(ckfpm_bias) / 4)] == -10.0
    assert np.sum(np.absolute(ckfpm_bias)) == 126400.0
    assert np.sum(ckfpm_time) == 113288.0


def test_ckpfm_sweep_bias():
    """ Test example_ckpfm_bias in Sweep mode """

    ckfpm_time, ckfpm_bias = example_ckpfm_bias(mode='Sweep')

    assert ckfpm_bias[0] == 0.0
    assert ckfpm_bias[-1] == 4.0
    assert ckfpm_bias[int(len(ckfpm_bias) / 4)] == 10.0
    assert ckfpm_bias[int(len(ckfpm_bias) / 2)] == 0.0
    assert ckfpm_bias[int(3 * len(ckfpm_bias) / 4)] == -10.0
    assert np.sum(np.absolute(ckfpm_bias)) == approx(120160.32064128257)

    assert np.sum(ckfpm_time) == 115200.0


def test_ckpfm_dualsweep_bias():
    """ Test example_ckpfm_bias in Dual_sweep mode """

    ckfpm_time, ckfpm_bias = example_ckpfm_bias(mode='Dual_sweep')

    assert ckfpm_bias[0] == 0.0
    assert ckfpm_bias[-1] == approx(-0.008016032064128709)
    assert ckfpm_bias[int(len(ckfpm_bias) / 4)] == 10.0
    assert ckfpm_bias[int(len(ckfpm_bias) / 2)] == 0.0
    assert ckfpm_bias[int(3 * len(ckfpm_bias) / 4)] == -10.0
    assert np.sum(np.absolute(ckfpm_bias)) == approx(199680.64128256514)

    assert np.sum(ckfpm_time) == approx(385793.27999999997)
