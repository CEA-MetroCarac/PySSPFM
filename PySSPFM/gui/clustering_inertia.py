"""
--> Executable Script
Graphical interface for clustering inertia
 (run clustering_inertia.main)
"""

import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PySSPFM.settings import get_setting
from PySSPFM.toolbox.clustering_inertia import \
    main_clustering_inertia as main_script
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
    title = "Clustering inertia"
    app, scrollable_frame = init_secondary_wdw(parent=parent, wdw_title=title)

    default_user_pars = {'relative': False,
                         'method': 'kmeans',
                         'lim cluster': 10,
                         'label meas': ['piezoresponse']}

    # Set default parameter values
    default_parameters = {
        'dir path in': '',
        'dir path in prop': '',
        'dir path out': '',
        'user_pars': default_user_pars,
        'verbose': True,
        'show plots': True,
        'save': False,
    }
    user_parameters = default_parameters.copy()

    def launch():
        # Update the user_parameters with the new values from the widgets
        user_params = {
            'relative': relative_var.get(),
            'method': method_var.get(),
            'lim cluster': lim_cluster_var.get(),
            'label meas': extract_var(label_meas_loop_var)
        }
        user_parameters['dir path in'] = dir_path_in_var.get()
        user_parameters['dir path in prop'] = extract_var(dir_path_prop_var)
        user_parameters['dir path out'] = extract_var(dir_path_out_var)
        user_parameters["user_pars"] = user_params
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
        main_script(user_parameters["user_pars"],
                    user_parameters['dir path in'],
                    verbose=user_parameters['verbose'],
                    show_plots=user_parameters['show plots'],
                    save_plots=user_parameters['save'],
                    dir_path_out=user_parameters['dir path out'],
                    dir_path_in_props=user_parameters['dir path in prop'])

        # Save parameters
        if user_parameters['save']:
            create_json_res(user_parameters, user_parameters['dir path out'],
                            fname="clustering_inertia_params.json",
                            verbose=user_parameters['verbose'])

    def browse_dir_in():
        dir_path_in = filedialog.askdirectory()
        dir_path_in_var.set(dir_path_in)

    def browse_dir_prop():
        dir_path_prop = filedialog.askdirectory()
        dir_path_prop_var.set(dir_path_prop)

    def browse_dir_out():
        dir_path_out = filedialog.askdirectory()
        dir_path_out_var.set(dir_path_out)

    # Window title: Clustering inertia
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
           "- Summary: Input Directory for Curves Files " \
           "(default: 'best_nanoloops')\n" \
           "- Description: This parameter specifies the directory path for " \
           "the curve files, to perform clustering analysis.\n" \
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
                dirname="curve_clustering", lvl=1, create_path=False,
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
    label_prop = ttk.Label(scrollable_frame,
                           text="Directory properties (in) (*):")
    row = grid_item(label_prop, row, column=0, sticky="e", increment=False)
    dir_path_prop_var = tk.StringVar()
    dir_path_prop_var.set(default_input_props_dir)
    entry_prop = ttk.Entry(scrollable_frame, textvariable=dir_path_prop_var)
    row = grid_item(entry_prop, row, column=1, sticky="ew", increment=False)
    strg = "- Name: dir_path_in_prop\n" \
           "- Summary: Properties files directory " \
           "(optional, default: properties)\n" \
           "- Description: This parameter specifies the directory containing " \
           "the properties files.\n" \
           "For loop clustering : text file generated after the 2nd step of " \
           "the analysis.\n" \
           "For curve clustering : CSV measurement file " \
           "(measurement sheet model).\n" \
           "- Value: It should be a string representing a directory path."
    entry_prop.bind("<Enter>",
                    lambda event, mess=strg: show_tooltip(entry_prop, mess))
    browse_button_prop = ttk.Button(scrollable_frame, text="Browse",
                                    command=browse_dir_prop)
    row = grid_item(browse_button_prop, row, column=2)

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

    # Section title: Common parameters
    label_common = ttk.Label(scrollable_frame, text="Common parameters",
                             font=("Helvetica", 14))
    row = grid_item(label_common, row, column=0, sticky="ew", columnspan=3)
    strg = "These parameters are always active and are common."
    label_common.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(label_common, mess))

    # Relative
    label_relative = ttk.Label(scrollable_frame, text="Relative:")
    row = grid_item(label_relative, row, column=0, sticky="e", increment=False)
    relative_var = tk.BooleanVar()
    relative_var.set(user_parameters['user_pars']['relative'])
    chck_relative = ttk.Checkbutton(scrollable_frame, variable=relative_var)
    row = grid_item(chck_relative, row, column=1, sticky="w")
    strg = "- Name: relative\n" \
           "- Summary: Activation key for relative clustering analysis.\n" \
           "- Description: This parameter serves as an activation key to " \
           "perform clustering analysis on relative curves (all curves " \
           "vary between 0 and 1). Always active for combined curves of " \
           "multiple measurements.\n" \
           "- Value: Boolean (True or False)."
    chck_relative.bind(
        "<Enter>", lambda event, mess=strg: show_tooltip(chck_relative, mess))

    # Method
    label_method = ttk.Label(scrollable_frame, text="Method:")
    row = grid_item(label_method, row, column=0, sticky="e", increment=False)
    method_var = ttk.Combobox(scrollable_frame, values=["kmeans", "gmm"])
    method_var.set(user_parameters['user_pars']['method'])
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
    def update_lim_clusters(_):
        lim_cluster_label.config(text=str(lim_cluster_var.get()))

    # Lim cluster
    label_lim = ttk.Label(scrollable_frame, text="Lim cluster:")
    row = grid_item(label_lim, row, column=0, sticky="e", increment=False)
    lim_cluster_var = \
        tk.IntVar(value=user_parameters['user_pars']['lim cluster'])
    scale_lim = ttk.Scale(scrollable_frame, from_=1, to=30,
                          variable=lim_cluster_var,
                          orient="horizontal", length=30,
                          command=update_lim_clusters)
    row = grid_item(scale_lim, row, column=1, sticky="ew", increment=False)
    strg = "- Name: lim_cluster\n" \
           "- Summary: Maximum limit of the number of clusters to determine " \
           "inertia\n" \
           "- Description: This parameter sets the maximum number of " \
           "clusters for which inertia values are calculated and associated.\n"\
           "- Value: Integer representing the maximum limit of " \
           "cluster number for which inertia values are calculated and " \
           "associated.\n"
    scale_lim.bind("<Enter>",
                   lambda event, mess=strg: show_tooltip(scale_lim, mess))
    lim_cluster_label = ttk.Label(scrollable_frame,
                                  text=str(lim_cluster_var.get()))
    row = grid_item(lim_cluster_label, row, column=2, sticky="w")

    # Measure
    label_name_loop = ttk.Label(scrollable_frame, text="Name(s):")
    row = grid_item(label_name_loop, row, column=0, sticky="e", increment=False)
    label_meas_loop_var = tk.StringVar()
    label_meas_loop_var.set(str(user_parameters['user_pars']['label meas']))
    entry_label_meas_loop = ttk.Entry(scrollable_frame,
                                      textvariable=label_meas_loop_var)
    row = grid_item(entry_label_meas_loop, row, column=1, sticky="ew")
    strg = "- Name: label_meas\n" \
           "- Summary: List of Measurement Name for Loops\n" \
           "- Description: This parameter contains a list of measurement " \
           "name in order to create the loop to be analyzed using a machine " \
           "learning algorithm of clustering.\n" \
           "If several name are filled, the loop will be normalized and " \
           "concatenated.\n" \
           "Choose from : piezoresponse, amplitude, phase, res freq " \
           "and q fact\n" \
           "- Value: A list containing strings.\n" \
           "\t- For example: ['piezoresponse'] or ['amplitude', 'phase']"
    entry_label_meas_loop.bind(
        "<Enter>",
        lambda event, mess=strg: show_tooltip(entry_label_meas_loop, mess))
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
