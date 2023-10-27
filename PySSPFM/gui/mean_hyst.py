"""
--> Executable Script
Graphical interface for mean loop (run mean_hyst.main_mean_hyst)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
import numpy as np

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.mean_hyst import main_mean_hyst as main_script
from PySSPFM.gui.utils import \
    (add_separator_grid, grid_item, show_tooltip, apply_style, extract_var,
     init_secondary_wdw, wdw_main_title)
from PySSPFM.utils.path_for_runable import save_path_management, save_user_pars


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
    app = init_secondary_wdw(parent=parent, wdw_title="Mean loop")

    # Set default parameter values
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'dir path in meas': '',
        'dir path in loop': '',
        'file path in pars': '',
        'mode': 'off',
        'mask': {'man mask': None,
                 'ref': {'meas': 'charac tot fit: area',
                         'mode': 'off',
                         'min val': 0.005,
                         'max val': None,
                         'fmt': '.2f',
                         'interactive': False}},
        'func': 'sigmoid',
        'method': 'least_square',
        'asymmetric': False,
        'inf thresh': 10,
        'sat thresh': 90,
        'del 1st loop': True,
        'pha corr': 'offset',
        'pha fwd': 0,
        'pha rev': 180,
        'pha func': 'cosine',
        'main elec': True,
        'locked elec slope': "None",
        'diff domain': {'min': -5., 'max': 5.},
        'sat mode': 'set',
        'sat domain': {'min': -9., 'max': 9.},
        'interp fact': 4,
        'interp func': 'linear',
        'verbose': True,
        'show plots': True,
        'save': False
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['dir path in meas'] = extract_var(dir_path_in_meas_var)
        user_parameters['dir path in loop'] = extract_var(dir_path_in_loop_var)
        user_parameters['file path in pars'] = \
            extract_var(file_path_in_pars_var)
        user_parameters['mode'] = mode_var.get()
        user_parameters['mask']['man mask'] = extract_var(man_mask_var)
        user_parameters['mask']['ref']['meas'] = ref_meas_var.get()
        user_parameters['mask']['ref']['mode'] = ref_mode_var.get()
        user_parameters['mask']['ref']['min val'] = extract_var(ref_min_var)
        user_parameters['mask']['ref']['max val'] = extract_var(ref_max_var)
        user_parameters['mask']['ref']['fmt'] = ref_fmt_var.get()
        user_parameters['mask']['ref']['interactive'] = ref_interact_var.get()
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
        user_parameters['main elec'] = main_elec_var.get()
        user_parameters['locked elec slope'] = \
            extract_var(locked_elec_slope_var)
        user_parameters['diff domain']['min'] = extract_var(diff_domain_min_var)
        user_parameters['diff domain']['max'] = extract_var(diff_domain_max_var)
        user_parameters['sat mode'] = sat_mode_var.get()
        user_parameters['sat domain']['min'] = extract_var(sat_domain_min_var)
        user_parameters['sat domain']['max'] = extract_var(sat_domain_max_var)
        user_parameters['interp fact'] = interp_fact_var.get()
        user_parameters['interp func'] = interp_func_var.get()
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save'] = save_var.get()

        # Create out directory if not exist
        if user_parameters['save'] is True:
            if user_parameters['dir path out'] is not None:
                if not os.path.exists(user_parameters['dir path out']):
                    os.makedirs(user_parameters['dir path out'])
                    print(f"path created : {user_parameters['dir path out']}")

        # Make plots if show or save plot are active
        make_plots = bool(user_parameters['show plots'] or
                          user_parameters['save'])

        # Data analysis
        start_time = datetime.now()
        figs = main_script(user_parameters, verbose=user_parameters["verbose"],
                           make_plots=make_plots)
        # Plot figures
        print_plots(figs, show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dirname=user_parameters['dir path out'], transparent=False)

        # Save parameters
        if user_parameters['save']:
            save_user_pars(
                user_parameters, user_parameters['dir path out'],
                start_time=start_time, verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_meas():
        dir_path_meas = filedialog.askdirectory()
        dir_path_in_meas_var.set(dir_path_meas)

    def browse_dir_loop():
        dir_path_loop = filedialog.askdirectory()
        dir_path_in_loop_var.set(dir_path_loop)

    def browse_file_pars():
        file_path_pars = filedialog.askopenfilename()
        file_path_in_pars_var.set(file_path_pars)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Create top frame
    top_frame = ttk.Frame(app)
    top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    apply_style(top_frame)
    top_frame.columnconfigure(0, weight=1)

    # Window title: Mean loop
    wdw_main_title(top_frame, "Mean loop")

    row = 3

    # Create left frame
    left_frame = ttk.Frame(app)
    left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ns")
    apply_style(left_frame)

    # Section title: File management
    label_file = ttk.Label(left_frame, text="File management",
                           font=("Helvetica", 14))
    row = grid_item(label_file, row, column=0, sticky="ew", columnspan=3)

    # Directory (in)
    label_in = ttk.Label(left_frame, text="Directory (in):")
    row = grid_item(label_in, row, column=0, sticky="e", increment=False)
    dir_path_in_var = tk.StringVar()
    dir_path_in_var.set(user_parameters['dir path in'])
    entry_in = ttk.Entry(left_frame, textvariable=dir_path_in_var)
    row = grid_item(entry_in, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in\n" \
           "- Summary: Results of analysis directory " \
           "(default: 'title_meas'_'yyyy-mm-dd-HHhMMm'_out_'mode')\n" \
           "- Description: This parameter specifies the directory containing " \
           "the results of analysis generated after the 1st and 2nd step " \
           "of the analysis.\n" \
           "- Value: It should be a string representing a directory path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(left_frame, text="Browse",
                                  command=browse_dir_in)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir = save_path_management(
                input_dir, dir_path_out=None, save=True, dirname="mean_loop",
                lvl=0, create_path=False, post_analysis=True)
        else:
            output_dir = ""
        return output_dir

    # Function to generate the default input meas directory path
    def generate_default_input_meas_dir(input_dir):
        if input_dir != "":
            input_meas_dir = os.path.join(input_dir, 'txt_ferro_meas')
        else:
            input_meas_dir = ""
        return input_meas_dir

    # Function to generate the default input loop directory path
    def generate_default_input_loop_dir(input_dir):
        if input_dir != "":
            input_loop_dir = os.path.join(input_dir, 'txt_loops')
        else:
            input_loop_dir = ""
        return input_loop_dir

    # Function to generate the default input pars file path
    def generate_default_input_pars_file(input_dir):
        if input_dir != "":
            input_pars_file = os.path.join(input_dir, 'results',
                                           'saving_parameters.txt')
        else:
            input_pars_file = ""
        return input_pars_file

    # Update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = dir_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        dir_path_out_var.set(def_output_dir)

    # Update the default input meas dir path when input dir changes
    def update_default_input_meas_dir():
        input_dir = dir_path_in_var.get()
        def_input_meas_dir = generate_default_input_meas_dir(input_dir)
        dir_path_in_meas_var.set(def_input_meas_dir)

    # Update the default input loop dir path when input dir changes
    def update_default_input_loop_dir():
        input_dir = dir_path_in_var.get()
        def_input_loop_dir = generate_default_input_loop_dir(input_dir)
        dir_path_in_loop_var.set(def_input_loop_dir)

    # Update the default input pars file path when input dir changes
    def update_default_input_pars_file():
        input_dir = dir_path_in_var.get()
        def_input_pars_file = generate_default_input_pars_file(input_dir)
        file_path_in_pars_var.set(def_input_pars_file)

    # Bind function (output dir) to input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Bind function (input meas dir) to input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_meas_dir())

    # Bind function (input loop dir) to input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_loop_dir())

    # Bind function (input pars file) to input directory widget
    dir_path_in_var.trace_add(
        "write", lambda *args: update_default_input_pars_file())

    # Directory measurements (in)
    default_input_dir = dir_path_in_var.get()
    default_input_meas_dir = generate_default_input_meas_dir(default_input_dir)
    label_meas = ttk.Label(left_frame, text="Directory measurements (in) (*):")
    row = grid_item(label_meas, row, column=0, sticky="e", increment=False)
    dir_path_in_meas_var = tk.StringVar()
    dir_path_in_meas_var.set(default_input_meas_dir)
    entry_meas = ttk.Entry(left_frame, textvariable=dir_path_in_meas_var)
    row = grid_item(entry_meas, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in_meas\n" \
           "- Summary: Ferroelectric measurements files directory " \
           "(optional, default: txt_ferro_meas)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the ferroelectric measurements text files generated after the " \
           "2nd step of the analysis.\n" \
           "- Value: It should be a string representing a directory path."
    entry_meas.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_meas, mess))
    browse_button_meas = ttk.Button(left_frame, text="Browse",
                                    command=browse_dir_meas)
    row = grid_item(browse_button_meas, row, column=2)

    # Directory txt loop (in)
    default_input_dir = dir_path_in_var.get()
    default_input_loop_dir = generate_default_input_loop_dir(default_input_dir)
    label_loop = ttk.Label(left_frame, text="Directory txt loops (in) (*):")
    row = grid_item(label_loop, row, column=0, sticky="e", increment=False)
    dir_path_in_loop_var = tk.StringVar()
    dir_path_in_loop_var.set(default_input_loop_dir)
    entry_loop = ttk.Entry(left_frame, textvariable=dir_path_in_loop_var)
    row = grid_item(entry_loop, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in_loop\n" \
           "- Summary: Txt loop files directory " \
           "(optional, default: txt_loops)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the loop text files generated after the " \
           "1st step of the analysis.\n" \
           "- Value: It should be a string representing a directory path."
    entry_loop.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_loop, mess))
    browse_button_loop = ttk.Button(left_frame, text="Browse",
                                    command=browse_dir_loop)
    row = grid_item(browse_button_loop, row, column=2)

    # File pars (in)
    default_input_dir = dir_path_in_var.get()
    default_input_pars_file = \
        generate_default_input_pars_file(default_input_dir)
    label_pars = ttk.Label(left_frame, text="File txt parameters (in) (*):")
    row = grid_item(label_pars, row, column=0, sticky="e", increment=False)
    file_path_in_pars_var = tk.StringVar()
    file_path_in_pars_var.set(default_input_pars_file)
    entry_pars = ttk.Entry(left_frame, textvariable=file_path_in_pars_var)
    row = grid_item(entry_pars, row, column=1, sticky="ew", increment=False)
    strg = "- Name: file_path_in_pars\n" \
           "- Summary: Measurement and analysis parameters txt file " \
           "(optional, default: results/saving_parameters.txt)\n" \
           "- Description: This parameter specifies the file containing " \
           "measurement and analysis parameters generated after the " \
           "2nd step of the analysis.\n" \
           "- Value: It should be a string representing a file path."
    entry_pars.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_pars, mess))
    browse_button_pars = ttk.Button(left_frame, text="Browse",
                                    command=browse_file_pars)
    row = grid_item(browse_button_pars, row, column=2)

    # Directory (out)
    default_input_dir = dir_path_in_var.get()
    default_output_dir = generate_default_output_dir(default_input_dir)
    label_out = ttk.Label(left_frame, text="Directory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
    dir_path_out_var = tk.StringVar()
    dir_path_out_var.set(default_output_dir)
    entry_out = ttk.Entry(left_frame, textvariable=dir_path_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_out\n" \
           "- Summary: Saving directory for analysis results figures " \
           "(optional, default: toolbox directory in the same root)\n" \
           "- Description: This parameter specifies the directory where the " \
           "figures generated as a result of the analysis will be saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(left_frame, text="Select",
                                   command=browse_dir_out)
    row = grid_item(browse_button_out, row, column=2)
    row = add_separator_grid(left_frame, row=row)

    # Section title: Mode
    label_mode = ttk.Label(left_frame, text="Mode", font=("Helvetica", 14))
    row = grid_item(label_mode, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(left_frame, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(left_frame, values=["off", "on", "coupled"])
    mode_var.set(user_parameters['mode'])
    row = grid_item(mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Measurement mode used for analysis.\n" \
           "- Description: This parameter specifies the mode used for " \
           "analysis.\n" \
           "- Value: A string with three possible values: 'on,' 'off,' or " \
           "'coupled.'"
    mode_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(mode_var, mess))
    row = add_separator_grid(left_frame, row=row)

    # Section title: Mask
    label_mask = ttk.Label(left_frame, text="Mask:", font=("Helvetica", 14))
    row = grid_item(label_mask, row, column=0, sticky="ew", columnspan=3)
    row = add_separator_grid(left_frame, row=row)

    # Subsection title: Mode manual
    label_man = ttk.Label(left_frame, text="Mode manual",
                          font=("Helvetica", 12))
    strg = "Mask is chosen manually"
    label_man.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_man, mess))
    row = grid_item(label_man, row, column=0, sticky="ew", columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(left_frame, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    man_mask_var = tk.StringVar()
    man_mask_var.set(str(user_parameters['mask']['man mask']))
    entry_man_mask = ttk.Entry(left_frame, textvariable=man_mask_var)
    row = grid_item(entry_man_mask, row, column=1, sticky="ew")
    strg = "- Name: man_mask\n" \
           "- Summary: Manual mask for selecting specific files\n" \
           "- Description: This parameter is a list of pixel indices.\n" \
           "- Value: Dictionary with mode keys and lists of indices as " \
           "values.\n" \
           "\t--> if list of pixels is []: all files are selected.\n" \
           "\t--> if list of pixels is None: criterion of selection " \
           "is made with reference measurement.\n" \
           "\t--> if list of pixels is [a, b, c ...] file of index " \
           "a, b, c [...] are not selected"
    entry_man_mask.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_man_mask, mess))
    row = add_separator_grid(left_frame, row=row)

    # Annotation
    label_annot = ttk.Label(left_frame, text="OR", font=("Helvetica", 12))
    row = grid_item(label_annot, row, column=0, sticky="ew", columnspan=3)
    row = add_separator_grid(left_frame, row=row)

    # Subsection title: Mode reference measurement
    label_ref = ttk.Label(left_frame, text="Mode reference measurement (*)",
                          font=("Helvetica", 12))
    strg = "Construct a mask with a criterion selection on ref values.\n" \
           "Active only if list of pixels is None"
    label_ref.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_ref, mess))
    row = grid_item(label_ref, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(left_frame, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    ref_mode_var = ttk.Combobox(left_frame, values=["off", "on", "coupled"])
    ref_mode_var.set(user_parameters['mask']['ref']['mode'])
    row = grid_item(ref_mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Mode for Reference Measurement\n" \
           "- Description: This parameter determines the mode used for " \
           "the reference measurement.\n" \
           "- Value: String indicating the chosen mode of reference " \
           "measurement ('off', 'on', or 'coupled')."
    ref_mode_var.bind("<Enter>",
                      lambda event, mess=strg: show_tooltip(ref_mode_var, mess))

    # Reference Measurement
    label_meas = ttk.Label(left_frame, text="Measurement:")
    row = grid_item(label_meas, row, column=0, sticky="e", increment=False)
    ref_meas_var = tk.StringVar()
    ref_meas_var.set(user_parameters['mask']['ref']['meas'])
    entry_ref_meas = ttk.Entry(left_frame, textvariable=ref_meas_var)
    row = grid_item(entry_ref_meas, row, column=1, sticky="ew")
    strg = "- Name: meas\n" \
           "- Summary: Reference measurement for mask determination\n" \
           "- Description: This parameter specifies the name of the " \
           "reference measurement used to determine the mask.\n" \
           "- Value: String, representing the chosen reference measurement."
    entry_ref_meas.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_ref_meas, mess))

    # Min Value
    label_min = ttk.Label(left_frame, text="Min Value (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    ref_min_var = tk.StringVar()
    ref_min_var.set(user_parameters['mask']['ref']['min val'])
    entry_ref_min = ttk.Entry(left_frame, textvariable=ref_min_var)
    row = grid_item(entry_ref_min, row, column=1, sticky="ew")
    strg = "- Name: min val\n" \
           "- Summary: Minimum value for reference mask\n" \
           "- Description: This parameter specifies the minimum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the minimum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no minimum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_min.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_min, mess))

    # Max Value
    label_max = ttk.Label(left_frame, text="Max Value (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    ref_max_var = tk.StringVar()
    ref_max_var.set(user_parameters['mask']['ref']['max val'])
    entry_ref_max = ttk.Entry(left_frame, textvariable=ref_max_var)
    row = grid_item(entry_ref_max, row, column=1, sticky="ew")
    strg = "- Name: max val\n" \
           "- Summary: Maximum value for reference mask\n" \
           "- Description: This parameter specifies the maximum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the maximum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no maximum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_max.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_ref_max, mess))

    # Format
    label_fmt = ttk.Label(left_frame, text="Format:")
    row = grid_item(label_fmt, row, column=0, sticky="e", increment=False)
    ref_fmt_var = tk.StringVar()
    ref_fmt_var.set(user_parameters['mask']['ref']['fmt'])
    entry_ref_fmt = ttk.Entry(left_frame, textvariable=ref_fmt_var)
    row = grid_item(entry_ref_fmt, row, column=1, sticky="ew")
    strg = "- Name: fmt\n" \
           "- Summary: Format for measurement reference (number of decimal)\n" \
           "- Description: This parameter specifies the format for the " \
           "measurement reference with a specified number of decimal " \
           "places.\n" \
           "- Value: String, representing the format of the printed value " \
           "in the map."
    entry_ref_fmt.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_ref_fmt, mess))

    # Reference interactive
    label_interact = ttk.Label(left_frame, text="Interactive:")
    row = grid_item(label_interact, row, column=0, sticky="e", increment=False)
    ref_interact_var = tk.BooleanVar()
    ref_interact_var.set(user_parameters['mask']['ref']['interactive'])
    chck_ref_interact = ttk.Checkbutton(left_frame, variable=ref_interact_var)
    row = grid_item(chck_ref_interact, row, column=1, sticky="w")
    strg = "- Name: interactive\n" \
           "- Summary: Interactive mode for constructing a mask from " \
           "reference.\n" \
           "- Description: This parameter enables interactive mode, " \
           "which allows users to determine mask limits interactively " \
           "using the reference measurement.\n" \
           "- Value: Boolean (True or False)."
    chck_ref_interact.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_ref_interact, mess))
    row = add_separator_grid(left_frame, row=row)

    # Section title: Map
    label_map = ttk.Label(left_frame, text="Map", font=("Helvetica", 14))
    strg = "Map parameters are active only if mask is built on ref " \
           "measurement (i.e. list of pixels is None)."
    label_map.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_map, mess))
    row = grid_item(label_map, row, column=0, sticky="ew", columnspan=3)

    # Interpolation Factor
    label_fact = ttk.Label(left_frame, text="Interpolation Factor:")
    row = grid_item(label_fact, row, column=0, sticky="e", increment=False)
    interp_fact_var = tk.IntVar()
    interp_fact_var.set(user_parameters['interp fact'])
    entry_interp_fact = ttk.Entry(left_frame, textvariable=interp_fact_var)
    row = grid_item(entry_interp_fact, row, column=1, sticky="ew")
    strg = "- Name: interp_fact\n" \
           "- Summary: Interpolation factor for sspfm maps interpolation.\n" \
           "- Description: This parameter determines the level of " \
           "interpolation to be applied to SSPFM maps.\n" \
           "- Value: Should be an integer.\n" \
           "- Active if: Mask is built on ref measurement (i.e. list of " \
           "pixels is None)."
    entry_interp_fact.bind("<Enter>", lambda event, mess=strg: show_tooltip(
        entry_interp_fact, mess))

    # Interpolation Function
    label_func = ttk.Label(left_frame, text="Interpolation Function:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    interp_func_var = ttk.Combobox(left_frame,
                                   values=['linear', 'cubic'])
    interp_func_var.set(user_parameters['interp func'])
    row = grid_item(interp_func_var, row, column=1, sticky="ew")
    strg = "- Name: interp_func\n" \
           "- Summary: Interpolation function\n" \
           "- Description: This parameter specifies the interpolation " \
           "function used for sspfm maps interpolation.\n" \
           "- Value: It can take one of the following values:" \
           " 'linear', or 'cubic'.\n" \
           "- Active if: Mask is built on ref measurement (i.e. list of " \
           "pixels is None)."
    interp_func_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(interp_func_var, mess))
    row = add_separator_grid(left_frame, row=row)

    # Create right frame
    right_frame = ttk.Frame(app)
    right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ns")
    apply_style(right_frame)

    # Section title: Hysteresis treatment
    label_hyst = ttk.Label(right_frame, text="Hysteresis treatment",
                           font=("Helvetica", 14))
    row = grid_item(label_hyst, row, column=0, sticky="ew", columnspan=3)
    strg = "Parameters for hysteresis fit and properties extraction"
    label_hyst.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_hyst, mess))

    # Fit function
    label_func = ttk.Label(right_frame, text="Function:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    func_var = ttk.Combobox(right_frame, values=["sigmoid", "arctan"])
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
    label_method = ttk.Label(right_frame, text="Method:")
    row = grid_item(label_method, row, column=0, sticky="e", increment=False)
    method_var = ttk.Combobox(
        right_frame, values=["leastsq", "least_square", "nelder"])
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
    label_asym = ttk.Label(right_frame, text="Asymmetric:")
    row = grid_item(label_asym, row, column=0, sticky="e", increment=False)
    asymmetric_var = tk.BooleanVar()
    asymmetric_var.set(user_parameters['asymmetric'])
    chck_asym = ttk.Checkbutton(right_frame, variable=asymmetric_var)
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
    def update_inf_thresh_label(event):
        inf_thresh_label.config(text=str(inf_thresh_var.get()))

    # Inflection Threshold
    label_thresh_inf = ttk.Label(right_frame, text="Inflection threshold [%]:")
    row = grid_item(label_thresh_inf, row, column=0, sticky="e",
                    increment=False)
    inf_thresh_var = tk.IntVar(value=user_parameters['inf thresh'])
    scale_thresh_inf = ttk.Scale(right_frame, from_=1, to=100,
                                 variable=inf_thresh_var, orient="horizontal",
                                 length=100, command=update_inf_thresh_label)
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
    inf_thresh_label = ttk.Label(right_frame, text=str(inf_thresh_var.get()))
    row = grid_item(inf_thresh_label, row, column=2, sticky="w")

    # Function to update the label text when the slider is moved
    def update_sat_thresh_label(event):
        sat_thresh_label.config(text=str(sat_thresh_var.get()))

    # Saturation Threshold
    label_thresh_sat = ttk.Label(right_frame, text="Saturation threshold [%]:")
    row = grid_item(label_thresh_sat, row, column=0, sticky="e",
                    increment=False)
    sat_thresh_var = tk.IntVar(value=user_parameters['sat thresh'])
    scale_thresh_sat = ttk.Scale(right_frame, from_=1, to=100,
                                 variable=sat_thresh_var, orient="horizontal",
                                 length=100, command=update_sat_thresh_label)
    row = grid_item(scale_thresh_sat, row, column=1, sticky="ew",
                    increment=False)
    strg = "- Name: sat_thresh\n" \
           "- Summary: Saturation Point Threshold\n" \
           "- Description: This parameter defines the threshold, " \
           "expressed as a percentage of the hysteresis amplitude, " \
           "used to calculate the value of the saturation point at " \
           "the end of the hysteresis switch.\n" \
           "- Value: Float, representing the threshold percentage."
    scale_thresh_sat.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(scale_thresh_sat, mess))
    sat_thresh_label = ttk.Label(right_frame, text=str(sat_thresh_var.get()))
    row = grid_item(sat_thresh_label, row, column=2, sticky="w")

    # Del First Loop
    label_del = ttk.Label(right_frame, text="Delete First Loop:")
    row = grid_item(label_del, row, column=0, sticky="e", increment=False)
    del_1st_loop_var = tk.BooleanVar()
    del_1st_loop_var.set(user_parameters['del 1st loop'])
    chck_del = ttk.Checkbutton(right_frame, variable=del_1st_loop_var)
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
    row = add_separator_grid(right_frame, row=row)

    # Section title: Phase treatment
    label_pha = ttk.Label(right_frame, text="Phase treatment",
                          font=("Helvetica", 14))
    row = grid_item(label_pha, row, column=0, sticky="ew", columnspan=3)
    strg = "Parameters for phase calibration"
    label_pha.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_pha, mess))

    # Phase Mode
    label_mode = ttk.Label(right_frame, text="Correction Method:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    phase_mode_var = ttk.Combobox(right_frame,
                                  values=["raw", "offset", "affine", "up_down"])
    phase_mode_var.set(user_parameters['pha corr'])
    row = grid_item(phase_mode_var, row, column=1, sticky="ew")
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
    label_fwd = ttk.Label(right_frame, text="Phase Forward Value:")
    row = grid_item(label_fwd, row, column=0, sticky="e", increment=False)
    pha_fwd_var = tk.StringVar()
    pha_fwd_var.set(user_parameters['pha fwd'])
    entry_pha_fwd = ttk.Entry(right_frame, textvariable=pha_fwd_var)
    row = grid_item(entry_pha_fwd, row, column=1, sticky="ew")
    strg = "- Name: pha_fwd\n" \
           "- Summary: Phase Forward Target Value\n" \
           "- Description: This parameter represents the target value " \
           "for the phase in the forward direction. It is used to generate" \
           " a multiplied coefficient equal to 1 between amplitude and " \
           "piezoresponse.\n" \
           "- Value: Float"
    entry_pha_fwd.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_pha_fwd, mess))

    # Phase Reverse Value
    label_rev = ttk.Label(right_frame, text="Phase Reverse Value:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    pha_rev_var = tk.StringVar()
    pha_rev_var.set(user_parameters['pha rev'])
    entry_pha_rev = ttk.Entry(right_frame, textvariable=pha_rev_var)
    row = grid_item(entry_pha_rev, row, column=1, sticky="ew")
    strg = "- Name: pha_rev\n" \
           "- Summary: Phase Reverse Target Value\n" \
           "- Description: This parameter represents the target value " \
           "for the phase in the reverse direction. It is used to generate" \
           " a multiplied coefficient equal to -1 between amplitude " \
           "and piezoresponse.\n" \
           "- Value: Float"
    entry_pha_rev.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_pha_rev, mess))

    # Function for Piezoresponse
    label_func = ttk.Label(right_frame, text="Function for Piezoresponse:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    func_pha_var = ttk.Combobox(right_frame, values=["cosine", "sine"])
    func_pha_var.set(user_parameters['pha func'])
    row = grid_item(func_pha_var, row, column=1, sticky="ew")
    strg = "- Name: pha_func\n" \
           "- Summary: Piezoresponse Function\n" \
           "- Description: This parameter represents the function used " \
           "to determine the piezoresponse from amplitude and phase. " \
           "The piezoresponse (PR) is calculated as PR = amp * func(pha), " \
           "where 'amp' is the amplitude and 'pha' is the phase.\n" \
           "- Value: Algebraic function ('sine' or 'cosine')"
    func_pha_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(func_pha_var, mess))

    # Main Electrostatic
    label_elec = ttk.Label(right_frame, text="Main Electrostatic:")
    row = grid_item(label_elec, row, column=0, sticky="e", increment=False)
    main_elec_var = tk.BooleanVar()
    main_elec_var.set(user_parameters['main elec'])
    chck_elec = ttk.Checkbutton(right_frame, variable=main_elec_var)
    row = grid_item(chck_elec, row, column=1, sticky="w")
    strg = "- Name: main_elec\n" \
           "- Summary: Dominant Electrostatics in On Field Mode\n" \
           "- Description: It determines whether the electrostatics are " \
           "higher than ferroelectric effects. In other words, it " \
           "indicates if the electrostatics are responsible for the " \
           "phase loop's sense of rotation in the On Field mode.\n" \
           "- Value: Boolean\n" \
           "- Active if: On Field mode is selected."
    chck_elec.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_elec, mess))

    # Locked Electrostatic Slope
    label_slope = ttk.Label(right_frame, text="Locked Electrostatic Slope:")
    row = grid_item(label_slope, row, column=0, sticky="e", increment=False)
    locked_elec_slope_var = ttk.Combobox(
        right_frame, values=["None", "negative", "positive"])
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
    row = add_separator_grid(right_frame, row=row)

    # Section title: Differential treatment
    label_diff = ttk.Label(right_frame, text="Differential treatment",
                           font=("Helvetica", 14))
    row = grid_item(label_diff, row, column=0, sticky="ew", columnspan=3)
    strg = "Parameters to determine linear part for differential loop.\n" \
           "Active if: coupled mode is selected."
    label_diff.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_diff, mess))

    # Differential Domain Min
    label_min = ttk.Label(right_frame, text="Min limit (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    diff_domain_min_var = tk.StringVar()
    diff_domain_min_var.set(user_parameters['diff domain']['min'])
    entry_min = ttk.Entry(right_frame, textvariable=diff_domain_min_var)
    row = grid_item(entry_min, row, column=1, sticky="ew")
    strg = "- Name: diff_domain (min)\n" \
           "- Summary: Voltage Range for Linear Differential Component " \
           "(Min Limit)\n" \
           "- Description: This parameter defines the voltage range " \
           "considered for the linear part of the differential component. " \
           "Value specifying the minimum voltage range for differential " \
           "analysis\n" \
           "- Value: float\n" \
           "\tIf left empty or set to None, no minimum limit is applied.\n" \
           "- Active if: coupled mode is selected."
    entry_min.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_min, mess))

    # Differential Domain Max
    label_max = ttk.Label(right_frame, text="Max limit (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    diff_domain_max_var = tk.StringVar()
    diff_domain_max_var.set(user_parameters['diff domain']['max'])
    entry_max = ttk.Entry(right_frame, textvariable=diff_domain_max_var)
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
           "- Active if: coupled mode is selected."
    entry_max.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_max, mess))
    row = add_separator_grid(right_frame, row=row)

    # Section title: Electrostatic decoupling saturation treatment
    label_sat = ttk.Label(right_frame,
                          text="Electrostatic decoupling (saturation)",
                          font=("Helvetica", 14))
    row = grid_item(label_sat, row, column=0, sticky="ew", columnspan=3)
    strg = "Electrostatic decoupling procedure based on analysis of " \
           "hysteresis saturation\n" \
           "Active if: On Field mode is selected."
    label_sat.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_sat, mess))

    # Saturation mode
    label_sat_mode = ttk.Label(right_frame, text="Mode:")
    row = grid_item(label_sat_mode, row, column=0, sticky="e", increment=False)
    sat_mode_var = ttk.Combobox(right_frame,
                                values=["set", "auto"])
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
    label_sat_min = ttk.Label(right_frame, text="Min limit (*):")
    row = grid_item(label_sat_min, row, column=0, sticky="e", increment=False)
    sat_domain_min_var = tk.StringVar()
    sat_domain_min_var.set(user_parameters['sat domain']['min'])
    entry_sat_min = ttk.Entry(right_frame, textvariable=sat_domain_min_var)
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
    label_sat_max = ttk.Label(right_frame, text="Max limit (*):")
    row = grid_item(label_sat_max, row, column=0, sticky="e", increment=False)
    sat_domain_max_var = tk.StringVar()
    sat_domain_max_var.set(user_parameters['sat domain']['max'])
    entry_sat_max = ttk.Entry(right_frame, textvariable=sat_domain_max_var)
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
    row = add_separator_grid(right_frame, row=row)

    # Section title: Save and plot
    label_chck = ttk.Label(right_frame, text="Save and plot",
                           font=("Helvetica", 14))
    row = grid_item(label_chck, row, column=0, sticky="ew", columnspan=3)

    # Verbose
    label_verb = ttk.Label(right_frame, text="Verbose:")
    row = grid_item(label_verb, row, column=0, sticky="e", increment=False)
    verbose_var = tk.BooleanVar()
    verbose_var.set(user_parameters['verbose'])
    chck_verb = ttk.Checkbutton(right_frame, variable=verbose_var)
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
    label_show = ttk.Label(right_frame, text="Show plots:")
    row = grid_item(label_show, row, column=0, sticky="e", increment=False)
    show_plots_var = tk.BooleanVar()
    show_plots_var.set(user_parameters['show plots'])
    chck_show = ttk.Checkbutton(right_frame, variable=show_plots_var)
    row = grid_item(chck_show, row, column=1, sticky="w")
    strg = "- Name: show_plots\n" \
           "- Summary: Activation key for generating matplotlib figures " \
           "during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for generating matplotlib figures during the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_show.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_show, mess))

    # Save
    label_save = ttk.Label(right_frame, text="Save:")
    row = grid_item(label_save, row, column=0, sticky="e", increment=False)
    save_var = tk.BooleanVar()
    save_var.set(user_parameters['save'])
    chck_save = ttk.Checkbutton(right_frame, variable=save_var)
    row = grid_item(chck_save, row, column=1, sticky="w")
    strg = "- Name: save\n" \
           "- Summary: Activation key for saving results during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for saving results generated during the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_save.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_save, mess))
    row = add_separator_grid(right_frame, row=row)

    # Create bottom frame
    bottom_frame = ttk.Frame(app)
    bottom_frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
    apply_style(bottom_frame)
    bottom_frame.columnconfigure(0, weight=1)

    # Submit button
    start_button = ttk.Button(bottom_frame, text="Start", command=launch)
    row = grid_item(start_button, row, column=0, sticky="e", columnspan=2)

    def exit_application():
        app.destroy()

    # Exit button
    exit_button = ttk.Button(bottom_frame, text="Exit",
                             command=exit_application)
    grid_item(exit_button, row, column=0, sticky="e", columnspan=2)

    app.mainloop()


if __name__ == '__main__':
    main()
