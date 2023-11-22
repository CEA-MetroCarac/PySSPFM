"""
Test of analysis, gen_data and plot methods
"""
from pytest import approx
import numpy as np

from examples.utils.nanoloop_to_hyst.ex_analysis import \
    example_analysis, ex_sort_prop


# class TestAnalysis(unittest.TestCase):


def test_sort_prop():
    """ Test ex_sort_prop """

    prop = ex_sort_prop()

    assert len(list(prop.keys())) == 3
    assert len(list(prop['on'].keys())) == 20
    assert len(list(prop['off'].keys())) == 20
    assert len(list(prop['coupled'].keys())) == 20


def test_analysis_multi_off():
    """ Test example_analysis: off field: multi loop """

    out = example_analysis(analysis='multi_off')
    (analysis_mode, datas_dict, dict_str, x_hyst, y_hyst, best_loop,
     read_volt, bckgnd_tab, props_tot, props_no_bckgnd,
     electrostatic_dict) = out

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    sum_x_hyst = np.sum(np.concatenate(x_hyst))
    sum_y_hyst = np.sum(np.concatenate(y_hyst))
    elec_list = list(electrostatic_dict.values())

    # print(sum_datas_dict)
    # print(sum_x_hyst)
    # print(sum_y_hyst)
    # print(np.sum(bckgnd_tab))
    # print(np.sum(best_loop.piezorep))
    # print(np.sum(list(props_tot.values())))
    # print(np.sum(list(props_no_bckgnd.values())))
    # print(np.sum(list(electrostatic_dict.values())))

    assert analysis_mode == 'multi_loop'
    assert sum_datas_dict == approx(48597.62513626559)
    assert dict_str == {'unit': 'nm', 'label': 'Off field', 'col': 'w'}
    assert sum_x_hyst == approx(5.1514348342607263e-14)
    assert sum_y_hyst == approx(-3.0582405907115238)
    assert np.sum(best_loop.piezorep.y_meas) == approx(-2.8958272377863805)
    assert read_volt == [-2.0, -1.0, 0.0, 1.0, 2.0]
    assert np.sum(bckgnd_tab) == approx(1.8011164390742098)
    assert np.sum(list(props_tot.values())) == approx(55.751250260969876)

    assert np.sum(list(props_no_bckgnd.values())) == approx(55.04487815218891)

    assert np.sum(elec_list) == approx(1.8444046841813353)


def test_analysis_mean_off():
    """ Test example_analysis: off field: mean loop """

    out = example_analysis(analysis='mean_off')
    (analysis_mode, datas_dict, dict_str, x_hyst, y_hyst, best_loop,
     read_volt, bckgnd_tab, props_tot, props_no_bckgnd,
     electrostatic_dict) = out

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    sum_x_hyst = np.sum(np.concatenate(x_hyst))
    sum_y_hyst = np.sum(np.concatenate(y_hyst))

    # print(sum_datas_dict)
    # print(sum_x_hyst)
    # print(sum_y_hyst)
    # print(np.sum(best_loop.piezorep))
    # print(np.sum(list(props_tot.values())))
    # print(np.sum(list(props_no_bckgnd.values())))

    assert analysis_mode == 'mean_loop'
    assert sum_datas_dict == approx(48234.66364225659)
    assert dict_str == {'unit': 'nm', 'label': 'Off field', 'col': 'w'}
    assert sum_x_hyst == approx(5.1514348342607263e-14)
    assert sum_y_hyst == approx(36.71570696942)
    assert np.sum(best_loop.piezorep.y_meas) == approx(36.04369866758542)

    assert read_volt is None
    assert bckgnd_tab is None
    assert np.sum(list(props_tot.values())) == approx(59.45611151439931)

    assert np.sum(list(props_no_bckgnd.values())) == approx(55.51232407613206)

    assert electrostatic_dict == {}


def test_analysis_mean_on():
    """ Test example_analysis: on field: mean loop """

    out = example_analysis(analysis='mean_on')
    (analysis_mode, datas_dict, dict_str, x_hyst, y_hyst, best_loop,
     read_volt, bckgnd_tab, props_tot, props_no_bckgnd,
     electrostatic_dict) = out

    sum_datas_dict = np.sum(np.concatenate(list(datas_dict.values())))
    sum_x_hyst = np.sum(np.concatenate(x_hyst))
    sum_y_hyst = np.sum(np.concatenate(y_hyst))
    elec_list = list(electrostatic_dict.values())

    # print(sum_datas_dict)
    # print(sum_x_hyst)
    # print(sum_y_hyst)
    # print(np.sum(best_loop.piezorep))
    # print(np.sum(list(props_tot.values())))
    # print(np.sum(list(props_no_bckgnd.values())))
    # print(np.sum(list(electrostatic_dict.values())))

    assert analysis_mode == 'on_f_loop'
    assert sum_datas_dict == approx(47130.14113616596)
    assert dict_str == {'unit': 'nm', 'label': 'On field', 'col': 'y'}
    assert sum_x_hyst == approx(5.1514348342607263e-14)
    assert sum_y_hyst == approx(35.749385588975855)
    assert np.sum(best_loop.piezorep.y_meas) == approx(35.02393812741746)
    assert read_volt is None
    assert bckgnd_tab is None
    assert np.sum(list(props_tot.values())) == approx(59.87070357013261)

    assert np.sum(list(props_no_bckgnd.values())) == approx(55.2989653801296)

    assert np.sum(elec_list) == approx(1.781444848093118)
