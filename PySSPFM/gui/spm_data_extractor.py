"""
--> Executable Script
Graphical interface for extract of all data from a spm file
(SSPFM script and raw measurements)
(run spm_data_extractor.main_spm_data_extractor)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.spm_data_extractor import \
    main_spm_data_extractor as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, init_secondary_wdw,
     wdw_main_title)


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
    title = "SPM data extractor"
    app = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'file path in': '',
        'nb hold seg start': 1,
        'nb hold seg end': 1,
        'verbose': True,
        'show plots': True}
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['file path in'] = file_path_in_var.get()
        user_parameters['nb hold seg start'] = nb_hold_seg_start_var.get()
        user_parameters['nb hold seg end'] = nb_hold_seg_end_var.get()
        user_parameters['verbose'] = verbose_var.get()
        user_parameters['show plots'] = show_plots_var.get()

        # Data analysis
        _, figs = main_script(
            user_parameters["file path in"],
            nb_hold_seg_start=user_parameters['nb hold seg start'],
            nb_hold_seg_end=user_parameters['nb hold seg end'],
            verbose=user_parameters['verbose'],
            make_plots=user_parameters['show plots'])

        # Plot figures
        if user_parameters['show plots']:
            print_plots(figs, show_plots=user_parameters['show plots'],
                        save_plots=False, dirname=None, transparent=False)

    def browse_file_in():
        file_path_in = filedialog.askopenfilename()
        file_path_in_var.set(file_path_in)

    # Window title: Phase offset analyzer
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
           "- Summary: Path of datacube SSPFM (.spm) raw file measurements.\n" \
           "- Description: This parameter specifies the path where " \
           "datacube SSPFM (.spm) raw file measurements are located. " \
           "It is used to indicate the path to the file containing " \
           "these measurement.\n" \
           "- Value: A string representing the file path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(app, text="Browse", command=browse_file_in)
    row = grid_item(browse_button_in, row, column=2)
    row = add_grid_separator(app, row=row)

    # Section title: Hold segments
    label_file = ttk.Label(app, text="Hold segments", font=("Helvetica", 14))
    row = grid_item(label_file, row, column=0, sticky="ew", columnspan=3)

    # Number of hold segments (start)
    label_hold_start = ttk.Label(app, text="Number of hold segments (start):")
    row = grid_item(label_hold_start, row, column=0, sticky="e",
                    increment=False)
    nb_hold_seg_start_var = tk.IntVar()
    nb_hold_seg_start_var.set(user_parameters['nb hold seg start'])
    entry_hold_start = ttk.Entry(app, textvariable=nb_hold_seg_start_var)
    row = grid_item(entry_hold_start, row, column=1, sticky="ew")
    strg = "- Name: nb_hold_seg_start\n" \
           "- Summary: Number of hold segments at the start of measurement.\n" \
           "- Description: This parameter is used to specify the number of " \
           "hold segments at the end of the SSPFM signal.\n" \
           "- Value: Should be an integer."
    entry_hold_start.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_hold_start, mess))

    # Number of hold segments (end)
    label_hold_end = ttk.Label(app, text="Number of hold segments (end):")
    row = grid_item(label_hold_end, row, column=0, sticky="e", increment=False)
    nb_hold_seg_end_var = tk.IntVar()
    nb_hold_seg_end_var.set(user_parameters['nb hold seg end'])
    entry_hold_end = ttk.Entry(app, textvariable=nb_hold_seg_end_var)
    row = grid_item(entry_hold_end, row, column=1, sticky="ew")
    strg = "- Name: nb_hold_seg_end\n" \
           "- Summary: Number of hold segments at the end of measurement.\n" \
           "- Description: This parameter is used to specify the number of " \
           "hold segments at the end of the SSPFM signal.\n" \
           "- Value: Should be an integer."
    entry_hold_end.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_hold_end, mess))
    row = add_grid_separator(app, row=row)

    # Section title: Plot
    label_chck = ttk.Label(app, text="Plot", font=("Helvetica", 14))
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
