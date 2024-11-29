"""
--> Executable Script
Graphical interface for automatic determination of phase offset for a list of
raw sspfm measurement file
(run phase_offset_analyzer.main_phase_offset_analyzer)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.toolbox.phase_offset_analyzer import \
    main_phase_offset_analyzer as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
     init_secondary_wdw, wdw_main_title, create_useful_links_button)
from PySSPFM.utils.core.figure import print_plots
from PySSPFM.utils.path_for_runable import save_path_management, create_json_res


def main(parent=None):
    """
    Create a graphical user interface for input parameters.

    Parameters
    ----------
    parent : tk.Tk or tk.Toplevel, optional
        The parent window, if provided, creates a secondary window.

    Returns
    -------
    None
    """
    # Create the main or secondary window
    title = "Phase offset analyzer"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_seg_params = {'cut seg [%]': {'start': 5, 'end': 5},
                          'mode': 'max',
                          'filter type': 'None',
                          'filter freq 1': 1e3,
                          'filter freq 2': 3e3,
                          'filter ord': 4}
    default_fit_params = {'fit pha': False,
                          'detect peak': False,
                          'sens peak detect': 1.5}
    default_user_parameters = {'dir path in': '',
                               'dir path out': '',
                               'range file': 'None',
                               'extension': 'spm',
                               'seg pars': default_seg_params,
                               'fit pars': default_fit_params,
                               'verbose': True,
                               'show plots': True,
                               'save': True}
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        seg_params = {
            'cut seg [%]': {'start': start_var.get(), 'end': end_var.get()},
            'mode': mode_var.get(),
            'filter type': extract_var(filter_type_var),
            'filter freq 1': extract_var(filter_freq_1_var),
            'filter freq 2': extract_var(filter_freq_2_var),
            'filter ord': filter_ord_var.get(),
        }
        fit_params = {
            'fit pha': fit_pha_var.get(),
            'detect peak': detect_peak_var.get(),
            'sens peak detect': extract_var(sens_peak_detect_var)
        }
        user_parameters["dir path in"] = dir_path_in_var.get()
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters["seg pars"] = seg_params
        user_parameters["fit pars"] = fit_params
        user_parameters['range file'] = extract_var(range_file_var)
        user_parameters['extension'] = extension_var.get()
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save'] = save_var.get()

        # Create out directory if not exist
        if user_parameters['save'] is True:
            if user_parameters['dir path out'] is not None:
                if not os.path.exists(user_parameters['dir path out']):
                    os.makedirs(user_parameters['dir path out'])
                    print(f"path created : {user_parameters['dir path out']}")

        # Data analysis
        make_plots = bool(user_parameters['show plots'] or
                          user_parameters['save'])
        _, _, figs = main_script(
            user_parameters, user_parameters["dir path in"],
            range_file=user_parameters['range file'],
            extension=user_parameters['extension'],
            verbose=user_parameters['verbose'], make_plots=make_plots)
        # Plot figures
        print_plots(figs, show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dirname=user_parameters['dir path out'], transparent=False)

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="phase_offset_analyzer_params.json",
                            verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Phase offset analyzer
    wdw_main_title(scrollable_frame, title)

    row = 3

    # Section title: File management
    label_file = ttk.Label(scrollable_frame, text="File management",
                           font=("Helvetica", 14))
    row = grid_item(label_file, row, column=0, sticky="ew", columnspan=3)

    # Directory (in)
    label_in = ttk.Label(scrollable_frame, text="Directory (in):")
    row = grid_item(label_in, row, column=0, sticky="e", increment=False)
    dir_path_in_var = tk.StringVar()
    dir_path_in_var.set(user_parameters['dir path in'])
    entry_in = ttk.Entry(scrollable_frame, textvariable=dir_path_in_var)
    row = grid_item(entry_in, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in\n" \
           "- Summary: Directory path of datacube SSPFM raw file " \
           "measurements.\n" \
           "- Description: This parameter specifies the directory path where " \
           "datacube SSPFM raw file measurements are located. It is used to " \
           "indicate the path to the directory containing these " \
           "measurements.\n" \
           "- Value: A string representing the directory path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(scrollable_frame, text="Browse",
                                  command=browse_dir_in)
    row = grid_item(browse_button_in, row, column=2)

    # Range file
    label_ind = ttk.Label(scrollable_frame, text="File range indices:")
    row = grid_item(label_ind, row, column=0, sticky="e", increment=False)
    range_file_var = tk.StringVar()
    range_file_var.set(str(user_parameters['range file']))
    entry_ref_ind = ttk.Entry(scrollable_frame, textvariable=range_file_var)
    row = grid_item(entry_ref_ind, row, column=1, sticky="ew")
    strg = "- Name: range_file\n" \
           "- Summary: List of Indices Range of Raw Measurement File for " \
           "Phase Offset Analysis\n" \
           "- Description: This parameter is a list that specifies the range " \
           "of indices of raw measurement files to be used for phase offset " \
           "analysis.\n" \
           "- Value: A list with dimensions (2) containing integers.\n" \
           "\t- [first_index_raw_measurement_file, " \
           "last_index_raw_measurement_file]. For example: [1, 10]\n" \
           "\t- If empty or None, all raw measurement files are analyzed."
    entry_ref_ind.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_ref_ind, mess))

    # Extension
    label_extension = ttk.Label(scrollable_frame,
                                text="Extension of raw SSPFM file")
    row = grid_item(label_extension, row, column=0, sticky="e", increment=False)
    extension_var = ttk.Combobox(scrollable_frame,
                                 values=["spm", "txt", "csv", "xlsx"])
    extension_var.set(user_parameters['extension'])
    row = grid_item(extension_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Extension of measurement files.\n" \
           "- Description: This parameter determines the file extension type " \
           "for measurement files.\n" \
           "- Value: A string with four possible values: 'spm', 'txt', " \
           "'csv', or 'xlsx'."
    extension_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(extension_var, mess))

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir = save_path_management(
                input_dir, dir_path_out=None, save=True,
                dirname="map_correlation", lvl=1, create_path=False,
                post_analysis=True)
        else:
            output_dir = ""
        return output_dir

    # Function to update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = dir_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        dir_path_out_var.set(def_output_dir)

    # Bind the function (output dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Directory (out)
    default_input_dir = dir_path_in_var.get()
    default_output_dir = generate_default_output_dir(default_input_dir)
    label_out = ttk.Label(scrollable_frame, text="\tDirectory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
    dir_path_out_var = tk.StringVar()
    dir_path_out_var.set(default_output_dir)
    entry_out = ttk.Entry(scrollable_frame, textvariable=dir_path_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_out\n" \
           "- Summary: Saving directory for analysis results figures " \
           "(optional, default: toolbox directory in the same root)\n" \
           "- Description: This parameter specifies the directory where the " \
           "figures generated as a result of the analysis will be saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(scrollable_frame, text="Select",
                                   command=browse_dir_out)
    row = grid_item(browse_button_out, row, column=2)
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Segments
    label_seg = ttk.Label(scrollable_frame, text="Segments",
                          font=("Helvetica", 14))
    row = grid_item(label_seg, row, column=0, sticky="ew", columnspan=3)
    strg = "Extraction of PFM amplitude and phase from segment " \
           "and signal treatment of the segment"
    label_seg.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_seg, mess))

    # Mode
    label_mode = ttk.Label(scrollable_frame, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(scrollable_frame,
                            values=["max", "fit", "single_freq", "dfrt"])
    mode_var.set(user_parameters['seg pars']['mode'])
    row = grid_item(mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Treatment method for extracting PFM amplitude and " \
           "phase from segments and signal treatment within the segment.\n" \
           "- Description: This parameter determines the treatment " \
           "method used for data analysis, specifically for " \
           "extracting PFM amplitude and phase data from segments and " \
           "for signal treatment within the segment.\n" \
           "- Value: A string with four possible values:\n" \
           "\t--> 'max': Peak maximum treatment " \
           "(frequency sweep in resonance)\n" \
           "\t--> 'fit': Peak fit treatment " \
           "(frequency sweep in resonance)\n," \
           "\t--> 'single_freq': Average of segment (single frequency, " \
           "in or out of resonance)\n," \
           "\t--> 'dfrt': Average of segment (dfrt)"
    mode_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(mode_var, mess))

    # Function to update the label text when the slider is moved
    def update_start_label(_):
        label_value_start.config(text=str(start_var.get()))

    # Cut segment (start)
    label_seg_start = ttk.Label(scrollable_frame,
                                text="Cut segment (start) [%]:")
    row = grid_item(label_seg_start, row, column=0, sticky="e", increment=False)
    start_var = tk.IntVar(
        value=user_parameters['seg pars']['cut seg [%]']['start'])
    scale_seg_start = ttk.Scale(scrollable_frame, from_=1, to=100,
                                variable=start_var,
                                orient="horizontal", length=100,
                                command=update_start_label)
    row = grid_item(scale_seg_start, row, column=1, sticky="ew",
                    increment=False)
    strg = "- Name: cut_seg_perc\n" \
           "- Summary: Segment Trimming Percentage (start)\n" \
           "- Description: This parameter specifies the percentage of the " \
           "segment length to be trimmed from the start of each" \
           " segment. It allows you to exclude a certain portion of each " \
           "segment from analysis at the beginning.\n" \
           "- Value: Integer value (in term of %)"
    scale_seg_start.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(scale_seg_start, mess))
    label_value_start = ttk.Label(scrollable_frame, text=str(start_var.get()))
    row = grid_item(label_value_start, row, column=2, sticky="w")

    # Function to update the label text when the slider is moved
    def update_end_label(_):
        label_value_end.config(text=str(end_var.get()))

    # Cut segment (end)
    label_seg_end = ttk.Label(scrollable_frame, text="Cut segment (end) [%]:")
    row = grid_item(label_seg_end, row, column=0, sticky="e", increment=False)
    end_var = tk.IntVar(
        value=user_parameters['seg pars']['cut seg [%]']['end'])
    scale_seg_end = ttk.Scale(scrollable_frame, from_=1, to=100,
                              variable=end_var,
                              orient="horizontal", length=100,
                              command=update_end_label)
    row = grid_item(scale_seg_end, row, column=1, sticky="ew", increment=False)
    strg = "- Name: cut_seg_perc\n" \
           "- Summary: Segment Trimming Percentage (end)\n" \
           "- Description: This parameter specifies the percentage of the " \
           "segment length to be trimmed from the end of each" \
           " segment. It allows you to exclude a certain portion of each " \
           "segment from analysis at the end.\n" \
           "- Value: Integer value (in term of %)"
    scale_seg_end.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(scale_seg_end, mess))
    label_value_end = ttk.Label(scrollable_frame, text=str(end_var.get()))
    row = grid_item(label_value_end, row, column=2, sticky="w")

    # Filter type
    label_filter = ttk.Label(scrollable_frame, text="Filter type:")
    row = grid_item(label_filter, row, column=0, sticky="e", increment=False)
    filter_type_var = ttk.Combobox(scrollable_frame, values=[
        "mean", "low", "high", "bandpass", "bandstop", "None"])
    filter_type_var.set(user_parameters['seg pars']['filter type'])
    row = grid_item(filter_type_var, row, column=1, sticky="ew")
    strg = "- Name: filter_type\n" \
           "- Summary: Type of Filter for Measurements.\n" \
           "- Description: This parameter specifies the type of filter to be " \
           "applied to the measurements.\n" \
           "- Value: A string with six possible values:\n" \
           "\t--> 'mean': Apply a Mean filter.\n" \
           "\t--> 'low': Apply a Low Butterworth filter.\n" \
           "\t--> 'high': Apply a High Butterworth filter.\n" \
           "\t--> 'bandpass': Apply a Bandpass Butterworth filter.\n" \
           "\t--> 'bandstop': Apply a Bandstop Butterworth filter.\n" \
           "\t--> None: Do not apply any filter."
    filter_type_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(filter_type_var, mess))

    # Filter first cutoff frequency
    label_freq = ttk.Label(scrollable_frame,
                           text="Filter first cutoff frequency:")
    row = grid_item(label_freq, row, column=0, sticky="e", increment=False)
    filter_freq_1_var = tk.StringVar()
    filter_freq_1_var.set(user_parameters['seg pars']['filter freq 1'])
    entry_freq = ttk.Entry(scrollable_frame, textvariable=filter_freq_1_var)
    entry_freq.grid(row=9, column=1, sticky="ew")
    row = grid_item(entry_freq, row, column=1, sticky="ew")
    strg = "- Name: filter_freq_1\n" \
           "- Summary: Filter Cutoff Frequency, First Value.\n" \
           "- Description: This parameter controls the cutoff frequency in " \
           "Hz of the filter used.\n" \
           "- Value: Float representing single cutoff frequency value if the " \
           "filter type is 'low' or 'high', or the first cutoff frequency " \
           "value if the  filter type is 'bandpass' or 'bandstop'.\n" \
           "- Active if: This parameter is active when the 'filter type' " \
           "option is neither 'mean' nor None."
    entry_freq.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_freq, mess))

    # Filter second cutoff frequency
    label_freq = ttk.Label(scrollable_frame,
                           text="Filter second cutoff frequency:")
    row = grid_item(label_freq, row, column=0, sticky="e", increment=False)
    filter_freq_2_var = tk.StringVar()
    filter_freq_2_var.set(user_parameters['seg pars']['filter freq 2'])
    entry_freq = ttk.Entry(scrollable_frame, textvariable=filter_freq_2_var)
    entry_freq.grid(row=9, column=1, sticky="ew")
    row = grid_item(entry_freq, row, column=1, sticky="ew")
    strg = "- Name: filter_freq_2\n" \
           "- Summary: Filter Cutoff Frequency, Second Value.\n" \
           "- Description: This parameter controls the cutoff frequency in " \
           "Hz of the filter used.\n" \
           "- Value: Float representing second cutoff frequency value if the " \
           "filter type is 'bandpass' or 'bandstop'.\n" \
           "- Active if: This parameter is active when the 'filter type' " \
           "option is either 'bandpass' or 'bandstop'."
    entry_freq.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_freq, mess))

    # Function to update the label text when the slider is moved
    def update_filter_ord_label(_):
        filter_ord_label.config(text=str(filter_ord_var.get()))

    # Filter older
    label_order = ttk.Label(scrollable_frame, text="Filter order:")
    row = grid_item(label_order, row, column=0, sticky="e", increment=False)
    filter_ord_var = tk.IntVar(value=user_parameters['seg pars']['filter ord'])
    scale_order = ttk.Scale(scrollable_frame, from_=1, to=100,
                            variable=filter_ord_var,
                            orient="horizontal", length=100,
                            command=update_filter_ord_label)
    row = grid_item(scale_order, row, column=1, sticky="ew", increment=False)
    strg = "- Name: filter_ord\n" \
           "- Summary: Filter Order.\n" \
           "- Description: This parameter controls the order of the filter " \
           "used. A higher value results in stronger filtering of the " \
           "signal.\n" \
           "- Value: An integer value, with a minimum value of 1.\n" \
           "- Active if: This parameter is active when the 'filter type' " \
           "option is not None."
    scale_order.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(scale_order, mess))
    filter_ord_label = ttk.Label(scrollable_frame,
                                 text=str(filter_ord_var.get()))
    row = grid_item(filter_ord_label, row, column=2, sticky="w")
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Fit
    label_fit = ttk.Label(scrollable_frame, text="Fit", font=("Helvetica", 14))
    row = grid_item(label_fit, row, column=0, sticky="ew", columnspan=3)
    strg = "Fit of each segment (amplitude and phase)"
    label_fit.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_fit, mess))

    # Fit phase
    label_fit_pha = ttk.Label(scrollable_frame, text="Fit phase (*):")
    row = grid_item(label_fit_pha, row, column=0, sticky="e", increment=False)
    fit_pha_var = tk.BooleanVar()
    fit_pha_var.set(user_parameters['fit pars']['fit pha'])
    chck_fit_pha = ttk.Checkbutton(scrollable_frame, variable=fit_pha_var)
    row = grid_item(chck_fit_pha, row, column=1, sticky="w")
    strg = "- Name: fit_pha\n" \
           "- Summary: Phase measurement fitting indicator.\n" \
           "- Description: This parameter is used to determine whether " \
           "phase measurements should be fitted during data processing.\n" \
           "- Value: Boolean (True or False).\n" \
           "- Active if: This parameter can be active when the data " \
           "processing mode is set to 'fit.'"
    chck_fit_pha.bind("<Enter>",
                      lambda event, mess=strg: show_tooltip(chck_fit_pha, mess))

    # Detect peak
    label_detect = ttk.Label(scrollable_frame, text="Detect peak (*):")
    row = grid_item(label_detect, row, column=0, sticky="e", increment=False)
    detect_peak_var = tk.BooleanVar()
    detect_peak_var.set(user_parameters['fit pars']['detect peak'])
    chck_detect = ttk.Checkbutton(scrollable_frame, variable=detect_peak_var)
    row = grid_item(chck_detect, row, column=1, sticky="w")
    strg = "- Name: detect_peak\n" \
           "- Summary: Peak detection for peak fitting.\n" \
           "- Description: This parameter controls the peak detection " \
           "for segments during data processing. When set to True, " \
           "it enables the detection of segments for which there is no " \
           "peak, and the fitting process is not performed for those " \
           "segments.\n" \
           "- Value: Boolean (True or False).\n" \
           "- Active if: This parameter is active when the 'fit' mode is " \
           "selected."
    chck_detect.bind("<Enter>",
                     lambda event, mess=strg: show_tooltip(chck_detect, mess))

    # Sensibility for peak detection
    label_fwd = ttk.Label(scrollable_frame,
                          text="Sensibility for peak detection (*):")
    row = grid_item(label_fwd, row, column=0, sticky="e", increment=False)
    sens_peak_detect_var = tk.StringVar()
    sens_peak_detect_var.set(user_parameters['fit pars']['sens peak detect'])
    entry_fwd = ttk.Entry(scrollable_frame, textvariable=sens_peak_detect_var)
    entry_fwd.grid(row=9, column=1, sticky="ew")
    row = grid_item(entry_fwd, row, column=1, sticky="ew")
    strg = "- Name: sens_peak_detect\n" \
           "- Summary: Sensitivity of peak detection.\n" \
           "- Description: This parameter determines how " \
           "sensitive the peak detection algorithm is. A higher value " \
           "makes the peak detection process more stringent, meaning " \
           "it will be harder to detect peaks.\n" \
           "- Value: A floating-point number representing the " \
           "sensitivity level.\n" \
           "- Active if: This parameter is active when the 'fit' mode is " \
           "selected and peak detection is enabled."
    entry_fwd.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_fwd, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Save and plot
    label_chck = ttk.Label(scrollable_frame, text="Plot and save",
                           font=("Helvetica", 14))
    row = grid_item(label_chck, row, column=0, sticky="ew", columnspan=3)

    # Verbose
    label_verb = ttk.Label(scrollable_frame, text="Verbose:")
    row = grid_item(label_verb, row, column=0, sticky="e", increment=False)
    verbose_var = tk.BooleanVar()
    verbose_var.set(user_parameters['verbose'])
    chck_verb = ttk.Checkbutton(scrollable_frame, variable=verbose_var)
    row = grid_item(chck_verb, row, column=1, sticky="w")
    strg = "- Name: verbose\n" \
           "- Summary: Activation key for printing verbosity during " \
           "analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for printing verbose information during the analysis.\n" \
           "- Value: Boolean (True or False)."
    chck_verb.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_verb, mess))

    # Show plots
    label_show = ttk.Label(scrollable_frame, text="Show plots:")
    row = grid_item(label_show, row, column=0, sticky="e", increment=False)
    show_plots_var = tk.BooleanVar()
    show_plots_var.set(user_parameters['show plots'])
    chck_show = ttk.Checkbutton(scrollable_frame, variable=show_plots_var)
    row = grid_item(chck_show, row, column=1, sticky="w")
    strg = "- Name: show_plots\n" \
           "- Summary: Activation key for generating matplotlib figures " \
           "during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for generating matplotlib figures during the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_show.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_show, mess))

    # Save analysis
    label_save = ttk.Label(scrollable_frame, text="Save analysis:")
    row = grid_item(label_save, row, column=0, sticky="e", increment=False)
    save_var = tk.BooleanVar()
    save_var.set(user_parameters['save'])
    chck_save = ttk.Checkbutton(scrollable_frame, variable=save_var)
    row = grid_item(chck_save, row, column=1, sticky="w")
    strg = "- Name: save\n" \
           "- Summary: Activation key for saving results of the analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for saving results generated after the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_save.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_save, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Submit button
    submit_button = ttk.Button(scrollable_frame, text="Start", command=launch)
    row = grid_item(submit_button, row, column=0, sticky="e", increment=False)

    def quit_application():
        app.destroy()

    # Exit button
    quit_button = ttk.Button(scrollable_frame, text="Exit",
                             command=quit_application)
    row = grid_item(quit_button, row, column=1, sticky="ew", increment=False)
    row = add_grid_separator(scrollable_frame, row=row)
    row = add_grid_separator(scrollable_frame, row=row)

    links_frame = ttk.Frame(scrollable_frame)
    label_links = ttk.Label(scrollable_frame, text="Useful Links", font=("Helvetica", 14))
    row = grid_item(label_links, row, column=0, sticky="ew", columnspan=3)
    grid_item(links_frame, row, column=0, columnspan=3)
    create_useful_links_button(links_frame)

    app.mainloop()


if __name__ == '__main__':
    main()
