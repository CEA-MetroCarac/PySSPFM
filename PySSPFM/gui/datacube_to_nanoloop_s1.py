"""
--> Executable Script
Graphical interface for 1st step of SSPFM data analysis
(run datacube_to_nanoloop_s1.main_script)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.data_processing.datacube_to_nanoloop_s1 import main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
     init_secondary_wdw, wdw_main_title)


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
    title = "SSPFM Data Analysis: Step 1 = datacube to nanoloop"
    app = init_secondary_wdw(parent=parent, wdw_title=title)

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
    default_pha_params = {'phase_file_path': '',
                          'method': 'static',
                          'offset': 0}
    default_user_parameters = {'file path in': '',
                               'root out': '',
                               'seg pars': default_seg_params,
                               'fit pars': default_fit_params,
                               'pha pars': default_pha_params,
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
        pha_params = {
            'phase_file_path': extract_var(phase_file_path_var),
            'method': pha_method_var.get(),
            'offset': pha_offset_var.get()
        }
        user_parameters["file path in"] = file_path_in_var.get()
        user_parameters['root out'] = extract_var(root_out_var)
        user_parameters["seg pars"] = seg_params
        user_parameters["fit pars"] = fit_params
        user_parameters["pha pars"] = pha_params
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save'] = save_var.get()

        # Data analysis
        main_script(user_parameters, user_parameters["file path in"],
                    verbose=user_parameters["verbose"],
                    show_plots=user_parameters['show plots'],
                    save=user_parameters['save'],
                    root_out=user_parameters['root out'])

    def browse_directory():
        root_out = filedialog.askdirectory()
        root_out_var.set(root_out)

    def browse_file():
        file_path_in = filedialog.askopenfilename()
        file_path_in_var.set(file_path_in)

    def browse_file_phase():
        phase_file_path_in = filedialog.askopenfilename()
        phase_file_path_var.set(phase_file_path_in)

    # Window title: SSPFM Data Analysis: Step 1 = seg to hyst
    wdw_main_title(app, title)

    row = 3

    # Section title: File management
    label_file = ttk.Label(app, text="File management", font=("Helvetica", 14))
    row = grid_item(label_file, row, column=0, sticky="ew", columnspan=3)

    # File (in)
    label_in = ttk.Label(app, text="File (in):")
    row = grid_item(label_in, row, column=0, sticky="e", increment=False)
    file_path_in_var = tk.StringVar()
    file_path_in_var.set(user_parameters['file path in'])
    entry_in = ttk.Entry(app, textvariable=file_path_in_var)
    row = grid_item(entry_in, row, column=1, sticky="ew", increment=False)
    strg = "- Name: file_path_in\n" \
           "- Summary: Path of datacube SSPFM raw file measurements.\n" \
           "- Description: This parameter specifies the path where " \
           "datacube SSPFM raw file measurements are located. " \
           "It is used to indicate the path to the file containing " \
           "these measurement.\n" \
           "- Value: A string representing the file path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(app, text="Browse", command=browse_file)
    row = grid_item(browse_button_in, row, column=2)

    # Directory (out)
    label_out = ttk.Label(app, text="Directory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
    root_out_var = tk.StringVar()
    root_out_var.set(user_parameters['root out'])
    entry_out = ttk.Entry(app, textvariable=root_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: root_out\n" \
           "- Summary: Saving directory for the result of the analysis " \
           "(optional, default: 'title_meas'_'yyyy-mm-dd-HHhMMm'_out_'mode'" \
           " directory in the same root)\n" \
           "- Description: This parameter specifies the directory where " \
           "the results of the analysis will be saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(app, text="Select", command=browse_directory)
    row = grid_item(browse_button_out, row, column=2)
    row = add_grid_separator(app, row=row)

    # Section title: Segments
    label_seg = ttk.Label(app, text="Segments", font=("Helvetica", 14))
    row = grid_item(label_seg, row, column=0, sticky="ew", columnspan=3)
    strg = "Extraction of PFM amplitude and phase from segment " \
           "and signal treatment of the segment"
    label_seg.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_seg, mess))

    # Mode
    label_mode = ttk.Label(app, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(app, values=["max", "fit", "single_freq", "dfrt"])
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
    label_seg_start = ttk.Label(app, text="Cut segment (start) [%]:")
    row = grid_item(label_seg_start, row, column=0, sticky="e", increment=False)
    start_var = tk.IntVar(
        value=user_parameters['seg pars']['cut seg [%]']['start'])
    scale_seg_start = ttk.Scale(app, from_=1, to=100, variable=start_var,
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
    label_value_start = ttk.Label(app, text=str(start_var.get()))
    row = grid_item(label_value_start, row, column=2, sticky="w")

    # Function to update the label text when the slider is moved
    def update_end_label(_):
        label_value_end.config(text=str(end_var.get()))

    # Cut segment (end)
    label_seg_end = ttk.Label(app, text="Cut segment (end) [%]:")
    row = grid_item(label_seg_end, row, column=0, sticky="e", increment=False)
    end_var = tk.IntVar(
        value=user_parameters['seg pars']['cut seg [%]']['end'])
    scale_seg_end = ttk.Scale(app, from_=1, to=100, variable=end_var,
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
    label_value_end = ttk.Label(app, text=str(end_var.get()))
    row = grid_item(label_value_end, row, column=2, sticky="w")

    # Filter type
    label_filter = ttk.Label(app, text="Filter type:")
    row = grid_item(label_filter, row, column=0, sticky="e", increment=False)
    filter_type_var = ttk.Combobox(app, values=[
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
    label_freq = ttk.Label(app, text="Filter first cutoff frequency:")
    row = grid_item(label_freq, row, column=0, sticky="e", increment=False)
    filter_freq_1_var = tk.StringVar()
    filter_freq_1_var.set(user_parameters['seg pars']['filter freq 1'])
    entry_freq = ttk.Entry(app, textvariable=filter_freq_1_var)
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
    label_freq = ttk.Label(app, text="Filter second cutoff frequency:")
    row = grid_item(label_freq, row, column=0, sticky="e", increment=False)
    filter_freq_2_var = tk.StringVar()
    filter_freq_2_var.set(user_parameters['seg pars']['filter freq 2'])
    entry_freq = ttk.Entry(app, textvariable=filter_freq_2_var)
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
    label_order = ttk.Label(app, text="Filter order:")
    row = grid_item(label_order, row, column=0, sticky="e", increment=False)
    filter_ord_var = tk.IntVar(value=user_parameters['seg pars']['filter ord'])
    scale_order = ttk.Scale(app, from_=1, to=100, variable=filter_ord_var,
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
    filter_ord_label = ttk.Label(app, text=str(filter_ord_var.get()))
    row = grid_item(filter_ord_label, row, column=2, sticky="w")
    row = add_grid_separator(app, row=row)

    # Section title: Fit
    label_fit = ttk.Label(app, text="Fit", font=("Helvetica", 14))
    row = grid_item(label_fit, row, column=0, sticky="ew", columnspan=3)
    strg = "Fit of each segment (amplitude and phase)"
    label_fit.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_fit, mess))

    # Fit phase
    label_fit_pha = ttk.Label(app, text="Fit phase (*):")
    row = grid_item(label_fit_pha, row, column=0, sticky="e", increment=False)
    fit_pha_var = tk.BooleanVar()
    fit_pha_var.set(user_parameters['fit pars']['fit pha'])
    chck_fit_pha = ttk.Checkbutton(app, variable=fit_pha_var)
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
    label_detect = ttk.Label(app, text="Detect peak (*):")
    row = grid_item(label_detect, row, column=0, sticky="e", increment=False)
    detect_peak_var = tk.BooleanVar()
    detect_peak_var.set(user_parameters['fit pars']['detect peak'])
    chck_detect = ttk.Checkbutton(app, variable=detect_peak_var)
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
    label_fwd = ttk.Label(app, text="Sensibility for peak detection (*):")
    row = grid_item(label_fwd, row, column=0, sticky="e", increment=False)
    sens_peak_detect_var = tk.StringVar()
    sens_peak_detect_var.set(user_parameters['fit pars']['sens peak detect'])
    entry_fwd = ttk.Entry(app, textvariable=sens_peak_detect_var)
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
    row = add_grid_separator(app, row=row)

    # Section title: Phase offset
    label_phase = ttk.Label(app, text="Phase offset", font=("Helvetica", 14))
    row = grid_item(label_phase, row, column=0, sticky="ew", columnspan=3)
    strg = "Phase offset analysis"
    label_phase.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_phase, mess))

    # Phase offset file path (in)
    label_phase_file = ttk.Label(app, text="Phase offset file path (in) (*):")
    row = grid_item(label_phase_file, row, column=0, sticky="e",
                    increment=False)
    phase_file_path_var = tk.StringVar()
    phase_file_path_var.set(user_parameters["pha pars"]["phase_file_path"])
    entry_phase_file = ttk.Entry(app, textvariable=phase_file_path_var)
    row = grid_item(entry_phase_file, row, column=1, sticky="ew",
                    increment=False)
    strg = "- Name: phase_file_path\n" \
           "- Summary: Path of phase offset list file " \
           "(optional, default: None)\n" \
           "- Description: This parameter contains the path of phase offset " \
           "list file (On Field / Off Field / Mean) associated to each " \
           "datacube file, to be applied to each file.\n" \
           "If None, phase offset value will be determined with 'static' or " \
           "'dynamic' 'method' parameter.\n" \
           "- Value: It should be a string representing a directory path."
    entry_phase_file.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_phase_file, mess))
    browse_button_phase_file = ttk.Button(app, text="Select",
                                          command=browse_file_phase)
    row = grid_item(browse_button_phase_file, row, column=2)

    # Method
    label_pha_method = ttk.Label(app, text="Method:")
    row = grid_item(label_pha_method, row, column=0, sticky="e",
                    increment=False)
    pha_method_var = ttk.Combobox(app, values=["static", "dynamic"])
    pha_method_var.set(user_parameters["pha pars"]["method"])
    row = grid_item(pha_method_var, row, column=1, sticky="ew")
    strg = "- Name: method\n" \
           "- Summary: Treatment Method for Phase Offset Application on " \
           "Measurements\n" \
           "- Description: This parameter determines the treatment method " \
           "used for phase offset application to measurements. It specifies " \
           "how phase offset is performed in analysis.\n" \
           "- Value: String indicating the method for phase offset " \
           "analysis.\n" \
           "\t--> 'static': Phase offset value remains constant and is " \
           "specified by the user.\n" \
           "\t--> 'dynamic': Phase offset value is determined for each file " \
           "through specific phase analysis and is applied to the subsequent " \
           "file (useful for long measurements with phase drift)." \
           "\t--> None: No phase offset processing is performed: raw phase " \
           "values are used for analysis.\n" \
           "Active if: This parameter is active when 'phase_file_path' " \
           "parameters is None."
    pha_method_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(pha_method_var, mess))

    # Value
    label_value_offset = ttk.Label(app, text="Offset:")
    row = grid_item(label_value_offset, row, column=0, sticky="e",
                    increment=False)
    pha_offset_var = tk.StringVar()
    pha_offset_var.set(user_parameters['pha pars']['offset'])
    entry_fwd = ttk.Entry(app, textvariable=pha_offset_var)
    entry_fwd.grid(row=9, column=1, sticky="ew")
    row = grid_item(entry_fwd, row, column=1, sticky="ew")
    strg = "- Name: offset\n" \
           "- Summary: Phase offset value applied to measurements.\n" \
           "- Description: This parameter allows the user to specify a " \
           "constant phase offset value for the analysis, which is applied " \
           "to all phase values.\n" \
           "- Value: A floating-point number representing the " \
           "phase offset.\n" \
           "- Active if: This parameter is active when 'phase_file_path' " \
           "parameters is None.\n" \
           "If it's the case, this parameter is active " \
           "for the analysis of the first raw measurement file in all cases, " \
           "and for all raw measurement files when the selected 'method' for " \
           "phase offset analysis is 'static'."
    entry_fwd.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_fwd, mess))
    row = add_grid_separator(app, row=row)

    # Section title: Save and plot
    label_chck = ttk.Label(app, text="Plot and save", font=("Helvetica", 14))
    row = grid_item(label_chck, row, column=0, sticky="ew", columnspan=3)

    # Verbose
    label_verb = ttk.Label(app, text="Verbose:")
    row = grid_item(label_verb, row, column=0, sticky="e", increment=False)
    verbose_var = tk.BooleanVar()
    verbose_var.set(user_parameters['verbose'])
    chck_verb = ttk.Checkbutton(app, variable=verbose_var)
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
    label_show = ttk.Label(app, text="Show plots:")
    row = grid_item(label_show, row, column=0, sticky="e", increment=False)
    show_plots_var = tk.BooleanVar()
    show_plots_var.set(user_parameters['show plots'])
    chck_show = ttk.Checkbutton(app, variable=show_plots_var)
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
    label_save = ttk.Label(app, text="Save analysis:")
    row = grid_item(label_save, row, column=0, sticky="e", increment=False)
    save_var = tk.BooleanVar()
    save_var.set(user_parameters['save'])
    chck_save = ttk.Checkbutton(app, variable=save_var)
    row = grid_item(chck_save, row, column=1, sticky="w")
    strg = "- Name: save\n" \
           "- Summary: Activation key for saving results of the analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for saving results generated after the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_save.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_save, mess))
    row = add_grid_separator(app, row=row)

    # Submit button
    submit_button = ttk.Button(app, text="Start", command=launch)
    row = grid_item(submit_button, row, column=0, sticky="e", increment=False)

    def quit_application():
        app.destroy()

    # Exit button
    quit_button = ttk.Button(app, text="Exit", command=quit_application)
    grid_item(quit_button, row, column=1, sticky="ew", increment=False)

    app.mainloop()


if __name__ == '__main__':
    main()
