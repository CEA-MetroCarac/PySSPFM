"""
--> Executable Script
Graphical interface for 2nd step of SSPFM data analysis
(run nanoloop_to_hyst_s2.main_script)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np

from PySSPFM.data_processing.nanoloop_to_hyst_s2 import main_script
from PySSPFM.gui.utils import \
    (grid_item, add_grid_separator, show_tooltip, extract_var,
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
    title = "SSPFM Data Analysis: Step 2 = nanoloop to hyst"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'dir path in': '',
        'root out': '',
        'func': 'sigmoid',
        'method': 'least_square',
        'asymmetric': False,
        'inf thresh': 10,
        'sat thresh': 90,
        'del 1st loop': True,
        'pha corr': 'raw',
        'pha fwd': 0,
        'pha rev': 180,
        'pha func': 'cosine',
        'main_elec_file_path': '',
        'main elec': True,
        'locked elec slope': 'None',
        'diff mode': 'set',
        'diff domain': {'min': -5., 'max': 5.},
        'sat mode': 'set',
        'sat domain': {'min': -9., 'max': 9.},
        'verbose': True,
        'show plots': True,
        'save': True
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['root out'] = extract_var(root_out_var)
        user_parameters['func'] = func_var.get()
        user_parameters['method'] = method_var.get()
        user_parameters['asymmetric'] = asymmetric_var.get()
        user_parameters['inf thresh'] = inf_thresh_var.get()
        user_parameters['sat thresh'] = sat_thresh_var.get()
        user_parameters['del 1st loop'] = del_1st_loop_var.get()
        user_parameters['pha corr'] = phase_mode_var.get()
        user_parameters['pha fwd'] = extract_var(pha_fwd_var)
        user_parameters['pha rev'] = extract_var(pha_rev_var)
        user_parameters['pha func'] = np.cos \
            if func_pha_var.get() == 'cosine' else np.sin
        user_parameters['main_elec_file_path'] = \
            extract_var(main_elec_file_path_var)
        user_parameters['main elec'] = main_elec_var.get()
        user_parameters['locked elec slope'] = \
            extract_var(locked_elec_slope_var)
        user_parameters['diff mode'] = diff_mode_var.get()
        user_parameters['diff domain']['min'] = extract_var(diff_domain_min_var)
        user_parameters['diff domain']['max'] = extract_var(diff_domain_max_var)
        user_parameters['sat mode'] = sat_mode_var.get()
        user_parameters['sat domain']['min'] = extract_var(sat_domain_min_var)
        user_parameters['sat domain']['max'] = extract_var(sat_domain_max_var)
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save'] = save_var.get()

        # Data analysis
        main_script(user_parameters, user_parameters['dir path in'],
                    verbose=user_parameters["verbose"],
                    show_plots=user_parameters['show plots'],
                    save=user_parameters['save'],
                    root_out=user_parameters['root out'])

    def browse_directory():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_file():
        file_path_in = filedialog.askopenfilename()
        main_elec_file_path_var.set(file_path_in)

    # Window title: SSPFM Data Analysis: Step 2 = hyst to map
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
           "- Summary: Directory path for text nanoloop files generated " \
           "after the first step of the analysis (default: 'nanoloops')\n" \
           "- Description: This parameter specifies the directory path" \
           " where the text nanoloop files generated after the first step " \
           "of the analysis are located.\n" \
           "- Value: String (directory path)."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(scrollable_frame, text="Browse",
                                  command=browse_directory)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir, _ = os.path.split(input_dir)
        else:
            output_dir = ""
        return output_dir

    # Function to update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = dir_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        root_out_var.set(def_output_dir)

    # Bind the function (output dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Directory (out)
    label_out = ttk.Label(scrollable_frame, text="Directory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
    root_out_var = tk.StringVar()
    default_input_dir = dir_path_in_var.get()
    default_output_dir = generate_default_output_dir(default_input_dir)
    root_out_var.set(default_output_dir)
    entry_out = ttk.Entry(scrollable_frame, textvariable=root_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: root_out\n" \
           "- Summary: Saving directory for the result of the analysis " \
           "(optional, default: 'title_'_'yyyy-mm-dd-HHhMMm'_out_'mode'" \
           " directory in the same root)\n" \
           "- Description: This parameter specifies the directory where " \
           "the results of the analysis will be saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(scrollable_frame, text="Select",
                                   command=browse_directory)
    row = grid_item(browse_button_out, row, column=2)
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Hysteresis treatment
    label_hyst = ttk.Label(scrollable_frame, text="Hysteresis treatment",
                           font=("Helvetica", 14))
    row = grid_item(label_hyst, row, column=0, sticky="ew", columnspan=3)
    strg = "Parameters for hysteresis fit and properties extraction"
    label_hyst.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_hyst, mess))

    # Fit function
    label_func = ttk.Label(scrollable_frame, text="Function:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    func_var = ttk.Combobox(scrollable_frame, values=["sigmoid", "arctan"])
    func_var.set(user_parameters['func'])
    row = grid_item(func_var, row, column=1, sticky="ew")
    strg = "- Name: func\n" \
           "- Summary: Function used for hysteresis fit.\n" \
           "- Description: This parameter specifies the algebraic function " \
           "used to fit hysteresis branches.\n" \
           "- Value: String ('sigmoid' or 'arctan')."
    func_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(func_var, mess))

    # Fit method
    label_method = ttk.Label(scrollable_frame, text="Method:")
    row = grid_item(label_method, row, column=0, sticky="e", increment=False)
    method_var = ttk.Combobox(scrollable_frame,
                              values=["leastsq", "least_square", "nelder"])
    method_var.set(user_parameters['method'])
    row = grid_item(method_var, row, column=1, sticky="ew")
    strg = "- Name: method\n" \
           "- Summary: Method used for the fit.\n" \
           "- Description: This parameter specifies the fitting method used " \
           "for the analysis.\n" \
           "- Value: String ('leastsq' or 'least_square': " \
           "faster but harder to converge // 'nelder': vice versa)."
    method_var.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(method_var, mess))

    # Asymmetric fit
    label_asym = ttk.Label(scrollable_frame, text="Asymmetric:")
    row = grid_item(label_asym, row, column=0, sticky="e", increment=False)
    asymmetric_var = tk.BooleanVar()
    asymmetric_var.set(user_parameters['asymmetric'])
    chck_asym = ttk.Checkbutton(scrollable_frame, variable=asymmetric_var)
    row = grid_item(chck_asym, row, column=1, sticky="w")
    strg = "- Name: asymmetric\n" \
           "- Summary: Asymmetric Hysteresis Fit\n" \
           "- Description: This parameter determines whether an asymmetric " \
           "fit of hysteresis should be performed. An asymmetric fit " \
           "allows each branch of the hysteresis curve to have a " \
           "different slope coefficient.\n" \
           "- Value: Boolean (True or False)."
    chck_asym.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_asym, mess))

    # Function to update the label text when the slider is moved
    def update_inf_thresh_label(_):
        label_value_inf.config(text=str(inf_thresh_var.get()))

    # Inflection Threshold
    label_thresh_inf = ttk.Label(scrollable_frame,
                                 text="Inflection threshold [%]:")
    row = grid_item(label_thresh_inf, row, column=0, sticky="e",
                    increment=False)
    inf_thresh_var = tk.IntVar(value=user_parameters['inf thresh'])
    scale_thresh_inf = ttk.Scale(scrollable_frame, from_=1, to=100,
                                 variable=inf_thresh_var,
                                 orient="horizontal", length=100,
                                 command=update_inf_thresh_label)
    row = grid_item(scale_thresh_inf, row, column=1, sticky="ew",
                    increment=False)
    strg = "- Name: inf_thresh\n" \
           "- Summary: Inflection Point Threshold\n" \
           "- Description: This parameter defines the threshold, " \
           "expressed as a percentage of the hysteresis amplitude, " \
           "used to calculate the value of the inflection point at " \
           "the beginning of the hysteresis switch.\n" \
           "- Value: Float, representing the threshold percentage."
    scale_thresh_inf.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(scale_thresh_inf, mess))
    label_value_inf = ttk.Label(scrollable_frame,
                                text=str(inf_thresh_var.get()))
    row = grid_item(label_value_inf, row, column=2, sticky="w")

    # Function to update the label text when the slider is moved
    def update_sat_thresh_label(_):
        label_value_sat.config(text=str(sat_thresh_var.get()))

    # Saturation Threshold
    label_thresh_sat = ttk.Label(scrollable_frame,
                                 text="Saturation threshold [%]:")
    row = grid_item(label_thresh_sat, row, column=0, sticky="e",
                    increment=False)
    sat_thresh_var = tk.IntVar(value=user_parameters['sat thresh'])
    scale_thresh_sat = ttk.Scale(scrollable_frame, from_=1, to=100,
                                 variable=sat_thresh_var,
                                 orient="horizontal", length=100,
                                 command=update_sat_thresh_label)
    row = grid_item(scale_thresh_sat, row, column=1, sticky="ew",
                    increment=False)
    strg = "- Name: sat_thresh\n" \
           "- Summary: Saturation Point Threshold\n" \
           "- Description: This parameter defines the threshold, " \
           "expressed as a percentage of the hysteresis amplitude, " \
           "used to calculate the value of the saturation point at " \
           "the end of the hysteresis switch.\n" \
           "- Value: Float, representing the threshold percentage."
    scale_thresh_sat.bind("<Enter>", lambda event, mess=strg: show_tooltip(
        scale_thresh_sat, mess))
    label_value_sat = ttk.Label(scrollable_frame,
                                text=str(sat_thresh_var.get()))
    row = grid_item(label_value_sat, row, column=2, sticky="w")

    # Del First Loop
    label_del = ttk.Label(scrollable_frame, text="Delete First Loop:")
    row = grid_item(label_del, row, column=0, sticky="e", increment=False)
    del_1st_loop_var = tk.BooleanVar()
    del_1st_loop_var.set(user_parameters['del 1st loop'])
    chck_del = ttk.Checkbutton(scrollable_frame, variable=del_1st_loop_var)
    row = grid_item(chck_del, row, column=1, sticky="w")
    strg = "- Name: del_1st_loop\n" \
           "- Summary: Delete First Loop\n" \
           "- Description: If this parameter is set to True, it " \
           "deletes the first loop of the analysis, which is typically " \
           "used for calculating the mean hysteresis.\nThis can be " \
           "useful when the first write voltage values are equal to " \
           "zero, indicating that the material is in a pristine state, " \
           "and the loop shape would be different from the polarized state. " \
           "Deleting the first loop helps to avoid artifacts in the " \
           "analysis.\n" \
           "- Value: Boolean (True or False)"
    chck_del.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(chck_del, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Phase treatment
    label_pha = ttk.Label(scrollable_frame, text="Phase treatment",
                          font=("Helvetica", 14))
    row = grid_item(label_pha, row, column=0, sticky="ew", columnspan=3)
    strg = "Parameters for phase calibration"
    label_pha.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_pha, mess))

    # Correction Method
    label_corr = ttk.Label(scrollable_frame, text="Correction Method:")
    row = grid_item(label_corr, row, column=0, sticky="e", increment=False)
    phase_mode_var = ttk.Combobox(scrollable_frame,
                                  values=["raw", "offset", "affine", "up_down"])
    phase_mode_var.set(user_parameters['pha corr'])
    row = grid_item(phase_mode_var, row, column=1, sticky="w")
    strg = "- Name: pha_corr\n" \
           "- Summary: Phase Correction Mode\n" \
           "- Description: This parameter specifies the correction mode " \
           "for the value of the phase nanoloop. " \
           "There are four possible correction modes:\n" \
           "\t- 'raw': No correction is applied.\n" \
           "\t- 'offset': Offset correction is applied.\n" \
           "\t- 'affine': Affine correction is applied.\n" \
           "\t- 'up_down': Phase is set to the up value or down value.\n" \
           "- Value: String (one of 'raw', 'offset', 'affine', 'up_down')"
    phase_mode_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(phase_mode_var, mess))

    # Phase Forward Value
    label_fwd = ttk.Label(scrollable_frame, text="Phase Forward Value:")
    row = grid_item(label_fwd, row, column=0, sticky="e", increment=False)
    pha_fwd_var = tk.StringVar()
    pha_fwd_var.set(user_parameters['pha fwd'])
    entry_fwd = ttk.Entry(scrollable_frame, textvariable=pha_fwd_var)
    row = grid_item(entry_fwd, row, column=1, sticky="ew")
    strg = "- Name: pha_fwd\n" \
           "- Summary: Phase Forward Target Value\n" \
           "- Description: This parameter represents the target value " \
           "for the phase in the forward direction. It is used to generate" \
           " a multiplied coefficient equal to 1 between amplitude and " \
           "piezoresponse.\n" \
           "- Value: Float"
    entry_fwd.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_fwd, mess))

    # Phase Reverse Value
    label_rev = ttk.Label(scrollable_frame, text="Phase Reverse Value:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    pha_rev_var = tk.StringVar()
    pha_rev_var.set(user_parameters['pha rev'])
    entry_rev = ttk.Entry(scrollable_frame, textvariable=pha_rev_var)
    row = grid_item(entry_rev, row, column=1, sticky="ew")
    strg = "- Name: pha_rev\n" \
           "- Summary: Phase Reverse Target Value\n" \
           "- Description: This parameter represents the target value " \
           "for the phase in the reverse direction. It is used to generate" \
           " a multiplied coefficient equal to -1 between amplitude " \
           "and piezoresponse.\n" \
           "- Value: Float"
    entry_rev.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_rev, mess))

    # Function for Piezoresponse
    label_func_pha = ttk.Label(scrollable_frame,
                               text="Function for Piezoresponse:")
    row = grid_item(label_func_pha, row, column=0, sticky="e", increment=False)
    func_pha_var = ttk.Combobox(scrollable_frame, values=["cosine", "sine"])
    func_pha_var.set(user_parameters['pha func'])
    row = grid_item(func_pha_var, row, column=1, sticky="ew")
    strg = "- Name: pha_func\n" \
           "- Summary: Piezoresponse Function\n" \
           "- Description: This parameter represents the function used " \
           "to determine the piezoresponse from amplitude and phase. " \
           "The piezoresponse (PR) is calculated as PR = amp * func(pha), " \
           "where 'amp' is the amplitude and 'pha' is the phase.\n" \
           "- Value: Algebraic function ('sine' or 'cosine')"
    func_pha_var.bind("<Enter>",
                      lambda event, mess=strg: show_tooltip(func_pha_var, mess))

    # Main electrostatic file path (in)
    label_elec_file = ttk.Label(scrollable_frame,
                                text="Main electrostatic file path (in) (*):")
    row = grid_item(label_elec_file, row, column=0, sticky="e",
                    increment=False)
    main_elec_file_path_var = tk.StringVar()
    main_elec_file_path_var.set(user_parameters['main_elec_file_path'])
    entry_elec_file = ttk.Entry(scrollable_frame,
                                textvariable=main_elec_file_path_var)
    row = grid_item(entry_elec_file, row, column=1, sticky="ew",
                    increment=False)
    strg = "- Name: main_elec_file_path\n" \
           "- Summary: Path of boolean values for dominant electrostatics in " \
           "on field mode for each file (optional, default: None)\n" \
           "- Description: This parameter contains the path of boolean value " \
           "for dominant electrostatics in on field mode for each file. It " \
           "determines whether the electrostatics are higher than " \
           "ferroelectric effects.\n" \
           "In other words, it indicates if the electrostatics are " \
           "responsible for the phase loop's sense of rotation in the " \
           "On Field mode.\n" \
           "If None, the value will be determined with 'main_elec' " \
           "parameter.\n" \
           "- Value: It should be a string representing a directory path."
    entry_elec_file.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_elec_file, mess))
    browse_button_elec_file = ttk.Button(scrollable_frame, text="Select",
                                         command=browse_file)
    row = grid_item(browse_button_elec_file, row, column=2)

    # Main Electrostatic
    label_elec = ttk.Label(scrollable_frame, text="Main Electrostatic:")
    row = grid_item(label_elec, row, column=0, sticky="e", increment=False)
    main_elec_var = tk.BooleanVar()
    main_elec_var.set(user_parameters['main elec'])
    chck_elec = ttk.Checkbutton(scrollable_frame, variable=main_elec_var)
    row = grid_item(chck_elec, row, column=1, sticky="w")
    strg = "- Name: main_elec\n" \
           "- Summary: Dominant Electrostatics in On Field Mode\n" \
           "- Description: It determines whether the electrostatics are " \
           "higher than ferroelectric effects. In other words, it " \
           "indicates if the electrostatics are responsible for the " \
           "phase loop's sense of rotation in the On Field mode.\n" \
           "- Value: Boolean\n" \
           "- Active if: 'phase_file_path' parameters is None and if " \
           "On Field mode is selected."
    chck_elec.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_elec, mess))

    # Locked Electrostatic Slope
    label_slope = ttk.Label(scrollable_frame,
                            text="Locked Electrostatic Slope:")
    row = grid_item(label_slope, row, column=0, sticky="e", increment=False)
    locked_elec_slope_var = ttk.Combobox(
        scrollable_frame, values=["None", "negative", "positive"])
    locked_elec_slope_var.set(user_parameters['locked elec slope'])
    row = grid_item(locked_elec_slope_var, row, column=1, sticky="ew")
    strg = "- Name: locked_elec_slope\n" \
           "- Summary: Locked Electrostatic Slope\n" \
           "- Description: It specifies and locked the sign of the " \
           "electrostatic slope in the loop whatever measurement " \
           "parameters (theory: grounded tip: negative, bottom: positive).\n" \
           "- Value: 'negative', 'positive', or None\n" \
           "- Active if: On Field mode is selected."
    locked_elec_slope_var.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(locked_elec_slope_var, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Differential treatment
    label_diff = ttk.Label(scrollable_frame, text="Differential treatment",
                           font=("Helvetica", 14))
    row = grid_item(label_diff, row, column=0, sticky="ew", columnspan=3)
    strg = "Parameters to determine linear part for differential loop.\n" \
           "Active if: Differential mode is selected."
    label_diff.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_diff, mess))

    # Differential mode
    label_man = ttk.Label(scrollable_frame, text="Mode:")
    row = grid_item(label_man, row, column=0, sticky="e", increment=False)
    diff_mode_var = ttk.Combobox(scrollable_frame, values=["set", "auto"])
    diff_mode_var.set(user_parameters['diff mode'])
    row = grid_item(diff_mode_var, row, column=1, sticky="ew")
    strg = "- Name: diff_mode\n" \
           "- Summary: Differential Analysis Mode\n" \
           "- Description: This parameter determines the mode for " \
           "conducting differential analysis, which helps in identifying " \
           "the linear part of the differential loop. The specific mode " \
           "can be set by the user or determined automatically.\n" \
           "- Value: String indicating the mode for differential " \
           "analysis.\n" \
           "\t--> 'set' (user-defined linear differential domain in " \
           "diff_domain parameter)\n" \
           "\t--> 'auto' (automatic calculation).\n" \
           "- Active if: Differential mode is selected."
    diff_mode_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(diff_mode_var, mess))

    # Differential Domain Min
    label_min = ttk.Label(scrollable_frame, text="Min limit (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    diff_domain_min_var = tk.StringVar()
    diff_domain_min_var.set(user_parameters['diff domain']['min'])
    entry_min = ttk.Entry(scrollable_frame, textvariable=diff_domain_min_var)
    row = grid_item(entry_min, row, column=1, sticky="ew")
    strg = "- Name: diff_domain (min)\n" \
           "- Summary: Voltage Range for Linear Differential Component " \
           "(Min Limit)\n" \
           "- Description: This parameter defines the voltage range " \
           "considered for the linear part of the differential component. " \
           "Value specifying the minumum voltage range for differential " \
           "analysis\n" \
           "- Value: float\n" \
           "\tIf left empty or set to None, no minimum limit is applied.\n" \
           "- Active if: Differential mode is selected and automatic " \
           "differential domain determination is not enabled " \
           "(diff_domain_man is set to False)."
    entry_min.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_min, mess))

    # Differential Domain Max
    label_max = ttk.Label(scrollable_frame, text="Max limit (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    diff_domain_max_var = tk.StringVar()
    diff_domain_max_var.set(user_parameters['diff domain']['max'])
    entry_max = ttk.Entry(scrollable_frame, textvariable=diff_domain_max_var)
    row = grid_item(entry_max, row, column=1, sticky="ew")
    strg = "- Name: diff_domain (max)\n" \
           "- Summary: Voltage Range for Linear Differential Component " \
           "(Max Limit)\n" \
           "- Description: This parameter defines the voltage range " \
           "considered for the linear part of the differential component. " \
           "Value specifying the maximum voltage range for differential " \
           "analysis\n" \
           "- Value: float\n" \
           "\tIf left empty or set to None, no maximum limit is applied.\n" \
           "- Active if: Differential mode is selected and automatic " \
           "differential domain determination is not enabled " \
           "(diff_domain_man is set to False)."
    entry_max.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_max, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Electrostatic decoupling saturation treatment
    label_sat = ttk.Label(scrollable_frame,
                          text="Electrostatic decoupling (saturation)",
                          font=("Helvetica", 14))
    row = grid_item(label_sat, row, column=0, sticky="ew", columnspan=3)
    strg = "Electrostatic decoupling procedure based on analysis of " \
           "hysteresis saturation\n" \
           "Active if: On Field mode is selected."
    label_sat.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_sat, mess))

    # Saturation mode
    label_sat_mode = ttk.Label(scrollable_frame, text="Mode:")
    row = grid_item(label_sat_mode, row, column=0, sticky="e", increment=False)
    sat_mode_var = ttk.Combobox(scrollable_frame, values=["set", "auto"])
    sat_mode_var.set(user_parameters['sat mode'])
    row = grid_item(sat_mode_var, row, column=1, sticky="ew")
    strg = "- Name: sat_mode\n" \
           "- Summary: Saturation Electrostatic Analysis Mode\n" \
           "- Description: This parameter determines the mode for " \
           "analyzing the saturation electrostatic component, " \
           "which defines the saturation domain of the loop.\n" \
           "- Value: String indicating the mode for saturation " \
           "electrostatic analysis.\n" \
           "\t--> 'set' (user-defined saturation domain in sat_domain " \
           "parameter)\n" \
           "\t--> 'auto' (automatic calculation from hysteresis fit).\n" \
           "- Active if: On Field mode is selected."
    sat_mode_var.bind("<Enter>",
                      lambda event, mess=strg: show_tooltip(sat_mode_var, mess))

    # Saturation Domain Min
    label_sat_min = ttk.Label(scrollable_frame, text="Min limit (*):")
    row = grid_item(label_sat_min, row, column=0, sticky="e", increment=False)
    sat_domain_min_var = tk.StringVar()
    sat_domain_min_var.set(user_parameters['sat domain']['min'])
    entry_sat_min = ttk.Entry(scrollable_frame, textvariable=sat_domain_min_var)
    row = grid_item(entry_sat_min, row, column=1, sticky="ew")
    strg = "- Name: sat_domain\n" \
           "- Summary: Min Voltage Range for Saturation Electrostatic " \
           "Analysis\n" \
           "- Description: This parameter sets the voltage range for the " \
           "saturation part of the hysteresis, specifically the " \
           "minimum limit.\n" \
           "- Value: float.\n" \
           "\tIf left empty or set to None, the minimum limit is not " \
           "considered.\n" \
           "- Active if: On Field mode is selected and saturation mode is " \
           "set to 'set'."
    entry_sat_min.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_sat_min, mess))

    # Saturation Domain Max
    label_sat_max = ttk.Label(scrollable_frame, text="Max limit (*):")
    row = grid_item(label_sat_max, row, column=0, sticky="e", increment=False)
    sat_domain_max_var = tk.StringVar()
    sat_domain_max_var.set(user_parameters['sat domain']['max'])
    entry_sat_max = ttk.Entry(scrollable_frame, textvariable=sat_domain_max_var)
    row = grid_item(entry_sat_max, row, column=1, sticky="ew")
    strg = "- Name: sat_domain\n" \
           "- Summary: Max Voltage Range for Saturation Electrostatic " \
           "Analysis\n" \
           "- Description: This parameter sets the voltage range for the " \
           "saturation part of the hysteresis, specifically the " \
           "maximum limit.\n" \
           "- Value: float.\n" \
           "\tIf left empty or set to None, the maximum limit is not " \
           "considered.\n" \
           "- Active if: On Field mode is selected and saturation mode is " \
           "set to 'set'."
    entry_sat_max.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_sat_max, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Plot and save
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
    grid_item(quit_button, row, column=1, sticky="ew", increment=False)

    app.mainloop()


if __name__ == '__main__':
    main()
