"""
--> Executable Script
Graphical interface for sort and plot pixel extremum analysis
(run sort_plot_pixel.main_sort_plot_pixel)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.settings import get_setting
from PySSPFM.toolbox.sort_plot_pixel import main_sort_plot_pixel as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip,
     extract_var, init_secondary_wdw, wdw_main_title, create_useful_links_button)
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
    title = "Sort and plot pixels"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'dir path in prop': '',
        'dir path in loop': '',
        'dir path in pars': '',
        'prop key': {'mode': 'off',
                     'prop': 'charac tot fit: area'},
        'list pixels': None,
        'reverse': False,
        'del 1st loop': True,
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
        user_parameters['dir path in prop'] = extract_var(dir_path_in_prop_var)
        user_parameters['dir path in loop'] = extract_var(dir_path_in_loop_var)
        user_parameters['dir path in pars'] = \
            extract_var(dir_path_in_pars_var)
        user_parameters['prop key']['mode'] = mode_var.get()
        user_parameters['prop key']['prop'] = prop_var.get()
        user_parameters['list pixels'] = extract_var(list_pix_var)
        user_parameters['reverse'] = reverse_var.get()
        user_parameters['del 1st loop'] = del_1st_loop_var.get()
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

        # Data analysis
        main_script(user_parameters, user_parameters['dir path in'],
                    verbose=user_parameters['verbose'],
                    show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dirname=user_parameters['dir path out'])

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="sort_plot_pixel_params.json",
                            verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_prop():
        dir_path_prop = filedialog.askdirectory()
        dir_path_in_prop_var.set(dir_path_prop)

    def browse_dir_loop():
        dir_path_loop = filedialog.askdirectory()
        dir_path_in_loop_var.set(dir_path_loop)

    def browse_dir_pars():
        dir_path_pars = filedialog.askdirectory()
        dir_path_in_pars_var.set(dir_path_pars)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Pixel extremum analysis
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
           "- Summary: Results of analysis directory " \
           "(default: 'title_meas'_'yyyy-mm-dd-HHhMMm'_out_'mode')\n" \
           "- Description: This parameter specifies the directory containing " \
           "the results of analysis generated after the 1st and 2nd step " \
           "of the analysis.\n" \
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
                dirname="sort_plot_pixel", lvl=0, create_path=False,
                post_analysis=True)
        else:
            output_dir = ""
        return output_dir

    # Function to generate the default input properties directory path
    def generate_default_input_props_dir(input_dir):
        properties_folder_name = get_setting('default_properties_folder_name')
        if input_dir != "":
            input_props_dir = os.path.join(input_dir, properties_folder_name)
        else:
            input_props_dir = ""
        return input_props_dir

    # Function to generate the default input loop directory path
    def generate_default_input_loop_dir(input_dir):
        nanoloops_folder_name = get_setting('default_nanoloops_folder_name')
        if input_dir != "":
            input_loop_dir = os.path.join(input_dir, nanoloops_folder_name)
        else:
            input_loop_dir = ""
        return input_loop_dir

    # Function to generate the default input pars dir path
    def generate_default_input_pars_dir(input_dir):
        if input_dir != "":
            input_pars_dir = input_dir
        else:
            input_pars_dir = ""
        return input_pars_dir

    # Function to update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = dir_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        dir_path_out_var.set(def_output_dir)

    # Function to update the default input properties dir path when input
    # dir changes
    def update_default_input_props_dir():
        input_dir = dir_path_in_var.get()
        def_input_props_dir = generate_default_input_props_dir(input_dir)
        dir_path_in_prop_var.set(def_input_props_dir)

    # Function to update the default input loop dir path when input dir changes
    def update_default_input_loop_dir():
        input_dir = dir_path_in_var.get()
        def_input_loop_dir = generate_default_input_loop_dir(input_dir)
        dir_path_in_loop_var.set(def_input_loop_dir)

    # Update the default input pars dir path when input dir changes
    def update_default_input_pars_dir():
        input_dir = dir_path_in_var.get()
        def_input_pars_dir = generate_default_input_pars_dir(input_dir)
        dir_path_in_pars_var.set(def_input_pars_dir)

    # Bind the function (output dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Bind the function (input prop dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_props_dir())

    # Bind the function (input loop dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_loop_dir())

    # Bind function (input pars dir) to input directory widget
    dir_path_in_var.trace_add(
        "write", lambda *args: update_default_input_pars_dir())

    # Directory properties (in)
    default_input_dir = dir_path_in_var.get()
    default_input_props_dir = generate_default_output_dir(default_input_dir)
    label_prop = ttk.Label(scrollable_frame,
                           text="Directory properties (in) (*):")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    dir_path_in_prop_var = tk.StringVar()
    dir_path_in_prop_var.set(default_input_props_dir)
    entry_prop = ttk.Entry(scrollable_frame, textvariable=dir_path_in_prop_var)
    row = grid_item(entry_prop, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in_prop\n" \
           "- Summary: Properties files directory " \
           "(optional, default: properties)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the properties text files generated after the 2nd step of the " \
           "analysis.\n" \
           "- Value: It should be a string representing a directory path."
    entry_prop.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_prop, mess))
    browse_button_prop = ttk.Button(scrollable_frame, text="Browse",
                                    command=browse_dir_prop)
    row = grid_item(browse_button_prop, row, column=2)

    # Directory txt loop (in)
    default_input_dir = dir_path_in_var.get()
    default_input_loop_dir = generate_default_output_dir(default_input_dir)
    label_loop = ttk.Label(scrollable_frame,
                           text="Directory nanoloops (in) (*):")
    row = grid_item(label_loop, row, column=0, sticky="e", increment=False)
    dir_path_in_loop_var = tk.StringVar()
    dir_path_in_loop_var.set(default_input_loop_dir)
    entry_loop = ttk.Entry(scrollable_frame, textvariable=dir_path_in_loop_var)
    row = grid_item(entry_loop, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in_loop\n" \
           "- Summary: Txt nanoloop files directory " \
           "(optional, default: nanoloops)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the nanoloop text files generated after the " \
           "1st step of the analysis.\n" \
           "- Value: It should be a string representing a directory path."
    entry_loop.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_loop, mess))
    browse_button_loop = ttk.Button(scrollable_frame, text="Browse",
                                    command=browse_dir_loop)
    row = grid_item(browse_button_loop, row, column=2)

    # Dir pars (in)
    default_input_dir = dir_path_in_var.get()
    default_input_pars_dir = \
        generate_default_input_pars_dir(default_input_dir)
    label_pars = ttk.Label(scrollable_frame,
                           text="Directory csv meas sheet (in) (*):")
    row = grid_item(label_pars, row, column=0, sticky="e", increment=False)
    dir_path_in_pars_var = tk.StringVar()
    dir_path_in_pars_var.set(default_input_pars_dir)
    entry_pars = ttk.Entry(scrollable_frame, textvariable=dir_path_in_pars_var)
    row = grid_item(entry_pars, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in_pars\n" \
           "- Summary: Path of the CSV measurement sheet directory " \
           "(optional, default: 'title_meas_out_mode')\n" \
           "- Description: This parameter specifies the directory containing " \
           "path of the CSV measurement sheet.\n" \
           "- Value: It should be a string representing a directory path."
    entry_pars.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_pars, mess))
    browse_button_pars = ttk.Button(scrollable_frame, text="Browse",
                                    command=browse_dir_pars)
    row = grid_item(browse_button_pars, row, column=2)

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

    # Section title: Property
    label_prop = ttk.Label(scrollable_frame, text="Property",
                           font=("Helvetica", 14))
    row = grid_item(label_prop, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(scrollable_frame, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(scrollable_frame, values=["off", "on", "coupled"])
    mode_var.set(user_parameters["prop key"]['mode'])
    row = grid_item(mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Mode used for property.\n" \
           "- Description: This parameter specifies the mode used for " \
           "property.\n" \
           "- Value: A string with three possible values: 'on,' 'off,' or " \
           "'coupled.'"
    mode_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(mode_var, mess))

    # Property
    label_prop_name = ttk.Label(scrollable_frame, text="Property:")
    row = grid_item(label_prop_name, row, column=0, sticky="e", increment=False)
    prop_var = tk.StringVar()
    prop_var.set(user_parameters['prop key']['prop'])
    entry_prop_name = ttk.Entry(scrollable_frame, textvariable=prop_var)
    row = grid_item(entry_prop_name, row, column=1, sticky="ew")
    strg = "- Name: prop\n" \
           "- Summary: Name of the propurement.\n" \
           "- Description: This parameter represents the name of the " \
           "property.\n" \
           "- Value: A string that contains the name of the property."
    entry_prop_name.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_prop_name, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Pixel selection
    label_meas = ttk.Label(scrollable_frame, text="Pixel selection",
                           font=("Helvetica", 14))
    row = grid_item(label_meas, row, column=0, sticky="ew", columnspan=3)

    # List of Pixels
    label_pix = ttk.Label(scrollable_frame, text="List of Pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    list_pix_var = tk.StringVar()
    list_pix_var.set(str(user_parameters['list pixels']))
    entry_list_pix = ttk.Entry(scrollable_frame, textvariable=list_pix_var)
    row = grid_item(entry_list_pix, row, column=1, sticky="ew")
    strg = "- Name: list_pix\n" \
           "- Summary: List of pixel indices to analyze.\n" \
           "- Description: This parameter is used to specify a list of " \
           "pixel indices for analysis.\n" \
           "- Value: A list of integers:\n" \
           "\t--> if list_pix is []: all pixel are analyzed in ascending " \
           "order in term of index\n" \
           "\t--> if list_pix is [a, b, c ...] file of index a, b, c [...] " \
           "are analyzed\n" \
           "\t--> if list_pix is None: all pixels are analyzed in ascending " \
           "order in term of value of prop"
    entry_list_pix.bind("<Enter>",
                        lambda event, mess=strg: show_tooltip(entry_list_pix,
                                                              mess))

    # Reverse
    label_reverse = ttk.Label(scrollable_frame, text="Reverse Pixel Order:")
    row = grid_item(label_reverse, row, column=0, sticky="e", increment=False)
    reverse_var = tk.BooleanVar()
    reverse_var.set(user_parameters['reverse'])
    chck_reverse = ttk.Checkbutton(scrollable_frame, variable=reverse_var)
    row = grid_item(chck_reverse, row, column=1, sticky="w")
    strg = "- Name: reverse\n" \
           "- Summary: Reverse the order of pixels to analyze.\n" \
           "- Description: This parameter allows you to control the order " \
           "in which pixels are analyzed. When set to True, it reverses " \
           "the order of pixels that are analyzed.\n" \
           "- Value: Boolean (True or False)."
    chck_reverse.bind("<Enter>",
                      lambda event, mess=strg: show_tooltip(chck_reverse, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Loop plotting
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
           "deletes the first loop of the analysis, which is typically " \
           "used for calculating the mean hysteresis.\nThis can be " \
           "useful when the first write voltage values are equal to " \
           "zero, indicating that the material is in a pristine state, " \
           "and the loop shape would be different from the polarized state. " \
           "Deleting the first loop helps to avoid artifacts in the " \
           "analysis.\nThis parameter has influence only on figure.\n" \
           "- Value: Boolean (True or False)"
    chck_del.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(chck_del, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Map
    label_title_map = ttk.Label(scrollable_frame, text="Map",
                                font=("Helvetica", 14))
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
