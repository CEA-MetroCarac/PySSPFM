"""
Functionalities for Bruker DATA CUBE Processing

Copyright Bruker Corporation 1988-2020. All rights reserved.

For using this script, the real-time software for the ramp channels
    has to be set to be:
        1. Deflection Error
        2. Input1, this is normally tip bias (Input2 in Piezo Response mode)
        3. Amplitude
        4. Phase
        5. Inphase
        6. Quadrature
"""
from collections import OrderedDict
import numpy as np
try:
    from nanoscope import files
    from nanoscope.constants import METRIC
except ModuleNotFoundError:
    print("To open DATACUBE spm file (Bruker), nanoscope module is "
          "required and NanoScope Analysis software (Bruker) should be "
          "installed on the computer")


class DataExtraction:
    """ DataExtraction object """
    def __init__(self, fpath):
        self.fpath = fpath
        self.info_dict = None
        self.raw_dict = None
        self.electrical_dict = None

    def data_extraction(self, raw_data=False, electrical_data=False):
        """
        Extracts various data from a datacube measurement.

        Parameters
        ----------
        raw_data: bool, optional
            If True, extract raw data. Default is False.
        electrical_data: bool, optional
            If True, extract electrical data. Default is False.

        Returns
        -------
        None
        """
        with files.ScriptFile(self.fpath) as file_:
            # Total # of segments
            num_segs = file_.segments_count

            # duration of each segment, genetic unit s
            durs = file_.segments_basic_info.durations

            # samples per segment for each segment
            samps = file_.segments_basic_info.sizes

            # surface control information
            # if measure per write is 0, drive_amp = 0
            freq_start = file_.surface_control_info.ramp_start
            freq_size = file_.surface_control_info.ramp_size
            drive_amp = file_.surface_control_info.amplitude

            # withdraw segment show ramp size set by script generator
            force_ramp_size = -file_.segments_ramp_info.ramp_sizes[-1]

            # tip bias on every segment
            tip_bias = file_.segments_bias_info.tip_biases  # unit V

            # ttl output setting on every segment
            ttl_output = file_.segments_basic_info.ttl_outputs

            # drive amplitude at every segment
            amps = [file_.segments_info[i].amplitude for i in
                    range(num_segs)]  # unit mV

            if electrical_data:
                amp = file_[2].get_script_segment_data(None, METRIC).y
                phas = file_[3].get_script_segment_data(None, METRIC).y
                inph = file_[4].get_script_segment_data(None, METRIC).y
                quad = file_[5].get_script_segment_data(None, METRIC).y
                electrical_data_dict = np.vstack((amp, phas, inph, quad)).T

            if raw_data:
                raw_dict = OrderedDict()
                # important modification
                # for channel in file_[1:]:
                for channel in file_:
                    scale_unit = channel.get_scale_unit(METRIC)
                    type_desc = channel.data_type_desc
                    if type_desc in [u'Input1', u'Input2']:
                        type_desc = 'Tip Bias'
                    key = u"{} ({})".format(type_desc, scale_unit)
                    raw_dict[key] = channel.get_script_segment_data(None,
                                                                    METRIC).y
                raw_dict['time'] = channel.get_script_segment_data(None,
                                                                   METRIC).x

        self.info_dict = dict(num_segs=num_segs,
                              durs=durs,
                              samps=samps,
                              freq_start=freq_start,
                              freq_size=freq_size,
                              drive_amp=drive_amp,
                              force_ramp_size=force_ramp_size,
                              tip_bias=tip_bias,
                              ttl_output=ttl_output,
                              amps=amps,
                              )

        if raw_data:
            self.raw_dict = raw_dict

        if electrical_data:
            self.electrical_dict = electrical_data_dict


def script_info(info_dict):
    """
    Return a dictionary of script parameters.

    The parameters returned here should correspond to the ones input into the
    SS-PFM script generator during script creation.
    Also returns two parameters that describe the modulation - Frequency
    Range and Drive Amplitude.

    Parameters
    ----------
    info_dict: dict
        A dictionary of relevant values read from the .spm file
    """
    # total number of segments
    num_segs = info_dict['num_segs']
    # tip bias on all segments, including force ramps
    tip_bias = info_dict['tip_bias']

    tba = tip_bias_analysis(tip_bias, num_segs, info_dict['ttl_output'])

    segs_per_write = tba['segs_per_write']
    # segs_per_read = tba['segs_per_read']
    write_wave_form = tba['write_wave_form']
    read_wave_form = tba['read_wave_form']
    write_num_voltages = tba['write_num_voltages']
    write_voltage_range = tba['write_voltage_range']
    read_num_voltages = tba['read_num_voltages']
    read_voltage_range = tba['read_voltage_range']
    meas_per_write = tba['meas_per_write']
    meas_per_read = tba['meas_per_read']

    durs = info_dict['durs'][1:-1]
    total_dur = round(sum(durs))
    # unit s
    write_seg_duration = int(round(durs[1] * 1000))
    # unit s
    read_seg_duration = int(round(durs[segs_per_write + 1] * 1000))

    samps_per_seg = info_dict['samps']
    write_samps_per_seg = samps_per_seg[1]
    read_samps_per_seg = samps_per_seg[segs_per_write + 1]
    freq_start, freq_size = info_dict['freq_start'], info_dict['freq_size']
    freq_range = (freq_start / 1000, (freq_start + freq_size) / 1000)
    drive_amp = int(info_dict['drive_amp'])

    force_ramp_size = int(info_dict['force_ramp_size'])
    tip_velocity = int(force_ramp_size / durs[-1])

    script_info_dict = OrderedDict()

    script_info_dict['Total # Segments'] = num_segs
    script_info_dict['Total Script Time (s)'] = total_dur

    script_info_dict['Ramp Size (nm)'] = force_ramp_size
    script_info_dict[r'Tip Velocity (nm/s)'] = tip_velocity

    # Basic write controls
    script_info_dict['Write Voltage Range (V)'] = write_voltage_range
    script_info_dict['Write Number of Voltages'] = write_num_voltages + 1

    # Advanced write Controls
    script_info_dict['Write Wave Form'] = write_wave_form
    script_info_dict['Measurements Per Write'] = meas_per_write
    script_info_dict['Write Segment Duration (ms)'] = write_seg_duration
    # the 1st seg is writen
    script_info_dict['Write Samples Per Segment'] = write_samps_per_seg

    # Basic read controls
    script_info_dict['Read Voltage Range (V)'] = read_voltage_range
    script_info_dict['Read Number of Voltages'] = read_num_voltages

    # Advanced read controls
    script_info_dict['Read Wave Form'] = read_wave_form
    script_info_dict['Measurements Per Read'] = meas_per_read
    script_info_dict['Read Segment Duration (ms)'] = read_seg_duration
    script_info_dict['Read Samples Per Segment'] = read_samps_per_seg

    script_info_dict['Frequency Range (kHz)'] = freq_range
    script_info_dict['Drive Amplitude (mV)'] = drive_amp

    return script_info_dict


def tip_bias_analysis(tip_biases_full, num_segs, ttl_outputs_full):
    """
    Return a dictionary of script parameters determined by analyzing the
    pattern of tip bias values in the script

    Parameters
    ----------
    tip_biases_full: list of floats (?)
        A list containing the tip bias of every segment in the script, in order
    num_segs: int
        The number of segments in the script
    ttl_outputs_full: list of floats (?)
        A list containing the TTL output setting of every segment, in order
    """
    # trim off approach and retract segments from end of script
    tip_biases = tip_biases_full[1:-1]
    ttl_outputs = ttl_outputs_full[1:-1]

    # Determine how many write/read segments happen at each write/read
    # voltage step
    first_voltage_count, second_voltage_count = 0, 0

    for tip_bias in tip_biases:
        if tip_bias == tip_biases[0]:
            first_voltage_count += 1
        else:
            break

    for tip_bias in tip_biases[first_voltage_count:]:
        if tip_bias == tip_biases[first_voltage_count]:
            second_voltage_count += 1
        else:
            break

    ind0 = first_voltage_count + second_voltage_count
    ind1 = first_voltage_count - 1
    if tip_biases[ind0] != tip_biases[ind1]:
        # Measurement per write/read
        segs_per_write = first_voltage_count
        segs_per_read = second_voltage_count
    else:
        segs_per_write = second_voltage_count
        segs_per_read = first_voltage_count - second_voltage_count

    # number of segments in a combined read/write step
    segs_per_wr = segs_per_write + segs_per_read

    # determine measurements per write/read by counting write/read segments that
    # do modulation
    meas_per_write = 0
    for i in range(0, segs_per_write):
        if ttl_outputs[i] == 2:
            meas_per_write += 1

    meas_per_read = 0
    for i in range(0, segs_per_read):
        if ttl_outputs[segs_per_write + i] == 2:
            meas_per_read += 1

    write_tip_biases = tip_biases[::segs_per_wr]
    # Exclude one end script generator show (w_step + 1)
    write_num_voltages = len(set(write_tip_biases)) - 1
    write_voltage_range = (
        min(set(write_tip_biases)), max(set(write_tip_biases)))

    read_tip_biases = tip_biases[segs_per_write::segs_per_wr]
    read_num_voltages = len(set(read_tip_biases))
    read_voltage_range = (min(set(read_tip_biases)), max(set(read_tip_biases)))

    # determine write wave form
    if write_tip_biases[0] == write_tip_biases.min():
        write_wave_form = 'Low, up'
    elif write_tip_biases[0] == write_tip_biases.max():
        write_wave_form = 'High, down'
    elif write_tip_biases[0] < write_tip_biases[1]:
        write_wave_form = 'Zero, up'
    else:
        write_wave_form = 'Zero, down'

    # determine read wave form
    if read_num_voltages > 1:
        # negative or 0: l2h; positive: h2l
        r_direct = read_tip_biases[0] - read_tip_biases[write_num_voltages * 2]
        read_wave_form = 'Low to High' if r_direct <= 0 else 'High to Low'
    else:
        read_wave_form = 'Single Read Step'

    # seg_ind = [i for i in range(num_segs)]
    seg_ind = list(range(num_segs))

    write_seg_indices, read_seg_indices = [], []
    for i in range(segs_per_write):
        write_seg_indices += list(seg_ind[(i + 1): -1: segs_per_wr])
    write_seg_indices.sort()
    mw_segs = [write_seg_indices[i::segs_per_write] for i in
               range(segs_per_write)]

    for i in range(segs_per_read):
        read_seg_indices += list(
            seg_ind[(segs_per_write + 1 + i): -1: segs_per_wr])
    read_seg_indices.sort()
    mr_segs = [read_seg_indices[i::segs_per_read] for i in range(segs_per_read)]

    full_len = (num_segs - 2) // read_num_voltages // segs_per_wr
    # length of one r step
    # 'half' length of one r step
    half_len = full_len // 2
    # for wave forms 'Zero, up' or 'Zero, down'
    quar_len_rounded_down = half_len // 2
    quar_len_rounded_up = (half_len + 1) // 2
    # 'trace' here refers to the part of the write wave form where the
    # voltage is increasing and 'retrace' to the part where it's decreasing
    if write_wave_form == 'Low, up':
        # one read step cycle
        t_r_cycle = (['trace'] * half_len + ['retrace'] * half_len)
    if write_wave_form == 'High, down':
        t_r_cycle = (['retrace'] * half_len + ['trace'] * half_len)
    if write_wave_form == 'Zero, up':
        t_r_cycle = ['trace'] * quar_len_rounded_down + [
            'retrace'] * half_len + ['trace'] * quar_len_rounded_up
    if write_wave_form == 'Zero, down':
        t_r_cycle = ['retrace'] * quar_len_rounded_down + [
            'trace'] * half_len + ['retrace'] * quar_len_rounded_up

    m_trace_retrace = t_r_cycle * read_num_voltages

    return dict(segs_per_write=segs_per_write,
                segs_per_read=segs_per_read,
                segs_per_wr=segs_per_wr,
                meas_per_write=meas_per_write,
                meas_per_read=meas_per_read,
                write_wave_form=write_wave_form,
                read_wave_form=read_wave_form,
                write_tip_biases=write_tip_biases,
                write_num_voltages=write_num_voltages,
                write_voltage_range=write_voltage_range,
                read_tip_biases=read_tip_biases,
                read_num_voltages=read_num_voltages,
                read_voltage_range=read_voltage_range,
                mw_segs=mw_segs,
                mr_segs=mr_segs,
                m_trace_retrace=m_trace_retrace
                )
