"""
--> Executable Script
Graphical interface for force curve clustering
 (run force_curve_clustering.main_force_curve_analysis)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.settings import get_setting
from PySSPFM.toolbox.force_curve_clustering import \
    main_force_curve_analysis as main_script
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
    title = "Force curve clustering"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    default_cluster_pars = {'nb clusters': 4,
                            'method': 'kmeans'}

    # Set default parameter values
    default_parameters = {
        'dir path in': '',
        'csv file path': '',
        'dir path out': '',
        'extension': 'spm',
        'mode': 'classic',
        'cluster_pars': default_cluster_pars,
        'verbose': True,
        'show plots': True,
        'save': False,
    }
    user_parameters = default_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        cluster_pars = {
            'nb clusters': clust_var.get(),
            'method': method_var.get()
        }
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['csv file path'] = extract_var(csv_path_in_var)
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters['extension'] = extension_var.get()
        user_parameters['mode'] = mode_var.get()
        user_parameters["cluster_pars"] = cluster_pars
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
        main_script(user_parameters['dir path in'],
                    cluster_pars=user_parameters["cluster_pars"],
                    extension=user_parameters["extension"],
                    mode=user_parameters["mode"],
                    verbose=user_parameters['verbose'],
                    show_plots=user_parameters['show plots'],
                    save=user_parameters['save'],
                    dir_path_out=user_parameters['dir path out'],
                    csv_file_path=user_parameters['csv file path'])

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="force_curve_clustering_params.json",
                            verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_file_csv_in():
        csv_path_in = filedialog.askdirectory()
        csv_path_in_var.set(csv_path_in)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Curve clustering
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
           "- Summary: Input Directory containing datacube SSPFM " \
           "raw file measurements\n" \
           "- Description: This parameter specifies the directory where " \
           "the datacube SSPFM raw file measurements are stored. " \
           "It is used to indicate the path to the folder containing the " \
           "files for processing and analysis.\n" \
           "- Value: String representing the directory path."
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
                dirname="force_curve_clustering", lvl=1, create_path=False,
                post_analysis=True)
        else:
            output_dir = ""
        return output_dir

    # Function to generate the default input csv file path from a directory
    def generate_default_input_csv_file(input_directory):
        if input_directory != "":
            csv_file_name = get_setting("default_parameters_file_name")
            input_csv_file = os.path.join(input_directory, csv_file_name)
        else:
            input_csv_file = ""
        return input_csv_file

    # Function to update the default output dir path when input dir changes
    def update_default_output_dir():
        input_dir = dir_path_in_var.get()
        def_output_dir = generate_default_output_dir(input_dir)
        dir_path_out_var.set(def_output_dir)

    # Function to update the default input csv file path when input file changes
    def update_default_input_csv_file():
        input_dir = dir_path_in_var.get()
        def_input_csv_file = generate_default_input_csv_file(input_dir)
        csv_path_in_var.set(def_input_csv_file)

    # Bind the function (output dir) to the input directory widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_output_dir())

    # Bind the function (input csv file) to the input file widget
    dir_path_in_var.trace_add("write",
                              lambda *args: update_default_input_csv_file())

    # CSV file (in)
    default_input_dir = dir_path_in_var.get()
    default_input_csv_file = generate_default_input_csv_file(default_input_dir)
    label = ttk.Label(scrollable_frame,
                      text="file path csv measurements (in) (*):")
    row = grid_item(label, row, column=0, sticky="e", increment=False)
    csv_path_in_var = tk.StringVar()
    csv_path_in_var.set(default_input_csv_file)
    entry2 = ttk.Entry(scrollable_frame, textvariable=csv_path_in_var)
    row = grid_item(entry2, row, column=1, sticky="ew", increment=False)
    strg = "- Name: csv_file_path\n" \
           "- Summary: File path of the CSV measurement file " \
           "(measurement sheet model).\n" \
           "- Description: This parameter specifies the file path to " \
           "the CSV file containing measurement parameters. It is used to " \
           "indicate the location of the CSV file, which serves as the " \
           "source of measurement data for processing.\n" \
           "- Value: A string representing the file path.\n" \
           "\t- If left empty, the system will automatically " \
           "select the CSV file path."
    entry2.bind("<Enter>", lambda event, mess=strg: show_tooltip(entry2, mess))
    browse_button_csv = ttk.Button(scrollable_frame, text="Browse",
                                   command=browse_file_csv_in)
    row = grid_item(browse_button_csv, row, column=2)

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

    # Section title: Extension of conversion
    label_conv = ttk.Label(scrollable_frame, text="Extension of conversion",
                           font=("Helvetica", 14))
    row = grid_item(label_conv, row, column=0, sticky="ew", columnspan=3)

    # Extension
    label_extension = ttk.Label(scrollable_frame, text="Extension:")
    row = grid_item(label_extension, row, column=0, sticky="e", increment=False)
    extension_var = ttk.Combobox(scrollable_frame,
                                 values=["spm", "txt", "csv", "xlsx"])
    extension_var.set(user_parameters['extension'])
    row = grid_item(extension_var, row, column=1, sticky="ew")
    strg = "- Name: mode\n" \
           "- Summary: Extension of converted spm files.\n" \
           "- Description: This parameter determines the extension type " \
           "used for conversion of .spm file.\n" \
           "- Value: A string with four possible values: " \
           "'spm' or 'txt' or 'csv' or 'xlsx'"
    extension_var.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(extension_var, mess))
    row = add_grid_separator(scrollable_frame, row=row)

    # Section title: Common parameters
    label_common = ttk.Label(scrollable_frame, text="Common parameters",
                             font=("Helvetica", 14))
    row = grid_item(label_common, row, column=0, sticky="ew", columnspan=3)
    strg = "These parameters are always active and are common."
    label_common.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_common, mess))

    # Method
    label_method = ttk.Label(scrollable_frame, text="Method:")
    row = grid_item(label_method, row, column=0, sticky="e", increment=False)
    method_var = ttk.Combobox(scrollable_frame, values=["kmeans", "gmm"])
    method_var.set(user_parameters['cluster_pars']['method'])
    row = grid_item(method_var, row, column=1, sticky="ew")
    strg = "- Name: method\n" \
           "- Summary: Name of the method used to perform the clustering.\n" \
           "- Description: This parameter determines the method used to " \
           "perform the clustering. Implemented methods are K-Means or " \
           "Gaussian Mixture Model. (GMM).\n" \
           "- Value: A string with two possible values:\n" \
           "\t--> 'kmeans': K-Means clustering\n" \
           "\t--> 'gmm': Gaussian Mixture Model clustering"
    method_var.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(method_var, mess))

    # Function to update the label text when the slider is moved
    def update_nb_clust(_):
        clust_label.config(text=str(clust_var.get()))

    # Nb clusters
    label_clust = ttk.Label(scrollable_frame, text="Nb clusters:")
    row = grid_item(label_clust, row, column=0, sticky="e", increment=False)
    clust_var = \
        tk.IntVar(value=user_parameters['cluster_pars']['nb clusters'])
    scale_clust = ttk.Scale(scrollable_frame, from_=1, to=30,
                            variable=clust_var,
                            orient="horizontal", length=30,
                            command=update_nb_clust)
    row = grid_item(scale_clust, row, column=1, sticky="ew", increment=False)
    strg = "- Name: nb_clusters\n" \
           "- Summary: Number of Clusters for Curve\n" \
           "- Description: This parameter determines the number of clusters " \
           "for the curve using a machine learning algorithm of clustering.\n" \
           "- Value: Integer representing the number of initial " \
           "clusters."
    scale_clust.bind("<Enter>",
                     lambda event, mess=strg: show_tooltip(scale_clust, mess))
    clust_label = ttk.Label(scrollable_frame, text=str(clust_var.get()))
    row = grid_item(clust_label, row, column=2, sticky="w")
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
