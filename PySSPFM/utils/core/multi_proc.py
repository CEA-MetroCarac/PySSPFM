from PySSPFM.data_processing.datacube_to_nanoloop_s1 import \
    single_script as single_script_s1
from PySSPFM.data_processing.nanoloop_to_hyst_s2 import \
    single_script as single_script_s2
from PySSPFM.toolbox.phase_offset_analyzer import \
    single_script as single_script_offset
from PySSPFM.free_1 import single_script_free

import multiprocessing
from functools import partial


def process_single_file_s1(file_path, common_args):
    single_script_s1(file_path_in=file_path, **common_args)


def run_multi_proc_s1(file_paths, common_args, processes=16):
    with multiprocessing.Pool(processes=processes) as pool:
        pool.map(partial(process_single_file_s1, common_args=common_args),
                 file_paths)


def process_single_file_s2(tab_path, common_args):
    result = single_script_s2(tab_path_in=tab_path, **common_args)
    return result


def run_multi_proc_s2(tab_paths, common_args, processes=16):
    with multiprocessing.Pool(processes=processes) as pool:
        results = pool.starmap(
            process_single_file_s2,
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
