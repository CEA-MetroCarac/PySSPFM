"""
--> Executable Script
Graphical interface for hysteresis clustering
 (run hysteresis_clustering.main_hysteresis_clustering)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime

from PySSPFM.settings import get_setting
from PySSPFM.toolbox.hysteresis_clustering import \
    main_hysteresis_clustering as main_script
from PySSPFM.gui.utils import \
    (add_grid_separator, grid_item, show_tooltip, extract_var,
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
    title = "Hysteresis clustering"
    app = init_secondary_wdw(parent=parent, wdw_title=title)

    # Set default parameter values
    default_user_parameters = {
        'dir path in': '',
        'dir path in prop': '',
        'dir path out': '',
        'nb clusters off': 4,
        'nb clusters on': 4,
        'nb clusters coupled': 4,
        'verbose': True,
        'show plots': True,
        'save': False,
    }
    user_parameters = default_user_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path in prop'] = extract_var(dir_path_prop_var)
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['nb clusters off'] = clust_off_var.get()
        user_parameters['nb clusters on'] = clust_on_var.get()
        user_parameters['nb clusters coupled'] = clust_coupled_var.get()
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
                    dir_path_out=user_parameters['dir path out'],
                    dir_path_in_props=user_parameters['dir path in prop'])

        # Save parameters
        if user_parameters['save']:
            save_user_pars(
                user_parameters, user_parameters['dir path out'],
                start_time=start_time, verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_prop():
        dir_path_prop = filedialog.askdirectory()
        dir_path_prop_var.set(dir_path_prop)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Hysteresis clustering
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
           "- Summary: Input Directory for Best Nanoloop TXT Files " \
           "(default: 'best_nanoloops')\n" \
           "- Description: This parameter specifies the directory path for " \
           "the best nanoloop .txt files generated after the second step of " \
           "the analysis.\n" \
           "- Value: String representing the directory path."
    entry_in.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(entry_in, mess))
    browse_button_in = ttk.Button(app, text="Browse", command=browse_dir_in)
    row = grid_item(browse_button_in, row, column=2)

    # Function to generate the default output directory path
    def generate_default_output_dir(input_dir):
        if input_dir != "":
            output_dir = save_path_management(
                input_dir, dir_path_out=None, save=True,
                dirname="hysteresis_clustering", lvl=1, create_path=False,
                post_analysis=True)
        else:
            output_dir = ""
        return output_dir

    # Function to generate the default input properties directory path
    def generate_default_input_props_dir(input_dir):
        properties_folder_name = get_setting('default_properties_folder_name')
        if input_dir != "":
            root, _ = os.path.split(input_dir)
            input_props_dir = os.path.join(root, properties_folder_name)
        else:
            input_props_dir = ""
        return input_props_dir

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
        dir_path_prop_var.set(def_input_props_dir)

    # Bind the function (output dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Bind the function (input prop dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_props_dir())

    # Directory properties (in)
    default_input_dir = dir_path_in_var.get()
    default_input_props_dir = generate_default_output_dir(default_input_dir)
    label_prop = ttk.Label(app, text="Directory properties (in) (*):")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    dir_path_prop_var = tk.StringVar()
    dir_path_prop_var.set(default_input_props_dir)
    entry_prop = ttk.Entry(app, textvariable=dir_path_prop_var)
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
    browse_button_prop = ttk.Button(app, text="Browse", command=browse_dir_prop)
    row = grid_item(browse_button_prop, row, column=2)

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
    row = add_grid_separator(app, row=row)

    # Section title: Hysteresis treatment
    label_treat = ttk.Label(app, text="Cluster (k-means)",
                            font=("Helvetica", 14))
    row = grid_item(label_treat, row, column=0, sticky="ew", columnspan=3)

    # Function to update the label text when the slider is moved
    def update_nb_clusters_off(event):
        clust_off_label.config(text=str(clust_off_var.get()))

    # Function to update the label text when the slider is moved
    def update_nb_clusters_on(event):
        clust_on_label.config(text=str(clust_on_var.get()))

    # Function to update the label text when the slider is moved
    def update_nb_clusters_coupled(event):
        clust_coupled_label.config(text=str(clust_coupled_var.get()))

    # Nb clusters (off)
    label_off = ttk.Label(app, text="Nb clusters (off):")
    row = grid_item(label_off, row, column=0, sticky="e", increment=False)
    clust_off_var = tk.IntVar(value=user_parameters['nb clusters off'])
    scale_off = ttk.Scale(app, from_=1, to=30, variable=clust_off_var,
                          orient="horizontal", length=30,
                          command=update_nb_clusters_off)
    row = grid_item(scale_off, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters_off\n" \
           "- Summary: Number of Clusters for Off Field Hysteresis Loop\n" \
           "- Description: This parameter determines the number of " \
           "clusters for the off-field hysteresis loop. " \
           "Machine learning algorythm of clustering (K-Means)\n" \
           "- Value: Integer representing the number of initial " \
           "clusters for the off-field hysteresis loop.\n" \
           "- Active if: Used in the analysis of off-field hysteresis loop."
    scale_off.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(scale_off, mess))
    clust_off_label = ttk.Label(app, text=str(clust_off_var.get()))
    row = grid_item(clust_off_label, row, column=2, sticky="w")

    # Nb clusters (on)
    label_on = ttk.Label(app, text="Nb clusters (on):")
    row = grid_item(label_on, row, column=0, sticky="e", increment=False)
    clust_on_var = tk.IntVar(value=user_parameters['nb clusters on'])
    scale_on = ttk.Scale(app, from_=1, to=30, variable=clust_on_var,
                         orient="horizontal", length=30,
                         command=update_nb_clusters_on)
    row = grid_item(scale_on, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters_on\n" \
           "- Summary: Number of Clusters for On Field Hysteresis Loop\n" \
           "- Description: This parameter determines the number of " \
           "clusters for the on-field hysteresis loop. " \
           "Machine learning algorythm of clustering (K-Means)\n" \
           "- Value: Integer representing the number of initial " \
           "clusters for the on-field hysteresis loop.\n" \
           "- Active if: Used in the analysis of on-field hysteresis loop."
    scale_on.bind("<Enter>",
                  lambda event, mess=strg: show_tooltip(scale_on, mess))
    clust_on_label = ttk.Label(app, text=str(clust_on_var.get()))
    row = grid_item(clust_on_label, row, column=2, sticky="w")

    # Nb clusters (coupled)
    label_coupled = ttk.Label(app, text="Nb clusters (coupled):")
    row = grid_item(label_coupled, row, column=0, sticky="e", increment=False)
    clust_coupled_var = tk.IntVar(value=user_parameters['nb clusters coupled'])
    scale_coupled = ttk.Scale(app, from_=1, to=30, variable=clust_coupled_var,
                              orient="horizontal", length=30,
                              command=update_nb_clusters_coupled)
    row = grid_item(scale_coupled, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters_coupled\n" \
           "- Summary: Number of Clusters for Differential Hysteresis Loop\n" \
           "- Description: This parameter determines the number of " \
           "clusters for the differential hysteresis loop. " \
           "Machine learning algorythm of clustering (K-Means)\n" \
           "- Value: Integer representing the number of initial " \
           "clusters for the differential hysteresis loop.\n" \
           "- Active if: Used in the analysis of differential hysteresis loop."
    scale_coupled.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(scale_coupled, mess))
    clust_coupled_label = ttk.Label(app, text=str(clust_coupled_var.get()))
    row = grid_item(clust_coupled_label, row, column=2, sticky="w")
    row = add_grid_separator(app, row=row)

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
