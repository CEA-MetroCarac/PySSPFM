"""
Tools for multiprocessing
"""

import multiprocessing
from functools import partial

from PySSPFM.data_processing.datacube_to_nanoloop_s1 import \
    single_script as single_script_s1
from PySSPFM.data_processing.nanoloop_to_hyst_s2 import \
    single_script as single_script_s2
from PySSPFM.toolbox.phase_offset_analyzer import \
    single_script as single_script_offset
from PySSPFM.toolbox.phase_inversion_analyzer import \
    single_script as single_script_grad
from PySSPFM.free_1 import single_script_free


def process_single_file_s1_classic(file_path, common_args):
    single_script_s1(file_path_in=file_path, **common_args)


def process_single_file_s1_phase(list_args, common_args):
    single_script_s1(file_path_in=list_args[0],
                     phase_offset=list_args[1], **common_args)


def run_multi_proc_s1(file_paths, phase_tab, common_args, processes=16):
    with multiprocessing.Pool(processes=processes) as pool:
        if phase_tab is not None:
            list_args = []
            for cont, (file_path, phase_val) in \
                    enumerate(zip(file_paths, phase_tab)):
                list_args.append([file_path])
                list_args[cont] += [phase_val]
            pool.map(partial(
                process_single_file_s1_phase, common_args=common_args),
                list_args)
        else:
            pool.map(partial(
                process_single_file_s1_classic, common_args=common_args),
                file_paths)


def process_single_file_s2_classic(tab_path, common_args):
    result = single_script_s2(tab_path_in=tab_path, **common_args)
    return result


def process_single_file_s2_revert(list_args, common_args):
    result = single_script_s2(tab_path_in=list_args[0],
                              user_pars=list_args[1], **common_args)
    return result


def run_multi_proc_s2(tab_paths, tab_user_pars, common_args, processes=16):
    with multiprocessing.Pool(processes=processes) as pool:
        if tab_user_pars is not None:
            list_args = []
            for cont, (tab_path, user_pars) in \
                    enumerate(zip(tab_paths, tab_user_pars)):
                list_args.append([tab_path])
                list_args[cont] += [user_pars]
            results = pool.starmap(
                process_single_file_s2_revert,
                [(list_arg, common_args) for list_arg in list_args])
        else:
            results = pool.starmap(
                process_single_file_s2_classic,
                [(tab_path, common_args) for tab_path in tab_paths])

    # Unpack the results
    tab_best_loops = [res[0] for res in results]
    tab_properties = [res[1] for res in results]
    tab_other_properties = [res[2] for res in results]

    return tab_best_loops, tab_properties, tab_other_properties


def process_single_file_free(file_name, common_args):
    result = single_script_free(file_name=file_name, **common_args)
    return result


def run_multi_proc_free(file_names, common_args, processes=16):
    tab_best_loops, tab_properties, tab_mean_voltage, tab_diff_piezorep_mean = \
        [], [], [], []
    with multiprocessing.Pool(processes=processes) as pool:
        results = [pool.apply_async(process_single_file_free,
                                    (file_name, common_args))
                   for file_name in file_names]
        for result in results:
            out = result.get()
            best_loops, properties, mean_voltage, diff_piezorep_mean = out
            tab_best_loops.append(best_loops)
            tab_properties.append(properties)
            tab_mean_voltage.append(mean_voltage)
            tab_diff_piezorep_mean.append(diff_piezorep_mean)
    return (tab_best_loops, tab_properties, tab_mean_voltage,
            tab_diff_piezorep_mean)


def process_phase_offset_analyzer(file_path_in, common_args):
    result = single_script_offset(file_path_in=file_path_in, **common_args)
    return result


def run_multi_phase_offset_analyzer(file_paths_in, common_args, processes=16):
    tab_phase_offset_val = []
    with multiprocessing.Pool(processes=processes) as pool:
        results = [pool.apply_async(process_phase_offset_analyzer,
                                    (file_path_in, common_args))
                   for file_path_in in file_paths_in]
        for result in results:
            phase_offset_val, _ = result.get()
            tab_phase_offset_val.append(phase_offset_val)
    return tab_phase_offset_val


def process_phase_inversion_analyzer_classic(file_path_in, common_args):
    result = single_script_grad(file_path_in=file_path_in, **common_args)
    return result


def process_phase_inversion_analyzer_phase(list_args, common_args):
    result = single_script_grad(file_path_in=list_args[0],
                                phase_offset=list_args[1], **common_args)
    return result


def run_multi_phase_inversion_analyzer(file_paths_in, phase_tab, common_args,
                                       processes=16):
    tab_phase_grad_val = []
    with multiprocessing.Pool(processes=processes) as pool:
        if phase_tab is not None:
            list_args = []
            for cont, (file_path, phase_val) in \
                    enumerate(zip(file_paths_in, phase_tab)):
                list_args.append([file_path])
                list_args[cont] += [phase_val]
            results = pool.map(partial(
                process_phase_inversion_analyzer_phase,
                common_args=common_args), list_args)
        else:
            results = [pool.apply_async(
                process_phase_inversion_analyzer_classic,
                (file_path_in, common_args)) for file_path_in in file_paths_in]
        for result in results:
            phase_grad_val, _ = result.get()
            tab_phase_grad_val.append(phase_grad_val)
    return tab_phase_grad_val
