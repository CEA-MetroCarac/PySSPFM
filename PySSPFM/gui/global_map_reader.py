"""
--> Executable Script
Graphical interface for global map reader
(run global_map_reader.main_global_map_reader)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.toolbox.global_map_reader import \
    main_global_map_reader as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
     init_secondary_wdw, wdw_main_title, create_useful_links_button)
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
    title = "Global map reader"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'interp fact': 4,
        'interp func': 'linear',
        'revert mask': {'on': False,
                        'off': False,
                        'coupled': False,
                        'other': False},
        'man mask': {'on': [],
                     'off': [],
                     'coupled': [],
                     'other': []},
        'ref': {'on': {'prop': 'charac tot fit: area',
                       'min val': None,
                       'max val': 0.005,
                       'fmt': '.5f',
                       'interactive': False},
                'off': {'prop': 'charac tot fit: area',
                        'min val': None,
                        'max val': 0.005,
                        'fmt': '.5f',
                        'interactive': False},
                'coupled': {'prop': 'r_2',
                            'min val': 0.95,
                            'max val': None,
                            'fmt': '.5f',
                            'interactive': False},
                'other': {'prop': 'deflection error',
                          'fmt': '.2f',
                          'min val': None,
                          'max val': 5,
                          'interactive': False}},
        'verbose': True,
        'show plots': True,
        'save': False,
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['interp fact'] = interp_fact_var.get()
        user_parameters['interp func'] = interp_func_var.get()
        user_parameters['revert mask']['off'] = revert_mask_off_var.get()
        user_parameters['revert mask']['on'] = revert_mask_on_var.get()
        user_parameters['revert mask']['coupled'] = \
            revert_mask_coupled_var.get()
        user_parameters['revert mask']['other'] = \
            revert_mask_other_var.get()
        user_parameters['man mask']['off'] = extract_var(man_mask_off_var)
        user_parameters['man mask']['on'] = extract_var(man_mask_on_var)
        user_parameters['man mask']['coupled'] = \
            extract_var(man_mask_coupled_var)
        user_parameters['man mask']['other'] = \
            extract_var(man_mask_other_var)
        user_parameters['ref']['off']["prop"] = ref_prop_off_var.get()
        user_parameters['ref']['on']["prop"] = ref_prop_on_var.get()
        user_parameters['ref']['coupled']["prop"] = ref_prop_coupled_var.get()
        user_parameters['ref']['other']["prop"] = ref_prop_other_var.get()
        user_parameters['ref']['off']["min val"] = extract_var(ref_min_off_var)
        user_parameters['ref']['on']["min val"] = extract_var(ref_min_on_var)
        user_parameters['ref']['coupled']["min val"] = \
            extract_var(ref_min_coupled_var)
        user_parameters['ref']['other']["min val"] = \
            extract_var(ref_min_other_var)
        user_parameters['ref']['off']["max val"] = extract_var(ref_max_off_var)
        user_parameters['ref']['on']["max val"] = extract_var(ref_max_on_var)
        user_parameters['ref']['coupled']["max val"] = \
            extract_var(ref_max_coupled_var)
        user_parameters['ref']['other']["max val"] = \
            extract_var(ref_max_other_var)
        user_parameters['ref']['off']["fmt"] = ref_fmt_off_var.get()
        user_parameters['ref']['on']["fmt"] = ref_fmt_on_var.get()
        user_parameters['ref']['coupled']["fmt"] = ref_fmt_coupled_var.get()
        user_parameters['ref']['other']["fmt"] = ref_fmt_other_var.get()
        user_parameters['ref']['off']["interactive"] = \
            ref_interact_off_var.get()
        user_parameters['ref']['on']["interactive"] = \
            ref_interact_on_var.get()
        user_parameters['ref']['coupled']["interactive"] = \
            ref_interact_coupled_var.get()
        user_parameters['ref']['other']["interactive"] = \
            ref_interact_other_var.get()
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save'] = save_var.get()

        # Create out directory if not exist
        if user_parameters['save']:
            if user_parameters['dir path out'] is not None:
                if not os.path.exists(user_parameters['dir path out']):
                    os.makedirs(user_parameters['dir path out'])
                    print(f"path created : {user_parameters['dir path out']}")

        # Data analysis
        main_script(user_parameters,
                    verbose=user_parameters['verbose'],
                    show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dir_path_in=user_parameters['dir path in'],
                    dir_path_out=user_parameters['dir path out'])

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="global_map_reader_params.json",
                            verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Global map reader
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
           "(default: properties)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the properties text files generated after the 2nd step of the " \
           "analysis.\n" \
           "- Value: It should be a string representing a directory path."
    entry_in.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(scrollable_frame, text="Browse",
                                  command=browse_dir_in)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir = save_path_management(
                input_dir, dir_path_out=None, save=True,
                dirname="global_map_reader", lvl=1, create_path=False,
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
    label_out = ttk.Label(scrollable_frame, text="Directory (out) (*):")
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

    # Section title: Map
    label_title_map = ttk.Label(scrollable_frame, text="Map", font=("Helvetica", 14))
    row = grid_item(label_title_map, row, column=0, sticky="ew", columnspan=3)

    # Interpolation Factor
    label_fact = ttk.Label(scrollable_frame, text="Interpolation Factor:")
    row = grid_item(label_fact, row, column=0, sticky="e", increment=False)
    interp_fact_var = tk.IntVar()
    interp_fact_var.set(user_parameters['interp fact'])
    entry_fact = ttk.Entry(scrollable_frame, textvariable=interp_fact_var)
    row = grid_item(entry_fact, row, column=1, sticky="ew")
    strg = "- Name: interp_fact\n" \
           "- Summary: Interpolation factor for sspfm maps interpolation.\n" \
           "- Description: This parameter determines the level of " \
           "interpolation to be applied to SSPFM maps.\n" \
           "- Value: Should be an integer."
    entry_fact.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_fact, mess))

    # Interpolation Function
    label_func = ttk.Label(scrollable_frame, text="Interpolation Function:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    interp_func_var = ttk.Combobox(scrollable_frame,
                                   values=['linear', 'cubic'])
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

    # Section title: Mask: Off Field
    label_mask_off = ttk.Label(scrollable_frame, text="Mask: Off Field",
                               font=("Helvetica", 14))
    row = grid_item(label_mask_off, row, column=0, sticky="ew",  columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode manual
    label_man_off = ttk.Label(scrollable_frame, text="Mode manual",
                              font=("Helvetica", 12))
    strg = "Mask is chosen manually"
    label_man_off.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_man_off, mess))
    row = grid_item(label_man_off, row, column=0, sticky="ew",  columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(scrollable_frame, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    man_mask_off_var = tk.StringVar()
    man_mask_off_var.set(str(user_parameters['man mask']['off']))
    entry_man_mask_off = ttk.Entry(scrollable_frame, textvariable=man_mask_off_var)
    row = grid_item(entry_man_mask_off, row, column=1, sticky="ew")
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
    entry_man_mask_off.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_man_mask_off, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Annotation
    label_annot = ttk.Label(scrollable_frame, text="OR", font=("Helvetica", 12))
    row = grid_item(label_annot, row, column=0, sticky="ew", columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode reference property
    label_ref_off = ttk.Label(
        scrollable_frame, text="Mode reference property (*)",
        font=("Helvetica", 12))
    strg = "Construct a mask with a criterion selection on ref values.\n" \
           "Active only if list of pixels is None"
    label_ref_off.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_ref_off, mess))
    row = grid_item(label_ref_off, row, column=0, sticky="ew", columnspan=3)

    # Reference property
    label_prop = ttk.Label(scrollable_frame, text="property:")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    ref_prop_off_var = tk.StringVar()
    ref_prop_off_var.set(user_parameters['ref']['off']['prop'])
    entry_ref_prop_off = ttk.Entry(scrollable_frame, textvariable=ref_prop_off_var)
    row = grid_item(entry_ref_prop_off, row, column=1, sticky="ew")
    strg = "- Name: prop\n" \
           "- Summary: Reference measurement for mask determination\n" \
           "- Description: This parameter specifies the name of the " \
           "reference measurement used to determine the mask.\n" \
           "- Value: String, representing the chosen reference property."
    entry_ref_prop_off.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_prop_off, mess))

    # Min Value
    label_min = ttk.Label(scrollable_frame, text="Min Value (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    ref_min_off_var = tk.StringVar()
    ref_min_off_var.set(user_parameters['ref']['off']['min val'])
    entry_ref_min_off = ttk.Entry(scrollable_frame, textvariable=ref_min_off_var)
    row = grid_item(entry_ref_min_off, row, column=1, sticky="ew")
    strg = "- Name: min val\n" \
           "- Summary: Minimum value for reference mask\n" \
           "- Description: This parameter specifies the minimum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the minimum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no minimum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_min_off.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_min_off, mess))

    # Max Value
    label_max = ttk.Label(scrollable_frame, text="Max Value (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    ref_max_off_var = tk.StringVar()
    ref_max_off_var.set(user_parameters['ref']['off']['max val'])
    entry_ref_max_off = ttk.Entry(scrollable_frame, textvariable=ref_max_off_var)
    row = grid_item(entry_ref_max_off, row, column=1, sticky="ew")
    strg = "- Name: max val\n" \
           "- Summary: Maximum value for reference mask\n" \
           "- Description: This parameter specifies the maximum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the maximum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no maximum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_max_off.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_max_off, mess))

    # Format
    label_format = ttk.Label(scrollable_frame, text="Format:")
    row = grid_item(label_format, row, column=0, sticky="e", increment=False)
    ref_fmt_off_var = tk.StringVar()
    ref_fmt_off_var.set(user_parameters['ref']['off']['fmt'])
    entry_ref_fmt_off = ttk.Entry(scrollable_frame, textvariable=ref_fmt_off_var)
    row = grid_item(entry_ref_fmt_off, row, column=1, sticky="ew")
    strg = "- Name: fmt\n" \
           "- Summary: Format for property reference (number of decimal)\n" \
           "- Description: This parameter specifies the format for the " \
           "property reference with a specified number of decimal " \
           "places.\n" \
           "- Value: String, representing the format of the printed value " \
           "in the map."
    entry_ref_fmt_off.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_fmt_off, mess))

    # Reference interactive
    label_interact = ttk.Label(scrollable_frame, text="Interactive:")
    row = grid_item(label_interact, row, column=0, sticky="e", increment=False)
    ref_interact_off_var = tk.BooleanVar()
    ref_interact_off_var.set(user_parameters['ref']['off']['interactive'])
    chck_ref_interact_off = ttk.Checkbutton(scrollable_frame,
                                            variable=ref_interact_off_var)
    row = grid_item(chck_ref_interact_off, row, column=1, sticky="w")
    strg = "- Name: interactive\n" \
           "- Summary: Interactive mode for constructing a mask from " \
           "reference.\n" \
           "- Description: This parameter enables interactive mode, " \
           "which allows users to determine mask limits interactively " \
           "using the reference property.\n" \
           "- Value: Boolean (True or False)."
    chck_ref_interact_off.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_ref_interact_off, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Revert Mask
    label_rev = ttk.Label(scrollable_frame, text="Revert:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    revert_mask_off_var = tk.BooleanVar()
    revert_mask_off_var.set(user_parameters['revert mask']['off'])
    chck_revert_mask_off = ttk.Checkbutton(scrollable_frame,
                                           variable=revert_mask_off_var)
    row = grid_item(chck_revert_mask_off, row, column=1, sticky="w")
    strg = "- Name: revert_mask\n" \
           "- Summary: Revert option of the mask for selecting specific " \
           "files.\n" \
           "- Description: This parameter specifies if the mask should be " \
           "reverted (True), or not (False).\n" \
           "- Value: Boolean (True or False)."
    chck_revert_mask_off.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_revert_mask_off, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Mask: On Field
    label_mask_on = ttk.Label(scrollable_frame, text="Mask: On Field",
                              font=("Helvetica", 14))
    row = grid_item(label_mask_on, row, column=0, sticky="ew", columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode manual
    label_man_on = ttk.Label(scrollable_frame, text="Mode manual",
                             font=("Helvetica", 12))
    strg = "Mask is chosen manually"
    label_man_on.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_man_on, mess))
    row = grid_item(label_man_on, row, column=0, sticky="ew",  columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(scrollable_frame, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    man_mask_on_var = tk.StringVar()
    man_mask_on_var.set(str(user_parameters['man mask']['on']))
    entry_man_mask_on = ttk.Entry(scrollable_frame, textvariable=man_mask_on_var)
    row = grid_item(entry_man_mask_on, row, column=1, sticky="ew")
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
    entry_man_mask_on.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_man_mask_on, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Annotation
    label_annot = ttk.Label(scrollable_frame, text="OR", font=("Helvetica", 12))
    row = grid_item(label_annot, row, column=0, sticky="ew", columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode reference property
    label_ref_on = ttk.Label(
        scrollable_frame, text="Mode reference property (*)",
        font=("Helvetica", 12))
    strg = "Construct a mask with a criterion selection on ref values.\n" \
           "Active only if list of pixels is None"
    label_ref_on.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_ref_on, mess))
    row = grid_item(label_ref_on, row, column=0, sticky="ew", columnspan=3)

    # Reference Property
    label_prop = ttk.Label(scrollable_frame, text="Property:")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    ref_prop_on_var = tk.StringVar()
    ref_prop_on_var.set(user_parameters['ref']['on']['prop'])
    entry_ref_prop_on = ttk.Entry(scrollable_frame, textvariable=ref_prop_on_var)
    row = grid_item(entry_ref_prop_on, row, column=1, sticky="ew")
    strg = "- Name: prop\n" \
           "- Summary: Reference measurement for mask determination\n" \
           "- Description: This parameter specifies the name of the " \
           "reference property used to determine the mask.\n" \
           "- Value: String, representing the chosen reference property."
    entry_ref_prop_on.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_prop_on, mess))

    # Min Value
    label_min = ttk.Label(scrollable_frame, text="Min Value (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    ref_min_on_var = tk.StringVar()
    ref_min_on_var.set(user_parameters['ref']['on']['min val'])
    entry_ref_min_on = ttk.Entry(scrollable_frame, textvariable=ref_min_on_var)
    row = grid_item(entry_ref_min_on, row, column=1, sticky="ew")
    strg = "- Name: min val\n" \
           "- Summary: Minimum value for reference mask\n" \
           "- Description: This parameter specifies the minimum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the minimum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no minimum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_min_on.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_min_on, mess))

    # Max Value
    label_max = ttk.Label(scrollable_frame, text="Max Value (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    ref_max_on_var = tk.StringVar()
    ref_max_on_var.set(user_parameters['ref']['on']['max val'])
    entry_ref_max_on = ttk.Entry(scrollable_frame, textvariable=ref_max_on_var)
    row = grid_item(entry_ref_max_on, row, column=1, sticky="ew")
    strg = "- Name: max val\n" \
           "- Summary: Maximum value for reference mask\n" \
           "- Description: This parameter specifies the maximum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the maximum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no maximum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_max_on.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_max_on, mess))

    # Format
    label_format = ttk.Label(scrollable_frame, text="Format:")
    row = grid_item(label_format, row, column=0, sticky="e", increment=False)
    ref_fmt_on_var = tk.StringVar()
    ref_fmt_on_var.set(user_parameters['ref']['on']['fmt'])
    entry_ref_fmt_on = ttk.Entry(scrollable_frame, textvariable=ref_fmt_on_var)
    row = grid_item(entry_ref_fmt_on, row, column=1, sticky="ew")
    strg = "- Name: fmt\n" \
           "- Summary: Format for property reference (number of decimal)\n" \
           "- Description: This parameter specifies the format for the " \
           "property reference with a specified number of decimal " \
           "places.\n" \
           "- Value: String, representing the format of the printed value " \
           "in the map."
    entry_ref_fmt_on.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_fmt_on, mess))

    # Reference interactive
    label_interact = ttk.Label(scrollable_frame, text="Interactive:")
    row = grid_item(label_interact, row, column=0, sticky="e", increment=False)
    ref_interact_on_var = tk.BooleanVar()
    ref_interact_on_var.set(user_parameters['ref']['on']['interactive'])
    chck_ref_interact_on = ttk.Checkbutton(scrollable_frame,
                                           variable=ref_interact_on_var)
    row = grid_item(chck_ref_interact_on, row, column=1, sticky="w")
    strg = "- Name: interactive\n" \
           "- Summary: Interactive mode for constructing a mask from " \
           "reference.\n" \
           "- Description: This parameter enables interactive mode, " \
           "which allows users to determine mask limits interactively " \
           "using the reference property.\n" \
           "- Value: Boolean (True or False)."
    chck_ref_interact_on.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_ref_interact_on, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Revert Mask
    label_rev = ttk.Label(scrollable_frame, text="Revert:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    revert_mask_on_var = tk.BooleanVar()
    revert_mask_on_var.set(user_parameters['revert mask']['on'])
    chck_revert_mask_on = ttk.Checkbutton(
        scrollable_frame, variable=revert_mask_on_var)
    row = grid_item(chck_revert_mask_on, row, column=1, sticky="w")
    strg = "- Name: revert_mask\n" \
           "- Summary: Revert option of the mask for selecting specific " \
           "files.\n" \
           "- Description: This parameter specifies if the mask should be " \
           "reverted (True), or not (False).\n" \
           "- Value: Boolean (True or False)."
    chck_revert_mask_on.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_revert_mask_on, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Mask: Coupled
    label_mask_coupled = ttk.Label(scrollable_frame, text="Mask: Coupled",
                                   font=("Helvetica", 14))
    row = grid_item(label_mask_coupled, row, column=0, sticky="ew",
                    columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode manual
    label_man_coupled = ttk.Label(scrollable_frame, text="Mode manual",
                                  font=("Helvetica", 12))
    strg = "Mask is chosen manually"
    label_man_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(label_man_coupled, mess))
    row = grid_item(label_man_coupled, row, column=0, sticky="ew",
                    columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(scrollable_frame, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    man_mask_coupled_var = tk.StringVar()
    man_mask_coupled_var.set(str(user_parameters['man mask']['coupled']))
    entry_man_mask_coupled = ttk.Entry(scrollable_frame,
                                       textvariable=man_mask_coupled_var)
    row = grid_item(entry_man_mask_coupled, row, column=1, sticky="ew")
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
    entry_man_mask_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_man_mask_coupled, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Annotation
    label_annot = ttk.Label(scrollable_frame, text="OR", font=("Helvetica", 12))
    row = grid_item(label_annot, row, column=0, sticky="ew", columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode reference property
    label_ref_coupled = ttk.Label(
        scrollable_frame, text="Mode reference property (*)",
        font=("Helvetica", 12))
    strg = "Construct a mask with a criterion selection on ref values.\n" \
           "Active only if list of pixels is None"
    label_ref_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(label_ref_coupled, mess))
    row = grid_item(label_ref_coupled, row, column=0, sticky="ew", columnspan=3)

    # Reference Property
    label_prop = ttk.Label(scrollable_frame, text="Property:")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    ref_prop_coupled_var = tk.StringVar()
    ref_prop_coupled_var.set(user_parameters['ref']['coupled']['prop'])
    entry_ref_prop_coupled = ttk.Entry(scrollable_frame,
                                       textvariable=ref_prop_coupled_var)
    row = grid_item(entry_ref_prop_coupled, row, column=1, sticky="ew")
    strg = "- Name: prop\n" \
           "- Summary: Reference property for mask determination\n" \
           "- Description: This parameter specifies the name of the " \
           "reference property used to determine the mask.\n" \
           "- Value: String, representing the chosen reference property."
    entry_ref_prop_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_prop_coupled, mess))

    # Min Value
    label_min = ttk.Label(scrollable_frame, text="Min Value (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    ref_min_coupled_var = tk.StringVar()
    ref_min_coupled_var.set(user_parameters['ref']['coupled']['min val'])
    entry_ref_min_coupled = ttk.Entry(scrollable_frame,
                                      textvariable=ref_min_coupled_var)
    row = grid_item(entry_ref_min_coupled, row, column=1, sticky="ew")
    strg = "- Name: min val\n" \
           "- Summary: Minimum value for reference mask\n" \
           "- Description: This parameter specifies the minimum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the minimum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no minimum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_min_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_min_coupled, mess))

    # Max Value
    label_max = ttk.Label(scrollable_frame, text="Max Value (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    ref_max_coupled_var = tk.StringVar()
    ref_max_coupled_var.set(user_parameters['ref']['coupled']['max val'])
    entry_ref_max_coupled = ttk.Entry(scrollable_frame,
                                      textvariable=ref_max_coupled_var)
    row = grid_item(entry_ref_max_coupled, row, column=1, sticky="ew")
    strg = "- Name: max val\n" \
           "- Summary: Maximum value for reference mask\n" \
           "- Description: This parameter specifies the maximum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the maximum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no maximum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_max_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_max_coupled, mess))

    # Format
    label_format = ttk.Label(scrollable_frame, text="Format:")
    row = grid_item(label_format, row, column=0, sticky="e", increment=False)
    ref_fmt_coupled_var = tk.StringVar()
    ref_fmt_coupled_var.set(user_parameters['ref']['coupled']['fmt'])
    entry_ref_fmt_coupled = ttk.Entry(scrollable_frame,
                                      textvariable=ref_fmt_coupled_var)
    row = grid_item(entry_ref_fmt_coupled, row, column=1, sticky="ew")
    strg = "- Name: fmt\n" \
           "- Summary: Format for property reference (number of decimal)\n" \
           "- Description: This parameter specifies the format for the " \
           "property reference with a specified number of decimal " \
           "places.\n" \
           "- Value: String, representing the format of the printed value " \
           "in the map."
    entry_ref_fmt_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_fmt_coupled, mess))

    # Reference interactive
    label_interact = ttk.Label(scrollable_frame, text="Interactive:")
    row = grid_item(label_interact, row, column=0, sticky="e", increment=False)
    ref_interact_coupled_var = tk.BooleanVar()
    ref_interact_coupled_var.set(
        user_parameters['ref']['coupled']['interactive'])
    chck_ref_interact_coupled = ttk.Checkbutton(
        scrollable_frame, variable=ref_interact_coupled_var)
    row = grid_item(chck_ref_interact_coupled, row, column=1, sticky="w")
    strg = "- Name: interactive\n" \
           "- Summary: Interactive mode for constructing a mask from " \
           "reference.\n" \
           "- Description: This parameter enables interactive mode, " \
           "which allows users to determine mask limits interactively " \
           "using the reference property.\n" \
           "- Value: Boolean (True or False)."
    chck_ref_interact_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_ref_interact_coupled, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Revert Mask
    label_rev = ttk.Label(scrollable_frame, text="Revert:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    revert_mask_coupled_var = tk.BooleanVar()
    revert_mask_coupled_var.set(user_parameters['revert mask']['coupled'])
    chck_revert_mask_coupled = ttk.Checkbutton(
        scrollable_frame, variable=revert_mask_coupled_var)
    row = grid_item(chck_revert_mask_coupled, row, column=1, sticky="w")
    strg = "- Name: revert_mask\n" \
           "- Summary: Revert option of the mask for selecting specific " \
           "files.\n" \
           "- Description: This parameter specifies if the mask should be " \
           "reverted (True), or not (False).\n" \
           "- Value: Boolean (True or False)."
    chck_revert_mask_coupled.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_revert_mask_coupled, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Mask: Other
    label_mask_other = ttk.Label(scrollable_frame, text="Mask: Other",
                                 font=("Helvetica", 14))
    row = grid_item(label_mask_other, row, column=0, sticky="ew",
                    columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode manual
    label_man_other = ttk.Label(scrollable_frame, text="Mode manual",
                                font=("Helvetica", 12))
    strg = "Mask is chosen manually"
    label_man_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(label_man_other, mess))
    row = grid_item(label_man_other, row, column=0, sticky="ew",
                    columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(scrollable_frame, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    man_mask_other_var = tk.StringVar()
    man_mask_other_var.set(str(user_parameters['man mask']['other']))
    entry_man_mask_other = ttk.Entry(scrollable_frame,
                                     textvariable=man_mask_other_var)
    row = grid_item(entry_man_mask_other, row, column=1, sticky="ew")
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
    entry_man_mask_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_man_mask_other, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Annotation
    label_annot = ttk.Label(scrollable_frame, text="OR", font=("Helvetica", 12))
    row = grid_item(label_annot, row, column=0, sticky="ew", columnspan=3)
    row = add_grid_separator(scrollable_frame, row=row)

    # Subsection title: Mode reference property
    label_ref_other = ttk.Label(
        scrollable_frame, text="Mode reference property (*)",
        font=("Helvetica", 12))
    strg = "Construct a mask with a criterion selection on ref values.\n" \
           "Active only if list of pixels is None"
    label_ref_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(label_ref_other, mess))
    row = grid_item(label_ref_other, row, column=0, sticky="ew", columnspan=3)

    # Reference Property
    label_prop = ttk.Label(scrollable_frame, text="Property:")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    ref_prop_other_var = tk.StringVar()
    ref_prop_other_var.set(user_parameters['ref']['other']['prop'])
    entry_ref_prop_other = ttk.Entry(scrollable_frame,
                                     textvariable=ref_prop_other_var)
    row = grid_item(entry_ref_prop_other, row, column=1, sticky="ew")
    strg = "- Name: prop\n" \
           "- Summary: Reference property for mask determination\n" \
           "- Description: This parameter specifies the name of the " \
           "reference property used to determine the mask.\n" \
           "- Value: String, representing the chosen reference property."
    entry_ref_prop_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_prop_other, mess))

    # Min Value
    label_min = ttk.Label(scrollable_frame, text="Min Value (*):")
    row = grid_item(label_min, row, column=0, sticky="e", increment=False)
    ref_min_other_var = tk.StringVar()
    ref_min_other_var.set(user_parameters['ref']['other']['min val'])
    entry_ref_min_other = ttk.Entry(scrollable_frame,
                                    textvariable=ref_min_other_var)
    row = grid_item(entry_ref_min_other, row, column=1, sticky="ew")
    strg = "- Name: min val\n" \
           "- Summary: Minimum value for reference mask\n" \
           "- Description: This parameter specifies the minimum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the minimum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no minimum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_min_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_min_other, mess))

    # Max Value
    label_max = ttk.Label(scrollable_frame, text="Max Value (*):")
    row = grid_item(label_max, row, column=0, sticky="e", increment=False)
    ref_max_other_var = tk.StringVar()
    ref_max_other_var.set(user_parameters['ref']['other']['max val'])
    entry_ref_max_other = ttk.Entry(scrollable_frame,
                                    textvariable=ref_max_other_var)
    row = grid_item(entry_ref_max_other, row, column=1, sticky="ew")
    strg = "- Name: max val\n" \
           "- Summary: Maximum value for reference mask\n" \
           "- Description: This parameter specifies the maximum value " \
           "required for the reference mask.\n" \
           "- Value: Float, representing the maximum required value of the " \
           "reference.\n" \
           "\t--> If set to None, there is no maximum value limit.\n" \
           "- Active if: This parameter is active when interactive mode is " \
           "disabled."
    entry_ref_max_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_max_other, mess))

    # Format
    label_format = ttk.Label(scrollable_frame, text="Format:")
    row = grid_item(label_format, row, column=0, sticky="e", increment=False)
    ref_fmt_other_var = tk.StringVar()
    ref_fmt_other_var.set(user_parameters['ref']['other']['fmt'])
    entry_ref_fmt_other = ttk.Entry(scrollable_frame, textvariable=ref_fmt_other_var)
    row = grid_item(entry_ref_fmt_other, row, column=1, sticky="ew")
    strg = "- Name: fmt\n" \
           "- Summary: Format for property reference (number of decimal)\n" \
           "- Description: This parameter specifies the format for the " \
           "property reference with a specified number of decimal " \
           "places.\n" \
           "- Value: String, representing the format of the printed value " \
           "in the map."
    entry_ref_fmt_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_ref_fmt_other, mess))

    # Reference interactive
    label_interact = ttk.Label(scrollable_frame, text="Interactive:")
    row = grid_item(label_interact, row, column=0, sticky="e", increment=False)
    ref_interact_other_var = tk.BooleanVar()
    ref_interact_other_var.set(
        user_parameters['ref']['other']['interactive'])
    chck_ref_interact_other = ttk.Checkbutton(
        scrollable_frame, variable=ref_interact_other_var)
    row = grid_item(chck_ref_interact_other, row, column=1, sticky="w")
    strg = "- Name: interactive\n" \
           "- Summary: Interactive mode for constructing a mask from " \
           "reference.\n" \
           "- Description: This parameter enables interactive mode, " \
           "which allows users to determine mask limits interactively " \
           "using the reference property.\n" \
           "- Value: Boolean (True or False)."
    chck_ref_interact_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_ref_interact_other, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Revert Mask
    label_rev = ttk.Label(scrollable_frame, text="Revert:")
    row = grid_item(label_rev, row, column=0, sticky="e", increment=False)
    revert_mask_other_var = tk.BooleanVar()
    revert_mask_other_var.set(user_parameters['revert mask']['other'])
    chck_revert_mask_other = ttk.Checkbutton(
        scrollable_frame, variable=revert_mask_other_var)
    row = grid_item(chck_revert_mask_other, row, column=1, sticky="w")
    strg = "- Name: revert_mask\n" \
           "- Summary: Revert option of the mask for selecting specific " \
           "files.\n" \
           "- Description: This parameter specifies if the mask should be " \
           "reverted (True), or not (False).\n" \
           "- Value: Boolean (True or False)."
    chck_revert_mask_other.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(chck_revert_mask_other, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Save and plot
    label_chk = ttk.Label(scrollable_frame, text="Save and plot",
                          font=("Helvetica", 14))
    row = grid_item(label_chk, row, column=0, sticky="ew", columnspan=3)

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
