"""
--> Executable Script
Graphical interface for pixel extremum analysis
(run sort_plot_pixel.main_sort_plot_pixel)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from PySSPFM.toolbox.sort_plot_pixel import main_sort_plot_pixel as main_script
from PySSPFM.gui.utils import \
    (add_separator_grid, grid_item, show_tooltip,
     extract_var, init_secondary_wdw, wdw_main_title)
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
    app = init_secondary_wdw(parent=parent, wdw_title="Pixel extremum analysis")

    # Set default parameter values
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'dir path in meas': '',
        'dir path in loop': '',
        'dir path in pars': '',
        'meas key': {'mode': 'off',
                     'meas': 'charac tot fit: area'},
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
        user_parameters['dir path in meas'] = extract_var(dir_path_in_meas_var)
        user_parameters['dir path in loop'] = extract_var(dir_path_in_loop_var)
        user_parameters['file path in pars'] = \
            extract_var(file_path_in_pars_var)
        user_parameters['meas key']['mode'] = mode_var.get()
        user_parameters['meas key']['meas'] = meas_var.get()
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
        start_time = datetime.now()
        main_script(user_parameters, user_parameters['dir path in'],
                    verbose=user_parameters['verbose'],
                    show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dirname=user_parameters['dir path out'])

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

    # Window title: Pixel extremum analysis
    wdw_main_title(app, "Pixel extremum analysis")

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
           "- Summary: Results of analysis directory " \
           "(default: 'title_meas'_'yyyy-mm-dd-HHhMMm'_out_'mode')\n" \
           "- Description: This parameter specifies the directory containing " \
           "the results of analysis generated after the 1st and 2nd step " \
           "of the analysis.\n" \
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
                dirname="plot_pix_extrem", lvl=0, create_path=False,
                post_analysis=True)
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

    # Function to update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = dir_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        dir_path_out_var.set(def_output_dir)

    # Function to update the default input meas dir path when input dir changes
    def update_default_input_meas_dir():
        input_dir = dir_path_in_var.get()
        def_input_meas_dir = generate_default_input_meas_dir(input_dir)
        dir_path_in_meas_var.set(def_input_meas_dir)

    # Function to update the default input loop dir path when input dir changes
    def update_default_input_loop_dir():
        input_dir = dir_path_in_var.get()
        def_input_loop_dir = generate_default_input_loop_dir(input_dir)
        dir_path_in_loop_var.set(def_input_loop_dir)

    # Update the default input pars file path when input dir changes
    def update_default_input_pars_file():
        input_dir = dir_path_in_var.get()
        def_input_pars_file = generate_default_input_pars_file(input_dir)
        file_path_in_pars_var.set(def_input_pars_file)

    # Bind the function (output dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Bind the function (input meas dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_meas_dir())

    # Bind the function (input loop dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_loop_dir())

    # Bind function (input pars file) to input directory widget
    dir_path_in_var.trace_add(
        "write", lambda *args: update_default_input_pars_file())

    # Directory measurements (in)
    default_input_dir = dir_path_in_var.get()
    default_input_meas_dir = generate_default_output_dir(default_input_dir)
    label_meas = ttk.Label(app, text="Directory measurements (in) (*):")
    row = grid_item(label_meas, row, column=0, sticky="e", increment=False)
    dir_path_in_meas_var = tk.StringVar()
    dir_path_in_meas_var.set(default_input_meas_dir)
    entry_meas = ttk.Entry(app, textvariable=dir_path_in_meas_var)
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
    browse_button_meas = ttk.Button(app, text="Browse", command=browse_dir_meas)
    row = grid_item(browse_button_meas, row, column=2)

    # Directory txt loop (in)
    default_input_dir = dir_path_in_var.get()
    default_input_loop_dir = generate_default_output_dir(default_input_dir)
    label_loop = ttk.Label(app, text="Directory txt loops (in) (*):")
    row = grid_item(label_loop, row, column=0, sticky="e", increment=False)
    dir_path_in_loop_var = tk.StringVar()
    dir_path_in_loop_var.set(default_input_loop_dir)
    entry_loop = ttk.Entry(app, textvariable=dir_path_in_loop_var)
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
    browse_button_loop = ttk.Button(app, text="Browse", command=browse_dir_loop)
    row = grid_item(browse_button_loop, row, column=2)

    # File pars (in)
    default_input_dir = dir_path_in_var.get()
    default_input_pars_file = \
        generate_default_input_pars_file(default_input_dir)
    label_pars = ttk.Label(app, text="File txt parameters (in) (*):")
    row = grid_item(label_pars, row, column=0, sticky="e", increment=False)
    file_path_in_pars_var = tk.StringVar()
    file_path_in_pars_var.set(default_input_pars_file)
    entry_pars = ttk.Entry(app, textvariable=file_path_in_pars_var)
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
    browse_button_pars = ttk.Button(app, text="Browse",
                                    command=browse_file_pars)
    row = grid_item(browse_button_pars, row, column=2)

    # Directory (out)
    default_input_dir = dir_path_in_var.get()
    default_output_dir = generate_default_output_dir(default_input_dir)
    label_out = ttk.Label(app, text="Directory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
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

    # Section title: Measurement
    label_meas = ttk.Label(app, text="Measurement", font=("Helvetica", 14))
    row = grid_item(label_meas, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(app, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(app, values=["off", "on", "coupled"])
    mode_var.set(user_parameters["meas key"]['mode'])
    row = grid_item(mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Mode used for measurement.\n" \
           "- Description: This parameter specifies the mode used for " \
           "measurement.\n" \
           "- Value: A string with three possible values: 'on,' 'off,' or " \
           "'coupled.'"
    mode_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(mode_var, mess))

    # Measurement
    label_meas_name = ttk.Label(app, text="Measurement:")
    row = grid_item(label_meas_name, row, column=0, sticky="e", increment=False)
    meas_var = tk.StringVar()
    meas_var.set(user_parameters['meas key']['meas'])
    entry_meas_name = ttk.Entry(app, textvariable=meas_var)
    row = grid_item(entry_meas_name, row, column=1, sticky="ew")
    strg = "- Name: meas\n" \
           "- Summary: Name of the measurement.\n" \
           "- Description: This parameter represents the name of the " \
           "measurement.\n" \
           "- Value: A string that contains the name of the measurement."
    entry_meas_name.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_meas_name, mess))
    row = add_separator_grid(app, row=row)

    # Section title: Pixel selection
    label_meas = ttk.Label(app, text="Pixel selection", font=("Helvetica", 14))
    row = grid_item(label_meas, row, column=0, sticky="ew", columnspan=3)

    # List of Pixels
    label_pix = ttk.Label(app, text="List of Pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    list_pix_var = tk.StringVar()
    list_pix_var.set(str(user_parameters['list pixels']))
    entry_list_pix = ttk.Entry(app, textvariable=list_pix_var)
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
           "order in term of value of meas"
    entry_list_pix.bind("<Enter>",
                        lambda event, mess=strg: show_tooltip(entry_list_pix,
                                                              mess))

    # Reverse
    label_reverse = ttk.Label(app, text="Reverse Pixel Order:")
    row = grid_item(label_reverse, row, column=0, sticky="e", increment=False)
    reverse_var = tk.BooleanVar()
    reverse_var.set(user_parameters['reverse'])
    chck_reverse = ttk.Checkbutton(app, variable=reverse_var)
    row = grid_item(chck_reverse, row, column=1, sticky="w")
    strg = "- Name: reverse\n" \
           "- Summary: Reverse the order of pixels to analyze.\n" \
           "- Description: This parameter allows you to control the order " \
           "in which pixels are analyzed. When set to True, it reverses " \
           "the order of pixels that are analyzed.\n" \
           "- Value: Boolean (True or False)."
    chck_reverse.bind("<Enter>",
                      lambda event, mess=strg: show_tooltip(chck_reverse, mess))
    row = add_separator_grid(app, row=row)

    # Section title: Loop plotting
    label_pha = ttk.Label(app, text="Loop plotting", font=("Helvetica", 14))
    row = grid_item(label_pha, row, column=0, sticky="ew", columnspan=3)

    # Del First Loop
    label_del = ttk.Label(app, text="Delete First Loop:")
    row = grid_item(label_del, row, column=0, sticky="e", increment=False)
    del_1st_loop_var = tk.BooleanVar()
    del_1st_loop_var.set(user_parameters['del 1st loop'])
    chck_del = ttk.Checkbutton(app, variable=del_1st_loop_var)
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
    row = add_separator_grid(app, row=row)

    # Section title: Map
    label_title_map = ttk.Label(app, text="Map", font=("Helvetica", 14))
    row = grid_item(label_title_map, row, column=0, sticky="ew", columnspan=3)

    # Interpolation Factor
    label_fact = ttk.Label(app, text="Interpolation Factor:")
    row = grid_item(label_fact, row, column=0, sticky="e", increment=False)
    interp_fact_var = tk.IntVar()
    interp_fact_var.set(user_parameters['interp fact'])
    entry_fact = ttk.Entry(app, textvariable=interp_fact_var)
    row = grid_item(entry_fact, row, column=1, sticky="ew")
    strg = "- Name: interp_fact\n" \
           "- Summary: Interpolation factor for sspfm maps interpolation.\n" \
           "- Description: This parameter determines the level of " \
           "interpolation to be applied to SSPFM maps.\n" \
           "- Value: Should be an integer."
    entry_fact.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_fact, mess))

    # Interpolation Function
    label_func = ttk.Label(app, text="Interpolation Function:")
    row = grid_item(label_func, row, column=0, sticky="e", increment=False)
    interp_func_var = ttk.Combobox(app,
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
