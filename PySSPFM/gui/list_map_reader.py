"""
--> Executable Script
Graphical interface for list map reader
(run list_map_reader.main_list_map_reader)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.list_map_reader import main_list_map_reader as main_script
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
    title = "List map reader"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

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
        'meas time': None,
        'revert mask': False,
        'man mask': [],
        'ref': {'mode': 'off',
                'prop': 'charac tot fit: R_2 hyst',
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
        user_parameters['meas time'] = extract_var(meas_time_var)
        user_parameters['revert mask'] = revert_mask_var.get()
        user_parameters['man mask'] = extract_var(man_mask_var)
        user_parameters['ref']['prop'] = ref_prop_var.get()
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
        figs = main_script(user_parameters, user_parameters['dir path in'],
                           verbose=user_parameters['verbose'])
        # Plot figures
        print_plots(figs, show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dirname=user_parameters['dir path out'], transparent=False)

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="list_map_reader_params.json",
                            verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

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

    # Directory (in)
    label_in = ttk.Label(scrollable_frame, text="Directory (in):")
    row = grid_item(label_in, row, column=0, sticky="e", increment=False)
    dir_path_in_var = tk.StringVar()
    dir_path_in_var.set(user_parameters['dir path in'])
    entry_in = ttk.Entry(scrollable_frame, textvariable=dir_path_in_var)
    row = grid_item(entry_in, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in\n" \
           "- Summary: Properties files directory " \
           "(properties)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the properties text files generated after the 2nd step of the " \
           "analysis or 'phase_offset.txt' generated with " \
           "'phase_offset_analyzer.py' or 'phase_inversion.txt' generated " \
           "with 'phase_inversion_analyzer.py'.\n" \
           "- Value: It should be a string representing a directory path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(scrollable_frame, text="Browse",
                                  command=browse_dir_in)
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
    label = ttk.Label(scrollable_frame, text="\tDirectory (out) (*):")
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

    # Section title: Properties
    label_meax = ttk.Label(scrollable_frame, text="Properties",
                           font=("Helvetica", 14))
    row = grid_item(label_meax, row, column=0, sticky="ew", columnspan=3)

    # Property
    label_ind = ttk.Label(scrollable_frame, text="Map to plot:")
    row = grid_item(label_ind, row, column=0, sticky="e", increment=False)
    ind_maps_var = tk.StringVar()
    ind_maps_var.set(str(user_parameters['ind maps']))
    entry_ref_ind = ttk.Entry(scrollable_frame, textvariable=ind_maps_var)
    row = grid_item(entry_ref_ind, row, column=1, sticky="ew")
    strg = "- Name: ind_maps\n" \
           "- Summary: List of Property Modes and Names for Plotting\n" \
           "- Description: This parameter is a list that specifies which " \
           "property modes and their corresponding names should be " \
           "used for plotting.\n" \
           "- Value: A list with dimensions (n, 2) containing strings.\n" \
           "\t- It contains pairs of property modes and associated " \
           "names in the format [['mode', 'name']].\n" \
           "\t- For example, [['off', 'charac tot fit: area'], " \
           "['off', 'fit pars: ampli_0'], ['on', 'charac tot fit: area'], " \
           "['on', 'fit pars: ampli_0']]"
    entry_ref_ind.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_ind, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Map
    label_map = ttk.Label(scrollable_frame, text="Map", font=("Helvetica", 14))
    row = grid_item(label_map, row, column=0, sticky="ew", columnspan=3)

    # Interpolation Factor
    label_fact = ttk.Label(scrollable_frame, text="Interpolation Factor:")
    row = grid_item(label_fact, row, column=0, sticky="e", increment=False)
    interp_fact_var = tk.IntVar()
    interp_fact_var.set(user_parameters['interp fact'])
    entry_interp_fact = ttk.Entry(scrollable_frame,
                                  textvariable=interp_fact_var)
    row = grid_item(entry_interp_fact, row, column=1, sticky="ew")
    strg = "- Name: interp_fact\n" \
           "- Summary: Interpolation factor for sspfm maps interpolation.\n" \
           "- Description: This parameter determines the level of " \
           "interpolation to be applied to SSPFM maps.\n" \
           "- Value: Should be an integer."
    entry_interp_fact.bind("<Enter>", lambda event, mess=strg: show_tooltip(
        entry_interp_fact, mess))

    # Interpolation Function
    label_func = ttk.Label(scrollable_frame, text="Interpolation Function:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    interp_func_var = ttk.Combobox(scrollable_frame, values=['linear', 'cubic'])
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
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Measurement time
    label_title = ttk.Label(scrollable_frame, text="Measurement time:",
                            font=("Helvetica", 14))
    row = grid_item(label_title, row, column=0, sticky="ew", columnspan=3)

    # Real measurement time
    label_meas_time = ttk.Label(scrollable_frame,
                                text="Real measurement time (*):")
    row = grid_item(label_meas_time, row, column=0, sticky="e", increment=False)
    meas_time_var = tk.StringVar()
    meas_time_var.set(user_parameters['meas time'])
    entry_meas_time = ttk.Entry(scrollable_frame, textvariable=meas_time_var)
    row = grid_item(entry_meas_time, row, column=1, sticky="ew")
    strg = "- Name: meas_time\n" \
           "- Summary: Real duration of the measurement in hours.\n" \
           "- Description: This parameter represents the actual duration of " \
           "the measurement in hours. It is used to generate a time axis for " \
           "the property graphs corresponding to the measurements.\n" \
           "- Value: float\n" \
           "\tIf left empty or set to None, no time axis is generated, and " \
           "only the line index is used as the x-axis values."
    entry_meas_time.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_meas_time, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Mask
    label_mask = ttk.Label(scrollable_frame, text="Mask:",
                           font=("Helvetica", 14))
    row = grid_item(label_mask, row, column=0, sticky="ew", columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title
    label_man = ttk.Label(scrollable_frame, text="Mode manual",
                          font=("Helvetica", 12))
    strg = "Mask is chosen manually"
    label_man.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_man, mess))
    row = grid_item(label_man, row, column=0, sticky="ew", columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(scrollable_frame, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    man_mask_var = tk.StringVar()
    man_mask_var.set(str(user_parameters['man mask']))
    entry_man_mask = ttk.Entry(scrollable_frame, textvariable=man_mask_var)
    row = grid_item(entry_man_mask, row, column=1, sticky="ew")
    strg = "- Name: man_mask\n" \
           "- Summary: Manual mask for selecting specific files\n" \
           "- Description: This parameter is a list of pixel indices.\n" \
           "- Value: Dictionary with mode keys and lists of indices as " \
           "values.\n" \
           "\t--> if list of pixels is []: all files are selected.\n" \
           "\t--> if list of pixels is None: criterion of selection " \
           "is made with reference property.\n" \
           "\t--> if list of pixels is [a, b, c ...] file of index " \
           "a, b, c [...] are not selected"
    entry_man_mask.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_man_mask, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Annotation
    label_annot = ttk.Label(scrollable_frame, text="OR", font=("Helvetica", 12))
    row = grid_item(label_annot, row, column=0, sticky="ew", columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode reference property
    label_ref = ttk.Label(scrollable_frame, text="Mode reference property (*)",
                          font=("Helvetica", 12))
    strg = "Construct a mask with a criterion selection on ref values.\n" \
           "Active only if list of pixels is None"
    label_ref.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_ref, mess))
    row = grid_item(label_ref, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(scrollable_frame, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    ref_mode_var = ttk.Combobox(scrollable_frame,
                                values=["off", "on", "coupled"])
    ref_mode_var.set(user_parameters['ref']['mode'])
    row = grid_item(ref_mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Mode for Reference Property\n" \
           "- Description: This parameter determines the mode used for " \
           "the reference property.\n" \
           "- Value: String indicating the chosen mode of reference " \
           "property ('off', 'on', or 'coupled')."
    ref_mode_var.bind("<Enter>",
                      lambda event, mess=strg: show_tooltip(ref_mode_var, mess))

    # Reference Property
    label_prop = ttk.Label(scrollable_frame, text="Property:")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    ref_prop_var = tk.StringVar()
    ref_prop_var.set(user_parameters['ref']['prop'])
    entry_ref_prop = ttk.Entry(scrollable_frame, textvariable=ref_prop_var)
    row = grid_item(entry_ref_prop, row, column=1, sticky="ew")
    strg = "- Name: prop\n" \
           "- Summary: Reference property for mask determination\n" \
           "- Description: This parameter specifies the name of the " \
           "reference property used to determine the mask.\n" \
           "- Value: String, representing the chosen reference property."
    entry_ref_prop.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_prop, mess))

    # Min Value
    label_min = ttk.Label(scrollable_frame, text="Min Value (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    ref_min_var = tk.StringVar()
    ref_min_var.set(user_parameters['ref']['min val'])
    entry_ref_min = ttk.Entry(scrollable_frame, textvariable=ref_min_var)
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
    label_max = ttk.Label(scrollable_frame, text="Max Value (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    ref_max_var = tk.StringVar()
    ref_max_var.set(user_parameters['ref']['max val'])
    entry_ref_max = ttk.Entry(scrollable_frame, textvariable=ref_max_var)
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
    label_fmt = ttk.Label(scrollable_frame, text="Format:")
    row = grid_item(label_fmt, row, column=0, sticky="e", increment=False)
    ref_fmt_var = tk.StringVar()
    ref_fmt_var.set(user_parameters['ref']['fmt'])
    entry_ref_fmt = ttk.Entry(scrollable_frame, textvariable=ref_fmt_var)
    row = grid_item(entry_ref_fmt, row, column=1, sticky="ew")
    strg = "- Name: fmt\n" \
           "- Summary: Format for property reference (number of decimal)\n" \
           "- Description: This parameter specifies the format for the " \
           "property reference with a specified number of decimal " \
           "places.\n" \
           "- Value: String, representing the format of the printed value " \
           "in the map."
    entry_ref_fmt.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_fmt, mess))

    # Reference interactive
    label_interact = ttk.Label(scrollable_frame, text="Interactive:")
    row = grid_item(label_interact, row, column=0, sticky="e", increment=False)
    ref_interact_var = tk.BooleanVar()
    ref_interact_var.set(user_parameters['ref']['interactive'])
    chck_ref_interact = ttk.Checkbutton(scrollable_frame,
                                        variable=ref_interact_var)
    row = grid_item(chck_ref_interact, row, column=1, sticky="w")
    strg = "- Name: interactive\n" \
           "- Summary: Interactive mode for constructing a mask from " \
           "reference.\n" \
           "- Description: This parameter enables interactive mode, " \
           "which allows users to determine mask limits interactively " \
           "using the reference property.\n" \
           "- Value: Boolean (True or False)."
    chck_ref_interact.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_ref_interact, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Revert Mask
    label_rev = ttk.Label(scrollable_frame, text="Revert:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    revert_mask_var = tk.BooleanVar()
    revert_mask_var.set(user_parameters['revert mask'])
    chck_revert_mask = ttk.Checkbutton(scrollable_frame,
                                       variable=revert_mask_var)
    row = grid_item(chck_revert_mask, row, column=1, sticky="w")
    strg = "- Name: revert_mask\n" \
           "- Summary: Revert option of the mask for selecting specific " \
           "files.\n" \
           "- Description: This parameter specifies if the mask should be " \
           "reverted (True), or not (False).\n" \
           "- Value: Boolean (True or False)."
    chck_revert_mask.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_revert_mask, mess))
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
