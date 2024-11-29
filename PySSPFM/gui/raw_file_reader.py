"""
--> Executable Script
Graphical interface for raw file reader
(run raw_file_reader.main_raw_file_reader)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.raw_file_reader import main_raw_file_reader as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
     init_secondary_wdw, wdw_main_title, create_useful_links_button)
from PySSPFM.utils.path_for_runable import save_path_management


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
    title = "Raw file reader"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'file path in': '',
        'dir path out': '',
        'mode': "classic",
        'verbose': True,
        'show plots': True,
        'save plots': False
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['file path in'] = file_path_in_var.get()
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['mode'] = mode_var.get()
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save plots'] = save_plots_var.get()

        # Create out directory if not exist
        if user_parameters['save plots'] is True:
            if user_parameters['dir path out'] is not None:
                if not os.path.exists(user_parameters['dir path out']):
                    os.makedirs(user_parameters['dir path out'])
                    print(f"path created : {user_parameters['dir path out']}")

        # Data analysis
        figs = main_script(user_parameters['file path in'],
                           mode=user_parameters['mode'],
                           verbose=user_parameters['verbose'])
        # Plot figures
        print_plots(figs, save_plots=user_parameters['save plots'],
                    show_plots=user_parameters['show plots'],
                    dirname=user_parameters['dir path out'],
                    transparent=False)

    def browse_file_in():
        file_path_in = filedialog.askopenfilename()
        file_path_in_var.set(file_path_in)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Raw file reader
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
           "- Summary: Path of datacube SSPFM raw file measurements.\n" \
           "- Description: This parameter specifies the path where " \
           "datacube SSPFM raw file measurements are located. " \
           "It is used to indicate the path to the file containing " \
           "these measurement.\n" \
           "- Value: A string representing the file path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(scrollable_frame, text="Browse",
                                  command=browse_file_in)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir = save_path_management(
                input_dir, dir_path_out=None, save=True,
                dirname="raw_file_reader", lvl=1, create_path=False,
                post_analysis=False)
        else:
            output_dir = ""
        return output_dir

    # Function to update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = file_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        dir_path_out_var.set(def_output_dir)

    # Bind the function (output dir) to the input directory widget
    file_path_in_var.trace_add("write",
                               lambda *args: update_default_output_dir())

    # Directory (out)
    label_out = ttk.Label(scrollable_frame, text="\tDirectory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
    dir_path_out_var = tk.StringVar()
    default_input_file = file_path_in_var.get()
    default_output_dir = generate_default_output_dir(default_input_file)
    dir_path_out_var.set(default_output_dir)
    entry_out = ttk.Entry(scrollable_frame, textvariable=dir_path_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_out\n" \
           "- Summary: Saving directory for analysis results figures " \
           "(optional, default: 'title_meas'_toolbox directory in the same " \
           "root)\n" \
           "- Description: This parameter specifies the directory where the " \
           "figures generated as a result of the analysis will be saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(scrollable_frame, text="Select",
                                   command=browse_dir_out)
    row = grid_item(browse_button_out, row, column=2)
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Analysis mode
    label_analysis = ttk.Label(scrollable_frame, text="Analysis mode",
                               font=("Helvetica", 14))
    row = grid_item(label_analysis, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(scrollable_frame, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(scrollable_frame, values=["classic", "dfrt"])
    mode_var.set(user_parameters['mode'])
    row = grid_item(mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Treatment used for segment data analysis " \
           "(extraction of PFM measurements).\n" \
           "- Description: This parameter determines the treatment method " \
           "used for segment data analysis, specifically for the extraction " \
           "of PFM measurements.\n" \
           "- Value: A string with two possible values: " \
           "'classic' (sweep or single_freq) or 'dfrt'"
    mode_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(mode_var, mess))
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

    # Save plots
    label_save = ttk.Label(scrollable_frame, text="Save plots:")
    row = grid_item(label_save, row, column=0, sticky="e", increment=False)
    save_plots_var = tk.BooleanVar()
    save_plots_var.set(user_parameters['save plots'])
    chck_save = ttk.Checkbutton(scrollable_frame, variable=save_plots_var)
    row = grid_item(chck_save, row, column=1, sticky="w")
    strg = "- Name: save_plots\n" \
           "- Summary: Activation key for saving figures during analysis.\n" \
           "- Description: This parameter serves as an activation key " \
           "for saving figures generated during the analysis process.\n" \
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
