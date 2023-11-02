"""
Example of map methods
"""

import numpy as np

from PySSPFM.utils.path_for_runable import save_path_example
from PySSPFM.utils.map.main import main_mapping


def example_map(mask_mode, verbose=False, make_plots=False):
    """
    Example of map functions.

    Parameters
    ----------
    mask_mode: str
        Mode for creating the mask. Possible values: 'ref prop: man',
        'ref prop: auto', 'man mask'.
    verbose: bool, optional
        Verbosity flag (default is False).
    make_plots: bool, optional
        Flag indicating whether to make plots (default is False).

    Returns
    -------
    mask: array-like
        Mask array.
    """
    assert mask_mode in ['ref prop: man', 'ref prop: auto', 'man mask']

    # saving path management
    dir_path_out, save_plots = save_path_example(
        "map", save_example_exe=make_plots, save_test_exe=not make_plots)

    nb_prop = 3
    # Bug pix = missing file
    nb_bug_pix = 2
    # Bug ref = abnormal value in ref prop for considered pix index
    bug_ref = [2, 3, 4, 10, 11, 12, 13, 14, 18, 19, 20, 28]
    ref_range = {'min': 0.95, 'max': 1}
    prop_range = {'min': 5, 'max': 10}
    dim_pix = {'x': 8, 'y': 8}
    dim_mic = {'x': 3.5, 'y': 3.5}
    dict_interp = {'fact': 4, 'func': 'linear'}
    dict_ref = {'prop': 'R²', 'fmt': '.5f', 'min val': None, 'max val': None,
                'interactive': True}
    dict_map = {'label': 'On field', 'col': 'w'}

    if mask_mode == 'ref prop: auto':
        dict_ref['min val'], dict_ref["interactive"] = ref_range['min'], False

    man_mask = None

    if mask_mode == 'man mask':
        man_mask = bug_ref

    np.random.seed(0)
    len_matrix = dim_pix['x'] * dim_pix['y'] - nb_bug_pix

    # Ref prop determination
    ref = np.random.random(len_matrix)
    ref *= (ref_range['max'] - ref_range['min'])
    ref += ref_range['min']

    # Prop determination
    prop = {}
    for i in range(nb_prop):
        prop[f'prop n {i}'] = np.random.random(len_matrix)
        prop[f'prop n {i}'] *= (prop_range['max'] - prop_range['min'])
        prop[f'prop n {i}'] += prop_range['min']

    # Add bug in ref prop and in prop
    for position in bug_ref:
        ref_val = np.random.randint(0, int(ref_range['min'] * 100)) / 100
        ref[position] = ref_val

        for i in range(nb_prop):
            prop_val = np.random.randint(0, int(prop_range['min'] * 100)) / 100
            prop[f'prop n {i}'][position] = prop_val

    mask_mode_lab = mask_mode
    for elem_del, elem_add in zip(
            ['prop', ': man', ': auto'], [dict_ref['prop'], '', '']):
        mask_mode_lab = mask_mode_lab.replace(elem_del, elem_add)

    dict_map['mask mode'] = mask_mode_lab

    if mask_mode == 'man mask':
        ref = None
        dict_ref = None

    # ex main_mapping
    mask = main_mapping(prop, dim_pix, dim_mic=dim_mic, dict_interp=dict_interp,
                        dict_map=dict_map, ref=ref, dict_ref=dict_ref,
                        mask=man_mask, verbose=verbose, show_plots=make_plots,
                        save_plots=save_plots, dir_path_out=dir_path_out)

    if verbose:
        print(f'mask: {mask}')

    return mask


if __name__ == '__main__':
    figs = []
    # Ref prop is R² for example, but also could be work of switching ...
    # - 'ref prop: man': select manually the mask from ref prop
    # - 'ref prop: auto': select automatically the mask from ref prop
    # - 'man mask': user define a mask
    example_map(mask_mode='ref prop: man', verbose=True, make_plots=True)
    example_map(mask_mode='ref prop: auto', verbose=True, make_plots=True)
    example_map(mask_mode='man mask', verbose=True, make_plots=True)
