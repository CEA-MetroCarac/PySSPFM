"""
--> Executable Script
Graphical interface for list map reader
(run list_map_reader.main_list_map_reader)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.list_map_reader import main_list_map_reader as main_script
from PySSPFM.gui.utils import \
    (add_separator_grid, grid_item, show_tooltip, extract_var,
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
    app = init_secondary_wdw(parent=parent, wdw_title="List map reader")

    # Set default parameter values
    ind_maps = [['off', 'charac tot fit: area'],
                ['off', 'fit pars: ampli_0'],
                ['on', 'charac tot fit: area'],
                ['on', 'fit pars: ampli_0']]
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'ind maps': ind_maps,
        'interp fact': 4,
        'interp func': 'linear',
        'man mask': [],
        'ref': {'mode': 'off',
                'meas': 'charac tot fit: R_2 hyst',
                'min val': 0.95,
                'max val': None,
                'fmt': '.5f',
                'interactive': False},
        'verbose': True,
        'show plots': True,
        'save': False
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['ind maps'] = extract_var(ind_maps_var)
        user_parameters['interp fact'] = interp_fact_var.get()
        user_parameters['interp func'] = interp_func_var.get()
        user_parameters['man mask'] = extract_var(man_mask_var)
        user_parameters['ref']['meas'] = ref_meas_var.get()
        user_parameters['ref']['mode'] = ref_mode_var.get()
        user_parameters['ref']['min val'] = extract_var(ref_min_var)
        user_parameters['ref']['max val'] = extract_var(ref_max_var)
        user_parameters['ref']['fmt'] = ref_fmt_var.get()
        user_parameters['ref']['interactive'] = ref_interact_var.get()
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
        start_time = datetime.now()
        figs = main_script(user_parameters, user_parameters['dir path in'],
                           verbose=user_parameters['verbose'])
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

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: List map reader
    wdw_main_title(app, "List map reader")

    row = 3

    # Section title: File management
    label_file = ttk.Label(app, text="File management", font=("Helvetica", 14))
    row = grid_item(label_file, row, column=0, sticky="ew", columnspan=3)

    # Directory (in)
    label_in = ttk.Label(app, text="Directory (in):")
    row = grid_item(label_in, row, column=0, sticky="e", increment=False)
    dir_path_in_var = tk.StringVar()
    dir_path_in_var.set(user_parameters['dir path in'])
    entry_in = ttk.Entry(app, textvariable=dir_path_in_var)
    row = grid_item(entry_in, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in\n" \
           "- Summary: Ferroelectric measurements files directory " \
           "(txt_ferro_meas)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the ferroelectric measurements text files generated after the " \
           "2nd step of the analysis.\n" \
           "- Value: It should be a string representing a directory path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(app, text="Browse", command=browse_dir_in)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir = save_path_management(
                input_dir, dir_path_out=None, save=True,
                dirname="list_map_reader", lvl=1, create_path=False,
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
    label = ttk.Label(app, text="\tDirectory (out) (*):")
    row = grid_item(label, row, column=0, sticky="e", increment=False)
    dir_path_out_var = tk.StringVar()
    dir_path_out_var.set(default_output_dir)
    entry_out = ttk.Entry(app, textvariable=dir_path_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_out\n" \
           "- Summary: Saving directory for analysis results figures " \
           "(optional, default: toolbox directory in the same root)\n" \
           "- Description: This parameter specifies the directory where the " \
           "figures generated as a result of the analysis will be saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(app, text="Select", command=browse_dir_out)
    row = grid_item(browse_button_out, row, column=2)
    row = add_separator_grid(app, row=row)

    # Section title: Measurements
    label_meax = ttk.Label(app, text="Measurements", font=("Helvetica", 14))
    row = grid_item(label_meax, row, column=0, sticky="ew", columnspan=3)

    # Measurement
    label_ind = ttk.Label(app, text="Map to plot:")
    row = grid_item(label_ind, row, column=0, sticky="e", increment=False)
    ind_maps_var = tk.StringVar()
    ind_maps_var.set(str(user_parameters['ind maps']))
    entry_ref_ind = ttk.Entry(app, textvariable=ind_maps_var)
    row = grid_item(entry_ref_ind, row, column=1, sticky="ew")
    strg = "- Name: ind_maps\n" \
           "- Summary: List of Measurement Modes and Names for Plotting\n" \
           "- Description: This parameter is a list that specifies which " \
           "measurement modes and their corresponding names should be " \
           "used for plotting.\n" \
           "- Value: A list with dimensions (n, 2) containing strings.\n" \
           "\t- It contains pairs of measurement modes and associated " \
           "names in the format [['mode', 'name']].\n" \
           "\t- For example, [['off', 'charac tot fit: area'], " \
           "['off', 'fit pars: ampli_0'], ['on', 'charac tot fit: area'], " \
           "['on', 'fit pars: ampli_0']]"
    entry_ref_ind.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_ind, mess))
    row = add_separator_grid(app, row=row)

    # Section title: Map
    label_map = ttk.Label(app, text="Map", font=("Helvetica", 14))
    row = grid_item(label_map, row, column=0, sticky="ew", columnspan=3)

    # Interpolation Factor
    label_fact = ttk.Label(app, text="Interpolation Factor:")
    row = grid_item(label_fact, row, column=0, sticky="e", increment=False)
    interp_fact_var = tk.IntVar()
    interp_fact_var.set(user_parameters['interp fact'])
    entry_interp_fact = ttk.Entry(app, textvariable=interp_fact_var)
    row = grid_item(entry_interp_fact, row, column=1, sticky="ew")
    strg = "- Name: interp_fact\n" \
           "- Summary: Interpolation factor for sspfm maps interpolation.\n" \
           "- Description: This parameter determines the level of " \
           "interpolation to be applied to SSPFM maps.\n" \
           "- Value: Should be an integer."
    entry_interp_fact.bind("<Enter>", lambda event, mess=strg: show_tooltip(
        entry_interp_fact, mess))

    # Interpolation Function
    label_func = ttk.Label(app, text="Interpolation Function:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    interp_func_var = ttk.Combobox(app, values=['linear', 'cubic'])
    interp_func_var.set(user_parameters['interp func'])
    row = grid_item(interp_func_var, row, column=1, sticky="ew")
    strg = "- Name: interp_func\n" \
           "- Summary: Interpolation function\n" \
           "- Description: This parameter specifies the interpolation " \
           "function used for sspfm maps interpolation.\n" \
           "- Value: It can take one of the following values:" \
           " 'linear', or 'cubic'."
    interp_func_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(interp_func_var, mess))
    row = add_separator_grid(app, row=row)

    # Section title: Mask
    label_mask = ttk.Label(app, text="Mask:", font=("Helvetica", 14))
    row = grid_item(label_mask, row, column=0, sticky="ew", columnspan=3)
    row = add_separator_grid(app, row=row)

    # Subsection title
    label_man = ttk.Label(app, text="Mode manual", font=("Helvetica", 12))
    strg = "Mask is chosen manually"
    label_man.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_man, mess))
    row = grid_item(label_man, row, column=0, sticky="ew", columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(app, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    man_mask_var = tk.StringVar()
    man_mask_var.set(str(user_parameters['man mask']))
    entry_man_mask = ttk.Entry(app, textvariable=man_mask_var)
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
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_man_mask, mess))
    row = add_separator_grid(app, row=row)

    # Annotation
    label_annot = ttk.Label(app, text="OR", font=("Helvetica", 12))
    row = grid_item(label_annot, row, column=0, sticky="ew", columnspan=3)
    row = add_separator_grid(app, row=row)

    # Subsection title: Mode reference measurement
    label_ref = ttk.Label(app, text="Mode reference measurement (*)",
                          font=("Helvetica", 12))
    strg = "Construct a mask with a criterion selection on ref values.\n" \
           "Active only if list of pixels is None"
    label_ref.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_ref, mess))
    row = grid_item(label_ref, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(app, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    ref_mode_var = ttk.Combobox(app, values=["off", "on", "coupled"])
    ref_mode_var.set(user_parameters['ref']['mode'])
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
    label_meas = ttk.Label(app, text="Measurement:")
    row = grid_item(label_meas, row, column=0, sticky="e", increment=False)
    ref_meas_var = tk.StringVar()
    ref_meas_var.set(user_parameters['ref']['meas'])
    entry_ref_meas = ttk.Entry(app, textvariable=ref_meas_var)
    row = grid_item(entry_ref_meas, row, column=1, sticky="ew")
    strg = "- Name: meas\n" \
           "- Summary: Reference measurement for mask determination\n" \
           "- Description: This parameter specifies the name of the " \
           "reference measurement used to determine the mask.\n" \
           "- Value: String, representing the chosen reference measurement."
    entry_ref_meas.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_meas, mess))

    # Min Value
    label_min = ttk.Label(app, text="Min Value (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    ref_min_var = tk.StringVar()
    ref_min_var.set(user_parameters['ref']['min val'])
    entry_ref_min = ttk.Entry(app, textvariable=ref_min_var)
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
    label_max = ttk.Label(app, text="Max Value (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    ref_max_var = tk.StringVar()
    ref_max_var.set(user_parameters['ref']['max val'])
    entry_ref_max = ttk.Entry(app, textvariable=ref_max_var)
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
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_max, mess))

    # Format
    label_fmt = ttk.Label(app, text="Format:")
    row = grid_item(label_fmt, row, column=0, sticky="e", increment=False)
    ref_fmt_var = tk.StringVar()
    ref_fmt_var.set(user_parameters['ref']['fmt'])
    entry_ref_fmt = ttk.Entry(app, textvariable=ref_fmt_var)
    row = grid_item(entry_ref_fmt, row, column=1, sticky="ew")
    strg = "- Name: fmt\n" \
           "- Summary: Format for measurement reference (number of decimal)\n" \
           "- Description: This parameter specifies the format for the " \
           "measurement reference with a specified number of decimal " \
           "places.\n" \
           "- Value: String, representing the format of the printed value " \
           "in the map."
    entry_ref_fmt.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_fmt, mess))

    # Reference interactive
    label_interact = ttk.Label(app, text="Interactive:")
    row = grid_item(label_interact, row, column=0, sticky="e", increment=False)
    ref_interact_var = tk.BooleanVar()
    ref_interact_var.set(user_parameters['ref']['interactive'])
    chck_ref_interact = ttk.Checkbutton(app, variable=ref_interact_var)
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
    row = add_separator_grid(app, row=row)

    # Section title: Save and plot
    label_chck = ttk.Label(app, text="Save and plot", font=("Helvetica", 14))
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

    # Save
    label_save = ttk.Label(app, text="Save:")
    row = grid_item(label_save, row, column=0, sticky="e", increment=False)
    save_var = tk.BooleanVar()
    save_var.set(user_parameters['save'])
    chck_save = ttk.Checkbutton(app, variable=save_var)
    row = grid_item(chck_save, row, column=1, sticky="w")
    strg = "- Name: save\n" \
           "- Summary: Activation key for saving results during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for saving results generated during the analysis process.\n" \
           "- Value: Boolean (True or False)."
    chck_save.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(chck_save, mess))
    row = add_separator_grid(app, row=row)

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
