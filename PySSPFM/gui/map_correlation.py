"""
--> Executable Script
Graphical interface for map correlation
(run map_correlation.main_map_correlation)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.utils.core.figure import print_plots
from PySSPFM.toolbox.map_correlation import main_map_correlation as main_script
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
    title = "Map correlation"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    ind_maps = [['off', 'charac tot fit: area'],
                ['off', 'fit pars: ampli_0'],
                ['on', 'charac tot fit: area'],
                ['on', 'fit pars: ampli_0']]
    default_user_parameters = {
        'dir path in': '',
        'dir path out': '',
        'dir path in prop': '',
        'dir path in loop': '',
        'dir path in pars': '',
        'ind maps': ind_maps,
        'mask': None,
        'revert mask': False,
        'show plots': True,
        'save': False,
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['mask'] = extract_var(mask_var)
        user_parameters['revert mask'] = revert_mask_var.get()
        user_parameters['ind maps'] = extract_var(ind_maps_var)
        user_parameters['show plots'] = show_plots_var.get()
        user_parameters['save'] = save_var.get()

        # Create out directory if not exist
        if user_parameters['save'] is True:
            if user_parameters['dir path out'] is not None:
                if not os.path.exists(user_parameters['dir path out']):
                    os.makedirs(user_parameters['dir path out'])
                    print(f"path created : {user_parameters['dir path out']}")

        # Data analysis
        _, figs = main_script(user_parameters, user_parameters['dir path in'])
        # Plot figures
        print_plots(figs, show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dirname=user_parameters['dir path out'], transparent=False)

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="map_correlation_params.json",
                            verbose=False)

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Map correlation
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
                dirname="map_correlation", lvl=1, create_path=False,
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
    label_out = ttk.Label(scrollable_frame, text="\tDirectory (out) (*):")
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

    # Section title: Properties
    label_prop = ttk.Label(scrollable_frame, text="Properties",
                           font=("Helvetica", 14))
    row = grid_item(label_prop, row, column=0, sticky="ew", columnspan=3)

    # Property
    label_ind = ttk.Label(scrollable_frame, text="Property:")
    row = grid_item(label_ind, row, column=0, sticky="e", increment=False)
    ind_maps_var = tk.StringVar()
    ind_maps_var.set(str(user_parameters['ind maps']))
    entry_ref_ind = ttk.Entry(scrollable_frame, textvariable=ind_maps_var)
    row = grid_item(entry_ref_ind, row, column=1, sticky="ew")
    strg = "- Name: ind_maps\n" \
           "- Summary: List of Property Modes and Names for " \
           "Cross Correlation Analysis\n" \
           "- Description: This parameter is a list that specifies which " \
           "property modes and their corresponding names should be " \
           "used for cross correlation analysis.\n" \
           "- Value: A list with dimensions (n, 2) containing strings.\n" \
           "\t- It contains pairs of property modes and associated " \
           "names in the format [['mode', 'name']].\n" \
           "\t- For example, [['off', 'charac tot fit: area'], " \
           "['off', 'fit pars: ampli_0'], ['on', 'charac tot fit: area'], " \
           "['on', 'fit pars: ampli_0']]"
    entry_ref_ind.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(entry_ref_ind, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Mask (manual)
    label_man = ttk.Label(scrollable_frame, text="Mask (manual):",
                          font=("Helvetica", 14))
    row = grid_item(label_man, row, column=0, sticky="ew", columnspan=3)

    # Manual Mask
    label_pix = ttk.Label(scrollable_frame, text="List of pixels:")
    row = grid_item(label_pix, row, column=0, sticky="e", increment=False)
    mask_var = tk.StringVar()
    mask_var.set(user_parameters['mask'])
    entry_mask = ttk.Entry(scrollable_frame, textvariable=mask_var)
    row = grid_item(entry_mask, row, column=1, sticky="ew")
    strg = "- Name: mask\n" \
           "- Summary: Manual mask for selecting specific files\n" \
           "- Description: This parameter is a list of pixel indices.\n" \
           "- Value: List of indices as values.\n" \
           "\t--> if list of pixels is None: no masked pixels\n" \
           "\t--> if list of pixels is [a, b, c ...] file of index " \
           "a, b, c [...] are masked for the analysis"
    entry_mask.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_mask, mess))

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

    # Section title: Plot and save
    label_chck = ttk.Label(scrollable_frame, text="Plot and save",
                           font=("Helvetica", 14))
    row = grid_item(label_chck, row, column=0, sticky="ew", columnspan=3)

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
