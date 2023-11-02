"""
--> Executable Script
Graphical interface for SPM file converter to another extension
('txt', 'csv', 'xlsx') (run spm_converter.main_spm_converter)
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.toolbox.spm_converter import main_spm_converter as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
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
    title = "SPM converter"
    app = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'mode': "classic",
        'extension': "txt",
        'verbose': True}
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['mode'] = mode_var.get()
        user_parameters['extension'] = extension_var.get()
        user_parameters['verbose'] = verbose_var.get()

        # Data analysis
        main_script(user_parameters['dir path in'],
                    mode=user_parameters['mode'],
                    extension=user_parameters['extension'],
                    dir_path_out=user_parameters['dir path out'],
                    verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: SSPFM Data Analysis: Step 1 = seg to hyst
    wdw_main_title(app, title)

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
           "- Summary: Directory of SPM datacube SSPFM raw file " \
           "measurements.\n" \
           "- Description: This parameter specifies the directory where " \
           "SPM datacube SSPFM raw file measurements are located. " \
           "It is used to indicate the path to the directory containing " \
           "these measurement files.\n" \
           "- Value: A string representing the directory path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(app, text="Browse", command=browse_dir_in)
    row = grid_item(browse_button_in, row, column=2)

    # Directory (out)
    label_out = ttk.Label(app, text="\tDirectory (out) (*):")
    row = grid_item(label_out, row, column=0, sticky="e", increment=False)
    dir_path_out_var = tk.StringVar()
    dir_path_out_var.set(user_parameters['dir path out'])
    entry_out = ttk.Entry(app, textvariable=dir_path_out_var)
    row = grid_item(entry_out, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_out\n" \
           "- Summary: Saving directory for conversion results " \
           "(optional, default: 'title_meas'_datacube_'extension' directory " \
           "in the same root)\n" \
           "- Description:  This parameter specifies the directory where the " \
           "converted files generated as a result of the analysis will be " \
           "saved.\n" \
           "- Value: It should be a string representing a directory path."
    entry_out.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(entry_out, mess))
    browse_button_out = ttk.Button(app, text="Select", command=browse_dir_out)
    row = grid_item(browse_button_out, row, column=2)
    row = add_grid_separator(app, row=row)

    # Section title: Analysis mode
    label_analysis = ttk.Label(app, text="Analysis mode",
                               font=("Helvetica", 14))
    row = grid_item(label_analysis, row, column=0, sticky="ew", columnspan=3)

    # Mode
    label_mode = ttk.Label(app, text="Mode:")
    row = grid_item(label_mode, row, column=0, sticky="e", increment=False)
    mode_var = ttk.Combobox(app, values=["classic", "dfrt"])
    mode_var.set(user_parameters['mode'])
    row = grid_item(mode_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Treatment used for segment data analysis " \
           "(extraction of PFM measurements).\n" \
           "- Description: This parameter determines the treatment method " \
           "used for segment data analysis, specifically for the extraction " \
           "of PFM measurements.\n" \
           "- Value: A string with two possible values: " \
           "'classic' (sweep) or 'dfrt'"
    mode_var.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(mode_var, mess))
    row = add_grid_separator(app, row=row)

    # Section title: Extension of conversion
    label_conv = ttk.Label(app, text="Extension of conversion",
                           font=("Helvetica", 14))
    row = grid_item(label_conv, row, column=0, sticky="ew", columnspan=3)

    # Extension
    label_extension = ttk.Label(app, text="Extension:")
    row = grid_item(label_extension, row, column=0, sticky="e", increment=False)
    extension_var = ttk.Combobox(app, values=["txt", "csv", "xlsx"])
    extension_var.set(user_parameters['extension'])
    row = grid_item(extension_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Extension of converted spm files.\n" \
           "- Description: This parameter determines the extension type " \
           "used for conversion of .spm file.\n" \
           "- Value: A string with three possible values: " \
           "'txt' or 'csv' or 'xlsx'"
    extension_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(extension_var, mess))
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
