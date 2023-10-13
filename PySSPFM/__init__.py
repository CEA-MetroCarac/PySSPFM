import pathlib
import settings

ROOT = pathlib.Path(__file__).parent.parent
EXAMPLES = ROOT / 'examples'
EXAMPLE_ROOT_PATH_IN = EXAMPLES / 'datas' / 'PySSPFM_example_in'
EXAMPLE_ROOT_PATH_OUT = EXAMPLES / 'datas' / 'PySSPFM_example_out'
DEFAULT_DATA_PATH_OUT = EXAMPLES / 'datas' / 'PySSPFM_data_out'
DEFAULT_LOGO_PATH = ROOT / 'PySSPFM' / 'logo_icon' / 'logoPySSPFM.png'
DEFAULT_ICON_PATH = ROOT / 'PySSPFM' / 'logo_icon' / 'iconPySSPFM.png'
