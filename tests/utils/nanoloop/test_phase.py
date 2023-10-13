"""
Test phase methods
"""
from pytest import approx

from examples.utils.nanoloop.ex_phase import ex_phase_calibration


# class TestPhase(unittest.TestCase):

def test_phase_up_down():
    """ Test ex_phase_calibration: up and down """

    treat_phase, result, dict_pha = ex_phase_calibration(pha_corr='up_down')

    # print(sum(treat_phase['on']))
    # print(sum(treat_phase['off']))

    assert dict_pha['grounded tip'] is True
    assert dict_pha['positive d33'] is True
    assert dict_pha['counterclockwise'] is True
    assert dict_pha['main elec'] is True
    assert dict_pha['corr'] == 'up_down'
    assert dict_pha['pha fwd'] == 0
    assert dict_pha['pha rev'] == 180
    assert dict_pha['locked elec slope'] is None

    assert result['on']['corr'] == 'up_down'
    assert result['on']['reverse'] is False
    assert result['on']['dict phase target']['low'] == 0
    assert result['on']['dict phase target']['high'] == 180
    assert result['on']['dict phase meas']['low'] == approx(49.748815534346974)
    assert result['on']['dict phase meas']['high'] == approx(238.738908651614)
    assert sum(treat_phase['on']) == 131760

    assert result['off']['corr'] == 'up_down'
    assert result['off']['reverse'] is False
    assert result['off']['dict phase target']['low'] == 180
    assert result['off']['dict phase target']['high'] == 0
    assert result['off']['dict phase meas']['low'] == approx(238.6397534672086)
    assert result['off']['dict phase meas']['high'] == approx(
        49.574424503970064)
    assert sum(treat_phase['off']) == 90180


def test_phase_affine():
    """ Test ex_phase_calibration: affine """

    treat_phase, result, dict_pha = ex_phase_calibration(pha_corr='affine')

    # print(sum(treat_phase['on']))
    # print(sum(treat_phase['off']))

    assert dict_pha['grounded tip'] is True
    assert dict_pha['positive d33'] is True
    assert dict_pha['counterclockwise'] is True
    assert dict_pha['main elec'] is True
    assert dict_pha['corr'] == 'affine'
    assert dict_pha['pha fwd'] == 0
    assert dict_pha['pha rev'] == 180
    assert dict_pha['locked elec slope'] is None

    assert result['on']['corr'] == 'affine'
    assert result['on']['reverse'] is False
    assert result['on']['coefs'][0] == approx(0.9524308763016022)
    assert result['on']['coefs'][1] == approx(-47.38230797434485)
    assert result['on']['dict phase target']['low'] == 0
    assert result['on']['dict phase target']['high'] == 180
    assert result['on']['dict phase meas']['low'] == approx(49.748815534346974)
    assert result['on']['dict phase meas']['high'] == approx(238.738908651614)
    assert sum(treat_phase['on']) == approx(131835.57233804)

    assert result['off']['corr'] == 'affine'
    assert result['off']['reverse'] is False
    assert result['off']['coefs'][0] == approx(0.9520518700443423)
    assert result['off']['coefs'][1] == approx(-47.19742355537679)
    assert result['off']['dict phase target']['low'] == 180
    assert result['off']['dict phase target']['high'] == 0
    assert result['off']['dict phase meas']['low'] == approx(238.6397534672086)
    assert result['off']['dict phase meas']['high'] == approx(
        49.574424503970064)
    assert sum(treat_phase['off']) == approx(90876.81644494568)


def test_phase_offset():
    """ Test ex_phase_calibration: offset """

    treat_phase, result, dict_pha = ex_phase_calibration(pha_corr='offset')

    # print(sum(treat_phase['on']))
    # print(sum(treat_phase['off']))

    assert dict_pha['grounded tip'] is True
    assert dict_pha['positive d33'] is True
    assert dict_pha['counterclockwise'] is True
    assert dict_pha['main elec'] is True
    assert dict_pha['corr'] == 'offset'
    assert dict_pha['pha fwd'] == 0
    assert dict_pha['pha rev'] == 180
    assert dict_pha['locked elec slope'] is None

    assert result['on']['corr'] == 'offset'
    assert result['on']['reverse'] is False
    assert result['on']['coefs'][0] == approx(1)
    assert result['on']['coefs'][1] == approx(-54.24386209298049)
    assert result['on']['dict phase target']['low'] == 0
    assert result['on']['dict phase target']['high'] == 180
    assert result['on']['dict phase meas']['low'] == approx(49.748815534346974)
    assert result['on']['dict phase meas']['high'] == approx(238.738908651614)
    assert sum(treat_phase['on']) == approx(131228.0204635996)

    assert result['off']['corr'] == 'offset'
    assert result['off']['reverse'] is False
    assert result['off']['coefs'][0] == approx(1)
    assert result['off']['coefs'][1] == approx(-54.10708898558934)
    assert result['off']['dict phase target']['low'] == 180
    assert result['off']['dict phase target']['high'] == 0
    assert result['off']['dict phase meas']['low'] == approx(238.6397534672086)
    assert result['off']['dict phase meas']['high'] == approx(
        49.574424503970064)
    assert sum(treat_phase['off']) == approx(88201.3768088286)


def test_raw_phase():
    """ Test ex_phase_calibration: raw """

    treat_phase, result, dict_pha = ex_phase_calibration(pha_corr='raw')

    # print(sum(treat_phase['on']))
    # print(sum(treat_phase['off']))

    assert dict_pha['grounded tip'] is True
    assert dict_pha['positive d33'] is True
    assert dict_pha['counterclockwise'] is True
    assert dict_pha['main elec'] is True
    assert dict_pha['corr'] == 'raw'
    assert dict_pha['pha fwd'] == 0
    assert dict_pha['pha rev'] == 180
    assert dict_pha['locked elec slope'] is None

    assert result['on']['corr'] == 'raw'
    assert sum(treat_phase['on']) == approx(218018.19981236802)

    assert result['off']['corr'] == 'raw'
    assert sum(treat_phase['off']) == approx(174772.7191857715)
