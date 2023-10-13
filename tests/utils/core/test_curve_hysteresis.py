"""
Test hysteresis functionalities
"""
from pytest import approx

from examples.utils.core.ex_curve_hysteresis import ex_hysteresis


def test_hysteresis():
    """
    Testing hysteresis creation and fitting
    """
    params, props = ex_hysteresis(verbose=False)

    ref_params = [1.0140943432266198, -0.1251035329489646,
                  10.357067717376768, 10.357067717376768,
                  2.9732593029309378, 2.9732593029309378,
                  -1.5131509846344615, 4.4853096531239744]
    ref_props = [-2.503457809291132, 5.475616477780645,
                 5.178533858688384, -5.178533858688384,
                 -0.2899502651819039, 3.262108933671417,
                 4.912788580126749, -4.912788580126749,
                 -1.5131509846344615, 4.4853096531239744,
                 5.998460637758436, 1.4860793342447565, 0.0,
                 5.1771459459738445, -5.177145945973844,
                 -1.5131509846344615, 4.4853096531239744,
                 5.998460637758436, 5.064627653237663,
                 -5.178517128923725, 10.243144782161387,
                 62.12646302528316, 0.0,
                 0.9897324051377718]

    assert params['offset'].value == approx(ref_params[0])
    assert params['slope'].value == approx(ref_params[1])
    assert params['ampli_0'].value == approx(ref_params[2])
    assert params['ampli_1'].value == approx(ref_params[3])
    assert params['coef_0'].value == approx(ref_params[4])
    assert params['coef_1'].value == approx(ref_params[5])
    assert params['x0_0'].value == approx(ref_params[6])
    assert params['x0_1'].value == approx(ref_params[7])

    assert props['x sat l'] == approx(ref_props[0])
    assert props['x sat r'] == approx(ref_props[1])
    assert props['y sat l'] == approx(ref_props[2])
    assert props['y sat r'] == approx(ref_props[3])
    assert props['x infl l'] == approx(ref_props[4])
    assert props['x infl r'] == approx(ref_props[5])
    assert props['y infl l'] == approx(ref_props[6])
    assert props['y infl r'] == approx(ref_props[7])
    assert props['x0 l'] == approx(ref_props[8])
    assert props['x0 r'] == approx(ref_props[9])
    assert props['x0 wid'] == approx(ref_props[10])
    assert props['x shift'] == approx(ref_props[11])
    assert props['y shift'] == ref_props[12]
    assert props['y0 l'] == approx(ref_props[13])
    assert props['y0 r'] == approx(ref_props[14])
    assert props['x inter l'] == approx(ref_props[15])
    assert props['x inter r'] == approx(ref_props[16])
    assert props['x wdw'] == approx(ref_props[17])
    assert props['y inter l'] == approx(ref_props[18])
    assert props['y inter r'] == approx(ref_props[19])
    assert props['y wdw'] == approx(ref_props[20])
    assert props['area'] == approx(ref_props[21])
    assert props['diff coef'] == approx(ref_props[22])
    assert props['R² hyst'] == approx(ref_props[23])
