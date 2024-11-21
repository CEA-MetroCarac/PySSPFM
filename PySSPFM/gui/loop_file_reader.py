"""
--> Executable Script
Graphical interface for nanoloop file reader
(run loop_file_reader.main_loop_file_reader)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.loop_file_reader import \
    main_loop_file_reader as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
     init_secondary_wdw, wdw_main_title)
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
    title = "Loop file reader"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'file path in': '',
        'csv path in': '',
        'dir path out': '',
        'del 1st loop': True,
        'corr': 'raw',
        'pha fwd': 0,
        'pha rev': 180,
        'func': 'cosine',
        'main elec': True,
        'grounded tip': False,
        'positive d33': True,
        'locked elec slope': 'None',
        'verbose': True,
        'show plots': True,
        'save': False,
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['file path in'] = file_path_in_var.get()
        user_parameters['csv path in'] = extract_var(csv_path_in_var)
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['del 1st loop'] = del_1st_loop_var.get()
        user_parameters['corr'] = corr_var.get()
        user_parameters['pha fwd'] = extract_var(pha_fwd_var)
        user_parameters['pha rev'] = extract_var(pha_rev_var)
        user_parameters['func'] = np.cos \
            if func_var.get() == 'cosine' else np.sin
        user_parameters['main elec'] = main_elec_var.get()
        user_parameters['grounded tip'] = grounded_tip_var.get()
        user_parameters['positive d33'] = pos_d33_var.get()
        user_parameters['locked elec slope'] = \
            extract_var(locked_elec_slope_var)
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
        figs = main_script(user_parameters['file path in'],
                           csv_path=user_parameters['csv path in'],
                           dict_pha=user_parameters,
                           del_1st_loop=user_parameters['del 1st loop'],
                           verbose=user_parameters['verbose'],
                           make_plots=make_plots)
        # Plot figures
        print_plots(figs, show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dirname=user_parameters['dir path out'], transparent=False)

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="loop_file_reader_params.json",
                            verbose=user_parameters['verbose'])

    def browse_file_in():
        file_path_in = filedialog.askopenfilename()
        file_path_in_var.set(file_path_in)

    def browse_file_csv_in():
        csv_path_in = filedialog.askdirectory()
        csv_path_in_var.set(csv_path_in)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: List map reader
    wdw_main_title(scrollable_frame, title)

    row = 3

    # Section title: File management
    label_file = ttk.Label(scrollable_frame, text="File management",
                           font=("Helvetica", 14))
    row = grid_item(label_file, row, column=0, sticky="ew", columnspan=3)

    # File (in)
    label_in = ttk.Label(scrollable_frame, text="File (in):")
    row = grid_item(label_in, row, column=0, sticky="e", increment=False)
    file_path_in_var = tk.StringVar()
    file_path_in_var.set(user_parameters['file path in'])
    entry_in = ttk.Entry(scrollable_frame, textvariable=file_path_in_var)
    row = grid_item(entry_in, row, column=1, sticky="ew", increment=False)
    strg = "- Name: file_path_in\n" \
           "- Summary: File path for text nanoloop file generated after " \
           "the first step of the analysis " \
           "(default: in 'nanoloops' directory)\n" \
           "- Description: This parameter specifies the file path" \
           " where the text nanoloop file generated after the first step of " \
           "the analysis is located.\n" \
           "- Value: String (file path)."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(scrollable_frame, text="Browse",
                                  command=browse_file_in)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_file):
        if input_file != "":
            output_dir = save_path_management(
                input_file, dir_path_out=None, save=True,
                dirname="loop_file_reader", lvl=2, create_path=False,
                post_analysis=True)
        else:
            output_dir = ""
        return output_dir

    # Function to generate the default input csv file path
    def generate_default_input_csv_file(input_file):
        if input_file != "":
            input_csv_file = input_file
            for _ in range(2):
                input_csv_file, _ = os.path.split(input_csv_file)
            input_csv_file, _ = input_csv_file.split("_out")
            tab_csv_file = input_csv_file.split("_")
            input_csv_file = "_".join(tab_csv_file[:-1])
        else:
            input_csv_file = ""
        return input_csv_file

    # Function to update the default output dir path when input file changes
    def update_default_output_dir():
        input_file = file_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_file)
        dir_path_out_var.set(def_output_dir)

    # Function to update the default input csv file path when input file changes
    def update_default_input_csv_file():
        input_file = file_path_in_var.get()
        def_input_csv_file = generate_default_input_csv_file(input_file)
        csv_path_in_var.set(def_input_csv_file)

    # Bind the function (output dir) to the input file widget
    file_path_in_var.trace_add("write",
                               lambda *args: update_default_output_dir())

    # Bind the function (input csv file) to the input file widget
    file_path_in_var.trace_add("write",
                               lambda *args: update_default_input_csv_file())

    # CSV file (in)
    default_input_file = file_path_in_var.get()
    default_input_csv_file = generate_default_input_csv_file(default_input_file)
    label = ttk.Label(scrollable_frame,
                      text="file path csv measurements (in) (*):")
    row = grid_item(label, row, column=0, sticky="e", increment=False)
    csv_path_in_var = tk.StringVar()
    csv_path_in_var.set(default_input_csv_file)
    entry2 = ttk.Entry(scrollable_frame, textvariable=csv_path_in_var)
    row = grid_item(entry2, row, column=1, sticky="ew", increment=False)
    strg = "- Name: csv_file_path\n" \
           "- Summary: File path of the CSV measurement file " \
           "(measurement sheet model).\n" \
           "- Description: This parameter specifies the file path to " \
           "the CSV file containing measurement parameters. It is used to " \
           "indicate the location of the CSV file, which serves as the " \
           "source of measurement data for processing.\n" \
           "- Value: A string representing the file path.\n" \
           "\t- If left empty, the system will automatically " \
           "select the CSV file path."
    entry2.bind("<Enter>", lambda event, mess=strg: show_tooltip(entry2, mess))
    browse_button_csv = ttk.Button(scrollable_frame, text="Browse",
                                   command=browse_file_csv_in)
    row = grid_item(browse_button_csv, row, column=2)

    # Directory (out)
    default_input_file = file_path_in_var.get()
    default_output_dir = generate_default_output_dir(default_input_file)
    label = ttk.Label(scrollable_frame, text="Directory (out) (*):")
    row = grid_item(label, row, column=0, sticky="e", increment=False)
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

    # Section title: Nanoloop plotting
    label_pha = ttk.Label(scrollable_frame, text="Loop plotting",
                          font=("Helvetica", 14))
    row = grid_item(label_pha, row, column=0, sticky="ew", columnspan=3)

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
           "deletes the first nanoloop of the analysis, which is typically " \
           "used for calculating the mean hysteresis.\nThis can be " \
           "useful when the first write voltage values are equal to " \
           "zero, indicating that the material is in a pristine state, " \
           "and the nanoloop shape would be different from the polarized " \
           "state. " \
           "Deleting the first nanoloop helps to avoid artifacts in the " \
           "analysis.\nThis parameter has influence only on figure.\n" \
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
    corr_var = ttk.Combobox(scrollable_frame,
                            values=["raw", "offset", "affine", "up_down"])
    corr_var.set(user_parameters['corr'])
    row = grid_item(corr_var, row, column=1, sticky="w")
    strg = "- Name: corr\n" \
           "- Summary: Phase Correction Mode\n" \
           "- Description: This parameter specifies the correction mode " \
           "for the value of the phase nanoloop. " \
           "There are four possible correction modes:\n" \
           "\t- 'raw': No correction is applied.\n" \
           "\t- 'offset': Offset correction is applied.\n" \
           "\t- 'affine': Affine correction is applied.\n" \
           "\t- 'up_down': Phase is set to the up value or down value.\n" \
           "- Value: String (one of 'raw', 'offset', 'affine', 'up_down')"
    corr_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(corr_var, mess))

    # Phase Forward
    label_fwd = ttk.Label(scrollable_frame, text="Phase Forward:")
    row = grid_item(label_fwd, row, column=0, sticky="e", increment=False)
    pha_fwd_var = ttk.Entry(scrollable_frame)
    pha_fwd_var.insert(0, str(user_parameters['pha fwd']))
    row = grid_item(pha_fwd_var, row, column=1, sticky="w")
    strg = "- Name: pha_fwd\n" \
           "- Summary: Phase Forward Target Value\n" \
           "- Description: This parameter represents the target value " \
           "for the phase in the forward direction. It is used to generate" \
           " a multiplied coefficient equal to 1 between amplitude and " \
           "piezoresponse.\n" \
           "- Value: Float"
    pha_fwd_var.bind("<Enter>",
                     lambda event, mess=strg: show_tooltip(pha_fwd_var, mess))

    # Phase Reverse
    label_rev = ttk.Label(scrollable_frame, text="Phase Reverse:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    pha_rev_var = ttk.Entry(scrollable_frame)
    pha_rev_var.insert(0, str(user_parameters['pha rev']))
    row = grid_item(pha_rev_var, row, column=1, sticky="w")
    strg = "- Name: pha_rev\n" \
           "- Summary: Phase Reverse Target Value\n" \
           "- Description: This parameter represents the target value " \
           "for the phase in the reverse direction. It is used to generate" \
           " a multiplied coefficient equal to -1 between amplitude " \
           "and piezoresponse.\n" \
           "- Value: Float"
    pha_rev_var.bind("<Enter>",
                     lambda event, mess=strg: show_tooltip(pha_rev_var, mess))

    # Function for Piezoresponse
    label_func = ttk.Label(scrollable_frame, text="Function for Piezoresponse:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    func_var = ttk.Combobox(scrollable_frame, values=["cosine", "sine"])
    func_var.set(user_parameters['func'])
    row = grid_item(func_var, row, column=1, sticky="w")
    strg = "- Name: pha_func\n" \
           "- Summary: Piezoresponse Function\n" \
           "- Description: This parameter represents the function used " \
           "to determine the piezoresponse from amplitude and phase. " \
           "The piezoresponse (PR) is calculated as PR = amp * func(pha), " \
           "where 'amp' is the amplitude and 'pha' is the phase.\n" \
           "- Value: Algebraic function ('sine' or 'cosine')"
    func_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(func_var, mess))

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
           "phase nanoloop's sense of rotation in the On Field mode.\n" \
           "- Value: Boolean\n" \
           "- Active if: On Field mode is selected."
    chck_elec.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_elec, mess))

    # Grounded Tip
    label_gnd = ttk.Label(scrollable_frame, text="Grounded Tip:")
    row = grid_item(label_gnd, row, column=0, sticky="e", increment=False)
    grounded_tip_var = tk.BooleanVar()
    grounded_tip_var.set(user_parameters['grounded tip'])
    chck_grounded = ttk.Checkbutton(scrollable_frame, variable=grounded_tip_var)
    row = grid_item(chck_grounded, row, column=1, sticky="w")
    strg = "- Name: grounded_tip\n" \
           "- Summary: Flag indicating whether the tip is grounded.\n" \
           "- Description: This parameter must be activated if the tip " \
           "is grounded. It influences the polarisation value, the sense " \
           "of rotation of hysteresis, and the sign of the electrostatic " \
           "slope.\n" \
           "- Value: Boolean (True or False)."
    chck_grounded.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(chck_grounded, mess))

    # Positive D33
    label_coef = ttk.Label(scrollable_frame, text="Positive d33:")
    row = grid_item(label_coef, row, column=0, sticky="e", increment=False)
    pos_d33_var = tk.BooleanVar()
    pos_d33_var.set(user_parameters['positive d33'])
    chck_pos_d33 = ttk.Checkbutton(scrollable_frame, variable=pos_d33_var)
    row = grid_item(chck_pos_d33, row, column=1, sticky="w")
    strg = "- Name: positive_d33\n" \
           "- Summary: Flag indicating positive d33.\n" \
           "- Description: This parameter must be activated if the d33 " \
           "value is positive. It influences the sense of rotation of " \
           "hysteresis.\n" \
           "- Value: Boolean (True or False)."
    chck_pos_d33.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(chck_pos_d33, mess))

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
           "electrostatic slope in the nanoloop whatever measurement " \
           "parameters (theory: grounded tip: negative, bottom: positive).\n" \
           "- Value: 'negative', 'positive', or None\n" \
           "- Active if: On Field mode is selected."
    locked_elec_slope_var.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(locked_elec_slope_var, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Save and plot
    label_chck = ttk.Label(scrollable_frame, text="Save and plot",
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

    # Save
    label_save = ttk.Label(scrollable_frame, text="Save:")
    row = grid_item(label_save, row, column=0, sticky="e", increment=False)
    save_var = tk.BooleanVar()
    save_var.set(user_parameters['save'])
    chck_save = ttk.Checkbutton(scrollable_frame, variable=save_var)
    row = grid_item(chck_save, row, column=1, sticky="w")
    strg = "- Name: save\n" \
           "- Summary: Activation key for saving results during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for saving results generated during the analysis process.\n" \
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
