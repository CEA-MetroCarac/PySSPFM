"""
Test fitting functionalities
"""
from pytest import approx

from examples.utils.core.ex_fitting import \
    (ex_gaussian_peak_fit, ex_sho_peak_fit, ex_sho_phase_fit,
     ex_sho_phase_switch_fit)


def test_gaussian_peak_fit():
    """ test ex_gaussian_peak_fit """
    gaussian_pars = ex_gaussian_peak_fit()
    gaussian_pars_val = [pars.value for pars in gaussian_pars.values()]
    target_pars = [10.263530347730656, 3.955672070340832, 0.0233435218625182,
                   1.9976776975995745, 0.0]
    for elem_pars, elem_target in zip(gaussian_pars_val, target_pars):
        assert elem_pars == approx(elem_target)


def test_sho_peak_fit():
    """ test ex_sho_peak_fit """
    sho_pars = ex_sho_peak_fit()
    sho_pars_val = [pars.value for pars in sho_pars.values()]
    target_pars = [1.0612698195104044, 9.568395446904102, 9.998240445405514,
                   1.9359077592571658, 0.0]
    for elem_pars, elem_target in zip(sho_pars_val, target_pars):
        assert elem_pars == approx(elem_target)


def test_sho_phase_fit():
    """ test ex_sho_phase_fit """
    sho_phase_pars = ex_sho_phase_fit()
    sho_phase_pars_val = [pars.value for pars in sho_phase_pars.values()]
    target_pars = [0.9985985077988063, 10.215378931180616, 9.967515484523119,
                   1.0041064481679576, 0.0]
    for elem_pars, elem_target in zip(sho_phase_pars_val, target_pars):
        assert elem_pars == approx(elem_target)


def test_sho_phase_switch_fit():
    """ test ex_sho_phase_switch_fit """
    sho_phase_switch_pars = ex_sho_phase_switch_fit()
    sho_phase_switch_pars_val = [pars.value
                                 for pars in sho_phase_switch_pars.values()]
    target_pars = [1.0976692783807431, 2.3684479138424592, 10.000000120218424,
                   1.0039096300857406, 0.0]
    for elem_pars, elem_target in zip(sho_phase_switch_pars_val, target_pars):
        assert elem_pars == approx(elem_target)
